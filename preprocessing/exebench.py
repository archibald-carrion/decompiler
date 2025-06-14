import sys # Printing, mostly
import json # Dataset fomatting
from pathlib import Path # File globbing
import zstandard as zstd # Decompression

def fix_example(example):
    """Generates C and x86 assembly files (in memory, as a dict) from an example in ExeBench's dataset
    ### Arguments:
        example (dict): Example collected from ExeBench's JSON \'text\' field
    ### Returns:
    A reformatted example dict, in the form \{ "c": \<c code\>, "asm"\: \{ \<optimization level\> \: \<x86 assembly code\> \} \}
    """
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

    # Flatten assemblies into features for each level of optimization
    example["asm"] = {target["opt"] : target["code"] for target in example["asm"]}

    # Remove troublesome/unecessary features
    unecessary_keys = filter(lambda x: x not in ["asm", "c"], example.keys())
    for key in list(unecessary_keys):
            del example[key]

    # All is done
    return example

def load_examples(split_directory: str):
    """Generates C and x86 assembly files (in memory, as dicts) as examples from ExeBench's dataset
    ### Arguments:
        split_directory (str): Directory to read ExeBench's split files from
    ### Returns:
    One yielded example at a time, in the form \{ "c": \<c code\>, "asm"\: \{ \<optimization level\> \: \<x86 assembly code\> \} \}
    
    Examples missing valid x86 code in all optimization level (e.g: the "asm" dict is empty) are omitted
    """
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
                        example = fix_example(data)

                        # Skip example if no target assemblies were found
                        if (len(example["asm"]) < 1):
                            continue

                        # Yield the fixed example
                        yield example

                    except Exception as err:
                        print(f"Unable to process example on split file {split_file}: {err}", file=sys.stderr)
                        print("Skipping example...", file=sys.stderr)

        except Exception as err:
            print(f"Unable to process split collection on file {split_file}: {err}", file=sys.stderr)
            print("Skipping split file...", file=sys.stderr)
