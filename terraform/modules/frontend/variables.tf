variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "project_name" {
  description = "Project name — used to name the S3 bucket (must be globally unique)"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {"BatchID" = "20260316"}
}

variable "alb_dns_name" {
  description = "ALB DNS name — added as a CloudFront origin so /api/* is proxied over HTTPS"
  type        = string
}
