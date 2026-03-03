#!/usr/bin/env bash
# Shared helper functions for deployment scripts.
# Source this file: source "$(dirname "${BASH_SOURCE[0]}")/_common.sh"

check_aws_cli() {
  if ! command -v aws &>/dev/null; then
    echo "ERROR: AWS CLI is not installed. Install it from https://aws.amazon.com/cli/"
    exit 1
  fi
}

check_aws_credentials() {
  check_aws_cli
  if ! aws sts get-caller-identity &>/dev/null; then
    echo "ERROR: AWS credentials are not configured or have expired."
    echo "Run 'aws configure' or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
    exit 1
  fi
}

check_terraform() {
  if ! command -v terraform &>/dev/null; then
    echo "ERROR: Terraform is not installed. Install it from https://developer.hashicorp.com/terraform/install"
    exit 1
  fi
}

check_docker() {
  if ! command -v docker &>/dev/null; then
    echo "ERROR: Docker is not installed. Install it from https://docs.docker.com/get-docker/"
    exit 1
  fi
  if ! docker info &>/dev/null 2>&1; then
    echo "ERROR: Docker is not running. Start Docker and try again."
    exit 1
  fi
}

check_terraform_init() {
  local tf_dir="$1"
  if [ ! -d "$tf_dir/.terraform" ]; then
    echo "ERROR: Terraform is not initialized. Run './scripts/deploy-init.sh' first."
    exit 1
  fi
}
