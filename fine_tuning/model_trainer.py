from os import path # Path manipulation
from sys import stderr # Error stream messages

from transformers import (
    EvalPrediction, # Predictions to score
    PreTrainedTokenizerBase, # Tokenization
    PreTrainedModel, # Model
    DataCollatorForLanguageModeling, # Data collation
    Trainer, # Model training management
    TrainingArguments, # Model training hyperparameters
    HfArgumentParser # Training arguments serialization
)

from .model_evaluation import compute_eval_metrics # Custom evaluation-split metrics
from .dataset_loading import DecompilationDataset # Datasets
from torch.cuda import is_available as is_cuda_available # CUDA detection

def create_training_args(
    checkpoints_dir: str,
    training_epochs: int, 
    seed: int, # To seed training batching and more
    gradient_accum_steps: int = 8 # Effective batch size is 8
) -> TrainingArguments:
    """ Create appropiate training arguments given some customization
    ### Arguments:
        checkpoints_dir (str): Directory to store / load the training checkpoints from
        training_epochs (int): Epochs to run the training for
        device_batch_size (int): Batches 
    ### Returns:
        training_args (TrainingArguments): Appropiate training arguments for distributed
        finetuning
    """
    # Validate checkpoints output directory path
    assert isinstance(checkpoints_dir, str), "Checkpoints directory path should be a string"
    checkpoints_dir = path.expanduser(checkpoints_dir)
    assert path.isdir(checkpoints_dir), "Invalid checkpoints directory path"

    # Validate other hyperparemeters
    assert isinstance(training_epochs, int) and training_epochs > 0, "Training epochs should be a positive integer"
    assert isinstance(seed, int), "Training seed must be an integer"
    assert isinstance(gradient_accum_steps, int) and gradient_accum_steps > 0, "Gradient accumulation steps should be a positive integer"

    try:
        training_args = TrainingArguments(
            # Save checkpoints and overwrite any if found
            output_dir=checkpoints_dir,
            overwrite_output_dir=True,
            load_best_model_at_end=True,
            # Training epochs, batches and rate/weight decays for scheduler
            num_train_epochs=training_epochs,
            auto_find_batch_size=True, # Find batch sizes that fit into memory. Requires 'accelerate' package
            gradient_accumulation_steps=gradient_accum_steps, # So we don't run out of CUDA memory when doing gradient descent
            eval_accumulation_steps=gradient_accum_steps, # (...) when running evaluations
            learning_rate=5e-5, # Small initial learning rate
            weight_decay=0.01, # Small initial weight decay
            eval_strategy="epoch", # Check up with the evaluation dataset every epoch
            batch_eval_metrics=False, # Collect custom metrics for the entire evaluation split at once
            save_strategy="epoch", # Save the checkpoints every epoch
            save_total_limit=1, # Save at most 1 model candidate every checkpoint
            # Warmup, logging and saving steps
            warmup_steps=100,
            logging_steps=10,
            # Use mixed-precision training whenever CUDA is available
            fp16=is_cuda_available(),
            # Misc. settings
            dataloader_pin_memory=False, # Do not pin memory
            remove_unused_columns=False, # Do not remove unused columns
            report_to="none", # Disable wandb/tensorboard/etc reporting integrations
            seed=seed
        )
    except Exception as err:
        print(f"Unable to create training arguments: {err}", file=stderr)
        raise Exception("Invalid training arguments")

    return training_args

def save_training_arguments(training_args: TrainingArguments, output_path: str):
    """ Save some training arguments into a JSON file 
    ### Arguments:
        training_args (TrainingArguments): Training arguments to save
        output_path (str): Path to JSON file to save contents into
    """
    # Validate trainer
    assert isinstance(training_args, TrainingArguments), "Training arguments should be TrainingArguments"

    # Validate training arguments output path
    assert isinstance(output_path, str), "Training arguments output path should be a string"
    output_path = path.expanduser(output_path)
    
    # Serialize contents
    try:
        with open(output_path, 'w') as f:
            f.write(training_args.to_json_string())
    except Exception as err:
        print(f"Unable to save TrainingArguments into file {output_path}: {err}", file=stderr)
        raise Exception("Invalid TrainingArguments serialization")

def load_training_args(arguments_path: str) -> TrainingArguments:
    """ Load previously-saved training arguments from a JSON file 
    ### Arguments:
        arguments_path (str): Path to JSON file to load contents from
    ### Returns:
        training_args (TrainingArguments): Training arguments previously stored via `save_training_arguments`
    """
    # Validate training arguments source path
    assert isinstance(arguments_path, str), "Training arguments source path should be a string"
    arguments_path = path.expanduser(arguments_path)
    assert path.isfile(arguments_path), "Invalid training arguments source path"
    
    # De-serialize contents
    try:
        training_args, = HfArgumentParser(TrainingArguments).parse_json_file(arguments_path)
    except Exception as err:
        print(f"Unable to load TrainingArguments from file {arguments_path}: {err}", file=stderr)
        raise Exception("Invalid TrainingArguments file")

    return training_args

def create_trainer(
    model: PreTrainedModel, tokenizer: PreTrainedTokenizerBase, 
    train_dataset: DecompilationDataset, eval_dataset: DecompilationDataset, 
    training_args: TrainingArguments
) -> Trainer:
    """ Setup and return trainer with given training hyperparemeters
    ### Arguments:
        model (PreTrainedModel): Model to train / finetuning
        tokenizer (PreTrainedTokenizerBase): Tokenizer to use in training / finetuning
        train_dataset (DecompilationDataset): Training split dataset
        eval_dataset (DecompilationDataset): Evaluation split dataset
        training_args (TrainingArguments): Hyperparameter configuration for training
    ### Returns:
        trainer (Trainer): Trainer with proper hyperparameters ready to train model
    """
    try:
        # Use typical collator for batching training in causal language models
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False,  # Causal LM, not masked LM
        )
        
        # Construct trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=eval_dataset,
            data_collator=data_collator,
            compute_metrics=compute_eval_metrics # Use custom evaluation-split metrics
        )
    except Exception as err:
        print(f"Unable to generate trainer: {err}", file=stderr)
        raise Exception("Invalid trainer")
    
    return trainer
