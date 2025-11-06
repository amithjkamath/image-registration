#!/bin/bash

# Quick deployment script for Hugging Face Spaces
# This script helps you deploy your Streamlit app to Hugging Face Spaces

set -e

echo "🚀 Hugging Face Spaces Deployment Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if huggingface-cli is installed
if ! command -v huggingface-cli &> /dev/null; then
    echo -e "${YELLOW}⚠️  Hugging Face CLI not found. Installing...${NC}"
    pip install huggingface_hub
fi

# Check if logged in
if ! huggingface-cli whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Hugging Face${NC}"
    echo "Please login with your Hugging Face token:"
    huggingface-cli login
fi

echo -e "${GREEN}✅ Hugging Face CLI ready${NC}"
echo ""

# Space details
SPACE_ID="amithkamath/image-registration"
SPACE_URL="https://huggingface.co/spaces/$SPACE_ID"

echo "Target Space: $SPACE_ID"
echo "Space URL: $SPACE_URL"
echo ""

# Check if remote exists
if git remote | grep -q "^hf$"; then
    echo -e "${GREEN}✅ Hugging Face remote already configured${NC}"
else
    echo -e "${YELLOW}⚠️  Adding Hugging Face remote...${NC}"
    git remote add hf "https://huggingface.co/spaces/$SPACE_ID"
fi

echo ""
echo "Files to be deployed:"
git ls-files | grep -E "(dockerfile|requirements\.txt|.*\.py|.*\.png|README\.md|LICENSE)"
echo ""

# Confirm deployment
read -p "Do you want to deploy these files to $SPACE_ID? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}📦 Preparing deployment...${NC}"
    
    # Check if there are uncommitted changes
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}⚠️  You have uncommitted changes. Committing them...${NC}"
        git add dockerfile requirements.txt image-registration-demo.py rawimage.png README.md LICENSE 2>/dev/null || true
        git commit -m "Deploy to Hugging Face Spaces"
    fi
    
    echo -e "${YELLOW}🚀 Pushing to Hugging Face Spaces...${NC}"
    
    # Push to Hugging Face
    if git push hf main; then
        echo ""
        echo -e "${GREEN}✅ Deployment successful!${NC}"
        echo ""
        echo "Your app is being built at:"
        echo "$SPACE_URL"
        echo ""
        echo "Check the build logs at:"
        echo "$SPACE_URL?logs=build"
        echo ""
        echo "Once built, your app will be available at:"
        echo "$SPACE_URL"
    else
        echo ""
        echo -e "${RED}❌ Deployment failed. Check the error messages above.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    exit 0
fi
