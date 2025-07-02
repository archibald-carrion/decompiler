#!/usr/bin/env python3
"""
DistilGPT2 Assembly Decompiler Fine-tuning Script
This script demonstrates how to fine-tune DistilGPT2 on assembly-to-C code pairs
to create a specialized model for decompiling assembly code to C.
Enhanced to use ALL C/ASM pairs from ALL optimization levels.
"""

import os
# Suppress oneDNN warning from TensorFlow
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch
from transformers import (
    GPT2LMHeadModel, 
    GPT2Tokenizer, 
    TrainingArguments, 
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import Dataset
import argparse
import time
import json
import glob
from torch.utils.data import DataLoader

# Metrics and plotting
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

# Set local directory for model storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# Create directories if they don't exist
os.makedirs(BASE_MODEL_DIR, exist_ok=True)
os.makedirs(FINETUNED_MODEL_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import transformers
        print(f"✓ Transformers version: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not installed. Run: pip install transformers")
        return False
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✓ CUDA device: {torch.cuda.get_device_name()}")
    except ImportError:
        print("❌ PyTorch not installed. Run: pip install torch")
        return False
    
    try:
        import datasets
        print(f"✓ Datasets library available")
    except ImportError:
        print("❌ Datasets not installed. Run: pip install datasets")
        return False
    
    return True

def load_base_model():
    """Load base DistilGPT2 model and tokenizer"""
    print(f"Loading base DistilGPT2 model...")
    
    # Check if model exists locally
    if os.path.exists(os.path.join(BASE_MODEL_DIR, "config.json")):
        print("✓ Found existing local model, loading from disk...")
        tokenizer = GPT2Tokenizer.from_pretrained(BASE_MODEL_DIR)
        model = GPT2LMHeadModel.from_pretrained(BASE_MODEL_DIR)
    else:
        print("⬇️  Downloading base model for first time...")
        tokenizer = GPT2Tokenizer.from_pretrained('distilgpt2')
        model = GPT2LMHeadModel.from_pretrained('distilgpt2')
        
        # Save to local directory
        print(f"💾 Saving base model to {BASE_MODEL_DIR}")
        tokenizer.save_pretrained(BASE_MODEL_DIR)
        model.save_pretrained(BASE_MODEL_DIR)
        print("✓ Base model saved locally!")
    
    # Set pad token
    tokenizer.pad_token = tokenizer.eos_token
    
    print(f"✓ Base model loaded")
    print(f"✓ Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    return model, tokenizer

def load_assembly_c_pairs(data_dir=DATA_DIR, use_all_optimizations=True, specific_optimization=None):
    """Load assembly-C code pairs from specified optimization levels"""
    print(f"📂 Loading assembly-C pairs from {data_dir}...")
    
    c_dir = os.path.join(data_dir, "C")
    
    if not os.path.exists(c_dir):
        print(f"❌ C directory not found: {c_dir}")
        return []
    
    all_pairs = []
    
    # Determine which optimization levels to process
    if use_all_optimizations:
        optimization_levels = ["O0", "Ofast", "Os"]
        print("🔧 Processing ALL optimization levels (O0, Ofast, Os)")
    elif specific_optimization:
        optimization_levels = [specific_optimization]
        print(f"🔧 Processing only {specific_optimization} optimization level")
    else:
        optimization_levels = ["O0"]  # Default fallback
        print("🔧 Processing only O0 optimization level (default)")
    
    # Get all C files first
    c_files = glob.glob(os.path.join(c_dir, "*.c"))
    print(f"📄 Found {len(c_files)} C files")
    
    if not c_files:
        print(f"❌ No C files found in {c_dir}")
        return []
    
    # Process each optimization level
    for opt_level in optimization_levels:
        asm_dir = os.path.join(data_dir, "ASM", opt_level)
        
        if not os.path.exists(asm_dir):
            print(f"⚠️  Assembly directory not found: {asm_dir}, skipping...")
            continue
        
        print(f"  📁 Processing {opt_level} optimization level...")
        pairs_for_this_opt = []
        
        for c_file in c_files:
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(c_file))[0]
            
            # Look for corresponding assembly file
            asm_file = os.path.join(asm_dir, f"{base_name}.s")
            
            if os.path.exists(asm_file):
                try:
                    # Read C code
                    with open(c_file, 'r', encoding='utf-8') as f:
                        c_code = f.read().strip()
                    
                    # Read assembly code
                    with open(asm_file, 'r', encoding='utf-8') as f:
                        asm_code = f.read().strip()
                    
                    # Only add if both files have content
                    if c_code and asm_code:
                        pairs_for_this_opt.append({
                            'assembly': asm_code,
                            'c_code': c_code,
                            'filename': base_name,
                            'optimization': opt_level
                        })
                        
                except Exception as e:
                    print(f"    ⚠️  Error reading files {base_name}: {e}")
                    continue
            else:
                print(f"    ⚠️  Missing assembly file for {base_name} in {opt_level}")
        
        print(f"    ✓ Loaded {len(pairs_for_this_opt)} pairs from {opt_level}")
        all_pairs.extend(pairs_for_this_opt)
    
    print(f"✅ Total loaded: {len(all_pairs)} assembly-C pairs")
    
    # Show statistics by optimization level
    if len(all_pairs) > 0:
        from collections import Counter
        opt_counts = Counter(pair['optimization'] for pair in all_pairs)
        print("📊 Pairs by optimization level:")
        for opt, count in sorted(opt_counts.items()):
            print(f"    {opt}: {count} pairs")
    
    if len(all_pairs) == 0:
        print("❌ No valid assembly-C pairs found!")
        print(f"Expected structure:")
        print(f"  {data_dir}/")
        print(f"    C/")
        print(f"      <filename1>.c")
        print(f"      <filename2>.c")
        print(f"      ...")
        print(f"    ASM/")
        print(f"      O0/")
        print(f"        <filename1>.s")
        print(f"        <filename2>.s")
        print(f"        ...")
        print(f"      Ofast/")
        print(f"        <filename1>.s")
        print(f"        <filename2>.s")
        print(f"        ...")
        print(f"      Os/")
        print(f"        <filename1>.s")
        print(f"        <filename2>.s")
        print(f"        ...")
        
        # List what we actually found
        print(f"\nActual directory contents:")
        if os.path.exists(c_dir):
            c_files_found = os.listdir(c_dir)
            print(f"  C files: {len([f for f in c_files_found if f.endswith('.c')])}")
            if len(c_files_found) <= 10:
                print(f"    {c_files_found}")
        
        asm_base_dir = os.path.join(data_dir, "ASM")
        if os.path.exists(asm_base_dir):
            for opt in ["O0", "Ofast", "Os"]:
                opt_dir = os.path.join(asm_base_dir, opt)
                if os.path.exists(opt_dir):
                    asm_files = [f for f in os.listdir(opt_dir) if f.endswith('.s')]
                    print(f"  {opt} ASM files: {len(asm_files)}")
    
    return all_pairs

def create_training_text(assembly, c_code):
    """Create training text in a format suitable for decompilation"""
    # Format: Assembly input -> C output
    # Using special tokens to separate input and output
    return f"<|assembly|>\n{assembly}\n<|c_code|>\n{c_code}<|endoftext|>"

def prepare_dataset(tokenizer, use_all_optimizations=True, specific_optimization=None, max_length=1024):
    """Prepare assembly-to-C dataset for training"""
    print("🔧 Preparing assembly-to-C dataset...")
    
    # Load assembly-C pairs
    pairs = load_assembly_c_pairs(
        data_dir=DATA_DIR, 
        use_all_optimizations=use_all_optimizations,
        specific_optimization=specific_optimization
    )
    
    if not pairs:
        print("❌ No training data found!")
        return None
    
    # Create training texts
    training_texts = []
    for pair in pairs:
        training_text = create_training_text(pair['assembly'], pair['c_code'])
        training_texts.append(training_text)
        
        # Show first example
        if len(training_texts) == 1:
            print(f"\n📝 Example training text format:")
            print("-" * 50)
            print(training_text[:500] + "..." if len(training_text) > 500 else training_text)
            print("-" * 50)
    
    # Tokenize the texts
    def tokenize_function(examples):
        return tokenizer(
            examples['text'],
            truncation=True,
            padding=True,
            max_length=max_length,
            return_tensors="pt"
        )
    
    # Create dataset
    dataset_dict = {"text": training_texts}
    dataset = Dataset.from_dict(dataset_dict)
    
    # Tokenize dataset
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset.column_names
    )
    
    print(f"✅ Dataset prepared with {len(tokenized_dataset)} examples")
    return tokenized_dataset

def finetune_model(model, tokenizer, dataset, output_dir=FINETUNED_MODEL_DIR):
    """Fine-tune the model on assembly-to-C data"""
    print("🔧 Starting assembly decompiler fine-tuning...")

    epochs = 2  # Hardcoded to 10 epochs because yes
    
    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # GPT-2 is not a masked language model
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,  # Hardcoded to 10 epochs
        per_device_train_batch_size=2,  # Slightly larger batch size
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=4,  # Simulate larger batch size
        warmup_steps=100,
        prediction_loss_only=False,  # Enable full logging for loss plotting
        logging_dir=os.path.join(output_dir, "logs"),
        logging_steps=50,  # Log more frequently
        save_steps=500,
        save_total_limit=2,
        seed=42,
        fp16=torch.cuda.is_available(),  # Use mixed precision if CUDA available
        dataloader_drop_last=True,
        report_to=None,  # Disable wandb/tensorboard logging
        learning_rate=5e-5,  # Lower learning rate for fine-tuning
        weight_decay=0.01,  # Add weight decay for regularization
    )
    
    # Create trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )
    
    # Start training
    print(f"🚀 Training for {epochs} epochs on {len(dataset)} examples...")
    start_time = time.time()
    

    train_result = trainer.train()
    training_time = time.time() - start_time
    print(f"✓ Training completed in {training_time:.2f} seconds")

    # Save the fine-tuned model
    print(f"💾 Saving decompiler model to {output_dir}")
    trainer.save_model()
    tokenizer.save_pretrained(output_dir)

    # Save training info
    training_info = {
        "base_model": "distilgpt2",
        "training_data": "Assembly-to-C code pairs (all optimization levels)",
        "num_examples": len(dataset),
        "epochs": epochs,
        "training_time": training_time,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(os.path.join(output_dir, "training_info.json"), "w") as f:
        json.dump(training_info, f, indent=2)

    # --- METRICS ---
    print("\n📊 Calculating training metrics...")
    # Store metrics per batch for plotting
    metrics_history = {
        'batch': [],
        'accuracy': [],
        'precision': [],
        'recall': [],
        'f1': [],
        'cross_entropy': [],
        'perplexity': []
    }
    all_labels = []
    all_preds = []
    all_losses = []
    cross_entropy = torch.nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id, reduction='none')
    model.eval()
    dataloader = DataLoader(dataset, batch_size=2, pin_memory=False)
    # Set loss_type in model config to avoid warning
    if hasattr(model, 'config'):
        model.config.loss_type = 'ForCausalLMLoss'
    batch_idx = 0
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch['input_ids']
            attention_mask = batch['attention_mask']
            # Convert to torch tensors if they are lists (datasets.Dataset may return lists)
            if isinstance(input_ids, list):
                input_ids = torch.stack(input_ids)
            if isinstance(attention_mask, list):
                attention_mask = torch.stack(attention_mask)
            labels = input_ids.clone()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            logits = outputs.logits
            preds = torch.argmax(logits, dim=-1)
            batch_labels = []
            batch_preds = []
            batch_losses = []
            for i in range(input_ids.shape[0]):
                mask = attention_mask[i].bool()
                true = input_ids[i][mask].cpu().numpy()
                pred = preds[i][mask].cpu().numpy()
                batch_labels.extend(true)
                batch_preds.extend(pred)
                all_labels.extend(true)
                all_preds.extend(pred)
                ce_loss = cross_entropy(logits[i][mask], input_ids[i][mask])
                batch_losses.extend(ce_loss.cpu().numpy())
                all_losses.extend(ce_loss.cpu().numpy())
            # Compute metrics for this batch
            if len(batch_labels) > 0:
                acc = accuracy_score(batch_labels, batch_preds)
                prec = precision_score(batch_labels, batch_preds, average='weighted', zero_division=0)
                rec = recall_score(batch_labels, batch_preds, average='weighted', zero_division=0)
                f1v = f1_score(batch_labels, batch_preds, average='weighted', zero_division=0)
                ce = float(np.mean(batch_losses))
                ppl = float(np.exp(ce))
                metrics_history['batch'].append(batch_idx)
                metrics_history['accuracy'].append(acc)
                metrics_history['precision'].append(prec)
                metrics_history['recall'].append(rec)
                metrics_history['f1'].append(f1v)
                metrics_history['cross_entropy'].append(ce)
                metrics_history['perplexity'].append(ppl)
            batch_idx += 1

    # Calculate overall metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision = precision_score(all_labels, all_preds, average='weighted', zero_division=0)
    recall = recall_score(all_labels, all_preds, average='weighted', zero_division=0)
    f1 = f1_score(all_labels, all_preds, average='weighted', zero_division=0)
    avg_cross_entropy = float(np.mean(all_losses))
    perplexity = float(np.exp(avg_cross_entropy))

    metrics = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "cross_entropy": avg_cross_entropy,
        "perplexity": perplexity
    }
    print(json.dumps(metrics, indent=2))

    # Save metrics to JSON and CSV
    metrics_path = os.path.join(output_dir, "training_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    pd.DataFrame([metrics]).to_csv(os.path.join(output_dir, "training_metrics.csv"), index=False)

    # Save per-batch metrics for plotting
    metrics_df = pd.DataFrame(metrics_history)
    metrics_df.to_csv(os.path.join(output_dir, "training_metrics_per_batch.csv"), index=False)

    # Plot all metrics curves
    plt.figure(figsize=(10, 7))
    for metric in ['accuracy', 'precision', 'recall', 'f1', 'cross_entropy', 'perplexity']:
        plt.plot(metrics_history['batch'], metrics_history[metric], label=metric)
    plt.xlabel('Batch')
    plt.ylabel('Metric Value')
    plt.title('Training Metrics per Batch')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "metrics_curves.png"))
    print(f"Metrics curves saved to {os.path.join(output_dir, 'metrics_curves.png')}")

    # Plot loss curve if available
    if 'loss' in train_result.metrics:
        print(f"Final training loss: {train_result.metrics['loss']}")
    else:
        log_dir = os.path.join(output_dir, "logs")
        loss_log = []
        for root, dirs, files in os.walk(log_dir):
            for file in files:
                if file.endswith(".json"):
                    with open(os.path.join(root, file), 'r') as f:
                        for line in f:
                            try:
                                entry = json.loads(line)
                                if 'loss' in entry:
                                    loss_log.append((entry['step'], entry['loss']))
                            except Exception:
                                continue
        if loss_log:
            steps, losses = zip(*sorted(loss_log))
            plt.figure(figsize=(8,5))
            plt.plot(steps, losses, marker='o')
            plt.xlabel('Step')
            plt.ylabel('Loss')
            plt.title('Training Loss Curve')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, "loss_curve.png"))
            print(f"Loss curve saved to {os.path.join(output_dir, 'loss_curve.png')}")
        else:
            print("No loss log found for plotting.")

    print("✅ Decompiler model saved successfully!")
    return trainer

def load_decompiler_model():
    """Load the fine-tuned decompiler model"""
    if not os.path.exists(os.path.join(FINETUNED_MODEL_DIR, "config.json")):
        print("❌ Decompiler model not found. Please run training first.")
        return None, None, None
    
    print("Loading fine-tuned decompiler model...")
    tokenizer = GPT2Tokenizer.from_pretrained(FINETUNED_MODEL_DIR)
    model = GPT2LMHeadModel.from_pretrained(FINETUNED_MODEL_DIR)
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    print(f"✓ Decompiler model loaded on {device}")
    return model, tokenizer, device

def decompile_assembly(model, tokenizer, device, assembly_code, max_length=512, temperature=0.7, top_p=0.9):
    """Decompile assembly code to C code"""
    print(f"\n🔧 Decompiling assembly to C code")
    print("-" * 60)
    print(f"Input assembly:\n{assembly_code[:200]}{'...' if len(assembly_code) > 200 else ''}")
    print("-" * 60)
    
    # Format input with special token
    prompt = f"<|assembly|>\n{assembly_code}\n<|c_code|>\n"
    
    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
    attention_mask = torch.ones_like(inputs)
    
    # Generate C code
    start_time = time.time()
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=len(inputs[0]) + max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            num_return_sequences=1,
            stop_strings=["<|endoftext|>", "<|assembly|>"],
            tokenizer=tokenizer
        )
    
    generation_time = time.time() - start_time
    
    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract only the C code part
    if "<|c_code|>" in generated_text:
        c_code = generated_text.split("<|c_code|>")[1].strip()
    else:
        c_code = generated_text[len(prompt):].strip()
    
    print(f"Generated C code:\n{c_code}")
    print(f"\nDecompilation time: {generation_time:.2f} seconds")
    print(f"Tokens generated: {len(outputs[0]) - len(inputs[0])}")
    
    return c_code

def main():

    print("🔧 DistilGPT2 Assembly Decompiler")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        print("\n❌ Missing requirements. Please install them and try again.")
        print("Required: pip install transformers torch datasets")
        return

    try:
        # Load base model
        model, tokenizer = load_base_model()

        # Prepare dataset
        dataset = prepare_dataset(
            tokenizer, 
            use_all_optimizations=True,
            specific_optimization=None
        )
        
        if dataset is None:
            print("❌ Failed to prepare dataset. Check your data directory structure.")
            return
        
        # Fine-tune model
        finetune_model(model, tokenizer, dataset)
        
        print("\n✅ Decompiler training completed successfully!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
if __name__ == "__main__":
    main()