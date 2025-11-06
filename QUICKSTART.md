# Quick Reference - Deploying to Hugging Face Spaces

## 🚀 Quick Start (Easiest Method)

```bash
# 1. Install Hugging Face CLI
pip install huggingface_hub

# 2. Login with your token
huggingface-cli login

# 3. Run the deployment script
./deploy.sh
```

## 📝 Manual Deployment Steps

### First Time Setup

```bash
# 1. Login to Hugging Face
huggingface-cli login

# 2. Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/amithkamath/image-registration

# 3. Push to deploy
git push hf main
```

### Subsequent Deployments

```bash
# 1. Commit your changes
git add .
git commit -m "Your update message"

# 2. Push to deploy
git push hf main
```

## 🔑 Getting Your Hugging Face Token

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "image-registration-deploy"
4. Access: **Write**
5. Click "Generate token"
6. Copy and save the token

## 🔒 Setting Up Secrets (Password Protection)

Your app uses password protection. You need to configure secrets:

### Option 1: Via Hugging Face UI (Recommended)

1. Go to: https://huggingface.co/spaces/amithkamath/image-registration/settings
2. Scroll to "Repository secrets"
3. Add secrets for your usernames/passwords

### Option 2: Create secrets.toml file

Create `.streamlit/secrets.toml` (locally, DO NOT commit):

```toml
[passwords]
your_username = "your_password"
another_user = "another_password"
```

Then set as environment variable in Space settings.

## 📊 Monitoring Your Deployment

- **Space URL**: https://huggingface.co/spaces/amithkamath/image-registration
- **Build Logs**: https://huggingface.co/spaces/amithkamath/image-registration?logs=build
- **Settings**: https://huggingface.co/spaces/amithkamath/image-registration/settings

## 🐛 Common Issues

### "Authentication failed"
→ Run `huggingface-cli login` again with a valid token

### "Build failed"
→ Check logs at the Space URL, verify dockerfile and requirements.txt

### "App doesn't start"
→ Ensure port 7860 is used and Streamlit command is correct in dockerfile

### "Secrets not working"
→ Verify secrets are set in Space settings, check key names match your code

## 📁 Required Files

Ensure these files are in your repo:
- ✅ `dockerfile` - Docker configuration
- ✅ `requirements.txt` - Python dependencies  
- ✅ `image-registration-demo.py` - Your Streamlit app
- ✅ `rawimage.png` - Sample image
- ✅ `README.md` - With Hugging Face metadata

## 🔄 Update Workflow

```bash
# 1. Make changes to your code
vim image-registration-demo.py

# 2. Test locally
streamlit run image-registration-demo.py

# 3. Commit and push
git add .
git commit -m "Update: description"
git push hf main

# 4. Monitor deployment
# Visit: https://huggingface.co/spaces/amithkamath/image-registration
```

## 🛠️ Testing Locally with Docker

Before deploying, test your Docker setup locally:

```bash
# Build the image
docker build -t image-registration .

# Run the container
docker run -p 7860:7860 image-registration

# Open browser
open http://localhost:7860
```

## 📚 Full Documentation

For detailed instructions, see: [DEPLOYMENT.md](./DEPLOYMENT.md)

## 🆘 Need Help?

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces-sdks-docker)
- [Hugging Face Forums](https://discuss.huggingface.co/)
- [Streamlit Docs](https://docs.streamlit.io/)
