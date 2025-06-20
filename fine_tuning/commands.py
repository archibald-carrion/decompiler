from os import path # Path resolution / manipulation
from sys import stderr # Error stream

# Pytorch datatypes
from torch import no_grad
from torch.cuda import is_available as is_cuda_available

# Loading the model
from .model_loading import load_model

# Downloading and/or testing the pre-trained model with a prompt
def download_test_model(model_path: str, test: bool):
    """ Test the downloaded OpenCoder model with a simple code generation task
    ### Arguments:
        model_path (str): Directory to load the model from
    ### Returns:
        True if model should be tested with a response, False otherwise
    """
    # Validate and expand local directory path
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Invalid directory for model testing"

    # Validate test flag
    assert isinstance(test, bool), "Test condition should be bool"

    # Load model
    print(f"Loading model from {model_path}...")
    try:
        # Load model and tokenizer from local directory path
        model, tokenizer = load_model(model_path)
        print("Model loaded succesfully!")
    except Exception as err:
        print(f"Unable to load model test due to error: {err}", file=stderr)
        raise Exception("Invalid model loading")
    
    # If desired, test it with a prompt
    if not test:
        pass

    # Test prompt for code generation
    print("Testing model with code generation prompt...")
    try:
        # Construct prompt by hand
        test_prompt = (
            "<|im_start|>system"
            + "\nYou are a helpful coding assistant.<|im_end|>"
            + "\n<|im_start|>user"
            + "\nWrite a Python function to calculate the factorial of a number.<|im_end|>"
            + "\n<|im_start|>assistant"
        )
        print(f"Prompt: {test_prompt.split('user')[-1].split('<|im_end|>')[0].strip()}")
        
        # Tokenize input
        inputs = tokenizer(test_prompt, return_tensors="pt")
        if is_cuda_available():
            inputs = {k: v.cuda() for k, v in inputs.items()}
        
        # Generate response
        with no_grad():
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

    # All is done
    pass

# Loading dataset
from .dataset_loading import DecompilationDataset

# Loading training arguments
from .model_trainer import load_training_args

# Collecting test metrics
from .model_evaluation import collect_test_metrics

# Evaluating the model on a test dataset
def eval_model(model_path: str, dataset_dir: str, train_args_path: str, output_dir: str):
    # Validate and expand paths
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Missing directory for model"

    assert isinstance(dataset_dir, str), "Local dataset directory path should be a string"
    dataset_dir = path.expanduser(dataset_dir)
    assert path.isdir(dataset_dir), "Missing directory for dataset"

    assert isinstance(train_args_path, str), "Local training arguments path should be a string"
    train_args_path = path.expanduser(train_args_path)
    assert path.isfile(train_args_path), "Missing file for training arguments"

    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    # Load training arguments
    print(f"Loading training arguments from {train_args_path}...")
    try:
        train_args = load_training_args(train_args_path)
        print("Training arguments loaded succesfully!")
    except Exception as err:
        print(f"Unable to load training arguments due to error: {err}", file=stderr)
        raise Exception("Invalid training arguments loading")

    # Load model
    print(f"Loading model from {model_path}...")
    try:
        # Load model and tokenizer from local directory path
        model, tokenizer = load_model(model_path)
        print("Model loaded succesfully!")
    except Exception as err:
        print(f"Unable to load model test due to error: {err}", file=stderr)
        raise Exception("Invalid model loading")

    # Load dataset
    test_dataset = "test.csv"
    print(f"Loading dataset from {dataset_dir} (with split '{test_dataset}')...")
    try:
        test_dataset = DecompilationDataset(dataset_dir, test_dataset, tokenizer)
        print("Dataset loaded succesfully!")
    except Exception as err:
        print(f"Unable to test split dataset test due to error: {err}", file=stderr)
        raise Exception("Invalid dataset loading")
    
    # Try collecting metrics on the testing dataset
    try:
        collect_test_metrics(model, tokenizer, train_args, test_dataset, output_dir)
    except Exception as err:
        print(f"Unable to collect metrics on test split due to error: {err}", file=stderr)
        raise Exception("Invalid metric collection")
