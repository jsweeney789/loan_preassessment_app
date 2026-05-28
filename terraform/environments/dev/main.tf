terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # S3 backend for remote state — create the bucket and DynamoDB table manually first
  backend "s3" {
    bucket       = "loan-preassessment-state"
    key          = "loan-preassessment/terraform.tfstate"
    region       = "us-east-1"
    use_lockfile = true
    encrypt      = true
  }
}


provider "aws" {
  region = var.aws_region
}

locals {
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

module "networking" {
  source = "../../modules/networking"

  environment          = var.environment
  vpc_cidr             = "10.0.0.0/16"
  availability_zones   = ["us-east-1a", "us-east-1b"]
  public_subnet_cidrs  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnet_cidrs = ["10.0.3.0/24", "10.0.4.0/24"]
  app_port             = 8000
  tags                 = local.tags
}

module "app" {
  source = "../../modules/app"

  environment = var.environment
  tags        = local.tags

  # Networking — wired from the networking module outputs
  vpc_id             = module.networking.vpc_id
  public_subnet_ids  = module.networking.public_subnet_ids
  private_subnet_ids = module.networking.private_subnet_ids
  alb_sg_id          = module.networking.alb_sg_id
  ecs_sg_id          = module.networking.ecs_sg_id

  # ECS sizing
  app_port           = 8000
  ecs_cpu            = var.ecs_cpu
  ecs_memory         = var.ecs_memory
  ecs_desired_count  = var.ecs_desired_count
  log_retention_days = var.log_retention_days
}



module "frontend" {
  source = "../../modules/frontend"

  environment  = var.environment
  project_name = var.project_name
  tags         = local.tags
}


data "aws_s3_bucket" "training_data" {
  bucket = var.training_data_s3
}

module "sagemaker" {
  source = "../../modules/sagemaker"

  environment  = var.environment
  project_name = var.project_name
  tags         = local.tags


  training_data_bucket_arn = data.aws_s3_bucket.training_data.arn

  # Set after first training run: terraform apply -var="model_artifact_s3_uri=s3://..."
  model_artifact_s3_uri = var.model_artifact_s3_uri
  inference_image_uri   = var.inference_image_uri
}