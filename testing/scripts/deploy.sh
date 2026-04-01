#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Validate input: Expects the full image name including repository and tag
if [ -z "$1" ]; then
  echo "Usage: $0 <FULL_IMAGE_NAME_WITH_TAG>"
  echo "Example: $0 your-ecr-repo/your-app:latest"
  exit 1
fi

FULL_IMAGE=$1
K8S_DEPLOYMENT_FILE="k8s/deployment.yaml"

echo "Deploying application with image: ${FULL_IMAGE}"

# --- Option 1: Using kubectl set image (recommended for robustness) ---
# This method directly updates the image in the live deployment without modifying the YAML file in the repo.
# Requires the deployment name and container name.
# You might need to retrieve these, or hardcode if stable.
# Example: Assuming deployment 'my-app-deployment' and container 'my-app-container'
# kubectl set image deployment/your-app-deployment your-app-container="${FULL_IMAGE}" --record
# If you don't know the exact deployment/container name, you might need to read it from `k8s/deployment.yaml`

# For simplicity and working directly with the file, we'll proceed with sed. 
# For production, consider `kubectl set image`, Kustomize, or Helm for image updates.

# --- Option 2: Using sed to update the image in the local deployment manifest ---
# This assumes a consistent image path and name in your deployment.yaml like 'image: your-app-image:TAG'
# You need to identify the exact image string to replace in k8s/deployment.yaml

# A more robust sed command might target a specific image name within the YAML structure.
# Example: sed -i "s|\(image: your-app-image:\).*|\1${IMAGE_TAG}|g" "${K8S_DEPLOYMENT_FILE}"
# For this example, let's assume the image name in deployment.yaml is 'your-app-image'
# and we want to replace 'your-app-image:some-old-tag' with the new full image string.

echo "Updating image in ${K8S_DEPLOYMENT_FILE} to ${FULL_IMAGE}"
# This sed command attempts to replace the image value for the 'your-app-image' container.
# It's a heuristic and might need adjustment based on the exact content of your deployment.yaml
sed -i "/name: your-app-container/,/image:/s|image: .*|image: ${FULL_IMAGE}|g" "${K8S_DEPLOYMENT_FILE}"
# If 'your-app-container' is not present or structure is different, you might need a simpler
# sed -i "s|image: your-registry/your-app:.*|image: ${FULL_IMAGE}|g" "${K8S_DEPLOYMENT_FILE}"


echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/database.yaml
kubectl apply -f "${K8S_DEPLOYMENT_FILE}"
kubectl apply -f k8s/ingress.yaml

echo "Deployment manifests applied. Waiting for rollout..."
# Assuming the deployment is named 'your-app-deployment' in k8s/deployment.yaml
kube_deployment_name=$(grep -E 'name:' ${K8S_DEPLOYMENT_FILE} | head -1 | awk '{print $2}')
if [ -z "$kube_deployment_name" ]; then
  echo "Could not determine deployment name from ${K8S_DEPLOYMENT_FILE}. Skipping rollout status check." >&2
else
  echo "Waiting for deployment ${kube_deployment_name} rollout to complete..."
  kubectl rollout status deployment/${kube_deployment_name} --timeout=5m
fi

echo "Deployment complete."

# Optional: Health check
echo "Running health check..."
./scripts/health-check.sh

echo "Health check complete. Application deployed successfully."
