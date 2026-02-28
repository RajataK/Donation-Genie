###############################################################################
# Security Groups Module – ALB, ECS Tasks, RDS
###############################################################################

# ---------------------------------------------------------------------------
# Data source: CloudFront origin-facing managed prefix list
# ---------------------------------------------------------------------------
data "aws_ec2_managed_prefix_list" "cloudfront" {
  name = "com.amazonaws.global.cloudfront.origin-facing"
}

# ---------------------------------------------------------------------------
# ALB Security Group
# ---------------------------------------------------------------------------
resource "aws_security_group" "alb" {
  name        = "${var.project_name}-${var.environment}-alb"
  description = "Security group for the Application Load Balancer"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-${var.environment}-alb"
  }
}

# ALB ingress: allow HTTP from CloudFront managed prefix list
resource "aws_vpc_security_group_ingress_rule" "alb_from_cloudfront" {
  security_group_id = aws_security_group.alb.id
  description       = "HTTP from CloudFront"

  prefix_list_id = data.aws_ec2_managed_prefix_list.cloudfront.id
  from_port      = 80
  to_port        = 80
  ip_protocol    = "tcp"
}

# ALB egress: allow traffic to ECS Tasks on port 8000
resource "aws_vpc_security_group_egress_rule" "alb_to_ecs" {
  security_group_id = aws_security_group.alb.id
  description       = "To ECS Tasks on port 8000"

  referenced_security_group_id = aws_security_group.ecs_tasks.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

# ---------------------------------------------------------------------------
# ECS Tasks Security Group
# ---------------------------------------------------------------------------
resource "aws_security_group" "ecs_tasks" {
  name        = "${var.project_name}-${var.environment}-ecs-tasks"
  description = "Security group for ECS Fargate tasks"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-${var.environment}-ecs-tasks"
  }
}

# ECS Tasks ingress: allow traffic from ALB on port 8000
resource "aws_vpc_security_group_ingress_rule" "ecs_from_alb" {
  security_group_id = aws_security_group.ecs_tasks.id
  description       = "From ALB on port 8000"

  referenced_security_group_id = aws_security_group.alb.id
  from_port                    = 8000
  to_port                      = 8000
  ip_protocol                  = "tcp"
}

# ECS Tasks egress: allow traffic to RDS on port 5432
resource "aws_vpc_security_group_egress_rule" "ecs_to_rds" {
  security_group_id = aws_security_group.ecs_tasks.id
  description       = "To RDS on port 5432"

  referenced_security_group_id = aws_security_group.rds.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}

# ECS Tasks egress: allow HTTPS to 0.0.0.0/0 (AWS API access via NAT)
resource "aws_vpc_security_group_egress_rule" "ecs_to_internet_https" {
  security_group_id = aws_security_group.ecs_tasks.id
  description       = "HTTPS to internet for AWS API access via NAT"

  cidr_ipv4   = "0.0.0.0/0"
  from_port   = 443
  to_port     = 443
  ip_protocol = "tcp"
}

# ---------------------------------------------------------------------------
# RDS Security Group
# ---------------------------------------------------------------------------
resource "aws_security_group" "rds" {
  name        = "${var.project_name}-${var.environment}-rds"
  description = "Security group for RDS PostgreSQL instance"
  vpc_id      = var.vpc_id

  tags = {
    Name = "${var.project_name}-${var.environment}-rds"
  }
}

# RDS ingress: allow traffic from ECS Tasks on port 5432
resource "aws_vpc_security_group_ingress_rule" "rds_from_ecs" {
  security_group_id = aws_security_group.rds.id
  description       = "From ECS Tasks on port 5432"

  referenced_security_group_id = aws_security_group.ecs_tasks.id
  from_port                    = 5432
  to_port                      = 5432
  ip_protocol                  = "tcp"
}
