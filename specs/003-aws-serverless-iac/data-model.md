# Data Model: AWS Serverless Infrastructure as Code

**Feature**: 003-aws-serverless-iac
**Date**: 2026-02-27

## Overview

This feature is Infrastructure-as-Code. The "data model" describes the AWS resources and their relationships, not database entities. The application database schema is unchanged — the existing Django models are deployed as-is on RDS PostgreSQL.

## Infrastructure Resource Model

### Resource Dependency Graph

```text
                    ┌──────────────┐
                    │  CloudFront  │
                    │ Distribution │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │ default /*  │ /api/*     │
              ▼            │            ▼
     ┌────────────┐        │    ┌──────────────┐
     │ S3 Bucket  │        │    │   ALB        │
     │ (frontend) │        │    │ (internal)   │
     └────────────┘        │    └──────┬───────┘
                           │           │
                           │    ┌──────▼───────┐
                           │    │ ECS Fargate  │
                           │    │  Service     │
                           │    └──────┬───────┘
                           │           │
                           │    ┌──────▼───────┐     ┌─────────────┐
                           │    │ ECS Task     │────▶│ ECR Repo    │
                           │    │ Definition   │     │ (image)     │
                           │    └──────┬───────┘     └─────────────┘
                           │           │
                           │    ┌──────▼───────┐
                           │    │ RDS Postgres │
                           │    │ (private)    │
                           │    └──────────────┘
                           │
              ┌────────────┴────────────┐
              │         VPC             │
              │  ┌────────┐ ┌────────┐  │
              │  │Public  │ │Private │  │
              │  │Subnets │ │Subnets │  │
              │  │(ALB,   │ │(ECS,   │  │
              │  │ NAT)   │ │ RDS)   │  │
              │  └────────┘ └────────┘  │
              └─────────────────────────┘
```

### Resource Entities

#### VPC & Networking

| Resource         | Purpose                          | Key Attributes                             |
| ---------------- | -------------------------------- | ------------------------------------------ |
| VPC              | Network isolation                | CIDR: `10.0.0.0/16`, DNS hostnames enabled |
| Public Subnet A  | ALB, NAT Gateway (AZ-a)          | CIDR: `10.0.1.0/24`                        |
| Public Subnet B  | ALB (AZ-b)                       | CIDR: `10.0.2.0/24`                        |
| Private Subnet A | ECS tasks, RDS (AZ-a)            | CIDR: `10.0.11.0/24`                       |
| Private Subnet B | ECS tasks, RDS (AZ-b)            | CIDR: `10.0.12.0/24`                       |
| Internet Gateway | Public subnet internet access    | Attached to VPC                            |
| NAT Gateway      | Private subnet outbound internet | Single, in Public Subnet A                 |

#### Security Groups

| Security Group | Inbound Rules                | Outbound Rules                   |
| -------------- | ---------------------------- | -------------------------------- |
| ALB SG         | CloudFront prefix list → 443 | ECS Tasks SG → 8000              |
| ECS Tasks SG   | ALB SG → 8000                | RDS SG → 5432, `0.0.0.0/0` → 443 |
| RDS SG         | ECS Tasks SG → 5432          | (none)                           |

#### Compute & Storage

| Resource            | Purpose                        | Key Attributes                                              |
| ------------------- | ------------------------------ | ----------------------------------------------------------- |
| ECR Repository      | Docker image storage           | Immutable tags, scan on push, 14-day untagged lifecycle     |
| ECS Cluster         | Container orchestration        | Fargate capacity provider                                   |
| ECS Service         | Keeps task running             | Desired count: 1, ALB target group attachment               |
| ECS Task Definition | Container spec                 | 512 CPU, 1024 MiB, Gunicorn on port 8000, awslogs driver    |
| ALB                 | Load balancing + health checks | Internal, health check: `/api/health/`, deregistration: 30s |
| ALB Target Group    | Routes to ECS tasks            | Port 8000, HTTP, health check interval: 30s                 |

#### Data

| Resource         | Purpose              | Key Attributes                                                    |
| ---------------- | -------------------- | ----------------------------------------------------------------- |
| RDS PostgreSQL   | Application database | db.t4g.micro, PostgreSQL 17, gp3 20GB, private subnets, encrypted |
| RDS Subnet Group | Multi-AZ placement   | Private Subnet A + Private Subnet B                               |

#### Content Delivery

| Resource                | Purpose                 | Key Attributes                                      |
| ----------------------- | ----------------------- | --------------------------------------------------- |
| S3 Bucket (frontend)    | Static SPA hosting      | Private, versioned, OAC access only                 |
| CloudFront Distribution | Edge delivery + routing | OAC for S3, ALB origin for `/api/*`, PriceClass_100 |
| CloudFront OAC          | S3 access control       | Signing behavior: always, protocol: sigv4           |

#### State Management

| Resource          | Purpose                 | Key Attributes                           |
| ----------------- | ----------------------- | ---------------------------------------- |
| S3 Bucket (state) | Terraform state storage | Versioned, encrypted, prevent_destroy    |
| DynamoDB Table    | Terraform state locking | Partition key: `LockID`, PAY_PER_REQUEST |

#### Secrets

| Secret              | Stored In       | Consumed By         |
| ------------------- | --------------- | ------------------- |
| `DATABASE_URL`      | Secrets Manager | ECS Task Definition |
| `DJANGO_SECRET_KEY` | Secrets Manager | ECS Task Definition |

### Resource Relationships

1. **CloudFront → S3**: Default origin via OAC. Bucket policy allows only this distribution's ARN.
2. **CloudFront → ALB**: Ordered cache behavior for `/api/*`. CachingDisabled policy, AllViewerExceptHostHeader request policy.
3. **ALB → ECS Service**: Target group registration. Health checks on `/api/health/`.
4. **ECS Task → ECR**: Image pull at task launch.
5. **ECS Task → RDS**: PostgreSQL connection via `DATABASE_URL` from Secrets Manager.
6. **ECS Task → Secrets Manager**: `secrets` block in container definition retrieves `DATABASE_URL` and `DJANGO_SECRET_KEY`.
7. **ECS Tasks → NAT Gateway**: Outbound internet via private subnet route table for AWS API calls.
8. **All resources → VPC**: Networking context for ALB, ECS, RDS, NAT.

### State Transitions

This feature has no application-level state transitions. Infrastructure state is managed entirely by Terraform:

- **Not created** → `terraform apply` → **Active**
- **Active** → `terraform plan` (change detected) → `terraform apply` → **Updated**
- **Active** → `terraform destroy` → **Destroyed**
- **Destroyed** → `terraform apply` → **Active** (re-created)
