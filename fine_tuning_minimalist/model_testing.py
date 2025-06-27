#!/usr/bin/env python3
"""
Minimal Assembly Decompiler Comparison
Sends assembly to three models and outputs JSON with results
"""

import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
import glob

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model")
FINETUNED_MODEL_V2_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model_v2")
VALIDATION_DATA_DIR = os.path.join(SCRIPT_DIR, "data_validation")

def load_model(model_dir):
    """Load model and tokenizer"""
    tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
    model = GPT2LMHeadModel.from_pretrained(model_dir)
    tokenizer.pad_token = tokenizer.eos_token
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    return model, tokenizer, device

def generate_c_code(model, tokenizer, device, assembly_code):
    """Generate C code from assembly"""
    prompt = f"<|assembly|>\n{assembly_code}\n<|c_code|>\n"
    inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=512).to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_length=len(inputs[0]) + 256,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1,
            early_stopping=True
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Extract C code
    if "<|c_code|>" in generated_text:
        c_code = generated_text.split("<|c_code|>")[1].strip()
    else:
        c_code = generated_text[len(prompt):].strip()
    
    # Clean up
    if "<|endoftext|>" in c_code:
        c_code = c_code.split("<|endoftext|>")[0].strip()
    if "<|assembly|>" in c_code:
        c_code = c_code.split("<|assembly|>")[0].strip()
    
    return c_code

def load_validation_data():
    """Load all assembly-C pairs from validation data"""
    pairs = []
    c_dir = os.path.join(VALIDATION_DATA_DIR, "C")
    
    if not os.path.exists(c_dir):
        return pairs
    
    c_files = glob.glob(os.path.join(c_dir, "*.c"))
    optimization_levels = ["O0", "Ofast", "Osize"]
    
    for opt_level in optimization_levels:
        asm_dir = os.path.join(VALIDATION_DATA_DIR, "ASM", opt_level)
        if not os.path.exists(asm_dir):
            continue
        
        for c_file in c_files:
            base_name = os.path.splitext(os.path.basename(c_file))[0]
            asm_file = os.path.join(asm_dir, f"{base_name}.s")
            
            if os.path.exists(asm_file):
                try:
                    with open(c_file, 'r', encoding='utf-8') as f:
                        c_code = f.read().strip()
                    with open(asm_file, 'r', encoding='utf-8') as f:
                        asm_code = f.read().strip()
                    
                    if c_code and asm_code:
                        pairs.append({
                            'filename': base_name,
                            'optimization': opt_level,
                            'assembly': asm_code,
                            'correct_c': c_code
                        })
                except:
                    continue
    
    return pairs

def main():
    # Load models
    print("Loading models...")
    base_model, base_tokenizer, base_device = load_model(BASE_MODEL_DIR)
    ft_model, ft_tokenizer, ft_device = load_model(FINETUNED_MODEL_DIR)
    ft_model_v2, ft_tokenizer_v2, ft_device_v2 = load_model(FINETUNED_MODEL_V2_DIR)
    
    # Load validation data
    print("Loading validation data...")
    validation_pairs = load_validation_data()
    
    results = []
    
    # Process each pair
    for i, pair in enumerate(validation_pairs):
        print(f"Processing {i+1}/{len(validation_pairs)}: {pair['filename']} ({pair['optimization']})")
        
        # Generate with base model
        base_output = generate_c_code(base_model, base_tokenizer, base_device, pair['assembly'])
        
        # Generate with fine-tuned model
        ft_output = generate_c_code(ft_model, ft_tokenizer, ft_device, pair['assembly'])
        
        # Generate with fine-tuned model v2
        ft_output_v2 = generate_c_code(ft_model_v2, ft_tokenizer_v2, ft_device_v2, pair['assembly'])
        
        # Store result
        result = {
            'filename': pair['filename'],
            'optimization': pair['optimization'],
            'assembly': pair['assembly'],
            'correct_c': pair['correct_c'],
            'base_model_output': base_output,
            'finetuned_model_output': ft_output,
            'finetuned_model_v2_output': ft_output_v2
        }
        
        results.append(result)
    
    # Save results to JSON
    output_file = os.path.join(SCRIPT_DIR, "decompiler_comparison_results_v2.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_file}")
    print(f"Processed {len(results)} samples")

if __name__ == "__main__":
    main()