variable "aws_region" {
  type = string
}

variable "environment" {
  type = string
}

variable "project_name" {
  type = string
}

variable "ecs_cpu" {
  type    = string
  default = "1024"
}

variable "ecs_memory" {
  type    = string
  default = "2048"
}

variable "ecs_desired_count" {
  type    = number
  default = 2
}

variable "log_retention_days" {
  type    = number
  default = 30
}

# ── SageMaker ─────────────────────────────────────────────────────────────────

variable "model_artifact_s3_uri" {
  description = "S3 URI of the trained model artifact. Leave empty until after the first training run."
  type        = string
  default     = ""
}

variable "inference_image_uri" {
  description = "Inference container image URI (AWS-managed or custom ECR)."
  type        = string
  default     = ""
}
