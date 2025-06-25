
# Fine-tuning System for Decompiler

This module provides a flexible, production-oriented system for fine-tuning large language models (LLMs) for decompilation tasks (assembly → C).

---

## System Architecture

```mermaid
flowchart TD
    A[Data Preparation] --> B[Dataset Mapping (CSV)]
    B --> C[Dataset Loader]
    C --> D[Model Loader]
    D --> E[Trainer]
    E --> F[Evaluation & Metrics]
    F --> G[Results/Plots]
```

**Key Components:**
- `dataset_loading.py`: Loads and tokenizes C/ASM pairs using a mapping CSV.
- `model_loading.py`: Downloads/loads OpenCoder-1.5B-Instruct or other models.
- `model_trainer.py`: Configures and runs HuggingFace Trainer with custom arguments.
- `commands.py`: CLI entry points for training, evaluation, and model download.
- `model_evaluation.py`: Collects and visualizes training/test metrics.
- `__main__.py`: Unified CLI for all major operations.

## Technologies Used
- **PyTorch**: Model training and dataset interface
- **HuggingFace Transformers**: Model, tokenizer, Trainer, TrainingArguments
- **HuggingFace Datasets**: Data handling and mapping
- **Docker**: Containerized training (see Dockerfile) (deprecated, needs update)
- **Pandas**: CSV mapping and data wrangling
- **Matplotlib**: Training/evaluation plots

## Usage


## Troubleshooting
- **Out of Memory:** Increase Docker/container memory limit.
- **No Data Found:** Ensure your data is in the correct folders and mappings.csv is present.
- **Slow Training:** Use GPU if available; reduce batch size if needed.

## Dependencies
All required Python dependencies are installed automatically from `requirements.txt` during Docker build or can be installed manually:

```sh
pip install -r fine_tuning/requirements.txt
```

---
For more details, see the source code and comments in each module.