from os import path, makedirs # Path manipulation
from sys import stderr # Error stream messages

from transformers import (
    EvalPrediction, # Collected predictions
    PreTrainedTokenizerBase, # Tokenization
    PreTrainedModel, # Model
    Trainer, # Model training management
    TrainingArguments, # Replicate training hyperparameters
    DataCollatorForLanguageModeling # Data collation
)

import torch # Hand-crafted metrics on the GPU (if possible)...
from torch.nn.functional import cross_entropy # ... 
from torcheval.metrics.functional import multiclass_confusion_matrix # ...
from math import exp # ...
from numpy import nan as np_nan, float64 as np_float64 # Mark values as missing when plotting

from transformers.modelcard import parse_log_history # Human-readable metric parsing
from .dataset_loading import DecompilationDataset # Datasets

import matplotlib.pyplot as plt # Plotting losses
from json import dump as json_dump # Serializing metrics

class BatchDecompilerMetrics:
    def __init__(self, class_count: int, device: str | torch.device | int):
        assert class_count > 0, "Invalid number of classes"

        # Keep track of device to compute evaluation metrics on
        self.work_device = device

        # Keep track of the universe of classes
        # We'll asume they reside in [0, class_count)
        self.classes = class_count

        # Keep track of a fresh confusion matrix
        self.confusion_matrix = torch.zeros(
            size=(class_count, class_count), dtype=torch.float, device=device)

        # Keep track of fresh logarithmic loss
        self.log_loss = float(0)

    def __call__(self, eval_preds: EvalPrediction, compute_result = False):
        with torch.no_grad():
            # Collect the logits and labels on the working device
            logits, labels = eval_preds
            logits, labels = logits.to(device=self.work_device), labels.to(device=self.work_device)

            # We'll asume one-hot encoding
            predicted_labels = torch.argmax(logits, dim=-1)

            # Flatten in case we got batches
            labels = labels.flatten()
            predicted_labels = predicted_labels.flatten()
            logits = logits.reshape((-1, logits.shape[-1]))

            # Update our confusion matrix and logarithmic loss trackers

            # ... When working the multiclass confusion matrix, submit only those predictions that
            # are NOT to be ignored / masked (e.g. labels with index -100)
            unmasked = torch.where(labels >= 0)
            self.confusion_matrix += multiclass_confusion_matrix(
                predicted_labels[unmasked], labels[unmasked], self.classes
            ).to(device=self.confusion_matrix.device)

            # ... The cross entropy function aready takes care of this with a default of -100 for
            # ignored tokens
            self.log_loss += cross_entropy(logits, labels, reduction="sum").item()
            
            # Compute result and reset trackers if also at end of evaluation cycle
            if compute_result:
                # Collect metrics precision, accuracy and f1-score based on confusion matrix
                samples = self.confusion_matrix.sum().item()

                observed = torch.sum(self.confusion_matrix, dim=1)
                predicted = torch.sum(self.confusion_matrix, dim=0)
                true_positives = self.confusion_matrix.diagonal()
                sample_weights = observed / samples

                # ... make sure to filter out where predictions or observations are zero
                where_predicted = torch.where(predicted > 0)
                where_observed = torch.where(observed > 0)

                recall = torch.sum((true_positives[where_predicted] / predicted[where_predicted]
                    ) * sample_weights[where_predicted]).item()
                precision = torch.sum((true_positives[where_observed] / observed[where_observed]
                    ) * sample_weights[where_observed]).item()
                accuracy = torch.sum(true_positives / samples).item() 
                f1 = (2 * (precision * recall) / (precision + recall) 
                    if precision + recall > 0 else 0)
                
                # Normalize logarithmic loss and collect perplexity
                log_loss = self.log_loss / samples
                perplexity = exp(log_loss)

                # Assemble metrics
                metrics = {
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "cross_entropy_loss": log_loss,
                    "perplexity": perplexity,
                }

                # Reset trackers for next evaluation cycle
                self.confusion_matrix = torch.zeros_like(self.confusion_matrix)
                self.log_loss = float(0)

                # Return metrics
                return metrics

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
    lines = {indicator: [line[indicator] for line in lines] for indicator in indicators}

    # ... and mark as missing entries non-number like (like "No Log")
    lines = {
        indicator: [entry if isinstance(entry, (int, float, np_float64)) else np_nan for entry in lines[indicator]]
        for indicator in indicators
    }

    # ... With a correspondence between the epochs and steps unit
    batch_size = (
        # Batch size per pass, from all devices
        max(trainer.args.per_device_train_batch_size, 1) * max(trainer.args.n_gpu, 1)
        # Passes until gradient accumulation
        * max(trainer.args.gradient_accumulation_steps, 1)
    )

    steps_per_epoch = len(trainer.train_dataset) / batch_size
    to_epoch = lambda steps: steps / steps_per_epoch
    to_step = lambda epochs: epochs * steps_per_epoch

    # Save logged metric lines for later
    lines_path = path.join(output_dir, "log_stats.json")
    print(f"Saving training stats to {lines_path}")
    try:
        with open(lines_path, 'w') as lines_file:
            json_dump(lines, lines_file)
    except Exception as err:
        print(f"Unable to save overall stats log into {lines_path}: {err}", file=stderr)
        print("Skipping saving...", file=stderr)

    # Generate loss-per-step plot
    fig_path = path.join(output_dir, "loss_per_step.png")
    print(f"Creating step-loss plot into {fig_path}")
    try:
        # ... Make it a single-celled plot
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # ... With a time series per-step for training and validation losses
        ax.set_title('Model loss over training')
        ax.set_ylabel("Loss")

        ax.plot("Step", "Training Loss", label='Training', markersize=12, data=lines)
        ax.plot("Step", "Validation Loss", label='Validation', markersize=12, data=lines)

        # TODO: Check for loss axis' boundaries
        # Loss may possibly be unbound (the default CausalLM loss is cross-entropy, for example)
        # Lets keep the loss axis unbounded for now
        #ax.set_ylim(0,1)

        # ... With a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax2 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax2.set_xlabel("Epoch")

        # Add legends and resize layout so it fits into plot
        fig.legend(loc="outside upper right")
        fig.tight_layout()

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

    # Generate metrics-per-step plot
    fig_path = path.join(output_dir, "metrics_per_step.png")
    print(f"Creating step-metrics plot into {fig_path}")
    try:
        # ... Make it a single-celled plot
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # ... With a time series per-step for each categorization metric
        ax.set_title('Model metrics for evaluation split per step')
        ax.set_ylabel("%")

        ax.plot("Step", "Precision", label='Precision', markersize=12, color="coral",data=lines)
        ax.plot("Step", "Recall", label='Recall', markersize=12, color="limegreen", data=lines)
        ax.plot("Step", "Accuracy", label='Accuracy', markersize=12, color="gold", data=lines)
        ax.plot("Step", "F1", label='F1', markersize=12, color="darkorchid", data=lines)

        # TODO: Check for axis boundaries
        # These may be super small and hard to make legible, so for now lets allow them to decide
        # the upper boundaries
        ax.set_ylim(bottom=0)
        ax.set_yticklabels([f'{(100 * y):.2f}%' for y in ax.get_yticks()]) # Y-axis ticks as percents

        # ... And with a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax2 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax2.set_xlabel("Epoch")

        # Add legends and resize layout so it fits into plot
        fig.legend(loc="outside upper right")
        fig.tight_layout()

        # Save plot to the appropiate path
        try:
            fig.savefig(fig_path)
            print(f"Saved step-metrics plot into {fig_path} succesfully")
        except Exception as err:
            print(f"Unable to save step-metrics plot into {fig_path}: {err}", file=stderr)
            print(f"Skipping plot saving...", file=stderr)

        # Clear memory and close the plot
        plt.close(fig)

    except Exception as err:
        print(f"Unhandled error while generating plot for evaluation-split metrics: {err}", file=stderr)
        print("Skipping plot generation...", file=stderr)

    # Generate LM-metrics-per-step plot
    fig_path = path.join(output_dir, "lm_metrics_per_step.png")
    print(f"Creating step-LM-metrics plot into {fig_path}")
    try:
        # ... Make it a single-celled plot
        fig, ax = plt.subplots(nrows=1, ncols=1)

        # ... With a time series per-step for training and validation losses
        ax.set_title('LM model metrics over training')
        ax.set_ylabel("Perplexity")
        ax_other = ax.twinx()
        ax_other.set_ylabel("Cross Entropy Loss")

        ax.plot("Step", "Perplexity", label='Perplexity', markersize=12, color="deepskyblue", data=lines)
        ax_other.plot("Step", "Cross Entropy Loss", label='Cross Entropy Loss', markersize=12, color="deeppink", data=lines)

        # TODO: Check for measurments axis' boundaries
        # Loss may possibly be unbound (the default CausalLM loss is cross-entropy, for example)
        # Lets keep the loss axis unbounded for now
        ax.set_ylim(bottom=0)
        ax_other.set_ylim(bottom=0)

        # ... With a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax2 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax2.set_xlabel("Epoch")

        # Add legends and resize layout so it fits into plot
        fig.legend(loc="outside upper right")
        fig.tight_layout()

        # Save plot to the appropiate path
        try:
            fig.savefig(fig_path)
            print(f"Saved step-LM-metrics plot into {fig_path} succesfully")
        except Exception as err:
            print(f"Unable to save step-LM-metrics plot into {fig_path}: {err}", file=stderr)
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
