terraform {
  required_version = ">= 1.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
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

  # Database credentials
  db_secret_arn = module.database.db_secret_arn

  # Database credentials
  db_secret_arn = module.database.db_secret_arn
}



module "database" {
  source = "../../modules/database"

  environment  = var.environment
  project_name = var.project_name
  tags         = local.tags

  # Networking — from networking module outputs
  vpc_id     = module.networking.vpc_id
  subnet_ids = module.networking.private_subnet_ids
  rds_sg_id  = module.networking.rds_sg_id

  # DB config
  db_name     = var.db_name
  db_name     = var.db_name
  db_username = var.db_username

  # Sizing defaults are fine for dev (db.t3.micro, 5GB, no multi-az)
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

module "cicd" {
  source = "../../cicd"

  environment  = var.environment
  project_name = var.project_name
  tags         = local.tags

  # CodeCommit
  codecommit_repo_name = var.codecommit_repo_name
  deploy_branch        = "main"

  # # Backend pipeline — from app module outputs
  # ecr_repository_url = module.app.ecr_repository_url
  # ecs_cluster_name   = module.app.ecs_cluster_name
  # ecs_service_name   = module.app.ecs_service_name

  # Frontend pipeline — from frontend module outputs
  frontend_bucket_name       = module.frontend.s3_bucket_name
  cloudfront_distribution_id = module.frontend.cloudfront_distribution_id

  # Terraform pipeline
  tf_state_bucket   = "loan-preassessment-state"
  terraform_version = var.terraform_version
}