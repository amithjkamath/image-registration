# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
# Dockerfile for Streamlit Image Registration Demo

FROM python:3.11-slim

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y \
    freeglut3-dev \
    libgtk2.0-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Create user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy application files
COPY --chown=user . /app

# Expose Streamlit default port
EXPOSE 7860

# Set Streamlit configuration
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run Streamlit app
CMD ["streamlit", "run", "image-registration-demo.py", "--server.port=7860", "--server.address=0.0.0.0"]