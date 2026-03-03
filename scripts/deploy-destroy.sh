#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TF_DIR="$REPO_ROOT/terraform/environments/dev"

source "$SCRIPT_DIR/_common.sh"

echo "=== Destroy Infrastructure ==="
echo ""
echo "WARNING: This will destroy ALL cloud resources in the dev environment."
echo "The Terraform state backend (S3 bucket + DynamoDB table) will be preserved."
echo ""

# Check prerequisites
check_terraform
check_aws_credentials
check_terraform_init "$TF_DIR"

# Confirmation prompt
read -rp "Type 'yes' to confirm destruction: " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
  echo "Aborted."
  exit 0
fi

echo ""

# Empty the frontend S3 bucket before destroying (Terraform can't delete non-empty buckets)
cd "$TF_DIR"
FRONTEND_BUCKET=$(terraform output -raw frontend_bucket_name 2>/dev/null || echo "")
if [ -n "$FRONTEND_BUCKET" ]; then
  echo "--- Emptying frontend S3 bucket ---"
  aws s3 rm "s3://$FRONTEND_BUCKET" --recursive || true
  echo ""
fi

# Destroy infrastructure
echo "--- Destroying infrastructure ---"
terraform destroy
echo ""

echo "=== Destruction Complete ==="
echo ""
echo "All dev environment resources have been destroyed."
echo "The state backend (S3 bucket + DynamoDB table) is preserved for future deployments."
echo ""
echo "To re-deploy, run:"
echo "  ./scripts/deploy-init.sh"
echo "  ./scripts/build-and-push.sh"
echo "  ./scripts/deploy-apply.sh"
