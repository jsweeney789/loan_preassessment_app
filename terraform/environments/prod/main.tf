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
    bucket         = "loan-preassessment-state"
    key            = "loan-preassessment/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "loan-preassessment-tf-locks"
    encrypt        = true
  }
}


# provider "aws" {
#   region = var.aws_region
# }