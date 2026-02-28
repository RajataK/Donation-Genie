variable "project_name" {
  description = "The name of the project, used as a prefix for the ECR repository"
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g. dev, staging, prod)"
  type        = string
}
