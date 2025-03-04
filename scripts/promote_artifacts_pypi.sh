#!/bin/bash

# Configuration
ARTIFACTORY_URL="https://trialc38vpm.jfrog.io"
DEV_REPO="dress-review-dev-pypi-local"
PROD_REPO="dress-review-prod-pypi-local"
PACKAGE_NAME="dress-review-dev-pypi-local"
PACKAGE_VERSION=""
PACKAGE_FILE="dist/dress_review-0.1.0-py3-none-any.whl"
BUILD_NAME="build-and-push"   
BUILD_NUMBER="3"
JFROG_CLI="jf"


SOURCE_IMAGE="dress-review-dev-pypi-local/dist/dress_review-0.1.0-py3-none-any.whl"
TARGET_IMAGE="dress-review-prod-pypi-local/dist/dress_review-0.1.0-py3-none-any.whl"


# Promote the PyPI package
promote_package() {
    echo "Promoting $PACKAGE_FILE from $DEV_REPO to $PROD_REPO..."
    
    # Copy packages from development to production
    $JFROG_CLI rt cp "$SOURCE_IMAGE" "$TARGET_IMAGE"
    
    if [ $? -eq 0 ]; then
        echo "Successfully promoted $PACKAGE_FILE to $PROD_REPO."
    else
        echo "Error: Failed to promote $PACKAGE_FILE."
        exit 1
    fi
}

# Promote the build 
promote_build() {   
    echo "Promoting build $BUILD_NAME#$BUILD_NUMBER to $PROD_REPO..."
        
    # Promoting build info to production
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

# Promote the package
promote_package

# Promote the build
promote_build

echo "Promotion process completed."



