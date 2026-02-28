# Quickstart: AWS Serverless Infrastructure as Code

**Feature**: 003-aws-serverless-iac
**Date**: 2026-02-27

## Prerequisites

1. **AWS CLI** configured with credentials (`aws configure` or environment variables)
2. **Terraform** >= 1.9 installed
3. **Docker** running locally (for building the backend image)
4. **Node.js** >= 24 (for building the frontend)

## First-Time Setup (Bootstrap)

Run once to create the Terraform state backend (S3 bucket + DynamoDB lock table):

```bash
./scripts/bootstrap.sh
```

This script:

1. Initializes `terraform/bootstrap/` with local state
2. Creates the S3 bucket and DynamoDB table
3. Migrates the bootstrap state to the new S3 bucket

## Build & Push Backend Image

Build the production Docker image and push to ECR:

```bash
./scripts/build-and-push.sh
```

This script:

1. Logs into ECR
2. Builds the backend Docker image (production stage)
3. Tags and pushes to the ECR repository

> **Note**: The ECR repository is created by Terraform. Run `deploy-apply.sh` at least once before this script, or create the ECR repository first with a targeted apply.

## Deploy Infrastructure

### Initialize Terraform

```bash
./scripts/deploy-init.sh
```

### Preview Changes

```bash
./scripts/deploy-plan.sh
```

Review the output carefully. It shows exactly what resources will be created, modified, or destroyed.

### Apply Changes

```bash
./scripts/deploy-apply.sh
```

After apply completes, the script outputs:

- CloudFront URL (the application URL)
- ALB DNS name (internal, for debugging)
- RDS endpoint (internal, for debugging)

### Deploy Frontend

After the infrastructure is created, build and deploy the frontend:

```bash
cd frontend
npm run build
aws s3 sync dist/ s3://<frontend-bucket-name> --delete
aws cloudfront create-invalidation --distribution-id <dist-id> --paths "/*"
```

> The bucket name and distribution ID are output by `deploy-apply.sh`.

## Destroy Infrastructure

```bash
./scripts/deploy-destroy.sh
```

This removes ALL cloud resources. The Terraform state backend (S3 bucket + DynamoDB table) is preserved for future deployments.

## Common Workflows

### Update backend code

```bash
./scripts/build-and-push.sh          # Build and push new image
./scripts/deploy-plan.sh             # Preview (should show task definition update)
./scripts/deploy-apply.sh            # Apply
```

### Update frontend code

```bash
cd frontend && npm run build && cd ..
aws s3 sync frontend/dist/ s3://<frontend-bucket-name> --delete
aws cloudfront create-invalidation --distribution-id <dist-id> --paths "/*"
```

### Run database migrations

```bash
aws ecs run-task \
  --cluster donation-genie-dev \
  --task-definition donation-genie-dev \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[<private-subnet-ids>],securityGroups=[<ecs-sg-id>]}" \
  --overrides '{"containerOverrides":[{"name":"django","command":["python","manage.py","migrate"]}]}'
```

## Estimated Costs (Idle)

| Resource                        | Monthly Cost                      |
| ------------------------------- | --------------------------------- |
| NAT Gateway                     | ~$32                              |
| ALB                             | ~$16                              |
| ECS Fargate (512 CPU, 1024 MiB) | ~$15                              |
| RDS db.t4g.micro                | ~$12 (Free Tier: $0)              |
| CloudFront                      | ~$1                               |
| S3 (both buckets)               | ~$1                               |
| ECR                             | ~$1                               |
| DynamoDB (state locks)          | ~$0                               |
| **Total**                       | **~$78/mo** (~$66 with Free Tier) |
