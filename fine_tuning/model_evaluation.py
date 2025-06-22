from os import path, makedirs # Path manipulation
from sys import stderr # Error stream messages

from transformers import (
    PreTrainedTokenizerBase, # Tokenization
    PreTrainedModel, # Model
    Trainer, # Model training management
    TrainingArguments, # Replicate training hyperparameters
    DataCollatorForLanguageModeling # Data collation
)

from torch.cuda import is_available as is_cuda_available # CUDA acceleration

from transformers.modelcard import parse_log_history # Human-readable metric parsing
from .dataset_loading import DecompilationDataset

import matplotlib.pyplot as plt # Plotting losses
from json import dump as json_dump # Serializing metrics

def collect_training_metrics(trainer: Trainer, output_dir: str):
    # Validate trainer
    assert isinstance(trainer, Trainer), "Trainer parameter should be a HF Trainer"
    assert len(trainer.state.log_history) > 0, "Trainer has no logged history of training metrics"

    # Validate output directory
    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    # Create output directory for plots 
    try:
        makedirs(output_dir, exist_ok=True)
    except Exception as err:
        print(f"Unable to create output directory for metrics {err}", file=stderr)
        raise Exception("Invalid output directory")

    # Get pretty-formatted metrics
    train_log, lines, eval_results = parse_log_history(trainer.state.log_history)

    # Assert that log lines exist
    assert isinstance(lines, list) and len(lines) > 0, "Missing metric lines from logged history"
    
    # Turn them into a time series
    indicators = list(lines[0].keys())
    lines = {indicator: [metric for metric in lines[indicator]] for indicator in indicators}

    # Generate loss-per-step plot
    fig_path = path.join(output_dir, "loss_per_step.png")
    print(f"Creating step-loss plot into {fig_path}")
    try:
        # ... With a correspondence between the epochs and steps unit
        epoch_for_step = dict(zip(lines["Step"], lines["Epoch"]))
        earliest_step_for_epoch = dict(zip(reversed(lines["Epoch"]), reversed(lines["Step"])))

        to_epoch = lambda step: epoch_for_step[step]
        to_step = lambda epoch: earliest_step_for_epoch[epoch]

        # ... Make it a single-celled plot
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # ... With a time series per-step for training and validation losses
        ax.plot("Step", "Training Loss", xlabel="Step", ylabel="Training Loss", data=lines)
        ax.plot("Step", "Validation Loss", xlabel="Step", ylabel="Training Loss", data=lines)
        ax.set_title('Model loss over training')

        # ... With a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax2 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax2.set_xlabel("Epoch")
        
        # Save plot to the appropiate path
        try:
            fig.savefig(fig_path)
            print(f"Saved step-loss plot into {fig_path} succesfully")
        except Exception as err:
            print(f"Unable to save step-loss plot into {fig_path}: {err}", file=stderr)
            print(f"Skipping plot saving...", file=stderr)

        # Clear memory and close the plot
        plt.close(fig)

    except Exception as err:
        print(f"Unhandled error while generating plot for training loss: {err}", file=stderr)
        print("Skipping plot generation...", file=stderr)

    # Save formatted training statistics
    if train_log is not None:
        train_log_path = path.join(output_dir, "train_stats.json")
        print(f"Saving training stats to {train_log_path}")
        try:
            with open(train_log_path, 'w') as train_log_file:
                json_dump(train_log, train_log_file)
        except Exception as err:
            print(f"Unable to save training stats into {train_log_path}: {err}", file=stderr)
            print("Skipping saving...", file=stderr)

    # Save formatted evaluation statistics
    if eval_results is not None:
        eval_results_path = path.join(output_dir, "eval_stats.json")
        print(f"Saving evaluation stats to {eval_results_path}")
        try:
            with open(eval_results_path, 'w') as eval_results_file:
                json_dump(eval_results, eval_results_file)
        except Exception as err:
            print(f"Unable to save evaluation stats into {eval_results_path}: {err}", file=stderr)
            print("Skipping saving...", file=stderr)

    # All is done
    print("Finished collecting stats")    

def collect_test_metrics(
    model: PreTrainedModel, tokenizer: PreTrainedTokenizerBase,
    training_args: TrainingArguments, test_dataset: DecompilationDataset,
    output_dir: str
):
    # Validate model and tokenizer
    assert isinstance(model, PreTrainedModel), "Model should be PreTrainedModel"
    assert isinstance(tokenizer, PreTrainedTokenizerBase), "Tokenizer should be PreTrainedTokenizerBase"

    # Validate training arguments
    assert isinstance(training_args, TrainingArguments)

    # Validate dataset
    assert isinstance(test_dataset, DecompilationDataset)

    # Validate output directory
    assert isinstance(output_dir, str), "Output directory should be a string"
    output_dir = path.expanduser(output_dir)

    # Create output directory for results
    try:
        makedirs(output_dir, exist_ok=True)
    except Exception as err:
        print(f"Unable to create output directory for metrics {err}", file=stderr)
        raise Exception("Invalid output directory")

    # Create new trainer instance, but using the current evaluation dataset
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
            eval_dataset=test_dataset,
            data_collator=data_collator
        )
    except Exception as err:
        print(f"Unable to generate trainer: {err}", file=stderr)
        raise Exception("Invalid trainer")
    
    # Evaluate trainer on test dataset
    test_results = trainer.evaluate()

    # Save formatted evaluation statistics from the test dataset
    test_results_path = path.join(output_dir, "test_stats.json")
    print(f"Saving evaluation stats on testing dataset to {test_results_path}")
    try:
        with open(test_results_path, 'w') as test_results_file:
            json_dump(test_results, test_results_file)
    except Exception as err:
        print(f"Unable to save evaluation stats on testing dataset into {test_results_path}: {err}",
            file=stderr)
        print("Skipping saving...", file=stderr)

    # All is done
    print("Finished collecting stats")
