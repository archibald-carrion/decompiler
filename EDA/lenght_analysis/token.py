import zstandard as zstd
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def extract_function_definitions(filepath):
    """Reads a .jsonl.zst file and extracts C function definitions."""
    function_definitions = []
    with open(filepath, 'rb') as f:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(f)
        text_stream = stream_reader.read().decode('utf-8')
        lines = text_stream.strip().split('\n')
        for line in lines:
            try:
                obj = json.loads(line)
                if "text" in obj and "func_def" in obj["text"]:
                    func_def = obj["text"]["func_def"]
                    function_definitions.append(func_def)
            except json.JSONDecodeError:
                continue
            except Exception as e:
                print(f"Error processing line: {e}")
    return function_definitions

def analyze_token_count(function_definitions):
    """Analyzes the number of tokens in each function definition."""
    token_counts = []
    
    for func in function_definitions:
        # Simple tokenization for C code
        # This splits on whitespace and also separates operators and punctuation
        tokens = re.findall(r'[a-zA-Z_]\w*|[{}()\[\];,.<>+\-*/&|^!~=?:]|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\d+(?:\.\d+)?', func)
        token_counts.append(len(tokens))
    
    return token_counts

def plot_token_count_histogram(token_counts, title="Distribution of Tokens per Function"):
    """Plots a histogram of the number of tokens with a logarithmic scale."""
    plt.figure(figsize=(10, 6))
    plt.hist(token_counts, bins=50, edgecolor='black', alpha=0.7, log=True)
    plt.title(title)
    plt.xlabel("Number of Tokens")
    plt.ylabel("Frequency (Log Scale)")
    plt.grid(axis='y', alpha=0.5)
    plt.show()

def plot_token_count_boxplot(token_counts, title="Box Plot of Tokens per Function"):
    """Plots a box plot of the number of tokens."""
    plt.figure(figsize=(8, 6))
    plt.boxplot(token_counts, vert=False, showfliers=True)
    plt.title(title)
    plt.xlabel("Number of Tokens")
    plt.grid(axis='x', alpha=0.5)
    plt.show()

def plot_cumulative_distribution(token_counts, title="Cumulative Distribution of Tokens"):
    """Plots the cumulative distribution of the number of tokens with a logarithmic x-axis."""
    sorted_counts = np.sort(token_counts)
    cumulative_probability = np.arange(1, len(sorted_counts) + 1) / len(sorted_counts)
    plt.figure(figsize=(10, 6))
    plt.plot(sorted_counts, cumulative_probability, marker='.', linestyle='-')
    plt.xscale('log')
    plt.title(title)
    plt.xlabel("Number of Tokens (Log Scale)")
    plt.ylabel("Cumulative Probability")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    folder_path = 'data/train_real_simple_io/'
    filepaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jsonl.zst')]
    
    if not filepaths:
        print(f"Error: No .jsonl.zst files found in the folder {folder_path}")
    else:
        all_function_defs = []
        for filepath in filepaths:
            if os.path.exists(filepath):
                function_defs = extract_function_definitions(filepath)
                all_function_defs.extend(function_defs)
            else:
                print(f"Error: File not found at {filepath}")
        
        if all_function_defs:
            token_counts = analyze_token_count(all_function_defs)
            
            print(f"Total number of function definitions found: {len(all_function_defs)}")
            print(f"Summary of token counts:")
            print(f"  Mean: {np.mean(token_counts):.2f}")
            print(f"  Median: {np.median(token_counts):.2f}")
            print(f"  Standard Deviation: {np.std(token_counts):.2f}")
            print(f"  Minimum: {np.min(token_counts)}")
            print(f"  Maximum: {np.max(token_counts)}")
            print(f"  Percentiles (25th, 50th, 75th): {np.percentile(token_counts, [25, 50, 75])}")
            
            plot_token_count_histogram(token_counts)
            plot_token_count_boxplot(token_counts)
            plot_cumulative_distribution(token_counts)
        else:
            print("No function definitions found in the files.")