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

from sklearn.metrics import log_loss as cross_entropy_loss, confusion_matrix # Hand-crafted metrics
from math import exp # ...
import numpy as np # ...
from scipy.special import softmax

from torch.cuda import is_available as is_cuda_available # CUDA detection

from transformers.modelcard import parse_log_history # Human-readable metric parsing
from .dataset_loading import DecompilationDataset # Datasets

import matplotlib.pyplot as plt # Plotting losses
from json import dump as json_dump # Serializing metrics

class BatchDecompilerMetrics:
    def __init__(self, class_count: int):
        assert class_count > 0, "Invalid number of classes"

        # Keep track of the universe of classes
        # We'll asume they reside in [0, class_count)
        self.classes = np.arange(class_count)

        # Keep track of a fresh confusion matrix
        self.confusion_matrix = np.zeros(shape=(class_count, class_count), dtype=np.float64)

        # Keep track of fresh logarithmic loss
        self.log_loss = float(0)

    def __call__(self, eval_preds: EvalPrediction, compute_result = False):
        if compute_result:
            # Collect metrics precision, accuracy and f1-score based on confusion matrix
            samples = self.confusion_matrix.sum()
            assert samples > 0, "Tried to collect statistics with no previous work"

            observed = self.confusion_matrix.sum(axis=1)
            predicted = self.confusion_matrix.sum(axis=0)
            true_positives = self.confusion_matrix.diagonal()
            sample_weights = (observed / samples)

            # ... make sure to filter out where predictions or observations are zero
            where_predicted = np.where(predicted > 0)
            where_observed = np.where(observed > 0)

            recall = ((true_positives[where_predicted] / predicted[where_predicted]
                ) * sample_weights[where_predicted]).sum()
            precision = ((true_positives[where_observed] / observed[where_observed]
                ) * sample_weights[where_observed]).sum()
            accuracy = true_positives.sum() / samples
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
            self.confusion_matrix = np.zeros_like(self.confusion_matrix)
            self.log_loss = float(0)

            # Return metrics
            return metrics
        else:
            # Collect the logits and labels on the cpu
            logits, labels = eval_preds
            logits, labels = logits.cpu().numpy(), labels.cpu().numpy() 

            # We'll asume one-hot encoding
            predicted_labels : np.ndarray = np.argmax(logits, axis=-1)

            # Flatten in case we got batches
            labels = labels.flatten()
            predicted_labels = predicted_labels.flatten()
            logits = logits.reshape((-1, logits.shape[-1]))

            # ... and also normalize logits, which yields likelihood for each predicted label
            # For this, we'll use SoftMax, since CausalLM models return the score before SoftMax
            logits = softmax(logits, axis=1)

            # Just in case, filter to keep only unmasked tokens. 
            # Older architecture classes like GPT2 do mask.
            # See: https://huggingface.co/docs/transformers/en/model_doc/gpt2#transformers.GPT2LMHeadModel.forward.labels
            # While newer architecture classes, like Llama, don't.
            # See: https://huggingface.co/docs/transformers/v4.52.3/en/model_doc/llama#transformers.LlamaForTokenClassification.forward.labels
            unmasked = np.where(labels >= 0)

            labels = labels[unmasked]
            predicted_labels = predicted_labels[unmasked]
            logits = logits[unmasked]

            # Update our confusion matrix and logarithmic loss trackers
            self.confusion_matrix += confusion_matrix(labels, predicted_labels, labels=self.classes)
            self.log_loss += cross_entropy_loss(labels, logits, labels=self.classes, normalize=False)

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
        ax.plot("Step", "Training Loss", label='Training', markersize=12, data=lines)
        ax.plot("Step", "Validation Loss", label='Validation', markersize=12, data=lines)
        ax.set_title('Model loss over training')
        ax.set_ylabel("Loss")
        ax.legend()

        # TODO: Check for loss axis' boundaries
        # Loss may possibly be unbound (the default CausalLM loss is cross-entropy, for example)
        # Lets keep the loss axis unbounded for now
        #ax.set_ylim(0,1)

        # ... With a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax2 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax2.set_xlabel("Epoch")

        # Resize layout so it fits into plot
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
        ax.set_ylim(0,1)
        ax.set_yticklabels([f'{(100 * y):.2f}%' for y in ax.get_yticks()]) # Y-axis ticks as percents

        ax.plot("Step", "Precision", label='Precision', markersize=12, color="coral",data=lines)
        ax.plot("Step", "Recall", label='Recall', markersize=12, color="limegreen", data=lines)
        ax.plot("Step", "Accuracy", label='Accuracy', markersize=12, color="gold", data=lines)
        ax.plot("Step", "F1", label='F1', markersize=12, color="darkorchid", data=lines)

        # ... With two additional vertical axis
        ax2 = ax.twinx()
        ax2.spines["right"].set_visible(True)

        ax3 = ax.twinx()
        ax3.spines["right"].set_position(("axes", 1.5))
        ax3.spines["right"].set_visible(True)

        # ... For a time series per-step for the other scores
        ax2.set_ylabel("Perplexity Score")
        ax2.plot("Step", "Perplexity", label='Perplexity', markersize=12, color="deepskyblue", data=lines)
        
        ax3.set_ylabel("Cross Entropy Loss")
        ax3.plot("Step", "Cross Entropy Loss", label='Cross Entropy Loss', markersize=12, color="deeppink", data=lines)

        # ... And with a step horizontal axis
        ax.set_xlabel("Step")

        # ... And an additional epoch horizontal axis
        ax4 = ax.secondary_xaxis("top", functions=(to_epoch, to_step))
        ax4.set_xlabel("Epoch")

        # Add legends and resize layout so it fits into plot
        fig.legend()
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
