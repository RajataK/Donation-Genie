#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TF_DIR="$REPO_ROOT/terraform/environments/dev"

source "$SCRIPT_DIR/_common.sh"

# Parse arguments
IMAGE_TAG="${1:-$(git -C "$REPO_ROOT" rev-parse --short HEAD 2>/dev/null || echo "latest")}"

echo "=== Build and Push Backend Image ==="
echo "Image tag: $IMAGE_TAG"
echo ""

# Check prerequisites
check_aws_credentials
check_docker

# Get ECR repository URL from Terraform output
if [ -f "$TF_DIR/.terraform/terraform.tfstate" ] || [ -f "$TF_DIR/.terraform.lock.hcl" ]; then
  ECR_REPO_URL=$(cd "$TF_DIR" && terraform output -raw ecr_repository_url 2>/dev/null || true)
fi

if [ -z "${ECR_REPO_URL:-}" ]; then
  echo "ERROR: Could not get ECR repository URL from Terraform outputs."
  echo "Make sure you have run './scripts/deploy-apply.sh' at least once."
  exit 1
fi

AWS_REGION=$(cd "$TF_DIR" && terraform output -raw 2>/dev/null | head -0; echo "eu-west-2")
AWS_REGION="${AWS_REGION:-eu-west-2}"
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "ECR Repository: $ECR_REPO_URL"
echo ""

# Log in to ECR
echo "--- Logging in to ECR ---"
aws ecr get-login-password --region "$AWS_REGION" \
  | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"
echo ""

# Build the production image
echo "--- Building production image ---"
docker build \
  --platform linux/amd64 \
  --target production \
  -t "$ECR_REPO_URL:$IMAGE_TAG" \
  -f "$REPO_ROOT/backend/Dockerfile" \
  "$REPO_ROOT/backend"
echo ""

# Push to ECR
echo "--- Pushing to ECR ---"
docker push "$ECR_REPO_URL:$IMAGE_TAG"
echo ""

echo "=== Done ==="
echo "Image pushed: $ECR_REPO_URL:$IMAGE_TAG"
