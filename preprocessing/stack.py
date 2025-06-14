import sys # Printing, mostly
import re # Pattern matching to filter out useless assemblies
import os # Manipulating files and paths
from subprocess import run as invoke # Invoking GCC
from tempfile import NamedTemporaryFile # Temporary files to write assemblies to
from datasets import load_dataset # HuggingFace downloading API
from huggingface_hub import login # HuggingFace auth API

def load_examples(token: str):
    """Generates C and x86 assembly files (in memory, as dicts) as examples from The Stack's dataset
    ### Arguments:
        token (str): The Stack's access token for reading its contents
    ### Returns:
    One yielded example at a time, in the form \{ "c": \<c code\>, "asm"\: \{ \<optimization level\> \: \<x86 assembly code\> \} \}
    
    Examples missing valid x86 code in all optimization level (e.g: the "asm" dict is empty) or missing any local scope symbolic labels (e.g: missing ".\<label name here\>\:") are omitted
    """

    # Log in to access gated dataset
    print("Logging in to access gated dataset...")
    try:
        login(token)
    except Exception as err:
        print(f"Unable to login to HuggingFace: {err}", file=sys.stderr)
        print("Skipping dataset...", file=sys.stderr)
        return

    # Load a stream of the dataset, pull as required
    print("Loading The Stack dataset...")
    try:
        ds = load_dataset("bigcode/the-stack", data_dir="data/c", split="train", streaming=True)
    except Exception as err:
        print(f"Unable to load The Stack's C files on 'train' split: {err}", file=sys.stderr)
        print("Skipping dataset...", file=sys.stderr)
        return

    # For every file in the C collection, generate assemblies for every level of optimization, to 
    # pair up as examples
    for i, sample in enumerate(ds):
        c_code: str = sample["content"]
        example = {"c": c_code }

        # Generate assemblies for every level of optimization
        opt_levels = ["O0", "Os", "O3"] # TODO: Okay to omit "Ofast"?
        example["asm"] = {}
        for opt in opt_levels:
            try:
                # Crete a temporary file to store the results on
                asm_file = NamedTemporaryFile(suffix=".s", mode='w+b', buffering=0, delete=False)
                asm_file.close() # Close the file first so that GCC may write on it, see https://github.com/python/cpython/issues/88221
                
                # Run GCC on the c code input, and check its results on the output file
                result = invoke(
                    ["gcc", "-march=x86-64", "-xc", "-S", "-o", asm_file.name, "-Wfatal-errors", "-pass-exit-codes", "-"],
                    capture_output=True, text=True,
                    input=c_code
                )

                # Add the result onto the assemblies if succesfull
                if result.returncode == 0:
                    # Read contents on temporary output file written by GCC
                    with open(file=asm_file.name, mode='r+b') as output:
                        asm_code = output.read().decode()

                        # If the generated x86 assembly code contains at least one local scope symbolic
                        # label, then include it on the example
                        if re.search(r"^\.[_\.A-Za-z0-9]+:", asm_code, re.MULTILINE):
                            example["asm"][opt] = asm_code
                        else:
                            print(f"No local scope symbolic label found on #{i} with level '{opt}'", file=sys.stderr)
                            print("Skipping assembly...", file=sys.stderr)
                    
                    # Remove temporary output file, it is no longer needed 
                    os.remove(asm_file.name)
                else:
                    print(f"GCC error when assembling file #{i} with level '{opt}':\n{result.stderr}", file=sys.stderr)
                    print("Skipping assembly...", file=sys.stderr)
                
                # No need to remove the temporary file on compiltation failure, GCC removes it on such cases
            except Exception as err:
                print(f"Unable to generate assembly on file #{i} with level '{opt}': {err}", file=sys.stderr)
                print("Skipping assembly...", file=sys.stderr)
        
        # Skip example if no target assemblies were found
        if (len(example["asm"]) < 1):
            continue

        # Yield example
        yield example
