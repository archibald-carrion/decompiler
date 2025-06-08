# 🏛️ Roman Empire Fine-tuning with Docker

This Docker setup automatically handles all dependencies, training, and cleanup for fine-tuning DistilGPT2 on Roman Empire content.

## 📋 Prerequisites

- Docker installed and running
- The `roman_empire_finetune.py` script in the same directory

## 🚀 Quick Start

### Method 1: Using the Wrapper Script (Recommended)

1. **Make the wrapper script executable:**
   ```bash
   chmod +x run_roman_training.sh
   ```

2. **Train the model:**
   ```bash
   ./run_roman_training.sh train
   ```

3. **Use the trained model interactively:**
   ```bash
   ./run_roman_training.sh interactive
   ```

4. **Generate specific text:**
   ```bash
   ./run_roman_training.sh generate "Julius Caesar was"
   ```

5. **Compare models:**
   ```bash
   ./run_roman_training.sh compare
   ```

### Method 2: Using Docker Compose

1. **Train the model:**
   ```bash
   docker-compose run --rm roman-empire-training python roman_empire_finetune.py --train
   ```

2. **Interactive mode:**
   ```bash
   docker-compose run --rm roman-empire-training python roman_empire_finetune.py --interactive
   ```

### Method 3: Direct Docker Commands

1. **Build the image:**
   ```bash
   docker build -t roman-empire-finetuning .
   ```

2. **Train the model:**
   ```bash
   docker run -it --rm -v $(pwd)/models:/app/models roman-empire-finetuning python roman_empire_finetune.py --train
   ```

## 📁 File Structure

```
your-project/
├── roman_empire_finetune.py    # Main fine-tuning script
├── run_roman_training.sh       # Wrapper script (recommended)
├── docker-compose.yml          # Docker Compose setup
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── models/                     # Persistent model storage (created automatically)
│   ├── distilgpt2/            # Base model
│   └── distilgpt2-roman-empire/ # Fine-tuned model
└── cache/                      # HuggingFace cache (created automatically)
```

## 🔧 Available Commands

| Command | Description |
|---------|-------------|
| `train` | Fine-tune the model on Roman Empire data |
| `train --epochs 5` | Fine-tune with custom number of epochs |
| `interactive` | Interactive text generation mode |
| `generate "prompt"` | Generate text from a specific prompt |
| `compare` | Compare base vs fine-tuned models |
| `info` | Show model information and storage details |

## 💾 Model Persistence

- **Models are saved to:** `./models/` directory on your host machine
- **Survives container deletion:** Yes, models persist between runs
- **Cache location:** `./cache/` directory (speeds up subsequent runs)

## 🧹 Automatic Cleanup

The wrapper script (`run_roman_training.sh`) automatically:
- ✅ Builds the Docker image
- ✅ Runs the training/generation
- ✅ Stops and removes the container
- ✅ Removes the Docker image
- ✅ Preserves your trained models

## 🐛 Troubleshooting

### Keras/TensorFlow Version Issues
The Docker setup uses specific versions that are compatible:
- Python 3.9
- PyTorch 2.0+
- Transformers 4.30+
- No TensorFlow conflicts

### GPU Support
To enable GPU support, uncomment the GPU section in `docker-compose.yml` and ensure you have:
- NVIDIA Docker runtime installed
- NVIDIA GPU drivers

### Permission Issues
If you encounter permission issues with model files:
```bash
sudo chown -R $USER:$USER ./models/
```

## 📊 Training Details

- **Base Model:** DistilGPT2 (82M parameters)
- **Training Data:** 20 curated Roman Empire texts
- **Default Epochs:** 3
- **Training Time:** ~2-5 minutes (depending on hardware)
- **Model Size:** ~330MB after fine-tuning

## 🎯 Example Usage

```bash
# Full training workflow
./run_roman_training.sh train

# Test the trained model
./run_roman_training.sh generate "The Roman Empire"

# Interactive exploration
./run_roman_training.sh interactive

# Compare with base model
./run_roman_training.sh compare
```

## 🔄 Re-training

To retrain the model:
1. Remove existing fine-tuned model: `rm -rf ./models/distilgpt2-roman-empire/`
2. Run training again: `./run_roman_training.sh train`

The base model will be reused (no re-download needed).

---

**Note:** The Docker container automatically deletes itself after each run, but your trained models remain safely stored in the `./models/` directory!