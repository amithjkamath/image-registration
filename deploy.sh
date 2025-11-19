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

# Check if hf CLI is installed
if ! command -v hf &> /dev/null; then
    echo -e "${YELLOW}⚠️  Hugging Face CLI not found. Installing...${NC}"
    pip install huggingface_hub
fi

# Check if logged in
if ! hf whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Hugging Face${NC}"
    echo "Please login with your Hugging Face token:"
    hf auth login
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
git ls-files | grep -E "(Dockerfile|requirements\.txt|.*\.py|README\.md|LICENSE)"
echo ""
echo "📊 Note: Images are loaded from HF dataset (amithjkamath/exampleimages)"
echo "   No need to include rawimage.png or other binary files"
echo ""

# Confirm deployment
read -p "Do you want to deploy these files to $SPACE_ID? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}📦 Preparing deployment...${NC}"
    
    # Add all essential files for the Space
    echo "Adding files to git..."
    git add Dockerfile requirements.txt image-registration-demo.py README.md LICENSE .gitignore 2>/dev/null || true
    
    # Remove deleted files (like rawimage.png)
    git add -u 2>/dev/null || true
    
    # Check if there are changes to commit
    if ! git diff-index --quiet HEAD --; then
        echo -e "${YELLOW}⚠️  Committing changes...${NC}"
        git commit -m "Deploy to Hugging Face Spaces - updated app with dataset integration"
    else
        echo -e "${GREEN}✅ No new changes to commit${NC}"
    fi
    
    echo -e "${YELLOW}🚀 Pushing to Hugging Face Spaces...${NC}"
    
    # Try to push to Hugging Face
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
        echo -e "${RED}❌ Push failed. The remote branch has changes that aren't in your local branch.${NC}"
        echo ""
        echo "This typically happens when:"
        echo "  - The Space was modified directly on Hugging Face"
        echo "  - You're deploying from a different machine"
        echo ""
        echo -e "${YELLOW}Options:${NC}"
        echo "  1. Pull and merge: git pull hf main (safer, preserves remote changes)"
        echo "  2. Force push: Overwrite remote with your local version (will lose remote changes)"
        echo ""
        read -p "Do you want to FORCE PUSH and overwrite the remote? (y/n) " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}⚠️  Force pushing to Hugging Face Spaces...${NC}"
            if git push hf main --force; then
                echo ""
                echo -e "${GREEN}✅ Force deployment successful!${NC}"
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
                echo -e "${RED}❌ Force push also failed. Check your permissions and network connection.${NC}"
                exit 1
            fi
        else
            echo ""
            echo -e "${YELLOW}Force push cancelled.${NC}"
            echo ""
            echo "To manually resolve, run:"
            echo "  git pull hf main"
            echo "  git push hf main"
            exit 1
        fi
    fi
else
    echo -e "${YELLOW}Deployment cancelled.${NC}"
    exit 0
fi
