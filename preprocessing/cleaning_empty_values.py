import zstandard as zstd
import json
import os

def extract_func_def_and_asm(filepath, all_data, asm_key="real_gcc_x86_O0"):
    """
    Extracts function definitions and assembly code pairs from a .jsonl.zst file
    and adds them to a provided data dictionary.

    Args:
        filepath (str): Path to the .jsonl.zst file.
        all_data (dict): Dictionary to store extracted data.
        asm_key (str, optional): The key for the desired assembly code.
            Defaults to "real_gcc_x86_O0".
    
    Returns:
        int: Number of pairs extracted from this file.
    """
    file_count = 0
    source_file = os.path.basename(filepath)
    print(f"Extracting function definitions and {asm_key} assembly from {source_file}...")

    try:
        with open(filepath, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(f)
            text_stream = stream_reader.read().decode('utf-8')
            lines = text_stream.strip().split('\n')

            for i, line in enumerate(lines):
                try:
                    obj = json.loads(line)
                    if "text" in obj and "func_def" in obj["text"] and "asm" in obj["text"]:
                        func_def = obj["text"]["func_def"]
                        if asm_key in obj["text"]["asm"]:
                            asm_code = obj["text"]["asm"][asm_key]["func_asm"]
                            # Include source file and line information to make entries unique
                            entry_id = f"{source_file}_{i}"
                            all_data[entry_id] = {
                                "source_file": source_file,
                                "func_def": func_def, 
                                "asm": asm_code,
                                "asm_variant": asm_key
                            }
                            file_count += 1
                        else:
                            print(f"Warning: Assembly key '{asm_key}' not found in entry. Skipping.")
                except json.JSONDecodeError:
                    print("Warning: Could not decode JSON from line. Skipping.")
                except KeyError as e:
                    print(f"Warning: Key error: {e}. Skipping entry.")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}. Skipping entry.")
        
        return file_count

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

def save_data(all_data, output_dir, output_format="json"):
    """
    Saves all extracted data to a single file in the specified format.
    
    Args:
        all_data (dict): Dictionary containing all extracted data.
        output_dir (str): Directory where output file will be stored.
        output_format (str, optional): The format of the output file.
            Either "json" or "txt". Defaults to "json".
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Number of pairs
    pair_count = len(all_data)
    
    if pair_count == 0:
        print("No data to save.")
        return
    
    if output_format == "json":
        output_filename = os.path.join(output_dir, "all_func_def_asm_pairs.json")
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            json.dump(all_data, outfile, indent=2)
        print(f"Saved {pair_count} pairs to {output_filename} in JSON format.")
    
    elif output_format == "txt":
        output_filename = os.path.join(output_dir, "all_func_def_asm_pairs.txt")
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for entry_id, data in all_data.items():
                outfile.write(f"Entry ID: {entry_id}\n")
                outfile.write(f"Source File: {data['source_file']}\n")
                outfile.write(f"Assembly Variant: {data['asm_variant']}\n")
                outfile.write(f"Function Definition:\n{data['func_def']}\n\n")
                outfile.write(f"Assembly Code:\n{data['asm']}\n\n")
                outfile.write("-" * 80 + "\n\n")
        print(f"Saved {pair_count} pairs to {output_filename} in text format.")
    
    else:
        print(f"Error: Invalid output format '{output_format}'. No file saved.")

if __name__ == "__main__":
    input_folder = 'data/train_real_simple_io/'
    output_folder = 'data/train_real_simple_io_cleaned/'
    
    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    filepaths = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.jsonl.zst')]

    if not filepaths:
        print(f"Error: No .jsonl.zst files found in the folder {input_folder}")
    else:
        # Dictionary to store all extracted data
        all_data = {}
        total_count = 0
        
        # Assembly variants to extract
        asm_variants = ["real_gcc_x86_O0"]
        # You can uncomment the following line to extract additional variants:
        # asm_variants.extend(["real_gcc_x86_Os", "real_gcc_arm_O3"])
        
        # Process all files and collect data
        for filepath in filepaths:
            for asm_key in asm_variants:
                file_count = extract_func_def_and_asm(filepath, all_data, asm_key=asm_key)
                total_count += file_count
                print(f"Extracted {file_count} pairs from {os.path.basename(filepath)} for {asm_key}.")
        
        print(f"\nTotal extracted pairs: {total_count}")
        
        # Save all collected data to single files
        save_data(all_data, output_folder, output_format="json")
        save_data(all_data, output_folder, output_format="txt")