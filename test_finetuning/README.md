# 🏛️ Roman Empire Fine-tuning with Docker

This Docker setup automatically handles all dependencies, training, and cleanup for fine-tuning DistilGPT2 on Roman Empire content.

## 📋 Prerequisites

- Docker installed and running
- The `roman_empire_finetune.py` script in the same directory

## 🚀 Quick Start

### Method 1: Using Docker Compose

1. **Train the model:**
   ```bash
   docker-compose run --rm roman-empire-training python roman_empire_finetune.py --train
   ```

2. **Interactive mode:**
   ```bash
   docker-compose run --rm roman-empire-training python roman_empire_finetune.py --interactive
   ```

### Method 2: Direct Docker Commands

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
test_finetuning/
├── Dockerfile
├── README.md
├── cache
├── data
├── docker-compose.yml
├── execution_error.txt
├── models
│   ├── distilgpt2
│   │   ├── config.json
│   │   ├── generation_config.json
│   │   ├── merges.txt
│   │   ├── model.safetensors
│   │   ├── special_tokens_map.json
│   │   ├── tokenizer_config.json
│   │   └── vocab.json
│   └── distilgpt2-roman-empire
│       ├── checkpoint-30
│       │   ├── config.json
│       │   ├── generation_config.json
│       │   ├── merges.txt
│       │   ├── model.safetensors
│       │   ├── optimizer.pt
│       │   ├── rng_state.pth
│       │   ├── scheduler.pt
│       │   ├── special_tokens_map.json
│       │   ├── tokenizer_config.json
│       │   ├── trainer_state.json
│       │   ├── training_args.bin
│       │   └── vocab.json
│       ├── config.json
│       ├── generation_config.json
│       ├── merges.txt
│       ├── model.safetensors
│       ├── special_tokens_map.json
│       ├── tokenizer_config.json
│       ├── training_args.bin
│       ├── training_info.json
│       └── vocab.json
├── prompt_model_comparison.py
├── prompt_poc_post_tuning.py
├── prompt_poc_pre_tuning.py
├── requirements.txt
├── roman_empire_finetune.py
└── run_roman_training.sh
```

## Model Usage
### Testing the prompt of the fine-tuned model
```bash
python prompt_poc_post_tuning.py --prompt "The Roman empire is"
```
### Testing the prompt of the base model
```bash
python prompt_poc_pre_tuning.py --prompt "The Roman empire is"
```
### Testing both models
Using the `prompt_model_comparison.py` script, you can compare the outputs of both the base and fine-tuned models for a set of prompts.
```bash
python prompt_model_comparison.py --prompt-file prompts.txt --output-json results.json
```
Or for a single prompt:
```bash
python prompt_model_comparison.py --prompt "The Roman Empire was" --output-json results.json
```

## 💾 Model Persistence

- **Models are saved to:** `./models/` directory on your host machine
- **Survives container deletion:** Yes, models persist between runs
- **Cache location:** `./cache/` directory (speeds up subsequent runs)
- 
---

**Note:** The Docker container automatically deletes itself after each run, but your trained models remain safely stored in the `./models/` directory!