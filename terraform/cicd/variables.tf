variable "environment" {
  description = "Deployment environment (dev, prod)"
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

# ── GitHub ────────────────────────────────────────────────────────────────────

variable "github_owner" {
  description = "GitHub username or org that owns the repo"
  type        = string
}

variable "github_repo" {
  description = "GitHub repository name"
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

variable "existing_github_connection_arn" {
  description = "ARN of a pre-existing CodeStar/CodeConnections connection to GitHub. When set, no new connection is created (useful when codeconnections:CreateConnection is not permitted)."
  type        = string
  default     = ""
}
