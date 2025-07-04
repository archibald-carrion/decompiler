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

# Set local directory for model storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model_v2")
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
        optimization_levels = ["O0", "Ofast", "Osize"]
        print("🔧 Processing ALL optimization levels (O0, Ofast, Osize)")
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
        print(f"      Osize/")
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
            for opt in ["O0", "Ofast", "Osize"]:
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

def finetune_model(model, tokenizer, dataset, output_dir=FINETUNED_MODEL_DIR, epochs=5):
    """Fine-tune the model on assembly-to-C data"""
    print("🔧 Starting assembly decompiler fine-tuning...")
    
    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # GPT-2 is not a masked language model
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=epochs,
        per_device_train_batch_size=2,  # Slightly larger batch size
        per_device_eval_batch_size=2,
        gradient_accumulation_steps=4,  # Simulate larger batch size
        warmup_steps=100,
        prediction_loss_only=True,
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
    
    trainer.train()
    
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

def test_decompiler():
    """Test the decompiler with sample assembly files"""
    model, tokenizer, device = load_decompiler_model()
    
    if model is None:
        print("Please train the model first using --train")
        return
    
    # Try to find test assembly files
    test_files = []
    for opt_level in ["O0", "Ofast", "Osize"]:
        asm_dir = os.path.join(DATA_DIR, "ASM", opt_level)
        if os.path.exists(asm_dir):
            asm_files = glob.glob(os.path.join(asm_dir, "*.s"))[:3]  # Take first 3 files
            test_files.extend([(f, opt_level) for f in asm_files])
    
    if not test_files:
        print("No test assembly files found in data directory")
        return
    
    print(f"\n🧪 Testing decompiler with {len(test_files)} files")
    
    for asm_file, opt_level in test_files[:3]:  # Test only first 3
        base_name = os.path.splitext(os.path.basename(asm_file))[0]
        print(f"\n{'='*80}")
        print(f"Testing: {base_name} ({opt_level})")
        print(f"{'='*80}")
        
        try:
            with open(asm_file, 'r') as f:
                assembly_code = f.read().strip()
            
            # Show original C if available
            c_file = os.path.join(DATA_DIR, "C", f"{base_name}.c")
            if os.path.exists(c_file):
                with open(c_file, 'r') as f:
                    original_c = f.read().strip()
                print(f"\nOriginal C code:\n{original_c}")
                print(f"\n{'-'*40}")
            
            decompile_assembly(model, tokenizer, device, assembly_code)
            
        except Exception as e:
            print(f"Error processing {base_name}: {e}")

def interactive_decompiler_mode():
    """Interactive mode for decompiling assembly code"""
    model, tokenizer, device = load_decompiler_model()
    
    if model is None:
        print("Please train the model first using --train")
        return
    
    print("\n🔧 Interactive Assembly Decompiler")
    print("Enter assembly code (end with '---' on a new line, or type 'quit' to exit)")
    print("-" * 60)
    
    while True:
        try:
            print("\nEnter assembly code:")
            assembly_lines = []
            
            while True:
                line = input()
                if line.strip().lower() == 'quit':
                    print("Goodbye!")
                    return
                elif line.strip() == '---':
                    break
                else:
                    assembly_lines.append(line)
            
            if not assembly_lines:
                print("No assembly code entered.")
                continue
            
            assembly_code = '\n'.join(assembly_lines)
            decompile_assembly(model, tokenizer, device, assembly_code)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

def show_model_info():
    """Show information about available models"""
    print("\n📊 Model Information")
    print("=" * 40)
    
    # Base model info
    if os.path.exists(BASE_MODEL_DIR):
        base_size = sum(os.path.getsize(os.path.join(BASE_MODEL_DIR, f)) 
                       for f in os.listdir(BASE_MODEL_DIR) 
                       if os.path.isfile(os.path.join(BASE_MODEL_DIR, f)))
        print(f"📁 Base Model: {base_size / (1024*1024):.1f} MB")
    else:
        print("📁 Base Model: Not downloaded")
    
    # Fine-tuned model info
    if os.path.exists(FINETUNED_MODEL_DIR):
        ft_size = sum(os.path.getsize(os.path.join(FINETUNED_MODEL_DIR, f)) 
                     for f in os.listdir(FINETUNED_MODEL_DIR) 
                     if os.path.isfile(os.path.join(FINETUNED_MODEL_DIR, f)))
        print(f"🔧 Decompiler Model: {ft_size / (1024*1024):.1f} MB")
        
        # Show training info if available
        info_file = os.path.join(FINETUNED_MODEL_DIR, "training_info.json")
        if os.path.exists(info_file):
            with open(info_file, 'r') as f:
                training_info = json.load(f)
            print(f"   📚 Training examples: {training_info['num_examples']}")
            print(f"   🔄 Epochs: {training_info['epochs']}")
            print(f"   ⏱️  Training time: {training_info['training_time']:.2f}s")
            print(f"   📅 Trained: {training_info['timestamp']}")
    else:
        print("🔧 Decompiler Model: Not trained yet")
    
    # Data directory info
    print(f"\n📂 Data Directory: {DATA_DIR}")
    c_dir = os.path.join(DATA_DIR, "C")
    if os.path.exists(c_dir):
        c_files = len(glob.glob(os.path.join(c_dir, "*.c")))
        print(f"   📄 C files: {c_files}")
    
    for opt_level in ["O0", "Ofast", "Osize"]:
        asm_dir = os.path.join(DATA_DIR, "ASM", opt_level)
        if os.path.exists(asm_dir):
            asm_files = len(glob.glob(os.path.join(asm_dir, "*.s")))
            print(f"   📄 {opt_level} assembly files: {asm_files}")

def cleanup_models():
    """Remove all model files"""
    import shutil
    
    removed = []
    if os.path.exists(BASE_MODEL_DIR):
        shutil.rmtree(BASE_MODEL_DIR)
        removed.append("Base model")
    
    if os.path.exists(FINETUNED_MODEL_DIR):
        shutil.rmtree(FINETUNED_MODEL_DIR)
        removed.append("Decompiler model")
    
    if removed:
        print(f"✓ Removed: {', '.join(removed)}")
    else:
        print("No models to remove")

def main():
    parser = argparse.ArgumentParser(description='DistilGPT2 Assembly Decompiler Fine-tuning')
    parser.add_argument('--train', action='store_true', help='Fine-tune model on assembly-to-C data')
    parser.add_argument('--epochs', type=int, default=5, help='Number of training epochs')
    parser.add_argument('--optimization', choices=['O0', 'Ofast', 'Osize', 'all'], default='all', 
                       help='Assembly optimization level to use for training (default: all)')
    parser.add_argument('--decompile', type=str, help='Path to assembly file to decompile')
    parser.add_argument('--interactive', action='store_true', help='Interactive decompilation mode')
    parser.add_argument('--test', action='store_true', help='Test decompiler with sample files')
    parser.add_argument('--info', action='store_true', help='Show model and data information')
    parser.add_argument('--cleanup', action='store_true', help='Remove all model files')
    
    args = parser.parse_args()
    
    print("🔧 DistilGPT2 Assembly Decompiler")
    print("=" * 50)
    
    # Handle utility commands
    if args.info:
        show_model_info()
        return
    
    if args.cleanup:
        cleanup_models()
        return
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Missing requirements. Please install them and try again.")
        print("Required: pip install transformers torch datasets")
        return
    
    # Training mode
    if args.train:
        try:
            # Load base model
            model, tokenizer = load_base_model()
            
            # Determine optimization level settings
            use_all_optimizations = (args.optimization == 'all')
            specific_optimization = None if use_all_optimizations else args.optimization
            
            # Prepare dataset
            dataset = prepare_dataset(
                tokenizer, 
                use_all_optimizations=use_all_optimizations,
                specific_optimization=specific_optimization
            )
            
            if dataset is None:
                print("❌ Failed to prepare dataset. Check your data directory structure.")
                return
            
            # Fine-tune model
            finetune_model(model, tokenizer, dataset, epochs=args.epochs)
            
            print("\n✅ Decompiler training completed successfully!")
            print("Use --test, --interactive, or --decompile to test the model")
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            import traceback
            traceback.print_exc()
            return
    
    # Decompilation modes
    elif args.decompile:
        if not os.path.exists(args.decompile):
            print(f"❌ Assembly file not found: {args.decompile}")
            return
        
        model, tokenizer, device = load_decompiler_model()
        if model:
            try:
                with open(args.decompile, 'r') as f:
                    assembly_code = f.read().strip()
                decompile_assembly(model, tokenizer, device, assembly_code)
            except Exception as e:
                print(f"Error reading assembly file: {e}")
    
    elif args.interactive:
        interactive_decompiler_mode()
    
    elif args.test:
        test_decompiler()
    
    else:
        # Default: show help and model info
        print("\n💡 Usage examples:")
        print("  python script.py --train --optimization all      # Train on ALL optimization levels (recommended)")
        print("  python script.py --train --optimization O0       # Train only on O0 optimized assembly")
        print("  python script.py --test                          # Test with sample files")
        print("  python script.py --interactive                   # Interactive decompilation")
        print("  python script.py --decompile file.s              # Decompile specific file")
        print("  python script.py --info                          # Show model and data info")
        print("\nExpected data structure:")
        print("  data/")
        print("    C/")
        print("      <file1>.c, <file2>.c, ...")
        print("    ASM/")
        print("      O0/")
        print("        <file1>.s, <file2>.s, ...")
        print("      Ofast/")
        print("        <file1>.s, <file2>.s, ...")
        print("      Osize/")
        print("        <file1>.s, <file2>.s, ...")
        print("\n🚀 Start with --train --optimization all to create the decompiler model using ALL your data!")
        show_model_info()

if __name__ == "__main__":
    main()