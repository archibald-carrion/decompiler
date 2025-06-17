#!/usr/bin/env python3
"""
Fine-tuning script for OpenCoder-1.5B-Instruct model
Trains on assembly code -> C function pairs
"""


import os
import json
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset as HFDataset
import logging
import psutil

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AssemblyCDataset(Dataset):
    def __init__(self, c_dir, asm_root_dir, tokenizer, max_length=2048):
        self.pairs = self.load_pairs(c_dir, asm_root_dir)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def load_pairs(self, c_dir, asm_root_dir):
        c_files = [f for f in os.listdir(c_dir) if f.endswith('.c')]
        opt_levels = [d for d in os.listdir(asm_root_dir) if os.path.isdir(os.path.join(asm_root_dir, d))]
        pairs = []
        for c_file in c_files:
            base = os.path.splitext(c_file)[0]
            c_path = os.path.join(c_dir, c_file)
            for opt in opt_levels:
                asm_dir = os.path.join(asm_root_dir, opt)
                asm_file = os.path.join(asm_dir, base + '.s')
                if os.path.exists(asm_file):
                    with open(asm_file, 'r', encoding='utf-8', errors='ignore') as f_asm:
                        asm_code = f_asm.read()
                    with open(c_path, 'r', encoding='utf-8', errors='ignore') as f_c:
                        c_code = f_c.read()
                    pairs.append({'assembly': asm_code, 'c_code': c_code, 'opt_level': opt})
        return pairs

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        item = self.pairs[idx]
        prompt = f"""Convert the following assembly code to C function (optimization: {item['opt_level']}):\n\nAssembly:\n```asm\n{item['assembly']}\n```\n\nC Function:\n```c\n{item['c_code']}\n```"""
        encoding = self.tokenizer(
            prompt,
            truncation=True,
            max_length=self.max_length,
            padding='max_length',
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': encoding['input_ids'].flatten()
        }

def setup_model_and_tokenizer(model_path="./model/opencoder_base_model"):
    """Load model and tokenizer from local path"""
    logger.info(f"Loading model and tokenizer from: {model_path}")
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True
    )
    return model, tokenizer

def create_trainer(model, tokenizer, train_dataset, output_dir="./opencoder-finetuned"):
    """Setup and return trainer"""
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=1,  # Small batch size for 1.5B model
        gradient_accumulation_steps=8,  # Effective batch size = 8
        warmup_steps=100,
        logging_steps=10,
        save_steps=500,
        # evaluation_strategy removed for compatibility
        # save_strategy may not be supported in older versions, so remove if error persists
        learning_rate=5e-5,
        weight_decay=0.01,
        fp16=torch.cuda.is_available(),
        dataloader_pin_memory=False,
        remove_unused_columns=False,
        report_to=None,  # Disable wandb/tensorboard
    )
    
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # Causal LM, not masked LM
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        data_collator=data_collator,
        # tokenizer argument removed due to deprecation
    )
    
    return trainer

def main():
    # Configuration
    C_DIR = "./data/C"  # Folder with C files
    ASM_ROOT_DIR = "./data/ASM"  # Root folder with all optimization subfolders
    MODEL_PATH = "./model/opencoder_base_model"  # Local model directory
    OUTPUT_DIR = "./opencoder-assembly-to-c"

    logger.info("==== Decompilation Fine-tuning Script Started ====")
    logger.info(f"C_DIR: {C_DIR}")
    logger.info(f"ASM_ROOT_DIR: {ASM_ROOT_DIR}")
    logger.info(f"MODEL_PATH: {MODEL_PATH}")
    logger.info(f"OUTPUT_DIR: {OUTPUT_DIR}")

    # Check if dataset exists
    if not os.path.exists(C_DIR) or not os.path.exists(ASM_ROOT_DIR):
        logger.error(f"Dataset folders not found: {C_DIR}, {ASM_ROOT_DIR}")
        logger.info("Please ensure the folders exist and contain the C and ASM files.")
        return

    try:
        # Log available system memory before model loading
        mem = psutil.virtual_memory()
        logger.info(f"[MEMORY] Available: {mem.available / 1024 ** 2:.2f} MB, Total: {mem.total / 1024 ** 2:.2f} MB")

        # Setup model and tokenizer
        logger.info("Loading model and tokenizer...")
        try:
            model, tokenizer = setup_model_and_tokenizer(MODEL_PATH)
        except RuntimeError as re:
            logger.error("RuntimeError during model loading (possible OOM):")
            logger.error(str(re), exc_info=True)
            return

        # Log memory after model loading
        mem = psutil.virtual_memory()
        logger.info(f"[MEMORY] After model load - Available: {mem.available / 1024 ** 2:.2f} MB, Used: {mem.used / 1024 ** 2:.2f} MB")
        if torch.cuda.is_available():
            logger.info(f"[CUDA] Allocated: {torch.cuda.memory_allocated() / 1024 ** 2:.2f} MB, Reserved: {torch.cuda.memory_reserved() / 1024 ** 2:.2f} MB")

        # Create dataset from C/ASM pairs (all optimizations)
        logger.info("Loading dataset...")
        dataset = AssemblyCDataset(C_DIR, ASM_ROOT_DIR, tokenizer)
        logger.info(f"Number of training samples loaded: {len(dataset)}")
        if len(dataset) == 0:
            logger.warning("No training samples found! Please check your data directories.")

        # Convert to HuggingFace dataset format
        logger.info("Converting to HuggingFace dataset format...")
        hf_dataset = HFDataset.from_dict({
            'input_ids': [item['input_ids'] for item in dataset],
            'attention_mask': [item['attention_mask'] for item in dataset],
            'labels': [item['labels'] for item in dataset]
        })

        # Create trainer
        logger.info("Creating Trainer...")
        trainer = create_trainer(model, tokenizer, hf_dataset, OUTPUT_DIR)

        # Log memory before training
        mem = psutil.virtual_memory()
        logger.info(f"[MEMORY] Before training - Available: {mem.available / 1024 ** 2:.2f} MB, Used: {mem.used / 1024 ** 2:.2f} MB")
        if torch.cuda.is_available():
            logger.info(f"[CUDA] Allocated: {torch.cuda.memory_allocated() / 1024 ** 2:.2f} MB, Reserved: {torch.cuda.memory_reserved() / 1024 ** 2:.2f} MB")

        # Start training
        logger.info("Starting training...")
        try:
            train_output = trainer.train()
            logger.info(f"Training output: {train_output}")
        except RuntimeError as re:
            logger.error("RuntimeError during training (possible OOM):")
            logger.error(str(re), exc_info=True)
            return

        # Save the final model
        logger.info(f"Saving model to {OUTPUT_DIR}")
        trainer.save_model()
        tokenizer.save_pretrained(OUTPUT_DIR)

        logger.info("Training completed!")
    except Exception as e:
        logger.error("An exception occurred during training:")
        logger.error(str(e), exc_info=True)

if __name__ == "__main__":
    main()