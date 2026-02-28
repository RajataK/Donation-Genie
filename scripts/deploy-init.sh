#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TF_DIR="$REPO_ROOT/terraform/environments/dev"

source "$SCRIPT_DIR/_common.sh"

echo "=== Initialize Terraform ==="
echo ""

# Check prerequisites
check_terraform
check_aws_credentials

# Initialize Terraform
cd "$TF_DIR"
echo "--- Running terraform init ---"
terraform init
echo ""

echo "=== Initialization Complete ==="
echo ""
echo "Next steps:"
echo "  ./scripts/deploy-plan.sh    # Preview changes"
echo "  ./scripts/deploy-apply.sh   # Apply changes"
