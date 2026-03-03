#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TF_DIR="$REPO_ROOT/terraform/environments/dev"

source "$SCRIPT_DIR/_common.sh"

echo "=== Preview Infrastructure Changes ==="
echo ""

# Check prerequisites
check_terraform
check_aws_credentials
check_terraform_init "$TF_DIR"

# Run plan
cd "$TF_DIR"
echo "--- Running terraform plan ---"
terraform plan -out=tfplan
echo ""

echo "=== Plan Complete ==="
echo ""
echo "To apply this plan, run:"
echo "  cd $TF_DIR && terraform apply tfplan"
echo ""
echo "Or use: ./scripts/deploy-apply.sh"
