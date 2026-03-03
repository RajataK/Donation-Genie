variable "vpc_id" {
  description = "ID of the VPC where security groups will be created"
  type        = string
}

variable "project_name" {
  description = "Name of the project, used in resource naming"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}
