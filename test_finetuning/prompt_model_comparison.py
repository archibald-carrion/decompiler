#!/usr/bin/env python3
"""
DistilGPT2 Proof of Concept Script
This script demonstrates how to use the DistilGPT2 model from Hugging Face
to generate text on your local machine.
"""


import os
# Suppress oneDNN warning from TensorFlow
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import argparse
import time
import json

# Set local directory for model storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2-roman-empire")
VANILLA_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2-roman-empire")

# Create models directory if it doesn't exist
os.makedirs(LOCAL_MODEL_DIR, exist_ok=True)

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
    
    return True

def load_model():
    """Load fine-tuned DistilGPT2-Roman-Empire model and tokenizer from local directory"""
    print(f"Loading fine-tuned DistilGPT2-Roman-Empire model from: {LOCAL_MODEL_DIR}")
    if os.path.exists(os.path.join(LOCAL_MODEL_DIR, "config.json")):
        print("✓ Found fine-tuned local model, loading from disk...")
        tokenizer = GPT2Tokenizer.from_pretrained(LOCAL_MODEL_DIR)
        model = GPT2LMHeadModel.from_pretrained(LOCAL_MODEL_DIR)
    else:
        print(f"❌ Fine-tuned model not found in {LOCAL_MODEL_DIR}.")
        print("Please make sure the fine-tuned model is present in the correct folder.")
        raise FileNotFoundError(f"Model not found in {LOCAL_MODEL_DIR}")

    # Set pad token (GPT2 doesn't have one by default)
    tokenizer.pad_token = tokenizer.eos_token

    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()

    print(f"✓ Model loaded on {device}")
    print(f"✓ Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"✓ Local model directory: {LOCAL_MODEL_DIR}")

    return model, tokenizer, device

def load_any_model(model_dir, model_label):
    """Load a GPT2 model and tokenizer from a local directory"""
    print(f"Loading {model_label} model from: {model_dir}")
    if os.path.exists(os.path.join(model_dir, "config.json")):
        print(f"✓ Found {model_label} model, loading from disk...")
        tokenizer = GPT2Tokenizer.from_pretrained(model_dir)
        model = GPT2LMHeadModel.from_pretrained(model_dir)
    else:
        print(f"❌ {model_label} model not found in {model_dir}.")
        raise FileNotFoundError(f"Model not found in {model_dir}")
    tokenizer.pad_token = tokenizer.eos_token
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    print(f"✓ {model_label} model loaded on {device}")
    return model, tokenizer, device

def get_prompts_from_file(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip()]
    return prompts

def generate_text(model, tokenizer, device, prompt, max_length=100, temperature=0.8, top_p=0.9):
    """Generate text using the model"""
    print(f"\nGenerating text with prompt: '{prompt}'")
    print("-" * 50)
    

    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt').to(device)
    # Create attention mask (all ones, same shape as inputs)
    attention_mask = torch.ones_like(inputs)

    # Generate text
    start_time = time.time()

    with torch.no_grad():
        outputs = model.generate(
            inputs,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
            num_return_sequences=1
        )

    generation_time = time.time() - start_time

    # Decode the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    print(f"Generated text:\n{generated_text}")
    print(f"\nGeneration time: {generation_time:.2f} seconds")
    print(f"Tokens generated: {len(outputs[0]) - len(inputs[0])}")

    return generated_text

def compare_models_on_prompts(prompts, max_length, temperature, top_p, output_json):
    vanilla_model, vanilla_tokenizer, vanilla_device = load_any_model(VANILLA_MODEL_DIR, "Vanilla DistilGPT2")
    finetuned_model, finetuned_tokenizer, finetuned_device = load_any_model(FINETUNED_MODEL_DIR, "Fine-tuned DistilGPT2-Roman-Empire")
    results = []
    for prompt in prompts:
        print(f"\n=== PROMPT: {prompt}")
        vanilla_output = generate_text(vanilla_model, vanilla_tokenizer, vanilla_device, prompt, max_length, temperature, top_p)
        finetuned_output = generate_text(finetuned_model, finetuned_tokenizer, finetuned_device, prompt, max_length, temperature, top_p)
        results.append({
            "prompt": prompt,
            "vanilla_distilgpt2": vanilla_output,
            "finetuned_distilgpt2_roman_empire": finetuned_output
        })
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Results saved to {output_json}")

def show_local_files():
    """Show what files are stored locally"""
    print(f"\n📁 Local model files in {LOCAL_MODEL_DIR}:")
    if os.path.exists(LOCAL_MODEL_DIR):
        total_size = 0
        for file in os.listdir(LOCAL_MODEL_DIR):
            file_path = os.path.join(LOCAL_MODEL_DIR, file)
            if os.path.isfile(file_path):
                size = os.path.getsize(file_path)
                total_size += size
                size_mb = size / (1024 * 1024)
                print(f"  - {file}: {size_mb:.1f} MB")
        print(f"  Total size: {total_size / (1024 * 1024):.1f} MB")
    else:
        print("  No local fine-tuned model files found")

def cleanup_local_files():
    """Remove local fine-tuned model files"""
    if os.path.exists(LOCAL_MODEL_DIR):
        import shutil
        shutil.rmtree(LOCAL_MODEL_DIR)
        print(f"✓ Removed local fine-tuned model directory: {LOCAL_MODEL_DIR}")
    else:
        print("No local fine-tuned model files to remove")
def interactive_mode(model, tokenizer, device):
    """Interactive text generation mode"""
    print("\n🤖 Interactive DistilGPT2 Text Generation")
    print("Enter your prompts (type 'quit' to exit, 'help' for options)")
    print("-" * 50)
    
    while True:
        try:
            prompt = input("\nEnter prompt: ").strip()
            
            if prompt.lower() == 'quit':
                print("Goodbye!")
                break
            elif prompt.lower() == 'help':
                print("\nOptions:")
                print("- Enter any text as a prompt")
                print("- 'quit' to exit")
                print("- 'help' to show this message")
                print("- 'files' to show local model files")
                continue
            elif prompt.lower() == 'files':
                show_local_files()
                continue
            elif not prompt:
                print("Please enter a prompt or 'quit' to exit")
                continue
            
            generate_text(model, tokenizer, device, prompt)
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Compare vanilla and fine-tuned DistilGPT2 models')
    parser.add_argument('--prompt', type=str, help='Text prompt for generation (overrides prompt file and default list)')
    parser.add_argument('--prompt-file', type=str, help='Path to a .txt file with prompts (one per line)')
    parser.add_argument('--max-length', type=int, default=100, help='Maximum length of generated text')
    parser.add_argument('--temperature', type=float, default=0.8, help='Sampling temperature')
    parser.add_argument('--top-p', type=float, default=0.9, help='Top-p sampling')
    parser.add_argument('--output-json', type=str, default='model_comparison_output.json', help='Output JSON file for results')
    parser.add_argument('--interactive', action='store_true', help='Run in interactive mode')
    parser.add_argument('--show-files', action='store_true', help='Show local model files and exit')
    parser.add_argument('--cleanup', action='store_true', help='Remove local model files and exit')
    
    args = parser.parse_args()
    
    print("🚀 DistilGPT2 Model Comparison")
    print("=" * 40)
    
    # Handle utility commands
    if args.show_files:
        show_local_files()
        return
    
    if args.cleanup:
        cleanup_local_files()
        return
    
    if not check_requirements():
        print("\n❌ Missing requirements. Please install them and try again.")
        return
    
    # Prompt selection logic
    if args.prompt:
        prompts = [args.prompt]
    elif args.prompt_file:
        prompts = get_prompts_from_file(args.prompt_file)
    else:
        prompts = [
            "The future of artificial intelligence",
            "Once upon a time in a distant galaxy",
            "The benefits of renewable energy include",
            "In the year 2050, technology will"
        ]
    compare_models_on_prompts(prompts, args.max_length, args.temperature, args.top_p, args.output_json)

if __name__ == "__main__":
    main()