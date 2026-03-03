# ------------------------------------------------------------------------------
# ECS Module – Input Variables
# ------------------------------------------------------------------------------

variable "project_name" {
  description = "Project name used for resource naming."
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. staging, production)."
  type        = string
}

variable "private_subnet_ids" {
  description = "List of private subnet IDs for the ECS tasks."
  type        = list(string)
}

variable "ecs_tasks_sg_id" {
  description = "Security group ID to attach to ECS tasks."
  type        = string
}

variable "target_group_arn" {
  description = "ARN of the ALB target group that routes traffic to the ECS service."
  type        = string
}

variable "ecr_repository_url" {
  description = "URL of the ECR repository containing the Django container image."
  type        = string
}

variable "image_tag" {
  description = "Docker image tag to deploy."
  type        = string
  default     = "latest"
}

variable "cpu" {
  description = "Fargate task CPU units (1 vCPU = 1024)."
  type        = number
  default     = 512
}

variable "memory" {
  description = "Fargate task memory in MiB."
  type        = number
  default     = 1024
}

variable "desired_count" {
  description = "Number of ECS task instances to run."
  type        = number
  default     = 1
}

variable "db_endpoint" {
  description = "RDS database endpoint (hostname without port)."
  type        = string
}

variable "db_name" {
  description = "Name of the PostgreSQL database."
  type        = string
}

variable "db_master_user_secret_arn" {
  description = "ARN of the Secrets Manager secret containing RDS master user credentials (JSON with username and password)."
  type        = string
}

variable "aws_region" {
  description = "AWS region for CloudWatch Logs configuration."
  type        = string
}

variable "allowed_hosts" {
  description = "Value for Django ALLOWED_HOSTS environment variable."
  type        = string
  default     = "*"
}
