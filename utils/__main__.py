# Tools
from .model_showcase import decompile
from .model_loading import load_model

# Argument parsing
import argparse
from sys import exit, argv, stderr
from os import path

# Elapsed time formatting
from datetime import timedelta

def main():
    # Register arguments
    parser = argparse.ArgumentParser(
        description='Decompile a x86 source code into C using the fine-tuned LLM model')
    
    parser.add_argument('model_path', type=str, 
        help='Path to directory where fine-tuned/pre-trained model resides')
    parser.add_argument('asm_path', type=str, 
        help='Path to file with containg x86 source code to decompile')
    parser.add_argument('c_path', type=str, 
        help='Output path to file where to store the results into')
    parser.add_argument('--temperature', type=float, required=False, default=0.5,
        help="Temperature to use when sampling the best predicted results")
    parser.add_argument('--top_p', type=float, required=False, default=0.5,
        help="Top-p parameter to use when sampling the best predicted results")

    # If no arguments are passed, print the usage
    if (len(argv) == 0):
        parser.parse_args(["-h"])
        exit(0)

    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()

     # - Expand the paths
    args.model_path = path.expanduser(args.model_path)
    args.asm_path = path.expanduser(args.asm_path)
    args.c_path = path.expanduser(args.c_path)

    # - Validate the sources
    assert path.isdir(args.model_path), "Invalid model directory"
    assert path.isfile(args.asm_path), "Invalid source x86 assembly"

    # - Load model
    print(f"Loading model from {args.model_path}...")
    try:
        # Load model and tokenizer from local directory path
        model, tokenizer = load_model(args.model_path)
        print("Model loaded succesfully!")
    except Exception as err:
        print(f"Unable to load model due to error: {err}", file=stderr)
        exit(-1)

    # - Load x86 source code
    print(f"Loading x86 source code from {args.asm_path}...")
    try:
        with open(args.asm_path, "r", encoding="utf-8") as f:
            asm_code = f.read()
        print("x86 source code loaded succesfully!")
    except Exception as err:
        print(f"Unable to load x86 source code due to error: {err}", file=stderr)
        exit(-1)

    # - Compute prediction
    print(f"Decompiling into {args.c_path}...")
    try:
        c_code, elapsed_ns = decompile(model, tokenizer, asm_code, args.top_p, args.temperature)
        if c_code:
            with open(args.c_path, "w", encoding="utf-8") as f:
                f.write(c_code)
            print(f"Decompiled succesfully!")
        else:
            print(f"Model generated no output!")
        
        print(f"Time taken: {timedelta(milliseconds=elapsed_ns/10E6)}")

    except Exception as err:
        print(f"Unable to decompile x86 source code due to error: {err}", file=stderr)
        exit(-1)

    print("All done!")
if __name__ == "__main__":
    main()