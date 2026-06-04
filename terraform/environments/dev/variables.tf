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
  default = "512"
}

variable "ecs_memory" {
  type    = string
  default = "1024"
}

variable "ecs_desired_count" {
  type    = number
  default = 2
}


variable "log_retention_days" {
  type    = number
  default = 7
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

variable "db_name" {
  description = "Name of the database to create"
  type        = string
  default     = "loandb"
}

variable "db_username" {
  description = "Master username for the RDS instance"
  type        = string
  default     = "loanadmin"
}

variable "training_data_s3" {
  description = "Name of existing s3 bucket containing training data"
  type        = string
}

# ── Google OAuth ──────────────────────────────────────────────────────────────

variable "google_client_id" {
  description = "Google OAuth client ID"
  type        = string
  default     = ""
}

variable "google_redirect_uri" {
  description = "Google OAuth redirect URI"
  type        = string
  default     = "https://d1u5g6nu2nj7p1.cloudfront.net/auth/google/callback"
}

# ── CI/CD ─────────────────────────────────────────────────────────────────────

variable "codecommit_repo_name" {
  description = "Name of the CodeCommit repository (created by the cicd module)"
  type        = string
  default     = "loan_preassessment_app"
}

variable "terraform_version" {
  description = "Terraform version for the pipeline build container"
  type        = string
  default     = "1.9.8"
}

variable "notification_email" {
  description = "Email address for pipeline failure alerts"
  type        = string
}

variable "cluster_admin_role_arn" {
  description = "IAM role ARN granted kubectl cluster-admin access on the EKS cluster"
  type        = string
}