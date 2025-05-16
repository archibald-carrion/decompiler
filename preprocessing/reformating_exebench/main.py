"""
This file's main purpose is to extract C functions and their assembly versions from a .jsonl.zst file,
and add them to a structured directory format for further analysis.
"""

import os
import csv
import json
import zstandard as zstd
import shutil
import hashlib
from collections import defaultdict

def extract_and_restructure(filepath, output_dir):
    """
    Extract files from .jsonl.zst and restructure according to specified format:
    - c/ directory for C source files
    - x86/ directory for assembly files
    - mappings.csv to track relationships between C and assembly files
    """
    # Create directory structure
    c_dir = os.path.join(output_dir, "c")
    x86_dir = os.path.join(output_dir, "x86")
    
    os.makedirs(c_dir, exist_ok=True)
    os.makedirs(x86_dir, exist_ok=True)
    
    # Initialize mappings data
    mappings = []
    
    # Extract data from zst file
    entries = extract_assembly_info(filepath)
    
    for i, entry in enumerate(entries):
        # Extract the function name if available
        func_name = None
        if isinstance(entry, dict) and "text" in entry:
            text_data = entry["text"]
            if "fname" in text_data:
                func_name = text_data["fname"]
            elif "func_def" in text_data:
                # Try to extract function name from definition
                func_def = text_data["func_def"]
                # Simple heuristic: look for first open parenthesis and get the word before it
                parts = func_def.split('(')[0].strip().split()
                if parts:
                    func_name = parts[-1]
        
        if not func_name:
            func_name = f"func_{i:06d}"
        
        # Create a unique identifier based on function name and a hash of the function definition
        func_def = entry.get("text", {}).get("func_def", "")
        hash_object = hashlib.md5(func_def.encode())
        hash_suffix = hash_object.hexdigest()[:6]  # Use first 6 chars of hash
        identifier = f"{func_name}_{hash_suffix}"
        
        # Process C source code
        source_code = entry.get("text", {}).get("func_def", "")
        
        # Process assembly versions
        asm_files = {}
        asm_entry = entry.get("text", {}).get("asm", {})
        if isinstance(asm_entry, dict):
            for config_name, config_data in asm_entry.items():
                if isinstance(config_data, dict) and "func_asm" in config_data and "target" in config_data:
                    # Extract architecture and optimization info
                    target = config_data["target"]
                    arch = "x86"
                    opt_level = target.get("o", "unknown")
                    
                    # Create a unique suffix for this assembly version
                    arch_suffix = f"{arch}"
                    opt_suffix = f"o{opt_level}" if opt_level != "s" else "os"
                    
                    # Key format: "arch_opt"
                    key = f"{arch_suffix}_{opt_suffix}"
                    asm_files[key] = {
                    "code": config_data["func_asm"],
                    "arch": arch,
                    "opt": opt_suffix
                    }
        # If we have source code and at least one assembly file, save them
        if source_code and asm_files:
            # Save the C source file
            c_filename = f"{identifier}.c"
            c_filepath = os.path.join(c_dir, c_filename)
            with open(c_filepath, 'w') as f:
                f.write(source_code)
            
            # Save each assembly file with appropriate suffix
            for key, asm_info in asm_files.items():
                asm_code = asm_info["code"]
                arch = asm_info["arch"]
                opt = asm_info["opt"]
                
                # Choose the appropriate directory based on architecture
                asm_dir = x86_dir

                asm_filename = f"{identifier}_{opt}.asm"
                asm_filepath = os.path.join(asm_dir, asm_filename)
                with open(asm_filepath, 'w') as f:
                    f.write(asm_code)

                # Add mapping entry
                mappings.append({
                    "c_file": c_filename,
                    "c_path": f"c/{c_filename}",
                    "asm_file": asm_filename,
                    "asm_path": f"{arch}/{asm_filename}",
                    "arch": arch,
                    "optimization": opt
                })
    
    # Write mappings to CSV
    mappings_filepath = os.path.join(output_dir, "mappings.csv")
    with open(mappings_filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        # Write header
        writer.writerow(["c_file", "c_path", "asm_file", "asm_path", "arch", "optimization"])
        # Write data
        for mapping in mappings:
            writer.writerow([
                mapping["c_file"], 
                mapping["c_path"], 
                mapping["asm_file"], 
                mapping["asm_path"],
                mapping["arch"],
                mapping["optimization"]
            ])
    
    return {
        "total_entries": len(entries),
        "total_c_files": len({m["c_file"] for m in mappings}),
        "total_asm_files": len(mappings),
        "mappings_path": mappings_filepath
    }

def extract_assembly_info(filepath):
    """Reads a .jsonl.zst file and extracts the full entries containing assembly information."""
    entries = []
    
    try:
        with open(filepath, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(f)
            text_stream = stream_reader.read().decode('utf-8')
            
            # Handle both newline-delimited entries and entries separated by markers
            if "--- Entry" in text_stream:
                # Format with entry markers
                parts = text_stream.split("--- Entry")
                for part in parts:
                    if part.strip():
                        try:
                            # Find the JSON part within the entry
                            json_start = part.find('{')
                            if json_start != -1:
                                json_text = part[json_start:].strip()
                                entry = json.loads(json_text)
                                if "text" in entry and "asm" in entry["text"]:
                                    entries.append(entry)
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error processing entry: {e}")
            else:
                # Regular JSONL format
                lines = text_stream.strip().split('\n')
                for line in lines:
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            if "text" in entry and "asm" in entry["text"]:
                                entries.append(entry)
                        except json.JSONDecodeError:
                            continue
                        except Exception as e:
                            print(f"Error processing line: {e}")
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        
    return entries

def build_analysis_dataframe(output_dir):
    """
    Build a pandas DataFrame from the mappings.csv file for analysis.
    """
    import pandas as pd
    
    mappings_filepath = os.path.join(output_dir, "mappings.csv")
    if not os.path.exists(mappings_filepath):
        raise FileNotFoundError(f"Mappings file not found at {mappings_filepath}")
    
    df = pd.read_csv(mappings_filepath)
    return df

if __name__ == "__main__":
    # Example usage
    input_filepath = "data/train_real_simple_io/data_0_time1677794311_default.jsonl.zst"
    output_directory = "data/structured_output"
    
    # Clear output directory if it exists
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    
    results = extract_and_restructure(input_filepath, output_directory)
    print(f"Processed {results['total_entries']} entries.")
    print(f"Created {results['total_c_files']} C files and {results['total_asm_files']} assembly files.")
    print(f"Mappings saved to: {results['mappings_path']}")
    
    # Analyze the results
    try:
        df = build_analysis_dataframe(output_directory)
        print(f"Created DataFrame with {len(df)} rows.")
        # Print distribution of optimization levels
        print("Optimization level distribution:")
        print(df['optimization'].value_counts())
        
        # Print distribution of architectures
        print("Architecture distribution:")
        print(df['arch'].value_counts())
    except Exception as e:
        print(f"Error analyzing results: {e}")