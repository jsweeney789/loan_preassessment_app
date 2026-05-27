variable "environment" {
  description = "Deployment environment (dev, prod)"
  type        = string
}

variable "tags" {
  description = "Common tags to apply to all resources"
  type = map(string)
  default = {
    "BatchID" = "20260316"
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones to deploy subnets into"
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets — one per AZ"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets — one per AZ"
  type        = list(string)
}

variable "app_port" {
  description = "Port the ECS container listens on"
  type        = number
  default     = 8000
}
