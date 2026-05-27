variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = { BatchID = "20260316" }
}

# ── Networking (passed in from the networking module outputs) ─────────────────

variable "vpc_id" {
  description = "ID of the VPC"
  type        = string
}

variable "public_subnet_ids" {
  description = "IDs of the public subnets (used by the ALB)"
  type        = list(string)
}

variable "private_subnet_ids" {
  description = "IDs of the private subnets (used by ECS tasks)"
  type        = list(string)
}

variable "alb_sg_id" {
  description = "Security group ID for the ALB"
  type        = string
}

variable "ecs_sg_id" {
  description = "Security group ID for ECS tasks"
  type        = string
}

# ── ECS sizing ────────────────────────────────────────────────────────────────

variable "app_port" {
  description = "Port the container listens on"
  type        = number
  default     = 8000
}

variable "ecs_cpu" {
  description = "CPU units for the Fargate task (256 / 512 / 1024 / 2048 / 4096)"
  type        = number
  default     = 512
}

variable "ecs_memory" {
  description = "Memory (MiB) for the Fargate task"
  type        = number
  default     = 1024
}

variable "ecs_desired_count" {
  description = "Desired number of running tasks"
  type        = number
  default     = 2
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 7
}
