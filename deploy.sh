#!/bin/bash
set -e

# === Configuration - CHANGE THESE ===
DOCKER_USERNAME="bananapeel202"
IMAGE_NAME="fencingfit"
AZURE_RESOURCE_GROUP="fencingfit"
AZURE_APP_SERVICE_PLAN="fencingfit"
AZURE_WEBAPP_NAME="fencingfit"  # Must be globally unique

# === Get the latest git commit short hash ===
GIT_HASH=$(git rev-parse --short HEAD)
IMAGE_TAG="$GIT_HASH"

echo "Using git commit hash as tag: $IMAGE_TAG"

# === Use docker buildx to build amd64 image and push ===
echo "Building and pushing multi-arch Docker image (linux/amd64)..."
docker buildx create --use || true  # create builder if doesn't exist
docker buildx build --platform linux/amd64 \
  -t $DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG \
  --push .

# === Create Azure Resource Group (if not exists) ===
echo "Creating resource group (if not exists)..."
az group create --name $AZURE_RESOURCE_GROUP --location westus

# === Create Azure App Service Plan (Linux) (if not exists) ===
echo "Creating App Service plan (if not exists)..."
az appservice plan create \
  --name $AZURE_APP_SERVICE_PLAN \
  --resource-group $AZURE_RESOURCE_GROUP \
  --is-linux \
  --sku B2 || echo "App Service plan already exists or created."

# === Create Web App (if not exists) ===
echo "Creating Web App (if not exists)..."
az webapp create \
  --resource-group $AZURE_RESOURCE_GROUP \
  --plan $AZURE_APP_SERVICE_PLAN \
  --name $AZURE_WEBAPP_NAME \
  --deployment-container-image-name $DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG || echo "Web App already exists or created."

az webapp config appsettings set \
--resource-group $AZURE_RESOURCE_GROUP \
--name $AZURE_WEBAPP_NAME \
--settings WEBSITES_PORT=3000

# === Configure Web App to use the new Docker image ===
echo "Configuring Web App to use image $DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG ..."
az webapp config container set \
  --resource-group $AZURE_RESOURCE_GROUP \
  --name $AZURE_WEBAPP_NAME \
  --docker-custom-image-name $DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG

# === Restart Web App to apply changes ===
echo "Restarting Web App..."
az webapp restart --name $AZURE_WEBAPP_NAME --resource-group $AZURE_RESOURCE_GROUP

echo "Deployment complete! Your app should be live at: https://$AZURE_WEBAPP_NAME.azurewebsites.net"