# -----------------------------------------------------------------------------
# CloudFront Module — Variables
# -----------------------------------------------------------------------------

variable "project_name" {
  description = "Name of the project, used in resource naming"
  type        = string
}

variable "environment" {
  description = "Deployment environment (e.g. dev, staging, prod)"
  type        = string
}

variable "s3_bucket_regional_domain_name" {
  description = "Regional domain name of the S3 bucket hosting the frontend assets"
  type        = string
}

variable "alb_dns_name" {
  description = "DNS name of the Application Load Balancer for the backend API"
  type        = string
}
