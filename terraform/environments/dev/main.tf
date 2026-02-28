terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# --- Networking ---

module "networking" {
  source = "../../modules/networking"

  project_name = var.project_name
  environment  = var.environment
}

# --- Security Groups ---

module "security_groups" {
  source = "../../modules/security-groups"

  vpc_id       = module.networking.vpc_id
  project_name = var.project_name
  environment  = var.environment
}

# --- ECR ---

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

# --- RDS ---

module "rds" {
  source = "../../modules/rds"

  project_name          = var.project_name
  environment           = var.environment
  private_subnet_ids    = module.networking.private_subnet_ids
  rds_sg_id             = module.security_groups.rds_sg_id
  instance_class        = var.rds_instance_class
  allocated_storage     = var.rds_allocated_storage
  max_allocated_storage = var.rds_max_allocated_storage
  db_name               = var.db_name
}

# --- ALB ---

module "alb" {
  source = "../../modules/alb"

  project_name      = var.project_name
  environment       = var.environment
  vpc_id            = module.networking.vpc_id
  public_subnet_ids = module.networking.public_subnet_ids
  alb_sg_id         = module.security_groups.alb_sg_id
}

# --- ECS ---

module "ecs" {
  source = "../../modules/ecs"

  project_name              = var.project_name
  environment               = var.environment
  private_subnet_ids        = module.networking.private_subnet_ids
  ecs_tasks_sg_id           = module.security_groups.ecs_tasks_sg_id
  target_group_arn          = module.alb.target_group_arn
  ecr_repository_url        = module.ecr.repository_url
  image_tag                 = var.image_tag
  cpu                       = var.ecs_cpu
  memory                    = var.ecs_memory
  desired_count             = var.ecs_desired_count
  db_endpoint               = module.rds.db_endpoint
  db_name                   = module.rds.db_name
  db_master_user_secret_arn = module.rds.master_user_secret_arn
  aws_region                = var.aws_region
  allowed_hosts             = "*"
}

# --- S3 Frontend ---

module "s3_frontend" {
  source = "../../modules/s3-frontend"

  project_name = var.project_name
  environment  = var.environment
}

# --- CloudFront ---

module "cloudfront" {
  source = "../../modules/cloudfront"

  project_name                   = var.project_name
  environment                    = var.environment
  s3_bucket_regional_domain_name = module.s3_frontend.bucket_regional_domain_name
  alb_dns_name                   = module.alb.alb_dns_name
}

# --- S3 Bucket Policy (resolves circular dependency) ---
# The S3 bucket needs the CloudFront distribution ARN for its policy,
# and CloudFront needs the S3 bucket domain. We break the cycle by
# creating the bucket policy here in the root module.

resource "aws_s3_bucket_policy" "frontend" {
  bucket = module.s3_frontend.bucket_id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFrontServicePrincipal"
        Effect    = "Allow"
        Principal = { Service = "cloudfront.amazonaws.com" }
        Action    = "s3:GetObject"
        Resource  = "${module.s3_frontend.bucket_arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = module.cloudfront.distribution_arn
          }
        }
      }
    ]
  })
}
