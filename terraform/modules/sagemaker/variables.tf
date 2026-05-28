variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "project_name" {
  description = "Project name — used to name the S3 artifact bucket"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = { "BatchID" = "20260316" }
}

variable "model_artifact_s3_uri" {
  description = "S3 URI of the trained model artifact (e.g. s3://bucket/model.tar.gz). Leave empty to skip endpoint creation until after first training run."
  type        = string
  
}

variable "inference_image_uri" {
  description = "ECR or AWS-managed container image URI for inference. Required when model_artifact_s3_uri is set."
  type        = string
}

variable "training_data_bucket_arn" {
  description = "ARN of the S3 bucket containing training/inference data"
  type        = string
}