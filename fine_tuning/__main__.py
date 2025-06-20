# Tools
from .model_loading import load_model, load_test_model

# Argument parsing
import argparse
from sys import exit, argv, stderr

def main():
    # Register arguments
    parser = argparse.ArgumentParser(description='Download, test, finetune and validate decompilation model')
    
    # Register subcommands
    sub_parsers = parser.add_subparsers(dest="selected_command", required=True,
        help='Select command to work with')
    
    # - Download and/or test model with a single prompt
    download_parser = sub_parsers.add_parser("download", 
        help="Download pre-trained model to local folder and/or test it with a single prompt")
    
    # - - Register arguments
    download_parser.add_argument('model_path', type=str, 
        help='Path to directory download pre-trained model into')
    download_parser.add_argument('--test', action='store_true',
        help="After downloading pre-trained model, test it running a simple prompt")
    
    # If no arguments are passed, print the usage
    if (len(argv) == 0):
        parser.parse_args(["-h"])
        exit(0)

    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()
    selected_command = args.selected_command
    
    # Run the download and/or testing of the pre-trained model
    if selected_command == "download":
        if args.test:
            load_test_model(args.model_path)
        else:
            load_model(args.model_path)
    else:
        print(f"Unrecognized commad {selected_command}", file=stderr)
        exit(-1)

if __name__ == "__main__":
    main()