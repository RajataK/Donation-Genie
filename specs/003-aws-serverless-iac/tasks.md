# Tasks: AWS Serverless Infrastructure as Code

**Input**: Design documents from `/specs/003-aws-serverless-iac/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested. IaC validation uses `terraform validate`, `terraform fmt -check`, and `terraform plan` as documented in the Constitution Check (TDD adapted for IaC).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the Terraform project structure, provider configuration, and version constraints.

- [x] T001 Create terraform/ directory structure matching plan.md layout: `terraform/bootstrap/`, `terraform/modules/{networking,security-groups,ecr,rds,alb,ecs,s3-frontend,cloudfront}/`, `terraform/environments/dev/`, and `scripts/`
- [x] T002 Create Terraform version constraints and AWS provider configuration in `terraform/environments/dev/main.tf` — require Terraform >= 1.9, AWS provider ~> 5.0, pin `us-east-1` region from variable
- [x] T003 [P] Add Terraform and AWS entries to `.gitignore`: `.terraform/`, `*.tfstate`, `*.tfstate.*`, `*.tfplan`, `.terraform.lock.hcl` (do NOT ignore lock file — commit it), `crash.log`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure modules that ALL user stories depend on — VPC networking, security groups, container registry, state backend, and production Dockerfile.

**CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Create bootstrap module in `terraform/bootstrap/main.tf`, `terraform/bootstrap/variables.tf`, `terraform/bootstrap/outputs.tf` — S3 bucket (versioned, AES256 encrypted, prevent_destroy lifecycle), DynamoDB table (LockID partition key, PAY_PER_REQUEST), and a `backend "s3" {}` block (commented out initially, uncommented after first apply + state migration). Variables: `project_name`, `aws_region`. Outputs: `state_bucket_name`, `dynamodb_table_name`.
- [x] T005 [P] Create networking module in `terraform/modules/networking/main.tf`, `terraform/modules/networking/variables.tf`, `terraform/modules/networking/outputs.tf` — use `terraform-aws-modules/vpc/aws ~> 5.0` with CIDR `10.0.0.0/16`, 2 AZs, public subnets (`10.0.1.0/24`, `10.0.2.0/24`), private subnets (`10.0.11.0/24`, `10.0.12.0/24`), single NAT gateway, DNS hostnames enabled. Variables: `project_name`, `environment`, `aws_region`. Outputs: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`.
- [x] T006 [P] Create security groups module in `terraform/modules/security-groups/main.tf`, `terraform/modules/security-groups/variables.tf`, `terraform/modules/security-groups/outputs.tf` — three SGs referencing each other by SG ID: (1) ALB SG: ingress from CloudFront managed prefix list on port 80, egress to ECS SG on 8000; (2) ECS Tasks SG: ingress from ALB SG on 8000, egress to RDS SG on 5432 and `0.0.0.0/0` on 443; (3) RDS SG: ingress from ECS Tasks SG on 5432, no egress. Use `aws_vpc_security_group_ingress_rule`/`aws_vpc_security_group_egress_rule` resources. Variables: `vpc_id`, `project_name`, `environment`. Outputs: `alb_sg_id`, `ecs_tasks_sg_id`, `rds_sg_id`.
- [x] T007 [P] Create ECR module in `terraform/modules/ecr/main.tf`, `terraform/modules/ecr/variables.tf`, `terraform/modules/ecr/outputs.tf` — repository with `image_tag_mutability = "IMMUTABLE"`, `image_scanning_on_push = true`, lifecycle policy expiring untagged images after 14 days. Variables: `project_name`, `environment`. Outputs: `repository_url`, `repository_name`.
- [x] T008 [P] Add production stage to `backend/Dockerfile` — new `AS production` stage: base `python:3.13-slim`, copy requirements, install production deps (including gunicorn), copy application code, run `python manage.py collectstatic --noinput`, expose port 8000, CMD `["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]`. Keep existing `development` stage unchanged.

**Checkpoint**: Foundation ready — Terraform modules for networking, security, ECR, and state backend exist. Production Dockerfile is ready. User story implementation can now begin.

---

## Phase 3: User Story 1 — Deploy Full Application to Cloud (Priority: P1) MVP

**Goal**: Deploy both frontend (S3 + CloudFront) and backend (ECS Fargate + ALB + RDS) to AWS so the application is publicly accessible.

**Independent Test**: Run deploy-apply, visit the CloudFront URL — frontend loads, `/api/health/` returns 200, frontend can communicate with backend.

### Implementation for User Story 1

- [x] T009 [P] [US1] Create RDS module in `terraform/modules/rds/main.tf`, `terraform/modules/rds/variables.tf`, `terraform/modules/rds/outputs.tf` — PostgreSQL 17 engine, `db.t4g.micro` default instance class, `gp3` storage (20 GB allocated, 100 GB max autoscaling), private subnet placement via `aws_db_subnet_group`, `publicly_accessible = false`, `storage_encrypted = true`, `manage_master_user_password = true`, `backup_retention_period = 7`, `skip_final_snapshot = true` (dev), `multi_az = false`. Variables: `project_name`, `environment`, `private_subnet_ids`, `rds_sg_id`, `instance_class`, `allocated_storage`, `max_allocated_storage`, `db_name`. Outputs: `db_endpoint`, `db_name`, `master_user_secret_arn`.
- [x] T010 [P] [US1] Create ALB module in `terraform/modules/alb/main.tf`, `terraform/modules/alb/variables.tf`, `terraform/modules/alb/outputs.tf` — internal ALB (`internal = true`) in public subnets, HTTP listener on port 80, target group on port 8000 (HTTP) with health check path `/api/health/` (interval 30s, timeout 5s, healthy threshold 2, unhealthy threshold 3), `deregistration_delay = 30`. Variables: `project_name`, `environment`, `vpc_id`, `public_subnet_ids`, `alb_sg_id`. Outputs: `alb_dns_name`, `alb_arn`, `target_group_arn`.
- [x] T011 [P] [US1] Create ECS module in `terraform/modules/ecs/main.tf`, `terraform/modules/ecs/variables.tf`, `terraform/modules/ecs/outputs.tf` — ECS cluster (Fargate capacity provider), task definition (512 CPU, 1024 MiB, `awslogs` log driver to CloudWatch, container port 8000, secrets from Secrets Manager for `DATABASE_URL` and `DJANGO_SECRET_KEY`, environment variables `DJANGO_ENV=production`, `DEBUG=False`, `ALLOWED_HOSTS=*`), ECS service (desired count 1, Fargate launch type, private subnets, ECS tasks SG, ALB target group attachment). Create `aws_secretsmanager_secret` + `aws_secretsmanager_secret_version` for `DJANGO_SECRET_KEY` using `random_password`. Construct `DATABASE_URL` secret from RDS outputs. Variables: `project_name`, `environment`, `private_subnet_ids`, `ecs_tasks_sg_id`, `target_group_arn`, `ecr_repository_url`, `image_tag`, `cpu`, `memory`, `desired_count`, `db_endpoint`, `db_name`, `db_master_user_secret_arn`, `aws_region`. Outputs: `cluster_name`, `service_name`.
- [x] T012 [P] [US1] Create S3 frontend module in `terraform/modules/s3-frontend/main.tf`, `terraform/modules/s3-frontend/variables.tf`, `terraform/modules/s3-frontend/outputs.tf` — private S3 bucket, block all public access, enable versioning, bucket policy allowing CloudFront distribution ARN via `aws:SourceArn` condition (pass `cloudfront_distribution_arn` as variable). Do NOT enable static website hosting (use REST API endpoint for OAC). Variables: `project_name`, `environment`, `cloudfront_distribution_arn`. Outputs: `bucket_id`, `bucket_arn`, `bucket_regional_domain_name`.
- [x] T013 [P] [US1] Create CloudFront module in `terraform/modules/cloudfront/main.tf`, `terraform/modules/cloudfront/variables.tf`, `terraform/modules/cloudfront/outputs.tf` — distribution with OAC for S3 origin (default `/*` behavior, `CachingOptimized` policy, GET/HEAD only, `compress = true`), ALB origin (ordered `/api/*` behavior, `CachingDisabled` policy, `AllViewerExceptHostHeader` request policy, all HTTP methods, HTTP-only origin protocol on port 80), `custom_error_response` blocks for 403→200 and 404→200 returning `/index.html`, `viewer_protocol_policy = "redirect-to-https"` on all behaviors, `price_class = "PriceClass_100"`. Variables: `project_name`, `environment`, `s3_bucket_regional_domain_name`, `s3_bucket_id`, `alb_dns_name`. Outputs: `distribution_id`, `distribution_arn`, `distribution_domain_name`.
- [x] T014 [US1] Create dev environment root module in `terraform/environments/dev/main.tf` — wire all modules together: networking → security-groups → ecr → rds → alb → ecs → s3-frontend → cloudfront. Pass outputs from upstream modules as inputs to downstream modules. Handle circular dependency between S3 frontend module (needs CloudFront ARN for bucket policy) and CloudFront module (needs S3 bucket domain) by creating the bucket policy as a separate `aws_s3_bucket_policy` resource in the root module after both are created.
- [x] T015 [P] [US1] Create dev environment variables in `terraform/environments/dev/variables.tf` and `terraform/environments/dev/terraform.tfvars` — define all variables per contracts/environment-variables.md: `aws_region` (default `"us-east-1"`), `project_name` (default `"donation-genie"`), `environment` (default `"dev"`), `ecs_cpu` (512), `ecs_memory` (1024), `ecs_desired_count` (1), `rds_instance_class` (`"db.t4g.micro"`), `rds_allocated_storage` (20), `rds_max_allocated_storage` (100), `db_name` (`"donation_genie"`), `image_tag` (`"latest"`).
- [x] T016 [P] [US1] Create dev environment backend config in `terraform/environments/dev/backend.tf` — S3 backend referencing bootstrap bucket name pattern `donation-genie-tf-state`, DynamoDB table `donation-genie-terraform-locks`, key `env/dev/terraform.tfstate`, region from variable, encrypt = true.
- [x] T017 [P] [US1] Create dev environment outputs in `terraform/environments/dev/outputs.tf` — output `cloudfront_url` (distribution domain name), `alb_dns_name`, `rds_endpoint`, `frontend_bucket_name` (for `aws s3 sync`), `ecr_repository_url` (for Docker push), `distribution_id` (for CloudFront invalidation), `ecs_cluster_name`, `ecs_service_name`.
- [x] T018 [US1] Create `scripts/build-and-push.sh` — check AWS credentials, get ECR repository URL from Terraform output (or accept as argument), `aws ecr get-login-password | docker login`, `docker build --target production -t <repo>:<tag> backend/`, `docker push`. Accept optional `--tag` argument (default: git SHA or `latest`). Make executable (`chmod +x`).
- [x] T019 [US1] Create `scripts/deploy-apply.sh` — `cd terraform/environments/dev`, `terraform apply`, display CloudFront URL and other outputs after successful apply. Include frontend deployment step: `cd frontend && npm ci && npm run build`, `aws s3 sync dist/ s3://<bucket> --delete`, `aws cloudfront create-invalidation --distribution-id <id> --paths "/*"`. Make executable.

**Checkpoint**: At this point, running bootstrap.sh → deploy-init.sh → build-and-push.sh → deploy-apply.sh deploys the full application. Frontend loads at CloudFront URL, `/api/health/` returns 200.

---

## Phase 4: User Story 2 — Preview and Control Infrastructure Changes (Priority: P2)

**Goal**: Developers can preview all proposed changes before applying, seeing exactly what will be created, modified, or destroyed.

**Independent Test**: Run deploy-plan.sh after making a Terraform change — output shows additions/modifications/deletions without modifying any resources. Run again with no changes — output says "No changes."

### Implementation for User Story 2

- [x] T020 [US2] Create `scripts/deploy-plan.sh` — `cd terraform/environments/dev`, `terraform plan -out=tfplan`, display formatted summary of proposed changes, save plan file for optional `terraform apply tfplan`. Check that terraform is initialized first (error if not). Make executable.

**Checkpoint**: Developer can preview changes before applying. "No changes" shown when infrastructure matches definitions.

---

## Phase 5: User Story 3 — Collaborative State Management (Priority: P3)

**Goal**: Infrastructure state is stored remotely in S3 with DynamoDB locking so multiple developers can collaborate without conflicts.

**Independent Test**: Two developers can each run deploy-plan.sh from their own machines and see the same current state. If one developer is applying, the other sees a lock error message.

### Implementation for User Story 3

- [x] T021 [US3] Create `scripts/bootstrap.sh` — check AWS credentials, `cd terraform/bootstrap`, `terraform init` (local state), `terraform apply -auto-approve`, then uncomment the `backend "s3" {}` block in `terraform/bootstrap/main.tf`, run `terraform init -migrate-state -force-copy` to move bootstrap state to S3. Print state bucket name and DynamoDB table name on success. Include idempotency check (skip if bucket already exists). Make executable.

**Checkpoint**: State stored in S3, DynamoDB provides locking. A second developer cloning the repo can run deploy-init.sh and see current state.

---

## Phase 6: User Story 4 — Simple Local CLI Workflow (Priority: P4)

**Goal**: Pre-built scripts let developers initialize, preview, and apply with simple commands — no need to memorize Terraform CLI details.

**Independent Test**: A new developer with AWS credentials can run: (1) `./scripts/bootstrap.sh`, (2) `./scripts/deploy-init.sh`, (3) `./scripts/deploy-apply.sh` — and have a fully deployed application.

### Implementation for User Story 4

- [x] T022 [US4] Create `scripts/deploy-init.sh` — check AWS credentials (verify `aws sts get-caller-identity` succeeds, error with clear message if not), `cd terraform/environments/dev`, `terraform init`. Print success message with next steps. Make executable.
- [x] T023 [US4] Add credential validation and consistent UX to all scripts in `scripts/` — add a shared helper function (inline or sourced from `scripts/_common.sh`) that: (1) checks `aws sts get-caller-identity` and prints clear error if credentials are missing/expired, (2) checks `terraform version` and prints clear error if Terraform is not installed, (3) checks `docker info` and prints clear error if Docker is not running (only in scripts that need it). Apply to all existing scripts: `bootstrap.sh`, `build-and-push.sh`, `deploy-init.sh`, `deploy-plan.sh`, `deploy-apply.sh`.

**Checkpoint**: All scripts validate prerequisites before running. Clear error messages guide developers when credentials/tools are missing.

---

## Phase 7: User Story 5 — Tear Down Infrastructure (Priority: P5)

**Goal**: Developers can completely destroy all cloud resources to avoid ongoing costs.

**Independent Test**: Run deploy-destroy.sh after a successful deployment — all AWS resources are removed, CloudFront URL no longer resolves, AWS cost dashboard shows no active resources (except state backend).

### Implementation for User Story 5

- [x] T024 [US5] Create `scripts/deploy-destroy.sh` — prompt for confirmation ("This will destroy ALL resources. Type 'yes' to continue"), empty the S3 frontend bucket first (`aws s3 rm s3://<bucket> --recursive`), then `cd terraform/environments/dev && terraform destroy`. Print confirmation of destruction and note that the state backend (S3 + DynamoDB) is preserved. Make executable.

**Checkpoint**: All cloud resources destroyed. State backend preserved for future re-deployment.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Validation, formatting, and documentation consistency.

- [x] T025 [P] Run `terraform fmt -recursive` on all `.tf` files in `terraform/` and fix any formatting issues
- [x] T026 [P] Run `terraform validate` on `terraform/bootstrap/` and `terraform/environments/dev/` — fix any validation errors
- [x] T027 Verify all scripts in `scripts/` have proper shebang (`#!/usr/bin/env bash`), `set -euo pipefail`, and are executable (`chmod +x`)
- [x] T028 Validate quickstart.md workflow: verify script names, argument patterns, and output descriptions match implemented scripts in `scripts/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion (T001, T002, T003) — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Phase 2 completion — all Terraform modules and deploy scripts
- **US2 (Phase 4)**: Depends on Phase 1 + Phase 2 (needs initialized Terraform) — can start in parallel with US1
- **US3 (Phase 5)**: Depends on Phase 2 (T004 bootstrap module exists) — can start in parallel with US1
- **US4 (Phase 6)**: Depends on US1 (T019), US2 (T020), US3 (T021) scripts existing — adds UX improvements
- **US5 (Phase 7)**: Depends on US1 (needs deployed resources to destroy) — can start after US1 scripts exist
- **Polish (Phase 8)**: Depends on all code being written (Phases 1–7)

### User Story Dependencies

- **US1 (P1)**: Blocked by Phase 2. THE MVP — all infrastructure modules + deploy scripts.
- **US2 (P2)**: Blocked by Phase 2. Single script task, can be written in parallel with US1.
- **US3 (P3)**: Blocked by Phase 2 (T004). Single script task, can be written in parallel with US1.
- **US4 (P4)**: Blocked by US1/US2/US3 scripts (adds shared validation across all scripts).
- **US5 (P5)**: Blocked by US1 (needs apply script and infrastructure context). Single script task.

### Within Phase 3 (US1)

- T009-T013 (modules) are all [P] — can be written in parallel
- T014 (root module) depends on T009-T013 (wires them together)
- T015-T017 (config files) are [P] — can be written in parallel with T014
- T018 (build-and-push) depends on T007 (ECR module) and T008 (production Dockerfile)
- T019 (deploy-apply) depends on T014 (root module complete)

### Parallel Opportunities

- **Phase 2**: T005, T006, T007, T008 all [P] (different directories, independent modules)
- **Phase 3**: T009, T010, T011, T012, T013 all [P] (different module directories)
- **Phase 3**: T015, T016, T017 all [P] (different files in dev environment)
- **US2 + US3 + US5**: Can all be written in parallel once their prerequisites exist

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch all independent module tasks together:
Task: "Create networking module in terraform/modules/networking/"      # T005
Task: "Create security groups module in terraform/modules/security-groups/"  # T006
Task: "Create ECR module in terraform/modules/ecr/"                    # T007
Task: "Add production stage to backend/Dockerfile"                     # T008
```

## Parallel Example: US1 Modules (Phase 3)

```bash
# Launch all US1 module tasks together:
Task: "Create RDS module in terraform/modules/rds/"           # T009
Task: "Create ALB module in terraform/modules/alb/"           # T010
Task: "Create ECS module in terraform/modules/ecs/"           # T011
Task: "Create S3 frontend module in terraform/modules/s3-frontend/"  # T012
Task: "Create CloudFront module in terraform/modules/cloudfront/"    # T013

# After modules complete, launch config files in parallel:
Task: "Create dev variables in terraform/environments/dev/variables.tf"  # T015
Task: "Create dev backend config in terraform/environments/dev/backend.tf"  # T016
Task: "Create dev outputs in terraform/environments/dev/outputs.tf"      # T017
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T008)
3. Complete Phase 3: US1 — Deploy Full Application (T009–T019)
4. **STOP and VALIDATE**: Run `terraform validate` and `terraform plan` — verify plan creates expected resources
5. Deploy and verify: frontend loads, `/api/health/` returns 200

### Incremental Delivery

1. Setup + Foundational → infrastructure scaffolding ready
2. Add US1 → Full deployment works → **MVP!**
3. Add US2 → Can preview before applying → safer deployments
4. Add US3 → Remote state with locking → team collaboration enabled
5. Add US4 → Consistent script UX → onboarding simplified
6. Add US5 → Clean destruction → cost control enabled
7. Polish → formatting, validation, documentation consistency

### Suggested MVP Scope

**US1 only** (Phases 1–3, tasks T001–T019). This delivers a fully deployable application on AWS. The remaining stories add workflow improvements but are not required for a working deployment.

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate the story independently
- `terraform fmt` and `terraform validate` should be run frequently during development, not just in Phase 8
- The S3 frontend bucket policy has a circular dependency with CloudFront (bucket needs distribution ARN, distribution needs bucket domain). T014 resolves this by creating the bucket policy as a separate resource in the root module.
- ALB listens on HTTP (port 80) — CloudFront handles HTTPS termination for viewers. Origin protocol is HTTP-only since ALB is internal.
