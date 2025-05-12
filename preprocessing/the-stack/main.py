import subprocess # Invoking GCC
import os # Filesystem
import sys # Printing, mostly
import argparse # Parsing arguments
import numpy as np # EDA 
import pandas as pd # EDA
from tqdm import tqdm # Progress bar
from math import inf, ceil # Quick progress bar math
from datasets import load_dataset # HuggingFace downloading API
from huggingface_hub import login # HuggingFace auth API

def download(output_dir: str, max_size: int, unit: str, max_files: int = inf, do_stats: bool = False):
    """Downloads the contents of files inside the Stack's dataset
    Arguments:
        output_dir (str): Directory to put files into
        max_size (int): Greatest size (in units of choice) to allow for the entire set download
        unit (str): Unit of choice (KB|MB|GB) to use for measuring maximum allowed size (and progress)
        max_files (int | inf): Greatest amount of individual files allowed to be downloaded. Defaults to inf.
        do_stats (bool): Whether to collect or not EDA statistics on file size. Defaults to False.
    """

    # Keep track of conversion factors for each unit to bytes
    unit_conversion = {"KB": 2**10, "MB": 2**20, "GB": 2**30}

    # Check valid parameters
    assert isinstance(output_dir, str), "Download output directory path should be a string"
    assert unit in unit_conversion, "Size unit should be GB, MB or KB"
    assert (isinstance(max_size, int) or isinstance(max_size, int)) and max_size > 0, "Maximum size should be a positive number"
    assert isinstance(max_files, int) or max_files == inf, "Maximum amount of files should be a positive integer"

    # Create the output directory if not already present
    try:
        os.makedirs(output_dir, exist_ok=True)
    except err:
        print("Unable to access directory path:", err)

    # Log in to access gated dataset
    print("Logging in to access gated dataset...")
    login()

    # Load a stream of the dataset, pull as required
    print("Loading dataset at", output_dir)
    ds = load_dataset("bigcode/the-stack", data_dir="data/c", streaming=True, split="train")

    # Download the contents until the maximum size or file count is exceeded
    total_size = 0
    downloaded_files = 0
    progress_delta = 0
    print("Downloading c source files, with at most", max_size, unit + "s of content")

    # Keep track of stats if desired
    if do_stats:
        sizes = pd.DataFrame(
            data = {
                'C': [] if max_files == inf else np.full(max_files, np.nan)  
            }
        )

    with tqdm(total=max_size, unit=unit, file=sys.stdout) as pbar:
        pbar.set_description("Downloading contents")
        for i, sample in enumerate(ds):
            # Continue only if max file limit won't be exceeded
            if downloaded_files + 1 > max_files:
                break

            # Get the i-th sample of the dataset
            content = sample["content"]
            size = len(content.encode("utf-8")) / unit_conversion[unit]

            # If adding it would exceed up the maximum allocated size, stop downloading 
            if total_size + size > max_size:
                break

            # Construct the output file path
            filename = f"{i}.c" 
            filepath = os.path.join(output_dir, filename)
            pbar.set_postfix_str(f"#{i+1}: {filename} ({round(size, 2)} {unit}s)")

            # Write its contents
            # If any meaningful error occurs, abort downloading the remaining files 
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    try:
                        f.write(content)
                    except (IOError, OSError) as err:
                        print(f"Error writing file #{i+1} contents:", err, file=sys.stderr)
                        f.close()
                        continue
            except (FileNotFoundError, PermissionError, OSError) as err:
                print(f"Error opening file #{i+1}:", err, file=sys.stderr)
                f.close()
                continue
            
            f.close()

            # Update the total size and total file count
            downloaded_files += 1
            total_size += size

            pbar.update(int(total_size) - progress_delta 
                if max_size > total_size + size else max_size - progress_delta)
            progress_delta = int(total_size)

            # Keep track of statistics if desired
            if do_stats:
                sizes.loc[i, "C"] = len(content.encode("utf-8"))

    # Report findings
    print(f"Downloaded {downloaded_files} files (~{round(total_size, 2)} {unit}s) to '{output_dir}'")
    if do_stats:
        print(f"Statistics for content sizes (bytes):")
        print(sizes.describe())

def assemble(input_dir: str, output_dir: str, flags: str = "", do_stats: bool = False):
    """Assembles C files inside a given directory onto another directory

    Args:
        input_dir (str): Directory where C files to assemble reside directly under
        output_dir (str): Directory to place resulting assemblies under
        flags (str, optional): Extra flags passed to _gcc_. Defaults to "".
        do_stats (bool, optional): Whether or not to collect basic EDA statistics on file sizes. Defaults to False.
    """
    # Check valid input and output directory
    assert os.path.isdir(input_dir), "Input path should be an existing directory"
    assert isinstance(output_dir, str), "Output path should be a string"
    assert isinstance(flags, str), "GCC flags should be a string"

    # Create the output directory if not already present
    try:
        os.makedirs(output_dir, exist_ok=True)
    except err:
        print("Unable to access directory path:", err)

    # For each file ending in *.c directly under the directory, assemble it
    sources = list(filter(lambda f: f.endswith(".c"), os.listdir(input_dir)))
    
    # Keep track of successes
    assembled: int = 0

    # Keep track of stats if desired
    if do_stats:
        sizes = pd.DataFrame(
            data = {
                'C': np.full(len(sources), np.nan), 
                'Assembly': np.full(len(sources), np.nan)
            }
        )

    with tqdm(total=len(sources), unit="files", file=sys.stdout) as pbar:
        pbar.set_description("Assembling files")
        for i, filename in enumerate(sources):
            # Keep track of the path of the source code, and the destination of its assembly
            # output 
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            output_path = output_path.rsplit(".", 1)[0] + ".s" # Output with extension extension to .s

            pbar.set_postfix_str(f"#{i+1}: {filename}")

            # Check size of source
            if do_stats:
                try:
                    sizes.loc[i, "C"] = os.path.getsize(input_path)
                except err:
                    print(f"Could not check size of source file at {input_path}:"
                        f"\n{err}", file=sys.stderr)
            
            # Try to assemble it
            # TODO: Fix invocation so assembly is readable
            result = subprocess.run(
                ["gcc", "-s", input_path, "-o", output_path, flags],
                capture_output = True, text=True
            )

            # Report and keep track of success
            if result.returncode == 0:
                assembled += 1

                # Check size of assembled result
                if do_stats:
                    try:
                        sizes.loc[i, "Assembly"] = os.path.getsize(output_path)
                    except err:
                        print(f"Could not check size of assembled file at {output_path}:"
                            f"\n{err}", file=sys.stderr)
                    
            else:
                print(f"Could not assemble {filename}:\n{result.stderr}", file=sys.stderr)
            
            pbar.update(1)
    
    # Report findings
    print(f"Assembled succesfully {assembled}/{len(sources)} ({round(assembled/len(sources) * 100)}%)")
    
    if do_stats:
        print("Statistics for content sizes (bytes):")
        print(sizes.describe())

if __name__ == "__main__":
    # Register arguments
    parser = argparse.ArgumentParser(description='Download and assemble source c files from The Stack')
    parser.add_argument('--size-stats', required=False, action='store_true', 
        help='Whether or not to calculate brief statistics for the size of the files')
    
    # Add subcommands: download / assemble
    command_parsers = parser.add_subparsers(dest='mode', required=True, 
        help="Download or assemble sources")

    # Options for download
    parser_download = command_parsers.add_parser('download', aliases=['do', 'd'])
    parser_download.set_defaults(mode='download')
    parser_download.add_argument('dir', type=str, 
        help='Path to output directory of downloaded files')
    parser_download.add_argument('max_size', type=int, 
        help='Maximum size (in units) of downloaded content for the entire file collection')
    parser_download.add_argument('unit', type=str, choices=["KB", "MB", "GB"], 
        help='Unit of size to use when limiting download size (bytes)')
    parser_download.add_argument('--max_files', type=int, required=False, default=inf, 
        help='Maximum amount of files to download')
    
    # Options for assembly
    parser_assemble = command_parsers.add_parser('assemble', aliases=['asm', 'a'])
    parser_assemble.set_defaults(mode='assemble')
    parser_assemble.add_argument('input_dir', type=str, 
        help='Path to directory where source C files directly reside under')
    parser_assemble.add_argument('output_dir', type=str, 
        help='Path to output directory of assembled files')
    parser_assemble.add_argument('--flags', type=str, required=False, default="-pass-exit-codes",
        help='Additional flags to pass to the GCC utility invocation')

    # If no arguments are passed, print the usage
    if (len(sys.argv) == 0):
        parser.parse_args(["-h"])
        sys.exit(0)
    
    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()

    if (args.mode == "download"):
        print("Downloading files...")
        download(args.dir, args.max_size, args.unit, args.max_files, args.size_stats)
    elif (args.mode == "assemble"):
        print("Assembling files...")
        assemble(args.input_dir, args.output_dir, args.flags, args.size_stats)
    else:
        print("Unknown command passed", file=sys.stderr)

    print("Done!")
