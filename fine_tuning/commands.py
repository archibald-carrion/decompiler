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

# Use training arguments
from transformers import TrainingArguments

# Construct trainer
from .model_trainer import create_trainer

# Train model
from .model_training import train_model

# Collect training metrics
from .model_evaluation import collect_training_metrics

# Finetuning the model on a training and validation dataset
def train_model(
    model_path: str, dataset_dir: str, output_dir: str,
    training_args: TrainingArguments, stats_dir: str | None = None
):
    # Validate and expand paths
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Missing directory for model"

    assert isinstance(dataset_dir, str), "Local dataset directory path should be a string"
    dataset_dir = path.expanduser(dataset_dir)
    assert path.isdir(dataset_dir), "Missing directory for dataset"

    assert stats_dir is None or isinstance(stats_dir, str), "When provided, training statistics output directory should be a string"
    stats_dir = path.expanduser(stats_dir)

    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    # Validate training arguments
    assert isinstance(training_args, TrainingArguments), "Invalid training arguments"

    # Load model
    print(f"Loading model and tokenizer from {model_path}...")

    try:
        model, tokenizer = load_model(model_path)
    except Exception as err:
        print(f"Unable to load model from '{model_path}': {err}", file=stderr)
        raise Exception("Invalid model loading")
    
    print("Model and tokenizer loaded succesfully!")

    # Load training and validation datasets
    print(f"Loading training and validation dataset splits from {dataset_dir}...")

    try:            
        train_dataset = DecompilationDataset("train.csv", dataset_dir, tokenizer)
        validate_dataset = DecompilationDataset("validation.csv", dataset_dir, tokenizer)
    except Exception as err:
        print(f"Unable to load training and validation datasets: {err}", file=stderr)
        raise Exception("Invalid datasets")
    
    print(f"Training and validation dataset splits loaded succesfully!")

    # Create training manager / trainer
    print(f"Creating trainer instance with provided training arguments and dataset splits...")

    try:
        trainer = create_trainer(model, tokenizer, train_dataset, validate_dataset, training_args)
    except Exception as err:
        print(f"Unable to initialize trainer instance: {err}", file=stderr)
        raise Exception("Invalid trainer")
    
    print(f"Trainer instance initialized succesfully!")

    # Begin training
    print(f"Booting up training...")

    try:
        train_model(trainer, output_dir)
    except Exception as err:
        print(f"An unhandled error ocurred while training the model: {err}", file=stderr)
        raise Exception("Invalid training")
    
    print(f"Training finished!")

    # If specified, collect training statistics 
    if stats_dir is None:
        print("No training statistics output directory specified. Skipping training stats recollection.")
    else:
        print(f"Recollecting training stats into {stats_dir}...")

        try:
            collect_training_metrics(trainer, stats_dir)
            print(f"Training stats recollected succesfully!")
        except Exception as err:
            print(f"Unable to generate training statistics: {err}", file=stderr)

    print("All done!")

# Construct and/or save custom training arguments
from .model_trainer import create_training_args, save_training_arguments

# Finetuning the model on a training and validation dataset, with custom arguments
def train_model_custom_args(
    model_path: str, dataset_dir: str, output_dir: str,
    checkpoints_dir: str, training_epochs: int, 
    seed: int, gradient_accum_steps: int,
    stats_dir: str | None = None,
    args_output_path: str | None = None
):
    # Validate and expand paths
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Missing directory for model"

    assert isinstance(dataset_dir, str), "Local dataset directory path should be a string"
    dataset_dir = path.expanduser(dataset_dir)
    assert path.isdir(dataset_dir), "Missing directory for dataset"

    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    assert stats_dir is None or isinstance(stats_dir, str), "When provided, training statistics output directory should be a string"
    stats_dir = path.expanduser(stats_dir) if stats_dir is not None else None

    # Validate provided training hyperparameters
    # ... Checkpoints directory path
    assert isinstance(checkpoints_dir, str), "Checkpoints directory path should be a string"
    checkpoints_dir = path.expanduser(checkpoints_dir)
    assert path.isdir(checkpoints_dir), "Missing directory for checkpoints"
    # ... Arguments output directory path
    assert args_output_path is None or isinstance(args_output_path, str), "When provided, training arguments output path should be a string"
    args_output_path = path.expanduser(args_output_path)
    # ... Numerical hyperparameters
    assert isinstance(training_epochs, int) and training_epochs > 0, "Training epochs should be a positive integer"
    assert isinstance(seed, int), "Training seed must be an integer"
    assert isinstance(gradient_accum_steps, int) and gradient_accum_steps > 0, "Gradient accumulation steps should be a positive integer"

    # Create training arguments
    print("Initializing training arguments...")
    try:
        training_args = create_training_args(checkpoints_dir, training_epochs, seed, gradient_accum_steps)
    except Exception as err:
        print(f"Unable to create training arguments: {err}", file=stderr)
        raise Exception("Invalid training arguments")
    
    print("Training arguments initialized!")

    # If specified, save them for later use
    if args_output_path is not None:
        print("Saving training arguments...")

        try:
            save_training_arguments(training_args, args_output_path)
        except Exception as err:
            print(f"Unable to save training arguments: {err}", file=stderr)
            raise Exception("Invalid training arguments serialization")

        print("Training arguments saved!")
    else:
        print("No output path for training arguments specified, skipping save.")

    # Carry on training the model
    train_model(model_path, dataset_dir, output_dir, training_args, stats_dir)

# Finetuning the model on a training and validation dataset, with pre-saved arguments
def train_model_presaved_args(
    model_path: str, dataset_dir: str, output_dir: str,
    args_path: str, stats_dir: str | None = None
):
    # Validate and expand paths
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)
    assert path.isdir(model_path), "Missing directory for model"

    assert isinstance(dataset_dir, str), "Local dataset directory path should be a string"
    dataset_dir = path.expanduser(dataset_dir)
    assert path.isdir(dataset_dir), "Missing directory for dataset"

    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    assert stats_dir is None or isinstance(stats_dir, str), "When provided, training statistics output directory should be a string"
    stats_dir = path.expanduser(stats_dir) if stats_dir is not None else None

    # Validate provided training path
    assert isinstance(args_path, str), "Training arguments path should be a string"
    args_path = path.expanduser(args_path)
    assert path.isfile(args_path), "Missing training argument file"

    # Load training arguments from disk
    print(f"Loading training arguments from {args_path}...")
    try:
        training_args = load_training_args(args_path)
    except Exception as err:
        print(f"Unable to load training arguments: {err}", file=stderr)
        raise Exception("Invalid training arguments")
    
    print("Training arguments loaded succesfully!")

    # Carry on training the model
    train_model(model_path, dataset_dir, output_dir, training_args, stats_dir)