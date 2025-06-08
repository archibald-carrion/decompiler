# Dockerfile for Roman Empire Fine-tuning
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the fine-tuning script
COPY roman_empire_finetune.py .

# Create directories for models (will be mounted as volumes)
RUN mkdir -p /app/models /app/data

# Set environment variables to avoid TensorFlow warnings
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/cache

# Default command - can be overridden
CMD ["python", "roman_empire_finetune.py", "--help"]