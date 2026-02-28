# Implementation Plan: AWS Serverless Infrastructure as Code

**Branch**: `003-aws-serverless-iac` | **Date**: 2026-02-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-aws-serverless-iac/spec.md`

## Summary

Deploy the Donation Genie frontend and backend to AWS using Terraform as Infrastructure as Code. The frontend (static SPA) is served from an S3 bucket via CloudFront. The backend (Django/Gunicorn) runs on ECS Fargate behind an ALB, with the Docker image stored in ECR. The database is RDS PostgreSQL. A single CloudFront distribution serves both: `/` for the frontend and `/api/*` routed to the ALB. Terraform state is stored in S3 with DynamoDB locking. Bash scripts provide simple init/plan/apply/destroy workflows.

## Technical Context

**Language/Version**: HCL (Terraform >= 1.9), Python 3.13 (backend Dockerfile), TypeScript 5.7 (frontend build)
**Primary Dependencies**: Terraform AWS Provider ~> 5.0, terraform-aws-modules/vpc/aws ~> 5.0
**Storage**: RDS PostgreSQL 17 (db.t4g.micro for dev), S3 (frontend assets + Terraform state)
**Testing**: `terraform validate`, `terraform fmt -check`, `terraform plan` (dry-run), smoke tests via health endpoint
**Target Platform**: AWS (us-east-1), CloudFront edge distribution
**Project Type**: Infrastructure-as-Code (Terraform) + production Dockerfiles + deployment scripts
**Performance Goals**: First deploy < 15 min, subsequent deploys < 5 min
**Constraints**: Idle cost target ~$75-80/mo (see Cost Analysis note below); single environment (dev)
**Scale/Scope**: Single environment, 1 ECS task, 1 RDS instance, 1 CloudFront distribution

> **Cost Analysis Note**: The spec defines SC-008 as "Monthly cloud costs for an idle deployment remain under $10." This is not achievable with the specified architecture. Fixed costs for always-on RDS (~$12/mo), NAT Gateway (~$32/mo), ALB (~$16/mo), and ECS Fargate (~$15/mo) total ~$75-80/mo minimum. This is the expected cost for the architecture the user specified (ECS + ALB + RDS + CloudFront). The $10 target would require a fundamentally different architecture (e.g., Lambda + Aurora Serverless v2 with scale-to-zero).

## Constitution Check

_GATE: Must pass before Phase 0 research. Re-check after Phase 1 design._

| Principle                      | Status  | Notes                                                                                                                                                                                                                                                                                   |
| ------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I. TDD (NON-NEGOTIABLE)        | ADAPTED | IaC does not follow traditional Red-Green-Refactor. Adapted as: (1) `terraform validate` + `terraform fmt -check` as static analysis, (2) `terraform plan` as the "test" before `apply`, (3) post-deploy smoke tests against `/api/health/`. See Complexity Tracking for justification. |
| II. Proven Solutions           | PASS    | Uses official Terraform AWS provider, community VPC module (`terraform-aws-modules/vpc/aws`), standard AWS services (ECS Fargate, ALB, RDS, CloudFront, S3). No custom or novel patterns.                                                                                               |
| III. No Premature Optimization | PASS    | Single environment, single NAT gateway, smallest viable instance sizes, no multi-region, no caching layers, no auto-scaling.                                                                                                                                                            |
| Accessibility                  | N/A     | No UI changes in this feature.                                                                                                                                                                                                                                                          |
| Contract-first API             | PASS    | No API changes. Existing OpenAPI schema served at `/api/schema/` remains unchanged. CloudFront routing preserves the `/api/*` path prefix.                                                                                                                                              |
| Responsive design              | N/A     | No UI changes in this feature.                                                                                                                                                                                                                                                          |

**Quality Gates**:

1. All tests pass: `terraform validate` succeeds, `terraform plan` produces valid plan, post-deploy health check returns 200.
2. Linting clean: `terraform fmt -check` reports no differences.
3. TDD evidence: Validate/plan run before apply in all scripts. See Complexity Tracking.
4. No NEEDS CLARIFICATION: All resolved in research phase.
5. Accessibility audit: N/A (infrastructure only, no UI changes).

## Project Structure

### Documentation (this feature)

```text
specs/003-aws-serverless-iac/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── cloudfront-routing.md
│   └── environment-variables.md
└── tasks.md
```

### Source Code (repository root)

```text
terraform/
├── bootstrap/                    # State backend (uses local state initially)
│   ├── main.tf                   # S3 bucket + DynamoDB lock table
│   ├── variables.tf
│   └── outputs.tf
│
├── modules/
│   ├── networking/               # VPC, subnets, NAT, IGW
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── security-groups/          # All security groups
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecr/                      # ECR repository
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/                      # PostgreSQL instance
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── alb/                      # ALB + target group + listener
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ecs/                      # Cluster, service, task definition
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── s3-frontend/              # Frontend bucket + OAC policy
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── cloudfront/               # Distribution + cache behaviors
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── environments/
    └── dev/                      # Dev environment
        ├── main.tf               # Root module calling all modules
        ├── backend.tf            # S3 backend configuration
        ├── variables.tf
        ├── terraform.tfvars
        └── outputs.tf

backend/
├── Dockerfile                    # Updated: add production stage
└── ...                           # Existing code unchanged

scripts/
├── bootstrap.sh                  # First-time: create state backend
├── build-and-push.sh             # Build Docker image, push to ECR
├── deploy-init.sh                # terraform init
├── deploy-plan.sh                # terraform plan
├── deploy-apply.sh               # terraform apply
└── deploy-destroy.sh             # terraform destroy
```

**Structure Decision**: The infrastructure code lives in a new top-level `terraform/` directory, separate from application code. Terraform is organized into reusable modules (one per AWS service/concern) called from environment-specific root modules. Deployment scripts live in `scripts/` at the repo root. The only change to existing code is adding a production stage to the backend Dockerfile.

## Complexity Tracking

| Violation           | Why Needed                                                                                                                                                                         | Simpler Alternative Rejected Because                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TDD adapted for IaC | Traditional Red-Green-Refactor cannot apply to declarative infrastructure definitions. Terraform files are declarations of desired state, not imperative code with testable units. | Writing Terratest or similar Go-based tests would add a Go toolchain dependency and significant complexity for a single-environment dev deployment. `terraform validate` + `terraform plan` provide equivalent safety: plan shows exactly what will change before any mutation occurs, serving the same purpose as a failing test before implementation. Post-deploy smoke tests verify the final result. |
