variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "notification_email" {
  description = "Email address that receives pipeline failure alerts via SNS"
  type        = string
}

variable "project_name" {
  description = "Project name — used for naming pipeline resources"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

# ── CodeCommit ────────────────────────────────────────────────────────────────

variable "codecommit_repo_name" {
  description = "Name of the CodeCommit repository to create and use as pipeline source"
  type        = string
}

variable "deploy_branch" {
  description = "Branch that triggers all pipelines"
  type        = string
  default     = "main"
}

# ── Backend pipeline inputs ───────────────────────────────────────────────────

variable "ecr_repository_url" {
  description = "ECR repository URL for the backend image"
  type        = string
}

variable "ecs_cluster_name" {
  description = "ECS cluster name"
  type        = string
}

variable "ecs_service_name" {
  description = "ECS service name"
  type        = string
}

# ── Frontend pipeline inputs ──────────────────────────────────────────────────

variable "frontend_bucket_name" {
  description = "S3 bucket name for the Angular build output"
  type        = string
}

variable "cloudfront_distribution_id" {
  description = "CloudFront distribution ID to invalidate on deploy"
  type        = string
}

# ── EKS pipeline inputs ───────────────────────────────────────────────────────

variable "eks_cluster_name" {
  description = "EKS cluster name — used by CodeBuild to run kubectl"
  type        = string
}

variable "eks_namespace" {
  description = "Kubernetes namespace to deploy into"
  type        = string
  default     = "loan-preassessment"
}

variable "db_secret_arn" {
  description = "Secrets Manager ARN for the RDS credentials secret"
  type        = string
}

variable "google_oauth_secret_arn" {
  description = "Secrets Manager ARN for the Google OAuth client secret"
  type        = string
}

variable "auth_secret_arn" {
  description = "Secrets Manager ARN for the JWT and session secrets"
  type        = string
}

variable "cors_origin" {
  description = "Allowed CORS origin (CloudFront domain) — injected as env var into the EKS pods"
  type        = string
}

variable "google_client_id" {
  description = "Google OAuth client ID — injected as env var into the EKS pods"
  type        = string
}

variable "google_redirect_uri" {
  description = "Google OAuth redirect URI — injected as env var into the EKS pods"
  type        = string
}

# ── Terraform pipeline inputs ─────────────────────────────────────────────────

variable "tf_state_bucket" {
  description = "S3 bucket holding Terraform remote state"
  type        = string
}

variable "terraform_version" {
  description = "Terraform version to install in the pipeline build container"
  type        = string
  default     = "1.9.8"
}

