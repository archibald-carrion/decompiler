# Tools
from .commands import download_test_model, eval_model, train_model_custom_args, train_model_presaved_args

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
    
    # - Train model on dataset
    train_parser = sub_parsers.add_parser("train", 
        help="Train model on training and validation split of a dataset")
    
    # - - Register arguments
    train_parser.add_argument('model_path', type=str, 
        help='Path to directory with pre-trained model (might be fine-tuned)')
    train_parser.add_argument('dataset_dir', type=str, 
        help='Path to directory with dataset files and training/validation splits')
    train_parser.add_argument('output_dir', type=str, 
        help='Path to directory to save model into after training')
    train_parser.add_argument('--stats_dir', type=str, required=False, default=None,
        help='Path to directory to save training statistics into')
    
    # - - Register training command training argument variants
    train_subparsers = train_parser.add_subparsers(dest='training_argument_source', required=True,
        help="Specify arguments for training model")  
    
    # - - - Manually specify training arguments
    train_custom_args = train_subparsers.add_parser("custom", 
        help="Specify custom training arguments, by hand")
    
    # - - - - Register arguments
    train_custom_args.add_argument('checkpoints_dir', type=str,
        help='Path to directory to save training checkpoints into')
    train_custom_args.add_argument('training_epochs', type=int,
        help='Total epochs to train for')
    train_custom_args.add_argument('--seed', type=int, required=False, default=0,
        help='Seed for initial training process. Doesnt guarantee determinism on GPUs')
    train_custom_args.add_argument('--gradient_accum_steps', type=int, required=False, default=8,
        help='Gradient accumulation steps. Helps manage batch size per device. Raise it if memory is scarce')
    train_custom_args.add_argument('--args_output_path', type=str, required=False, default=None,
        help='Path to JSON file to save custom training argument contents into')
    
    # - - - Load previously-saved training arguments
    train_presaved_args = train_subparsers.add_parser("presaved", 
        help="Load training arguments from JSON file")
    
    # - - - - Register arguments
    train_presaved_args.add_argument('args_path', type=str,
        help='Path to JSON file containing training arguments')
    
    # If no arguments are passed, print the usage
    if (len(argv) == 0):
        parser.parse_args(["-h"])
        exit(0)

    # Otherwise, parse the commands and run accordingly
    args = vars(parser.parse_args())
    selected_command = args["selected_command"]
    del args["selected_command"]
    
    # Run the download and/or testing of the pre-trained model
    if selected_command == "download":
        download_test_model(**args)
    elif selected_command == "evaluate":
        eval_model(**args)
    elif selected_command == "train":
        training_argument_source = args["training_argument_source"]
        del args["training_argument_source"]

        if training_argument_source == "custom":
            train_model_custom_args(**args)
        elif training_argument_source == "presaved":
            train_model_presaved_args(**args)
        else:
            print(f"Unrecognized training argument source {training_argument_source}", file=stderr)
            exit(-1)
    
    else:
        print(f"Unrecognized command {selected_command}", file=stderr)
        exit(-1)

if __name__ == "__main__":
    main()
