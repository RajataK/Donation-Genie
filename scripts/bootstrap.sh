#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BOOTSTRAP_DIR="$REPO_ROOT/terraform/bootstrap"

source "$SCRIPT_DIR/_common.sh"

echo "=== Bootstrap Terraform State Backend ==="
echo ""

# Check prerequisites
check_terraform
check_aws_credentials

# Check if state bucket already exists (idempotency)
BUCKET_NAME="donation-genie-tf-state"
if aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
  echo "State bucket '$BUCKET_NAME' already exists. Skipping bootstrap."
  echo ""
  echo "If you need to re-initialize, run:"
  echo "  cd $BOOTSTRAP_DIR && terraform init"
  exit 0
fi

cd "$BOOTSTRAP_DIR"

# Step 1: Initialize with local state
echo "--- Step 1: Initializing with local state ---"
terraform init
echo ""

# Step 2: Create the state backend resources
echo "--- Step 2: Creating S3 bucket and DynamoDB table ---"
terraform apply -auto-approve
echo ""

# Step 3: Migrate state to S3
echo "--- Step 3: Migrating state to S3 ---"
# Uncomment the backend block in main.tf
sed -i.bak 's|# backend "s3" {|backend "s3" {|' main.tf
sed -i.bak 's|#   bucket|  bucket|' main.tf
sed -i.bak 's|#   key|  key|' main.tf
sed -i.bak 's|#   region|  region|' main.tf
sed -i.bak 's|#   dynamodb_table|  dynamodb_table|' main.tf
sed -i.bak 's|#   encrypt|  encrypt|' main.tf
sed -i.bak 's|# }|  }|' main.tf
rm -f main.tf.bak

terraform init -migrate-state -force-copy
echo ""

# Get outputs
STATE_BUCKET=$(terraform output -raw state_bucket_name)
DYNAMO_TABLE=$(terraform output -raw dynamodb_table_name)

echo "=== Bootstrap Complete ==="
echo ""
echo "State Bucket:    $STATE_BUCKET"
echo "DynamoDB Table:  $DYNAMO_TABLE"
echo ""
echo "Next step: Run './scripts/deploy-init.sh' to initialize the dev environment."
