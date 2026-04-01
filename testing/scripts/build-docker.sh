#!/bin/bash
# Build Docker image locally

set -e

IMAGE_NAME=${1:-devops-automation-app}
IMAGE_TAG=${2:-latest}
DOCKERFILE=${3:-docker/Dockerfile}

echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"

docker build \
    -f "$DOCKERFILE" \
    -t "${IMAGE_NAME}:${IMAGE_TAG}" \
    -t "${IMAGE_NAME}:latest" \
    .

echo "✓ Docker image built successfully"
echo "Run 'docker run -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}' to start the container"
