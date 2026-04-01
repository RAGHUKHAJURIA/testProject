#!/bin/bash
# Deploy script for AWS ECS

set -e

ENVIRONMENT=${1:-dev}
CLUSTER="devops-automation-cluster-${ENVIRONMENT}"
SERVICE="devops-automation-service-${ENVIRONMENT}"
REGION=${AWS_REGION:-us-east-1}

echo "Deploying to $ENVIRONMENT environment..."

# Get current task definition
TASK_DEFINITION=$(aws ecs describe-services \
    --cluster "$CLUSTER" \
    --services "$SERVICE" \
    --region "$REGION" \
    --query 'services[0].taskDefinition' \
    --output text)

echo "Current task definition: $TASK_DEFINITION"

# Update service
echo "Updating service..."
aws ecs update-service \
    --cluster "$CLUSTER" \
    --service "$SERVICE" \
    --force-new-deployment \
    --region "$REGION"

# Wait for stability
echo "Waiting for service to stabilize..."
aws ecs wait services-stable \
    --cluster "$CLUSTER" \
    --services "$SERVICE" \
    --region "$REGION"

echo "Deployment complete!"

# Get service status
aws ecs describe-services \
    --cluster "$CLUSTER" \
    --services "$SERVICE" \
    --region "$REGION" \
    --query 'services[0].[serviceName, status, desiredCount, runningCount]' \
    --output table
