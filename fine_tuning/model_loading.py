# Path resolution / manipulation
from os import path, makedirs

# Import system
from sys import stderr, argv, exit

# PyTorch support 
import torch

# LM Models
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download

def load_model(model_path: str = "./model/opencoder_base_model"):
    """ Download the OpenCoder-1.5B-Instruct model and tokenizer to local folder without cache.
    Then, load it into memory
    ### Arguments:
        model_path (str): Directory to store / load the model from
    ### Returns:
        (model, tokenizer)
    """
    MODEL_REPO = "infly/OpenCoder-1.5B-Instruct"
    
    # Validate local directory path
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)

    # Download model
    print(f"Downloading model from {MODEL_REPO} to {model_path}...")
    
    # Create model directory if it doesn't exist
    try:
        makedirs(model_path, exist_ok=True)
    except Exception as err:
        print(f"Unable to create output directory for model: {err}", file=stderr)
        raise Exception("Invalid output directory for model")
    
    # Download model files to local directory (no cache)
    try:
        snapshot_download(
            repo_id=MODEL_REPO,
            local_dir=model_path,
            cache_dir=None,  # Disable cache
            local_dir_use_symlinks=False  # Ensure files are copied, not symlinked
        )
    except Exception as err:
        print(f"Unable to download model from {MODEL_REPO} into {model_path}: {err}")
        raise Exception("Model download failure")
    
    print(f"Model downloaded successfully to {model_path}")

    # Load the model from memory 
    print(f"Loading model and tokenizer from {model_path}")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            trust_remote_code=True
        )
    except Exception as err:
        print(f"Unable to load model and tokenizer into memory from {model_path}: {err}")
        raise Exception("Model load failure")
    
    print(f"Model and tokenizer loaded succesfully")
    return (model, tokenizer)

def load_test_model(model_path: str):
    """ Test the downloaded OpenCoder model with a simple code generation task
    ### Arguments:
        model_path (str): Directory to load the model from
    ### Returns:
        True if model could generate a response, False otherwise
    """
    # Validate and expand local directory path
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Invalid directory for model testing"

    # Keep track of test success
    success = True
    try:
        print(f"Loading model from {model_path}...")

        # Load model and tokenizer from local directory path
        model, tokenizer = load_model(model_path)
        
        # Test prompt for code generation
        test_prompt = (
            "<|im_start|>system"
            + "\nYou are a helpful coding assistant.<|im_end|>"
            + "\n<|im_start|>user"
            + "\nWrite a Python function to calculate the factorial of a number.<|im_end|>"
            + "\n<|im_start|>assistant"
        )
        
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
        
        print(f"\nModel Response: \n{response}\n")
        print("\nTest completed successfully!")
    except Exception as err:
        print(f"Unable to finish test due to error: {err}", file=stderr)
        success = False

    return success
