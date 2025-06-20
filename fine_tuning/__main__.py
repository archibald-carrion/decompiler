# Tools
from .commands import download_test_model, eval_model

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
        help='Path to directory to downloade pre-trained model into')
    download_parser.add_argument('--test', action='store_true',
        help="After downloading pre-trained model, test it running a simple prompt")
    

    # - Evaluate model on a test split of the dataset
    evaluate_parser = sub_parsers.add_parser("evaluate", 
        help="Evalute model on testing split of a dataset, and save results to a file")
    
    # - - Register arguments
    evaluate_parser.add_argument('model_path', type=str, 
        help='Path to directory with pre-trained model (might be fine-tuned)')
    evaluate_parser.add_argument('dataset_dir', type=str, 
        help='Path to directory with dataset files and testing split')
    evaluate_parser.add_argument('train_args_path', type=str, 
        help='Path to JSON file containing previously-stored TrainingArguments')
    evaluate_parser.add_argument('output_dir', type=str, 
        help='Path to directory to place resulting statistic files into')
    
    # If no arguments are passed, print the usage
    if (len(argv) == 0):
        parser.parse_args(["-h"])
        exit(0)

    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()
    selected_command = args.selected_command
    
    # Run the download and/or testing of the pre-trained model
    args = vars(args)
    del args["selected_command"]

    if selected_command == "download":
        download_test_model(**args)
    elif selected_command == "evaluate":
        eval_model(**args)
    else:
        print(f"Unrecognized commad {selected_command}", file=stderr)
        exit(-1)

if __name__ == "__main__":
    main()