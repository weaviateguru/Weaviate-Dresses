#!/bin/bash

# Configuration
ARTIFACTORY_URL="https://trialc38vpm.jfrog.io"
DEV_REPO="dress-review-dev-docker-local"
PROD_REPO="dress-review-prod-docker-local"
IMAGE_NAME="dress-review-dev-docker-local"            
TAG="cd71396a05737b75bc018e96e02ced2b508bdf2a"
BUILD_NAME="build-and-push-docker"   
BUILD_NUMBER="16"
JFROG_CLI="jf"

# Full image paths
SOURCE_IMAGE="$DEV_REPO/$IMAGE_NAME/$TAG/"
TARGET_IMAGE="$PROD_REPO/$IMAGE_NAME/$TAG/"


# Promote the Docker artifact
promote_artifact() {
    echo "Promoting $SOURCE_IMAGE to $PROD_REPO..."

    # Copy artifacts from development to production
    $JFROG_CLI rt cp "$SOURCE_IMAGE" "$TARGET_IMAGE"
    
    if [ $? -eq 0 ]; then
        echo "Successfully promoted $IMAGE_NAME:$TAG to $PROD_REPO."
    else
        echo "Error: Failed to promote $IMAGE_NAME:$TAG."
        exit 1
    fi
}

# Promote the build 
promote_build() {   
    echo "Promoting build $BUILD_NAME#$BUILD_NUMBER to $PROD_REPO..."
        
    #  Promote build info to production
    $JFROG_CLI rt build-promote "$BUILD_NAME" "$BUILD_NUMBER" "$PROD_REPO"
    
    if [ $? -eq 0 ]; then
        echo "Successfully promoted build $BUILD_NAME#$BUILD_NUMBER to $PROD_REPO."
    else
        echo "Error: Failed to promote build $BUILD_NAME#$BUILD_NUMBER."
        exit 1
    fi
}

# Main execution
echo "Starting promotion process..."

# Promote the artifact
promote_artifact

# Promote the build
promote_build

echo "Promotion process completed."



