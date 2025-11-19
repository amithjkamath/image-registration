#!/bin/bash

# Test script to verify the updated app works locally

echo "🧪 Testing Image Registration App with HF Dataset"
echo "=================================================="
echo ""

# Check if in correct directory
if [ ! -f "image-registration-demo.py" ]; then
    echo "❌ Error: image-registration-demo.py not found"
    echo "Please run this script from the repository root"
    exit 1
fi

echo "📦 Installing dependencies..."
uv pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

echo "🚀 Starting Streamlit app..."
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""
echo "Note: The first run will download the dataset from Hugging Face"
echo ""

streamlit run image-registration-demo.py
