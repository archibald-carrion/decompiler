# Path resolution / manipulation
import os

# Import system
import sys

# PyTorch support 
import torch

# LM Models
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download

# Argument parsing
import argparse

def download_model(local_dir: str = "./model/opencoder_base_model", model_name: str = "infly/OpenCoder-1.5B-Instruct"):
    """
    Download the OpenCoder-1.5B-Instruct model to local folder without cache
    """
    # Download model
    print(f"Downloading {model_name} to {local_dir}...")
    
    # Create model directory if it doesn't exist
    try:
        os.makedirs(local_dir, exist_ok=True)
    except Exception as err:
        print(f"Unable to create output directory for model: {err}", file=sys.stderr)
        raise Exception("Invalid output directory for model")
    
    # Download model files to local directory (no cache)
    snapshot_download(
        repo_id=model_name,
        local_dir=local_dir,
        cache_dir=None,  # Disable cache
        local_dir_use_symlinks=False  # Ensure files are copied, not symlinked
    )
    
    print(f"Model downloaded successfully to {local_dir}")
    return local_dir

def test_model(model_path: str):
    """
    Test the downloaded OpenCoder model with a simple code generation task
    """
    if not os.path.isdir(model_path):
        raise Exception("Invalid directory for model testing")

    print(f"Loading model from {model_path}...")
    
    # Load tokenizer and model from local directory
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=True
    )
    
    # Test prompt for code generation
    test_prompt = """<|im_start|>system
You are a helpful coding assistant.<|im_end|>
<|im_start|>user
Write a Python function to calculate the factorial of a number.<|im_end|>
<|im_start|>assistant"""
    
    print("Testing model with code generation prompt...")
    print(f"Prompt: {test_prompt.split('user')[-1].split('<|im_end|>')[0].strip()}")
    
    # Tokenize input
    inputs = tokenizer(test_prompt, return_tensors="pt")
    if torch.cuda.is_available():
        inputs = {k: v.cuda() for k, v in inputs.items()}
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode and print response
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    response = generated_text[len(test_prompt):].split("<|im_end|>")[0].strip()
    
    print("\nModel Response:")
    print(response)
    print("\nTest completed successfully!")

def main():
    """
    Main function to download and test the model
    """
    # Register arguments
    parser = argparse.ArgumentParser(description='Download and test pretrained OpenCoder Model')
    parser.add_argument('model_path', type=str, help='Path to output model weights on')
    
    # If no arguments are passed, print the usage
    if (len(sys.argv) == 0):
        parser.parse_args(["-h"])
        sys.exit(0)

    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()

    # Download and test model
    try:
        # Download model
        model_path = download_model(args.model_path)

        # Test model
        test_model(model_path)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()