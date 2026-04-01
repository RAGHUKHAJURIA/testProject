#!/bin/bash
# Initialize infrastructure with Terraform

set -e

ENVIRONMENT=${1:-dev}
REGION=${AWS_REGION:-us-east-1}

echo "Initializing infrastructure for $ENVIRONMENT environment..."

cd terraform/

# Initialize Terraform
echo "Initializing Terraform..."
terraform init -upgrade

# Validate
echo "Validating Terraform configuration..."
terraform validate

# Plan
echo "Planning infrastructure..."
terraform plan \
    -var="environment=$ENVIRONMENT" \
    -var="aws_region=$REGION" \
    -out=tfplan

echo "✓ Terraform plan complete"
echo "Review the plan above and run 'terraform apply tfplan' to deploy"
