# Contract: Environment Variables

**Feature**: 003-aws-serverless-iac
**Date**: 2026-02-27

## Overview

Environment variables configure the Django backend running in ECS Fargate. Secrets are stored in AWS Secrets Manager and injected at task startup. Non-sensitive configuration is set as plaintext environment variables in the task definition.

## ECS Task Definition Variables

### Secrets (from AWS Secrets Manager)

| Variable | Secret Name | Description |
|----------|-------------|-------------|
| `DATABASE_URL` | `donation-genie/dev/database-url` | PostgreSQL connection string: `postgres://USER:PASS@HOST:5432/DBNAME` |
| `DJANGO_SECRET_KEY` | `donation-genie/dev/django-secret-key` | Django cryptographic signing key |

### Environment Variables (plaintext in task definition)

| Variable | Value | Description |
|----------|-------|-------------|
| `DJANGO_ENV` | `production` | Loads production settings module |
| `DEBUG` | `False` | Disables Django debug mode |
| `ALLOWED_HOSTS` | `*` | CloudFront rewrites Host header; ALB health checks use container IP. Accept all since ALB SG restricts access. |
| `VITE_API_URL` | `/api` | Frontend API base URL (baked into frontend build, not used by backend) |

### Build-time Variables (frontend)

| Variable | Value | Description |
|----------|-------|-------------|
| `VITE_API_URL` | `/api` | API base URL used during `npm run build`. Baked into the JS bundle. |

## Django Settings Mapping

The backend reads these variables in `backend/config/settings/production.py`:

| Variable | Django Setting | Default |
|----------|---------------|---------|
| `DJANGO_SECRET_KEY` | `SECRET_KEY` | (none — required) |
| `DEBUG` | `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `ALLOWED_HOSTS` | `[]` |
| `DATABASE_URL` | `DATABASES['default']` | (none — required) |

## RDS Connection String Format

```
postgres://<username>:<password>@<rds-endpoint>:5432/donation_genie
```

- `<username>`: RDS master username (managed by RDS + Secrets Manager)
- `<password>`: RDS master password (managed by RDS + Secrets Manager)
- `<rds-endpoint>`: RDS instance endpoint (output from Terraform RDS module)
- Database name: `donation_genie`

## Terraform Variables

### Required (no defaults)

| Variable | Type | Description |
|----------|------|-------------|
| `aws_region` | string | AWS region for all resources |
| `project_name` | string | Project identifier used in resource naming |

### Optional (with defaults)

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `environment` | string | `"dev"` | Environment name (used in resource tags and naming) |
| `ecs_cpu` | number | `512` | ECS task CPU units |
| `ecs_memory` | number | `1024` | ECS task memory (MiB) |
| `ecs_desired_count` | number | `1` | Number of ECS tasks to run |
| `rds_instance_class` | string | `"db.t4g.micro"` | RDS instance type |
| `rds_allocated_storage` | number | `20` | RDS initial storage (GB) |
| `rds_max_allocated_storage` | number | `100` | RDS max autoscale storage (GB) |
| `db_name` | string | `"donation_genie"` | PostgreSQL database name |
