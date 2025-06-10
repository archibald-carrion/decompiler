
#!/bin/bash

# Set up environment variables to avoid TensorFlow warnings
export TF_ENABLE_ONEDNN_OPTS=0
export PYTHONUNBUFFERED=1
export HF_HOME="$(pwd)/cache"

# Create necessary directories
mkdir -p ./models ./data ./cache

# Install system dependencies (for Debian/Ubuntu)
sudo apt-get update
sudo apt-get install -y gcc g++ python3-venv

# Set up Python virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

# Upgrade pip and install Python dependencies in the venv
pip install --upgrade pip
pip install -r requirements.txt

# Run the fine-tuning script using the venv's python
python roman_empire_finetune.py "$@"