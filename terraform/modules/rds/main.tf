resource "aws_db_subnet_group" "this" {
  name       = "${var.project_name}-${var.environment}"
  subnet_ids = var.private_subnet_ids

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}

resource "aws_db_instance" "this" {
  identifier = "${var.project_name}-${var.environment}"

  engine         = "postgres"
  engine_version = "17"

  instance_class        = var.instance_class
  allocated_storage     = var.allocated_storage
  max_allocated_storage = var.max_allocated_storage
  storage_type          = "gp3"

  db_name  = var.db_name
  username = "genie"

  manage_master_user_password = true

  publicly_accessible = false
  storage_encrypted   = true
  multi_az            = false

  backup_retention_period   = 7
  skip_final_snapshot       = true
  final_snapshot_identifier = "${var.project_name}-${var.environment}-final"

  deletion_protection = var.deletion_protection

  vpc_security_group_ids = [var.rds_sg_id]
  db_subnet_group_name   = aws_db_subnet_group.this.name

  tags = {
    Name = "${var.project_name}-${var.environment}"
  }
}
