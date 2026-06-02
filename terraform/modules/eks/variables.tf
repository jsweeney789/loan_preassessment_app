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
  default     = { BatchID = "20260316" }
}

# ── Networking ────────────────────────────────────────────────────────────────

variable "vpc_id" {
  description = "VPC ID from the networking module"
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs — nodes and control plane endpoints live here"
  type        = list(string)
}

# ── Node group sizing ─────────────────────────────────────────────────────────

variable "node_instance_type" {
  description = "EC2 instance type for worker nodes"
  type        = string
  default     = "t3.medium"
}

variable "desired_nodes" {
  description = "Number of desired nodes in cluster"
  type        = number
  default     = 2
}

variable "max_nodes" {
  description = "Max number of nodes"
  type        = number
  default     = 3
}

variable "min_nodes" {
  description = "Min number of nodes"
  type        = number
  default     = 1
}
