# Research: AWS Serverless Infrastructure as Code

**Feature**: 003-aws-serverless-iac
**Date**: 2026-02-27

## R1: CloudFront Distribution Architecture

**Decision**: Single CloudFront distribution with two origins — S3 (default) and ALB (ordered behavior for `/api/*`).

**Rationale**: A unified domain eliminates CORS issues between frontend and backend. CloudFront provides automatic HTTPS termination, DDoS protection via AWS Shield Standard (free), and global edge caching for static assets.

**Key implementation details**:
- Use **Origin Access Control (OAC)**, not legacy Origin Access Identity (OAI). OAC supports per-distribution bucket policies and is actively maintained.
- Default behavior (`/*`) routes to S3 origin for the React SPA.
- Ordered behavior (`/api/*`) routes to ALB origin with `CachingDisabled` managed cache policy and `AllViewerExceptHostHeader` origin request policy (forwards all headers/cookies except Host to ALB).
- Add `custom_error_response` blocks for 403 and 404 that return `/index.html` with HTTP 200 — required for SPA client-side routing (direct navigation to `/search` or `/admin` would otherwise return 403 from S3).
- Use `price_class = "PriceClass_100"` (US/Europe only) for dev to reduce costs.
- Enable `compress = true` on all cache behaviors.

**Alternatives considered**:
- Separate domains for frontend and backend: Rejected — requires CORS configuration, complicates deployment, worse user experience.
- API Gateway instead of ALB: Rejected — user explicitly requested ALB for ECS health checks and load balancing.
- CloudFront Functions for SPA routing: Rejected — custom error responses are simpler and sufficient.

## R2: ECS Fargate Backend

**Decision**: ECS Fargate service with ECR-hosted Docker image, running Django + Gunicorn behind an internal ALB.

**Rationale**: Fargate eliminates server management while providing predictable pricing and scaling. ECR integrates natively with ECS for image pulls.

**Key implementation details**:
- **Task size (dev)**: 512 CPU units (0.5 vCPU), 1024 MiB memory. Supports 2 Gunicorn workers (formula: 2 × vCPU + 1 ≈ 2).
- **Gunicorn command**: `gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`
- **Logging**: `awslogs` driver shipping to CloudWatch Logs.
- **Secrets**: Store `DATABASE_URL`, `DJANGO_SECRET_KEY` in AWS Secrets Manager; reference via `secrets` block in task definition (never plaintext `environment`).
- **ECR**: Enable `image_tag_mutability = "IMMUTABLE"` and `image_scanning_on_push`. Lifecycle policy to expire untagged images after 14 days.
- **ALB**: Internal (not internet-facing) since CloudFront is the sole entry point. Health check on `/api/health/` with interval=30s, timeout=5s, healthy=2, unhealthy=3. Deregistration delay=30s.
- **Database migrations**: Run as a one-shot ECS task (`aws ecs run-task` with command override `["python", "manage.py", "migrate"]`) before deploying the new service version.
- **Production Dockerfile**: Add a `production` stage to existing backend Dockerfile — multi-stage build with gunicorn as entrypoint, `collectstatic` during build.

**Alternatives considered**:
- Lambda + API Gateway: Rejected — user explicitly requested ECS. Also, Django on Lambda requires ASGI adapter (Mangum) and has cold start issues.
- ECS on EC2: Rejected — adds server management overhead contrary to "serverless" requirement.

## R3: RDS PostgreSQL

**Decision**: RDS PostgreSQL 17 in private subnets, `db.t4g.micro` for dev environment.

**Rationale**: Managed PostgreSQL eliminates database administration. T4g (Graviton2) instances are ~20% cheaper than T3 equivalents. The project already uses PostgreSQL 17 in Docker Compose.

**Key implementation details**:
- **Instance class**: `db.t4g.micro` (2 vCPU, 1 GB RAM) — Free Tier eligible for first year, ~$12/mo after.
- **Storage**: `gp3`, 20 GB allocated, 100 GB max with autoscaling. gp3 provides 3000 IOPS baseline regardless of size.
- **Placement**: Private subnets only, `publicly_accessible = false`.
- **Security group**: Single inbound rule — TCP 5432 from ECS tasks security group only.
- **Encryption**: `storage_encrypted = true` using default AWS KMS key.
- **Backups**: `backup_retention_period = 7`, `skip_final_snapshot = true` (dev environment).
- **Multi-AZ**: Disabled for dev (`multi_az = false`). Requires a DB subnet group spanning 2 AZs regardless.
- **Password management**: Use `manage_master_user_password = true` to let RDS auto-generate and store the password in Secrets Manager.

**Alternatives considered**:
- Aurora Serverless v2: Rejected — more expensive at minimum ($0.12/ACU-hr vs ~$0.016/hr for t4g.micro), over-engineered for dev.
- Self-managed PostgreSQL on ECS: Rejected — adds operational complexity for database management.

## R4: S3 Configuration

**Decision**: Two S3 buckets — one for frontend static assets (CloudFront OAC), one for Terraform state (versioned + locked).

**Frontend bucket**:
- Block all public access (access exclusively through CloudFront OAC).
- Enable versioning for rollback capability.
- Do NOT enable S3 static website hosting — CloudFront serves via REST API endpoint (required for OAC).
- Bucket policy allows only the CloudFront distribution ARN via `aws:SourceArn` condition.

**Terraform state bucket**:
- Enable versioning for state recovery.
- Enable server-side encryption (AES256).
- DynamoDB table with `LockID` partition key (String), `PAY_PER_REQUEST` billing (essentially free).
- `prevent_destroy = true` lifecycle rule.

**Alternatives considered**:
- Terraform Cloud for state: Rejected — adds external dependency, S3 is simpler and already part of the AWS ecosystem.
- S3 native locking (Terraform 1.10+): Rejected for now — DynamoDB locking is more mature and well-documented.

## R5: Networking

**Decision**: VPC with 2 AZs, public + private subnets, single NAT gateway.

**Rationale**: ALB and RDS both require resources in at least 2 AZs. Private subnets for ECS tasks and RDS protect them from direct internet access. Single NAT gateway minimizes cost (~$32/mo vs ~$64/mo for one per AZ).

**Key implementation details**:
- **CIDR**: `10.0.0.0/16`
- **Public subnets**: `10.0.1.0/24`, `10.0.2.0/24` — ALB, NAT Gateway.
- **Private subnets**: `10.0.11.0/24`, `10.0.12.0/24` — ECS tasks, RDS.
- **NAT Gateway**: Single, in one public subnet. Required for ECS tasks to pull ECR images and reach AWS APIs.
- **VPC module**: `terraform-aws-modules/vpc/aws ~> 5.0` handles subnets, route tables, NAT, IGW.

**Security group strategy** (separate SGs per tier, referencing each other by SG ID):
- **ALB SG**: Ingress from CloudFront managed prefix list (`com.amazonaws.global.cloudfront.origin-facing`) on port 443. Egress to ECS SG on port 8000.
- **ECS Tasks SG**: Ingress from ALB SG on port 8000. Egress to RDS SG on 5432, and `0.0.0.0/0` on 443 (for AWS API access via NAT).
- **RDS SG**: Ingress from ECS Tasks SG on port 5432. No egress rules needed.

**Alternatives considered**:
- VPC endpoints instead of NAT Gateway: Rejected — 4 interface endpoints (ECR API, ECR DKR, CloudWatch Logs, Secrets Manager) cost ~$29/mo, comparable to NAT but more complex and don't cover external API calls.
- fck-nat instance: Rejected — lower cost (~$4/mo) but adds operational complexity (EC2 instance management, ENI routing) contrary to "proven solutions" principle.
- No private subnets (everything public): Rejected — security risk, RDS should never be publicly accessible.

## R6: Terraform Structure

**Decision**: Module-per-service organization with a bootstrap directory and environment-specific root modules.

**Rationale**: Modules provide clear boundaries, are reusable across environments, and keep each concern isolated. Bootstrap handles the chicken-and-egg problem of creating the S3 bucket that stores Terraform state.

**Bootstrap pattern**:
1. `terraform/bootstrap/` defines S3 bucket + DynamoDB table.
2. Run `terraform init` (local state) → `terraform apply`.
3. Add `backend "s3" {}` to bootstrap config.
4. Run `terraform init -migrate-state` to move bootstrap state into S3.
5. All environment configs reference this bucket.

**Module list**: `networking`, `security-groups`, `ecr`, `rds`, `alb`, `ecs`, `s3-frontend`, `cloudfront`.

**Alternatives considered**:
- Flat structure (no modules): Rejected — becomes unmanageable as infrastructure grows, harder to reason about dependencies.
- Terragrunt: Rejected — adds tooling complexity, overkill for single environment.
- CDK/Pulumi: Rejected — user explicitly requested Terraform.

## R7: Production Dockerfile Strategy

**Decision**: Add a `production` stage to the existing backend Dockerfile. Frontend built locally and uploaded to S3.

**Backend Dockerfile production stage**:
- Base: `python:3.13-slim`
- Install production requirements (includes gunicorn)
- Run `collectstatic` during build
- Entrypoint: gunicorn with 2 workers
- No dev dependencies, no source code mounting

**Frontend deployment**:
- Build locally via `npm run build` (produces `dist/`)
- Upload `dist/` contents to S3 frontend bucket via `aws s3 sync`
- Invalidate CloudFront cache after upload

**Alternatives considered**:
- Frontend Docker image served by nginx: Rejected — S3 + CloudFront is simpler, cheaper, and more performant for static assets.
- Separate production Dockerfile: Rejected — multi-stage builds in the same file are standard practice and keep the build context consistent.
