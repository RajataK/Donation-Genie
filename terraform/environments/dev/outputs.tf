output "cloudfront_url" {
  description = "CloudFront distribution URL (application entry point)"
  value       = "https://${module.cloudfront.distribution_domain_name}"
}

output "alb_dns_name" {
  description = "Internal ALB DNS name (for debugging)"
  value       = module.alb.alb_dns_name
}

output "rds_endpoint" {
  description = "RDS instance endpoint (for debugging)"
  value       = module.rds.db_endpoint
}

output "frontend_bucket_name" {
  description = "S3 bucket name for frontend deployment (aws s3 sync target)"
  value       = module.s3_frontend.bucket_id
}

output "ecr_repository_url" {
  description = "ECR repository URL for Docker image push"
  value       = module.ecr.repository_url
}

output "distribution_id" {
  description = "CloudFront distribution ID (for cache invalidation)"
  value       = module.cloudfront.distribution_id
}

output "ecs_cluster_name" {
  description = "ECS cluster name"
  value       = module.ecs.cluster_name
}

output "ecs_service_name" {
  description = "ECS service name"
  value       = module.ecs.service_name
}
