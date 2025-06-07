import subprocess # Invoking GCC
import os # Filesystem
import sys # Printing, mostly
import argparse # Parsing arguments
import numpy as np # EDA 
import pandas as pd # EDA
from tqdm import tqdm # Progress bar
from math import inf, ceil # Quick progress bar math
from datasets import load_dataset, concatenate_datasets # HuggingFace downloading API
from huggingface_hub import login # HuggingFace auth API

# TODO: Crashes after use. Fatal Python error: PyGILState_Release 
# Note: This doesn't seem to hurt the end result
# Check https://github.com/huggingface/datasets/issues/7357
def download(c_dir: str, asm_dir: str, max_size: int, unit: str, max_entries: int = inf, stats_out: str|None = None):
    """Downloads the contents of files inside the Stack's dataset
    Arguments:
        output_dir (str): Directory to put files into
        max_size (int): Greatest size (in units of choice) to allow for the entire set download
        unit (str): Unit of choice (KB|MB|GB) to use for measuring maximum allowed size (and progress)
        max_files (int | inf, optional): Greatest amount of individual entries allowed to be downloaded. Defaults to inf.
        stats_out (str | None, optional): Filepath to output statistics to. Default to None
    """

    # Keep track of conversion factors for each unit to bytes
    unit_conversion = {"KB": 2**10, "MB": 2**20, "GB": 2**30}

    # Check valid parameters
    assert isinstance(c_dir, str), "Download output C directory path should be a string"
    assert isinstance(asm_dir, str), "Download output ASM directory path should be a string"
    assert unit in unit_conversion, "Size unit should be GB, MB or KB"
    assert (isinstance(max_size, int) or isinstance(max_size, int)) and max_size > 0, "Maximum size should be a positive number"
    assert isinstance(max_entries, int) or max_entries == inf, "Maximum amount of entries should be a positive integer"
    assert isinstance(stats_out, str) or stats_out == None, "Filepath to output statistics should be a string or None"

    # Create the output directory if not already present
    try:
        os.makedirs(c_dir, exist_ok=True)
        os.makedirs(asm_dir, exist_ok=True)
    except err:
        print("Unable to access directory path:", err)

    # Log in to access gated dataset
    print("Logging in to access gated dataset...")
    login()

    # Load streams of the dataset splits, pull as required
    print("Loading dataset with C directory", c_dir, "and x86 directory", asm_dir)

    ds = []
    for split in ["valid_real", "valid_synth"]: # ["test_real", "test_synth", "valid_real", "valid_synth"]:
        print("Loading split", split)
        ds.append(load_dataset("jordiae/exebench", split=split, trust_remote_code=True))
    
    # Merge said streams into one
    print("Merging splits into one")
    ds = concatenate_datasets(ds)

    # Download the contents until the maximum size or entry count is exceeded
    total_size = 0
    downloaded_entries = 0
    progress_delta = 0
    print("Downloading C and ASM source files, with at most", max_size, unit + "s of content")

    # Keep track of stats if desired
    if stats_out != None:
        stats = pd.DataFrame(
            data = {
                'C filename': pd.array(data=[], dtype=pd.StringDtype()), 
                'x86 filename': pd.array(data=[], dtype=pd.StringDtype()),
                "Optimization level": pd.Categorical(values=[], 
                    categories=["Ofast", "Osize", "O0", "unknown"], ordered=True),
            }
        )

    with tqdm(total=max_size, unit=unit, file=sys.stdout) as pbar:
        pbar.set_description("Downloading contents")
        for i, sample in enumerate(ds):
            # Continue only if max file limit won't be exceeded
            if downloaded_entries + 1 > max_entries:
                break

            # Get the i-th sample of the dataset
            content = sample["text"]

            # Get the C source code and x86 assembly code from it
            # Skip the example if either is missing
            if "func_def" not in content or "asm" not in content:
                continue

            # Collect the content from the C source code
            c_filename = f"{i}.c"
            c_content = content["func_def"]
            c_size = len(c_content)

            # Collect the content from all the x86 assemblies with distinct targets and levels of 
            # optimizations
            assemblies = []
            for _, asm_content in content["asm"]:
                # Skip the properties with missing target and definitions
                if isinstance(asm_content, dict) and "func_asm" in asm_content and "target" in asm_content:
                    # Extract architecture and optimization info
                    target = asm_content["target"]
                    arch = "x86"
                    opt_level = target.get("o", "unknown")
                    
                    # Create a unique suffix for this assembly version
                    arch_suffix = f"{arch}"
                    opt_suffix = f"o{opt_level}" if opt_level != "s" else "os"
                    
                    # Add this file and its contents to the list
                    assemblies.append({
                        "filename": f"{i}_{arch_suffix}_{opt_suffix}.s",
                        "content": asm_content["func_asm"],
                        "opt_level": opt_level,
                        "size": len(asm_content["func_asm"])
                    })

            # Skip entry if no assemblies contents were found
            if len(assemblies) < 1:
                continue

            # Calculate the total contribution in storage from all source codes
            size = sum([asm["size"] for asm in assemblies]) + c_size

            # If adding it would exceed up the maximum allocated size, stop downloading 
            if total_size + size > max_size:
                break

            # Construct the C source code file    
            c_filepath = os.path.join(c_dir, c_filename)
            pbar.set_postfix_str(f"#{i+1}: {c_filename} ({round(size, 2)} {unit}s)")

            # Write its contents
            # If any meaningful error occurs, recover and continue downloading the remaining files
            write_success = False
            try:
                with open(c_filepath, "w", encoding="utf-8") as f:
                    try:
                        f.write(c_content)
                    except (IOError, OSError) as err:
                        print(f"Error writing C file contents on #{i+1} ({c_filename}):", err, file=sys.stderr)
                        write_success = False
            except (FileNotFoundError, PermissionError, OSError) as err:
                print(f"Error opening file #{i+1}:", err, file=sys.stderr)
                write_success = False
            f.close()

            # If the C file writing failed, abort all following writing attempts for assemblies
            if not write_success:
                print(f"Skipping writing assembly files for #{i+1}:", file=sys.stderr)
                continue

            # Construct the x86 assembly files from all variants
            # Keep track of writing success from each file
            for asm in assemblies:
                asm_filename = asm["filename"]
                asm_filepath = os.path.join(asm_dir, asm_filename)

                pbar.set_postfix_str(f"#{i+1}: {asm_filename} ({round(size, 2)} {unit}s)")

                # Write its contents
                # If any meaningful error occurs, recover and continue downloading the remaining files
                asm["write_success"] = True
                try:
                    with open(asm_filepath, "w", encoding="utf-8") as f:
                        try:
                            f.write(asm["content"])
                        except (IOError, OSError) as err:
                            print(f"Error writing file contents on #{i+1} ({asm_filename}):", err, file=sys.stderr)
                            asm["write_success"] = False
                except (FileNotFoundError, PermissionError, OSError) as err:
                    print(f"Error opening file contents on #{i+1} ({asm_filename}):", err, file=sys.stderr)
                    asm["write_success"] = False
                
                f.close()

            # If no assembly file was succesfully written, attempt to delete the C file and skip this
            # entry
            if not any([asm["write_success"] for asm in assemblies]):
                print(f"No assembly was succesfully written for #{i+1} ({c_filename}):", file=sys.stderr)
                print(f"Attempting to remove C source file for ({c_filename}):", file=sys.stderr)
                try:
                    if os.path.exists(c_filepath):
                        os.remove(c_filepath)
                except Exception as err:
                    print(f"Error removing file contents on #{i+1} ({c_filename}):", err, file=sys.stderr)

                continue

            # Update the total size and total entry count
            if write_success:
                downloaded_entries += 1
                total_size += size

                pbar.update(int(total_size) - progress_delta 
                    if max_size > total_size + size else max_size - progress_delta)
                progress_delta = int(total_size)

            # Keep track of statistics if desired
            if stats_out != None:
                for asm in filter(lambda asm: asm["write_success"], assemblies):
                    stats.loc[i, "C filename"] = c_filename
                    stats.loc[i, "x86 filename"] = asm["filename"]
                    stats.loc[i, "Optimization level"] = asm["opt_level"]

    # Report findings
    print(f"Downloaded {downloaded_entries}" + ("" if max_entries == inf else f"/{max_entries}") + 
        f" files to '{c_dir}'")
    print(f"Used ~{round(total_size, 2)}/{max_size} {unit}s (~{round((total_size / max_size) * 100, 2)}%) of storage")

    if stats_out != None:
        print("Statistics:")
        print(stats.describe(include="all"))

        print(f"Saving table to {stats_out}...")
        try:
            stats.to_csv(path_or_buf=stats_out, mode="w")
        except Exception as err:
            print(f"Unable to save statistics: {err}")

    return

if __name__ == "__main__":
    # Register arguments
    parser = argparse.ArgumentParser(description='Download source C files and x86 assemblies from ExeBench')
    parser.add_argument('--stats', required=False, default=None, 
        help='Path to file in which to store brief statistics for the process')
    
    parser.add_argument('c_dir', type=str, 
        help='Path to output directory of downloaded C files')
    parser.add_argument('asm_dir', type=str, 
        help='Path to output directory of downloaded x86 assembly files')
    parser.add_argument('max_size', type=int, 
        help='Maximum size (in units) of downloaded content for the entire file collection')
    parser.add_argument('unit', type=str, choices=["KB", "MB", "GB"], 
        help='Unit of size to use when limiting download size (bytes)')
    parser.add_argument('--max_entries', type=int, required=False, default=inf, 
        help='Maximum amount of entries to download')

    # If no arguments are passed, print the usage
    if (len(sys.argv) == 0):
        parser.parse_args(["-h"])
        sys.exit(0)
    
    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()

    print("Downloading files...")
    download(args.c_dir, args.asm_dir, args.max_size, args.unit, args.max_entries, args.stats)

    print("Done!")
