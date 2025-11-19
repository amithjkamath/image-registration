# Deploying to Hugging Face Spaces - Complete Guide

This guide will walk you through deploying your Streamlit Image Registration app to Hugging Face Spaces using Docker.

**Note**: This app loads images from a Hugging Face dataset (`amithjkamath/exampleimages`) instead of bundling them with the Space, which allows you to avoid the binary file restrictions on Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (sign up at https://huggingface.co/join)
2. Git installed on your local machine
3. Your Space already created at: https://huggingface.co/spaces/amithkamath/image-registration

## Step 1: Set Up Hugging Face CLI and Authentication

### Install Hugging Face CLI
```bash
pip install huggingface_hub
```

### Create a Hugging Face Token

1. Go to https://huggingface.co/settings/tokens
2. Click on "New token"
3. Give it a descriptive name (e.g., "image-registration-deploy")
4. Select "Write" access (required for pushing to your Space)
5. Click "Generate token"
6. **Important**: Copy and save this token securely - you won't be able to see it again!

### Login to Hugging Face

```bash
hf auth login
```

When prompted, paste your token. This will store your credentials in `~/.huggingface/token`.

Alternatively, you can set it as an environment variable:
```bash
export HF_TOKEN=your_token_here
```

## Step 2: Configure Git for Hugging Face

Hugging Face Spaces uses Git LFS (Large File Storage) for large files. Set up Git LFS:

```bash
# Install git-lfs if you haven't already
# On macOS:
brew install git-lfs

# Initialize git-lfs
git lfs install
```

## Step 3: Clone Your Hugging Face Space

```bash
# Clone your space repository
git clone https://huggingface.co/spaces/amithkamath/image-registration
cd image-registration
```

Alternatively, if you want to push from your existing local repository:

```bash
# In your current repo directory
git remote add hf https://huggingface.co/spaces/amithkamath/image-registration
```

## Step 4: Prepare Your Files

Make sure your repository contains the following files:

### Required Files:
- ✅ `dockerfile` - Your Docker configuration (already created)
- ✅ `requirements.txt` - Python dependencies (already created, includes `datasets` library)
- ✅ `image-registration-demo.py` - Your Streamlit app (updated to load from HF dataset)
- ✅ `README.md` - Documentation for your Space

### ⚠️ Important: Image Dataset
This app loads images from a separate Hugging Face dataset: `amithjkamath/exampleimages`

**Why?** Hugging Face Spaces with the blank Docker template don't support binary files like images in the repository. By loading images from a dataset, we circumvent this limitation.

**Your dataset**: https://huggingface.co/datasets/amithjkamath/exampleimages

The app will automatically download images from this dataset when it starts. Make sure the dataset is public or set up proper authentication if it's private.

### Optional but Recommended:
- `.gitignore` - To exclude unnecessary files
- `LICENSE` - Your license file

### Create a README.md for Hugging Face Space

Create or update your `README.md` with proper metadata at the top:

```markdown
---
title: Image Registration Demo
emoji: 🔄
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Image Registration Demo

This is a demonstration of how transformation matrices affect registration for the affine case.

[Rest of your existing README content...]
```

## Step 5: Set Up Secrets (for Password Protection)

Your app uses `st.secrets` for password protection. You need to set this up in Hugging Face Spaces:

1. Go to your Space settings: https://huggingface.co/spaces/amithkamath/image-registration/settings
2. Scroll down to "Repository secrets"
3. Add secrets as needed

For Streamlit secrets, create a `.streamlit/secrets.toml` file locally (DO NOT commit this to git):

```toml
[passwords]
username1 = "password1"
username2 = "password2"
```

Then in Hugging Face Space settings, add each secret:
- Key: `STREAMLIT_SECRETS`
- Value: The entire contents of your `secrets.toml` file

Alternatively, you can mount secrets as environment variables and modify your app to read from environment variables instead.

## Step 6: Update .gitignore

Create or update `.gitignore` to exclude sensitive and unnecessary files:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Other
*.log
```

## Step 7: Deploy to Hugging Face Spaces

### Method A: Push from Your Existing Repository

```bash
# Make sure all your files are committed
git add dockerfile requirements.txt image-registration-demo.py README.md
git commit -m "Initial deployment to Hugging Face Spaces with dataset integration"

# Push to Hugging Face (assuming you added the remote in Step 3)
git push hf main
```

### Method B: Clone and Deploy

If you cloned the HF space in Step 3:

```bash
# Copy your files to the cloned space directory
cp /path/to/your/repo/* /path/to/cloned/space/

# Add and commit
git add .
git commit -m "Deploy Streamlit app with Docker"

# Push to Hugging Face
git push origin main
```

### Method C: Using Hugging Face Hub Python API

```python
from huggingface_hub import HfApi

api = HfApi()

# Upload files
api.upload_folder(
    folder_path=".",
    repo_id="amithkamath/image-registration",
    repo_type="space",
    ignore_patterns=[".git/*", "__pycache__/*", ".streamlit/secrets.toml"]
)
```

## Step 8: Monitor Deployment

1. Go to your Space: https://huggingface.co/spaces/amithkamath/image-registration
2. Click on the "Logs" tab to see build progress
3. The build process will:
   - Build your Docker image
   - Install dependencies
   - Start your Streamlit app
4. Once completed, your app will be available at the Space URL

## Step 9: Troubleshooting

### Build Fails
- Check the logs in the "Logs" tab
- Verify all dependencies are correctly specified in `requirements.txt`
- Ensure the Dockerfile syntax is correct

### App Doesn't Start
- Check if the correct port (7860) is being used
- Verify the CMD in Dockerfile is correct
- Check for Python errors in the logs

### Secrets Not Working
- Ensure secrets are properly set in Space settings
- Verify the app can access them correctly

### Image Not Found
- Make sure `rawimage.png` is committed and pushed to the repository
- Check file paths are correct (relative to the working directory)

## Step 10: Update Your Deployment

When you want to update your app:

```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push hf main
```

The Space will automatically rebuild and redeploy.

## Advanced: Continuous Deployment from GitHub

If you want to maintain your code on GitHub and automatically deploy to Hugging Face:

1. Keep your main repository on GitHub
2. Set up a GitHub Action to push to Hugging Face on every commit to main
3. Create `.github/workflows/deploy-to-hf.yml`:

```yaml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches:
      - main

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          lfs: true
      
      - name: Push to Hugging Face Space
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: |
          git config --global user.email "github-actions@github.com"
          git config --global user.name "GitHub Actions"
          git remote add hf https://amithkamath:$HF_TOKEN@huggingface.co/spaces/amithkamath/image-registration
          git push hf main --force
```

4. Add your HF_TOKEN as a secret in your GitHub repository settings

## Useful Commands

```bash
# Check Space status
hf repo info amithkamath/image-registration --repo-type space

# View Space logs (if available via CLI)
hf repo logs amithkamath/image-registration --repo-type space

# Delete and recreate Space (careful!)
hf repo delete amithkamath/image-registration --repo-type space
```

## Resources

- [Hugging Face Spaces Docker Documentation](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Hugging Face Spaces Overview](https://huggingface.co/docs/hub/spaces-overview)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Git LFS Documentation](https://git-lfs.github.com/)

## Support

If you encounter issues:
1. Check the [Hugging Face Forums](https://discuss.huggingface.co/)
2. Review the [Spaces FAQ](https://huggingface.co/docs/hub/spaces-faq)
3. Open an issue in the Hugging Face Hub repository
