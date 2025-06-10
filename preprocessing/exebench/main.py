import os # Filesystem
import sys # Printing, mostly
import argparse # Parsing arguments 
import json # Dataset fomatting
import pandas as pd # EDA
from math import inf, ceil # Quick progress bar math
from tqdm import tqdm # Progress bar
from pathlib import Path # File globbing
import zstandard as zstd # Decompression

def fix_example(example):
    # Rename C content
    example["c"] = example["func_def"]

    # Match and re-structure assembly targets structure
    arch_from_target = lambda target: "gcc" if "gcc" in target else "arm"
    opt_from_target = lambda target: target.rsplit("_", 1)[-1]

    example['asm'] = [{
        'arch': arch_from_target(target), 
        'opt': opt_from_target(target), 
        'code': code['func_asm'] if code else None
    } for (target, code) in example['asm'].items()]

    # Filter for missing assembly code or invalid architectures
    example["asm"] = list(filter(
        lambda asm: asm["code"] is not None and asm["arch"] == "gcc", 
        example["asm"]
    ))

    # Remove redundant target feature in assemblies
    for target in example["asm"]:
        del target["arch"]

    # Remove troublesome/unecessary features
    unecessary_keys = filter(lambda x: x not in ["asm", "c"], example.keys())
    for key in list(unecessary_keys):
            del example[key]

    # All is done
    return example

def load_examples(split_directory: str):
    # For every split collection, generate examples
    for split_file in Path(split_directory).rglob('*.jsonl.zst'):
        # Decompress the split collection file
        try:
            with zstd.open(open(split_file, "rb"), "rt", encoding="utf-8") as f:
                # For every example in the split, fix the data accordingly
                for row in f:
                    try:
                        # Load the JSON data for the example
                        data = json.loads(row)
                        data = data['text']

                        # Skip example if missing key features
                        if "func_def" not in data.keys() or "asm" not in data.keys():
                            print("Split example missing 'func_def' and/or 'asm' fields", file=sys.stderr)
                            print("Skipping example...", file=sys.stderr)
                            continue

                        # Apply fixes to the example
                        data = fix_example(data)

                        # Skip example if no target assemblies were found
                        if (len(data["asm"]) < 1):
                            continue

                        # Yield the fixed example
                        yield data

                    except Exception as err:
                        print(f"Unable to process example on split file {split_file}: {err}", file=sys.stderr)
                        print("Skipping example...", file=sys.stderr)

        except Exception as err:
            print(f"Unable to process split collection on file {split_file}: {err}", file=sys.stderr)
            print("Skipping split file...", file=sys.stderr)

def process(data_dir: str, c_dir: str, asm_dir: str, max_size: int, unit: str, max_entries: int = inf, stats_out: str|None = None):
    """Processes the contents of files inside the Stack's dataset
    Arguments:
        output_dir (str): Directory to stream splits from
        c_dir (str): Directory to put C files into
        asm_dir (str): Directory to put x86 assembly files into
        max_size (int): Greatest size (in units of choice) to allow for the entire set processed output
        unit (str): Unit of choice (KB|MB|GB) to use for measuring maximum allowed size (and progress)
        max_files (int | inf, optional): Greatest amount of individual entries allowed to be processed. Defaults to inf.
        stats_out (str | None, optional): Filepath to output statistics to. Default to None
    """
    # Keep track of conversion factors for each unit to bytes
    unit_conversion = {"KB": 2**10, "MB": 2**20, "GB": 2**30}

    # Check valid parameters
    assert isinstance(data_dir, str) and os.path.isdir(data_dir), "Input data directory path should be valid and a string"
    assert isinstance(c_dir, str), "Output C directory path should be a string"
    assert isinstance(asm_dir, str), "Output x86 assembly directory path should be a string"
    assert unit in unit_conversion, "Size unit should be GB, MB or KB"
    assert (isinstance(max_size, int) or isinstance(max_size, int)) and max_size > 0, "Maximum size should be a positive number"
    assert isinstance(max_entries, int) or max_entries == inf, "Maximum amount of entries should be a positive integer"
    assert isinstance(stats_out, str) or stats_out == None, "Filepath to output statistics should be a string or None"

    # Create the output directory if not already present
    try:
        os.makedirs(c_dir, exist_ok=True)
        os.makedirs(asm_dir, exist_ok=True)
    except err:
        print("Unable to access directory path:", err, file=sys.stderr)
        raise Exception("Invalid directory")

    # Stream the contents until the maximum size or entry count is exceeded
    total_size = 0
    processed_entries = 0
    progress_delta = 0
    print("Streaming C and ASM source files, with at most", max_size, unit + "s of content")

    # Keep track of stats if desired
    if stats_out != None:
        stats = pd.DataFrame(
            data = {
                'C filename': pd.array(data=[], dtype=pd.StringDtype()), 
                'x86 filename': pd.array(data=[], dtype=pd.StringDtype()),
                "Optimization level": pd.Categorical(values=[], 
                    categories=["O0", "Os", "O3", "Ofast"], ordered=True),
            }
        )

    with tqdm(total=max_size, unit=unit, file=sys.stdout) as pbar:
        pbar.set_description("Streaming contents")

        # Load streams of the dataset splits, pull as required
        for i, sample in enumerate(load_examples(data_dir)):
            # Continue only if max file limit won't be exceeded
            if processed_entries + 1 > max_entries:
                break

            # Collect the content from the C source code
            c_filename = f"{i}.c"
            c_content = sample["c"]

            # Collect the assemblies
            assemblies = sample["asm"]

            # Calculate the total contribution in storage from all source codes
            size = (sum([len(asm["code"]) for asm in assemblies]) + len(c_content)) / unit_conversion[unit]

            # If adding it would exceed up the maximum allocated size, stop processing
            if total_size + size > max_size:
                break

            # Construct the C source code file    
            c_filepath = os.path.join(c_dir, c_filename)
            pbar.set_postfix_str(f"#{i+1}: {c_filename} ({round(size, 2)} {unit}s)")

            # Write its contents
            # If any meaningful error occurs, recover and continue processing the remaining files
            write_success = True
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
                asm_filename = f"{i}_{asm["opt"]}.s"
                asm_filepath = os.path.join(asm_dir, asm_filename)

                pbar.set_postfix_str(f"#{i+1}: {asm_filename} ({round(size, 2)} {unit}s)")

                # Write its contents
                # If any meaningful error occurs, recover and continue processing the remaining files
                asm["write_success"] = True
                try:
                    with open(asm_filepath, "w", encoding="utf-8") as f:
                        try:
                            f.write(asm["code"])
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
            processed_entries += 1
            total_size += size

            pbar.update(int(total_size) - progress_delta 
                if max_size > total_size + size else max_size - progress_delta)
            progress_delta = int(total_size)

            # Keep track of statistics if desired
            if stats_out != None:
                for asm in filter(lambda asm: asm["write_success"], assemblies):
                    stats.loc[i, "C filename"] = c_filename
                    stats.loc[i, "x86 filename"] = f"{i}_{asm["opt"]}.s"
                    stats.loc[i, "Optimization level"] = asm["opt"]

    # Report findings
    print(f"Processed {processed_entries}" + ("" if max_entries == inf else f"/{max_entries}") + 
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
    parser = argparse.ArgumentParser(description='Process source C files and x86 assemblies from ExeBench')
    parser.add_argument('--stats', required=False, default=None, 
        help='Path to file in which to store brief statistics for the process')
    
    parser.add_argument('data_dir', type=str, 
        help='Path to input directory of compressed (*.zst) dataset files (*.jsonl)')
    parser.add_argument('c_dir', type=str, 
        help='Path to output directory of processed C files')
    parser.add_argument('asm_dir', type=str, 
        help='Path to output directory of processed x86 assembly files')
    parser.add_argument('max_size', type=int, 
        help='Maximum size (in units) of processed content for the entire file collection')
    parser.add_argument('unit', type=str, choices=["KB", "MB", "GB"], 
        help='Unit of size to use when limiting processing output files total size (bytes)')
    parser.add_argument('--max_entries', type=int, required=False, default=inf, 
        help='Maximum amount of entries to process')

    # If no arguments are passed, print the usage
    if (len(sys.argv) == 0):
        parser.parse_args(["-h"])
        sys.exit(0)
    
    # Otherwise, parse the commands and run accordingly
    args = parser.parse_args()

    print("Processing files...")
    process(args.data_dir, args.c_dir, args.asm_dir, args.max_size, args.unit, args.max_entries, args.stats)

    print("Done!")
