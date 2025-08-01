from .stack import load_examples as stack_examples
from .exebench import load_examples as exebench_examples

from sys import stdout, stderr # Logging to streams
from os import path, makedirs, remove # Filesystem manipulation
from numbers import Number # Number datatype assertion
import pandas as pd # EDA
from tqdm import tqdm # Progress bar

def load_examples(exebench_dir: str, stack_token: str, max_exebench_budget: Number, max_stack_budget: Number):
    """Generates C and x86 assembly files (in memory, as dicts) as examples from both the ExeBench's and The Stack's datasets
    ### Arguments:
        exebench_dir (str): Directory to read ExeBench's split files from
        stack_token (str): The Stack's access token for reading its contents
        max_exebench_budget (Number): Greatest size (in units of choice) to allow for the processed examples generated from ExeBench
        max_stack_budget (Number): Greatest size (in units of choice) to allow for the processed examples generated from The Stack
    ### Returns:
    One yielded example at a time, in the form \{ "c": \<c code\>, "asm"\: \{ \<optimization level\> \: \<x86 assembly code\> \} \}
    """
    if max_exebench_budget > 0:
        print("Streaming C and ASM examples from ExeBench, locally")
        print(f"Splits located at {exebench_dir}")
        with tqdm(
            exebench_examples(split_directory=exebench_dir),
            desc="Streaming examples from ExeBench",
            total=max_exebench_budget, unit='B', unit_scale=True, unit_divisor=1024, file=stdout
        ) as pbar:
            for example in pbar:
                example_size = len(example["c"].encode('utf-8')) + sum([
                    len(asm.encode('utf-8')) for asm in example["asm"].values()])
                
                # Stop yielding examples if the budget is exceeded
                if example_size > max_exebench_budget:
                    break
            
                # Update the budget and yield the example
                max_exebench_budget -= example_size
                pbar.update(example_size)

                example["dataset"] = "exebench"
                yield example
    else:
        print("Skipping examples from ExeBench as specified budget size is 0...")

    # Load The Stack's examples until the size budget is spent
    if max_stack_budget > 0:
        print("Streaming C and ASM examples from The Stack's train split, from HuggingFace")
        with tqdm(
            stack_examples(stack_token),
            desc="Streaming examples from The Stack",
            total=max_stack_budget, unit='B', unit_scale=True, unit_divisor=1024, file=stdout
        ) as pbar:
            for example in pbar:
                example_size = len(example["c"].encode('utf-8')) + sum([
                    len(asm.encode('utf-8')) for asm in example["asm"].values()])
                
                # Stop yielding examples if the budget is exceeded
                if example_size > max_stack_budget:
                    break
            
                # Update the budget and yield the example
                max_stack_budget -= example_size
                pbar.update(example_size)

                example["dataset"] = "the-stack"
                yield example
    else:
        print("Skipping examples from The Stack as specified budget size is 0...")

def gen_examples(output_dir: str, exebench_dir: str, stack_token_file: str, max_exebench_size: Number, max_stack_size: Number, unit: str):
    """Generates C and x86 assembly files as examples from both the ExeBench's and The Stack's datasets, alongisde a mapping between each file type
    ### Arguments:
        output_dir (str): Directory to output dataset contents into
        exebench_dir (str): Directory to read ExeBench's split files from
        stack_token_file (str): File to read The Stack's access token from
        max_exebench_size (Number): Greatest size (in units of choice) to allow for the processed examples generated from ExeBench
        max_stack_size (Number): Greatest size (in units of choice) to allow for the processed examples generated from The Stack
        unit (str): Unit of choice (KB|MB|GB) to use for measuring maximum allowed size (and progress)
    """
    # Keep track of conversion factors for each unit to bytes
    unit_conversion = {"KB": 2**10, "MB": 2**20, "GB": 2**30}

    # Check valid parameters
    # Paths
    assert isinstance(output_dir, str), "Dataset output directory path should be a string"
    output_dir = path.expanduser(output_dir)

    assert isinstance(exebench_dir, str), "ExeBench's splits data directory path should be a string"
    exebench_dir = path.expanduser(exebench_dir)
    assert path.isdir(exebench_dir), "Invalid Exebench's splits data directory path"
    
    assert isinstance(stack_token_file, str), "The Stack's access token file path should be a string"
    stack_token_file = path.expanduser(stack_token_file)
    assert path.isfile(stack_token_file), "Invalid Stack access token file path"
    
    # Sizes
    assert isinstance(max_exebench_size, Number) and max_exebench_size >= 0, "Maximum size for ExeBench should be a non-negative number"
    assert isinstance(max_stack_size, Number) and max_stack_size >= 0, "Maximum size for The Stack should be a non-negative number"
    assert max_stack_size > 0 or max_exebench_size > 0, "Net size for dataset output should be a greater than zero"
    assert unit in unit_conversion, "Size unit should be GB, MB or KB"

    # Read the access token for The Stack
    try:
        with open(stack_token_file, "r", encoding="utf-8") as f:
            stack_token = f.readline() 
    except Exception as err:
        print("Unable to open or read file with The Stack's token:", err, file=stderr)
        raise Exception("Invalid access token file")

    # Create the output directory if not already present
    c_dir = path.join(output_dir, "c")
    asm_dir = path.join(output_dir, "asm")
    try:
        makedirs(output_dir, exist_ok=True)
        makedirs(c_dir, exist_ok=True)
        makedirs(asm_dir, exist_ok=True)
    except Exception as err:
        print("Unable to open or create output directory:", err, file=stderr)
        raise Exception("Invalid directory")

    # Create the mapping
    stats = pd.DataFrame(
        data = {
            'C filename': pd.array(data=[], dtype=pd.StringDtype()), 
            'x86 filename': pd.array(data=[], dtype=pd.StringDtype()),
            "Optimization level": pd.Categorical(values=[], 
                categories=["O0", "Os", "O3", "Ofast"], ordered=True),
            "Dataset": pd.Categorical(values=[], 
                categories=["exebench", "the-stack"], ordered=True)
        }
    )
    stats.index.name = "Index"

    # Stream the examples and write them to files
    print("Streaming and writing examples to disk")
    with tqdm(load_examples(exebench_dir, stack_token,
        max_exebench_budget = max_exebench_size * unit_conversion[unit],
        max_stack_budget = max_stack_size * unit_conversion[unit]),
        unit=" examples", desc="Generating examples", file=stdout
    ) as pbar:
        # Load streams of the dataset splits, pull as required
        next_entry_row = 0
        for i, sample in enumerate(pbar):
            # Collect the content from the C source code
            c_filename = f"{i}.c"
            c_code = sample["c"]

            # Construct the C source code file
            c_filepath = path.join(c_dir, c_filename)

            # Write its contents
            # If any meaningful error occurs, recover and continue processing the remaining files
            write_success = False
            try:
                with open(c_filepath, "w", encoding="utf-8") as f:
                    try:
                        f.write(c_code)
                        write_success = True
                    except (IOError, OSError) as err:
                        print(f"Error writing C file contents on #{i+1} ({c_filename}):", err, file=stderr)
            except (FileNotFoundError, PermissionError, OSError) as err:
                print(f"Error opening file #{i+1}:", err, file=stderr)

            # If the C file writing failed, abort all following writing attempts for assemblies
            if not write_success:
                print(f"Skipping writing assembly files for #{i+1}:", file=stderr)
                continue

            # Construct the x86 assembly files from all optimization levels
            # Keep track of writing success from each file
            write_success = False
            for (opt_level, asm_code) in sample["asm"].items():
                asm_filename = f"{i}_{opt_level}.s"
                asm_filepath = path.join(asm_dir, asm_filename)

                # Write its contents
                # If any meaningful error occurs, recover and continue processing the remaining files
                try:
                    with open(asm_filepath, "w", encoding="utf-8") as f:
                        try:
                            f.write(asm_code)
                            write_success = True

                            # Update the mapping
                            stats.loc[next_entry_row, "C filename"] = c_filename
                            stats.loc[next_entry_row, "x86 filename"] = asm_filename
                            stats.loc[next_entry_row, "Optimization level"] = opt_level
                            stats.loc[next_entry_row, "Dataset"] = sample["dataset"]

                            # Advance the row cursor
                            next_entry_row += 1
                        
                        except (IOError, OSError) as err:
                            print(f"Error writing file contents on #{i+1} ({asm_filename}):", err, file=stderr)
                
                except (FileNotFoundError, PermissionError, OSError) as err:
                    print(f"Error opening file contents on #{i+1} ({asm_filename}):", err, file=stderr)

            # If no assembly file was succesfully written, attempt to delete the C file and skip this
            # entry
            if not write_success:
                print(f"No assembly was succesfully written for #{i+1} ({c_filename}):", file=stderr)
                print(f"Attempting to remove C source file for ({c_filename}):", file=stderr)
                try:
                    if path.exists(c_filepath):
                        remove(c_filepath)
                except Exception as err:
                    print(f"Error removing file contents on #{i+1} ({c_filename}):", err, file=stderr)
                continue

    # Report findings
    print("Statistics:")
    print(stats.describe(include="all"))

    # Save mapping to file
    mappings_filename = "mappings.csv"
    mappings_filepath = path.join(output_dir, mappings_filename)

    print(f"Saving mappings table to {mappings_filepath}...")
    try:
        stats.to_csv(path_or_buf=mappings_filepath, mode="w")
    except Exception as err:
        print(f"Unable to save mappings: {err}")

    print("Mappings saved!")
    return
