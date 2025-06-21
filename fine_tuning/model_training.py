#!/usr/bin/env python3
"""
Fine-tuning script for OpenCoder-1.5B-Instruct model
Trains on assembly code -> C function pairs
"""

from os import path, makedirs # Path manipulation
import logging # Formatted logging

from transformers import Trainer

# Memory usage reports
from psutil import virtual_memory # Virtual memory
from torch.cuda import is_available as is_cuda_available, memory_allocated as cuda_memory_allocated, memory_reserved as cuda_memory_reserved # CUDA memory

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_model(trainer: Trainer, output_dir: str):
    """ Run trainer instance and save model to output directory
    ### Arguments:
        trainer (Trainer): Trainer instance to use during training
        output_dir (str): Directory to store the model into after training
    """
    # Validate trainer
    assert isinstance(trainer, Trainer), "Invalid trainer parameter"

    # Validate and expand output directory path
    assert isinstance(output_dir, str), "Output directory path for model should be a string"
    output_dir = path.expanduser(output_dir)
    
    # Begin training
    logger.info("====  Fine-tuning Start ====")
    try:
        # Log available virtual memory before training
        mem = virtual_memory()
        logger.info(f"[MEMORY] Before training - Available: {mem.available / 1024 ** 2:.2f} MB, Used: {mem.used / 1024 ** 2:.2f} MB")

        # Report CUDA memory as well
        if is_cuda_available():
            logger.info(
                f"[CUDA] Allocated: {cuda_memory_allocated() / 1024 ** 2:.2f} MB, "
                + f"Reserved: {cuda_memory_reserved() / 1024 ** 2:.2f} MB"
            )

        # Start training
        logger.info("Starting training...")

        try:
            train_output = trainer.train()
            logger.info(f"Training output: {train_output}")
        except RuntimeError as re:
            logger.error("RuntimeError during training (possible OOM):")
            logger.error(str(re), exc_info=True)
            return

        logger.info("Training completed!")

    except Exception as e:
        logger.error("An unhandled exception occurred during training:")
        logger.error(str(e), exc_info=True)

    logger.info("==== Fine-tuning End ====")


    # Save the final model
    logger.info(f"Saving model to {output_dir}...")

    try:
        makedirs(output_dir, exist_ok=True)
        trainer.save_model(output_dir)
    except Exception as err:
        logger.error("Unable to save model due to error:")
        logger.error(str(err), exc_info=True)
        return
    
    logger.info(f"Model saved succesfully under {output_dir}")