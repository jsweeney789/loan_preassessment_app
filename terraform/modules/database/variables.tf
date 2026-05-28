variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {BatchID = "20260316"}
}

variable "vpc_id" {
  description = "VPC ID from networking module"
  type        = string
}

variable "subnet_ids" {
  description = "Private subnet IDs from networking module"
  type        = list(string)
}

variable "rds_sg_id" {
  description = "Security group ID for RDS from networking module"
  type        = string
}

variable "db_name" {
  description = "Name of the database to create"
  type        = string
}

variable "db_username" {
  description = "Master username for the database"
  type        = string
}

variable "db_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Initial storage in GB"
  type        = number
  default     = 5
}

variable "db_max_allocated_storage" {
  description = "Max storage for autoscaling in GB — set to 0 to disable"
  type        = number
  default     = 20
}

variable "db_engine_version" {
  description = "PostgreSQL engine version"
  type        = string
  default     = "16.3"
}

variable "backup_retention_days" {
  description = "Number of days to retain automated backups"
  type        = number
  default     = 7
}

variable "multi_az" {
  description = "Enable Multi-AZ for high availability — true in prod, false in dev"
  type        = bool
  default     = false
}
