#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TF_DIR="$REPO_ROOT/terraform/environments/dev"

source "$SCRIPT_DIR/_common.sh"

echo "=== Deploy Infrastructure ==="
echo ""

# Check prerequisites
check_terraform
check_aws_credentials
check_terraform_init "$TF_DIR"

# Apply infrastructure
echo "--- Applying Terraform changes ---"
cd "$TF_DIR"
terraform apply
echo ""

# Get outputs
CLOUDFRONT_URL=$(terraform output -raw cloudfront_url 2>/dev/null || echo "")
FRONTEND_BUCKET=$(terraform output -raw frontend_bucket_name 2>/dev/null || echo "")
DISTRIBUTION_ID=$(terraform output -raw distribution_id 2>/dev/null || echo "")
ECR_REPO_URL=$(terraform output -raw ecr_repository_url 2>/dev/null || echo "")

# Build and deploy frontend
echo "--- Building frontend ---"
cd "$REPO_ROOT/frontend"
npm ci
npm run build
echo ""

if [ -n "$FRONTEND_BUCKET" ]; then
  echo "--- Deploying frontend to S3 ---"
  aws s3 sync dist/ "s3://$FRONTEND_BUCKET" --delete
  echo ""
fi

if [ -n "$DISTRIBUTION_ID" ]; then
  echo "--- Invalidating CloudFront cache ---"
  aws cloudfront create-invalidation \
    --distribution-id "$DISTRIBUTION_ID" \
    --paths "/*" \
    --output text \
    --no-cli-pager
  echo ""
fi

echo "=== Deployment Complete ==="
echo ""
echo "Application URL:    ${CLOUDFRONT_URL:-N/A}"
echo "ECR Repository:     ${ECR_REPO_URL:-N/A}"
echo "Frontend Bucket:    ${FRONTEND_BUCKET:-N/A}"
echo "Distribution ID:    ${DISTRIBUTION_ID:-N/A}"
