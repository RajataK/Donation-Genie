variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "donation-genie"
}

variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "eu-west-2"
}
