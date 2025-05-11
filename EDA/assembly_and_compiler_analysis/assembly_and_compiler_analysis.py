import zstandard as zstd
import json
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter, defaultdict
import pandas as pd
import seaborn as sns

# Get the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def extract_assembly_info(filepath):
    """Reads a .jsonl.zst file and extracts assembly information."""
    entries = []
    
    try:
        with open(filepath, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(f)
            text_stream = stream_reader.read().decode('utf-8')
            lines = text_stream.strip().split('\n')
            
            for line in lines:
                try:
                    entry = json.loads(line)
                    if "text" in entry and "asm" in entry["text"]:
                        asm_data = entry["text"]["asm"]
                        entries.append(asm_data)
                except json.JSONDecodeError:
                    continue
                except Exception as e:
                    print(f"Error processing line: {e}")
    except Exception as e:
        print(f"Error processing file {filepath}: {e}")
        
    return entries

def process_single_entry(entry_text):
    """Process a single JSON entry from text."""
    try:
        entry = json.loads(entry_text)
        if "text" in entry and "asm" in entry["text"]:
            return entry["text"]["asm"]
        return None
    except:
        return None

def extract_compiler_configs(asm_entries):
    """Extract compiler configurations from assembly entries."""
    compiler_configs = []
    
    for entry in asm_entries:
        configs = {}
        for key, value in entry.items():
            # Only process non-empty dictionary values
            if isinstance(value, dict) and "target" in value:
                target = value["target"]
                configs[key] = {
                    "impl": target.get("impl", ""),
                    "bits": target.get("bits", ""),
                    "lang": target.get("lang", ""),
                    "o": target.get("o", "")
                }
        
        compiler_configs.append(configs)
    
    return compiler_configs

def analyze_single_entry(entry_json):
    """Analyze a single entry from JSON."""
    if "text" in entry_json and "asm" in entry_json["text"]:
        asm_data = entry_json["text"]["asm"]
        configs = {}
        
        for key, value in asm_data.items():
            if isinstance(value, dict) and "target" in value:
                target = value["target"]
                configs[key] = {
                    "impl": target.get("impl", ""),
                    "bits": target.get("bits", ""),
                    "lang": target.get("lang", ""),
                    "o": target.get("o", "")
                }
        
        return configs
    return None

def count_compiler_configurations(configs):
    """Count the occurrences of each compiler configuration."""
    compiler_counts = Counter()
    arch_counts = Counter()
    opt_level_counts = Counter()
    
    for config_dict in configs:
        for key, config in config_dict.items():
            compiler_counts[config["impl"]] += 1
            arch_counts[f"{config['bits']}bit"] += 1
            opt_level_counts[f"O{config['o']}"] += 1
    
    return compiler_counts, arch_counts, opt_level_counts

def analyze_asm_size(asm_entries):
    """Analyze assembly code size (number of instructions)."""
    sizes = defaultdict(list)
    
    for entry in asm_entries:
        for key, value in entry.items():
            if isinstance(value, dict) and "func_asm" in value:
                # Count lines of assembly code
                line_count = len(value["func_asm"].strip().split('\n'))
                # Extract optimization level from key name
                if "O0" in key:
                    sizes["O0"].append(line_count)
                elif "O3" in key:
                    sizes["O3"].append(line_count)
                elif "Os" in key:
                    sizes["Os"].append(line_count)
    
    return sizes

def count_unique_configuration_patterns(configs):
    """Count unique patterns of compiler configurations in entries."""
    patterns = []
    
    for config_dict in configs:
        # Create a pattern string for this entry
        pattern = []
        keys = sorted(config_dict.keys())
        for key in keys:
            config = config_dict[key]
            pattern.append(f"{config['impl']}-{config['bits']}-{config['o']}")
        
        patterns.append(tuple(pattern))
    
    pattern_counts = Counter(patterns)
    return pattern_counts

def check_consistency(configs):
    """Check if all entries have the same compiler configurations."""
    if not configs:
        return True, "No configurations found"
    
    first_keys = set(configs[0].keys())
    for i, config in enumerate(configs[1:], 1):
        if set(config.keys()) != first_keys:
            return False, f"Entry {i} has different key set: {set(config.keys())} vs {first_keys}"
    
    # Check if all entries have the same configurations for each key
    for key in first_keys:
        first_config = configs[0][key]
        for i, config in enumerate(configs[1:], 1):
            if config[key] != first_config:
                return False, f"Entry {i}, key {key}: {config[key]} differs from {first_config}"
    
    return True, "All configurations are consistent"

def create_compiler_dataframe(configs):
    """Create a DataFrame for more detailed analysis."""
    data = []
    
    for i, config_dict in enumerate(configs):
        for key, config in config_dict.items():
            data.append({
                "entry_id": i,
                "config_name": key,
                "compiler": config["impl"],
                "arch_bits": config["bits"],
                "language": config["lang"],
                "opt_level": config["o"]
            })
    
    return pd.DataFrame(data)

def plot_compiler_statistics(compiler_counts, arch_counts, opt_level_counts):
    """Plot statistics about compiler usage."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Plot compiler implementations
    labels = list(compiler_counts.keys())
    values = list(compiler_counts.values())
    ax1.bar(labels, values)
    ax1.set_title('Compiler Implementations')
    ax1.set_ylabel('Count')
    
    # Plot architecture bits
    labels = list(arch_counts.keys())
    values = list(arch_counts.values())
    ax2.bar(labels, values)
    ax2.set_title('Architecture Bits')
    ax2.set_ylabel('Count')
    
    # Plot optimization levels
    labels = list(opt_level_counts.keys())
    values = list(opt_level_counts.values())
    ax3.bar(labels, values)
    ax3.set_title('Optimization Levels')
    ax3.set_ylabel('Count')
    
    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'compiler_statistics.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_asm_size_boxplot(sizes):
    """Plot a boxplot of assembly code sizes by optimization level."""
    plt.figure(figsize=(10, 6))
    
    data = []
    labels = []
    
    for opt_level, size_list in sizes.items():
        data.append(size_list)
        labels.append(opt_level)
    
    plt.boxplot(data, labels=labels)
    plt.title('Assembly Code Size by Optimization Level')
    plt.ylabel('Number of Assembly Lines')
    plt.xlabel('Optimization Level')
    plt.grid(True, axis='y', alpha=0.3)
    
    output_path = os.path.join(SCRIPT_DIR, 'asm_size_boxplot.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_optimization_effect(df):
    """Plot the effect of optimization on assembly size."""
    if df.empty:
        return None
    
    plt.figure(figsize=(12, 6))
    
    # Filter for entries with optimization level data
    opt_df = df[df['opt_level'].isin(['0', '3', 's'])]
    
    # Map optimization levels to their names
    opt_map = {'0': 'O0', '3': 'O3', 's': 'Os'}
    opt_df['opt_name'] = opt_df['opt_level'].map(opt_map)
    
    # Plot by compiler and optimization level
    sns.barplot(x='compiler', y='asm_size', hue='opt_name', data=opt_df)
    
    plt.title('Effect of Optimization Level on Assembly Size by Compiler')
    plt.ylabel('Average Assembly Size (lines)')
    plt.xlabel('Compiler')
    
    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'optimization_effect.png')
    plt.savefig(output_path)
    plt.close()
    
    return output_path

def plot_pattern_distribution(pattern_counts):
    """Plot the distribution of configuration patterns."""
    if not pattern_counts:
        return None
    
    # Get the top N patterns
    top_n = 10
    top_patterns = pattern_counts.most_common(top_n)
    
    labels = [f"Pattern {i+1}" for i in range(len(top_patterns))]
    values = [count for _, count in top_patterns]
    
    plt.figure(figsize=(12, 6))
    plt.bar(labels, values)
    plt.title(f'Top {top_n} Configuration Patterns')
    plt.ylabel('Count')
    plt.xlabel('Pattern')
    
    plt.tight_layout()
    output_path = os.path.join(SCRIPT_DIR, 'pattern_distribution.png')
    plt.savefig(output_path)
    plt.close()
    
    # Create a legend explaining the patterns
    legend_path = os.path.join(SCRIPT_DIR, 'pattern_legend.txt')
    with open(legend_path, 'w') as f:
        for i, (pattern, count) in enumerate(top_patterns):
            f.write(f"Pattern {i+1}: {pattern} (Count: {count})\n")
    
    return output_path

def parse_asm_size(asm_entries):
    """Parse assembly size information for each entry."""
    sizes_by_config = defaultdict(list)
    
    for entry in asm_entries:
        for key, value in entry.items():
            if isinstance(value, dict) and "func_asm" in value:
                # Count lines of assembly code
                line_count = len(value["func_asm"].strip().split('\n'))
                sizes_by_config[key].append(line_count)
    
    return sizes_by_config

def analyze_asm_instructions(asm_entries):
    """Analyze common assembly instructions used."""
    instruction_counts = Counter()
    
    for entry in asm_entries:
        for key, value in entry.items():
            if isinstance(value, dict) and "func_asm" in value:
                # Extract assembly instructions from each line
                asm_lines = value["func_asm"].strip().split('\n')
                for line in asm_lines:
                    # Simple extraction of the instruction
                    parts = line.strip().split()
                    if len(parts) > 1 and parts[0].endswith(':'):
                        # Skip labels
                        continue
                    if parts and not parts[0].startswith('.'):
                        # Count the instruction
                        instruction_counts[parts[0]] += 1
    
    return instruction_counts

def analyze_optimization_efficiency(asm_entries):
    """Analyze the efficiency of different optimization levels."""
    size_reduction = []
    
    for entry in asm_entries:
        # Find pairs of O0 and O3 configurations for the same architecture
        o0_size = None
        o3_size = None
        
        for key, value in entry.items():
            if isinstance(value, dict) and "func_asm" in value:
                if "O0" in key:
                    o0_size = len(value["func_asm"].strip().split('\n'))
                elif "O3" in key:
                    o3_size = len(value["func_asm"].strip().split('\n'))
        
        if o0_size is not None and o3_size is not None:
            # Calculate size reduction percentage
            reduction = ((o0_size - o3_size) / o0_size) * 100 if o0_size > 0 else 0
            size_reduction.append(reduction)
    
    return size_reduction

def run_analysis(sample_entry=None, folder_path=None):
    """Run the complete analysis."""
    results = {}
    
    # Process sample entry if provided
    if sample_entry:
        asm_data = process_single_entry(sample_entry)
        if asm_data:
            config = extract_compiler_configs([asm_data])
            results["sample_analysis"] = {
                "configs": config[0] if config else None
            }
    
    # Process all files in the folder
    if folder_path:
        filepaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                    if f.endswith('.jsonl.zst')]
        
        if not filepaths:
            results["error"] = f"No .jsonl.zst files found in the folder {folder_path}"
            return results
        
        all_asm_entries = []
        for filepath in filepaths:
            if os.path.exists(filepath):
                asm_entries = extract_assembly_info(filepath)
                all_asm_entries.extend(asm_entries)
            else:
                print(f"Error: File not found at {filepath}")
        
        if not all_asm_entries:
            results["error"] = "No assembly information found in the files."
            return results
        
        # Extract compiler configurations
        all_configs = extract_compiler_configs(all_asm_entries)
        
        # Check consistency
        is_consistent, consistency_message = check_consistency(all_configs)
        
        # Count compiler configurations
        compiler_counts, arch_counts, opt_level_counts = count_compiler_configurations(all_configs)
        
        # Analyze assembly size
        asm_sizes = analyze_asm_size(all_asm_entries)
        
        # Count unique configuration patterns
        pattern_counts = count_unique_configuration_patterns(all_configs)
        
        # Analyze assembly instructions
        instruction_counts = analyze_asm_instructions(all_asm_entries)
        
        # Analyze optimization efficiency
        size_reduction = analyze_optimization_efficiency(all_asm_entries)
        
        # Create dataframe for more analysis
        df = create_compiler_dataframe(all_configs)
        
        # Store results
        results["bulk_analysis"] = {
            "total_entries": len(all_asm_entries),
            "consistency": {
                "is_consistent": is_consistent,
                "message": consistency_message
            },
            "compiler_counts": dict(compiler_counts),
            "arch_counts": dict(arch_counts),
            "opt_level_counts": dict(opt_level_counts),
            "pattern_counts": dict(pattern_counts.most_common(10)),
            "asm_sizes": {k: {
                "mean": np.mean(v),
                "median": np.median(v),
                "min": min(v),
                "max": max(v)
            } for k, v in asm_sizes.items() if v},
            "top_instructions": dict(instruction_counts.most_common(20)),
            "optimization_efficiency": {
                "mean_reduction": np.mean(size_reduction) if size_reduction else None,
                "median_reduction": np.median(size_reduction) if size_reduction else None
            }
        }
        
        # Generate plots
        results["plots"] = {}
        
        # Plot compiler statistics
        results["plots"]["compiler_stats"] = plot_compiler_statistics(
            compiler_counts, arch_counts, opt_level_counts)
        
        # Plot assembly size boxplot
        results["plots"]["asm_size"] = plot_asm_size_boxplot(asm_sizes)
        
        # Plot pattern distribution
        results["plots"]["pattern_dist"] = plot_pattern_distribution(pattern_counts)
    
    return results

def analyze_from_json(json_text):
    """Analyze assembly and compiler information from JSON text."""
    try:
        entry = json.loads(json_text)
        configs = analyze_single_entry(entry)
        
        if configs:
            print("\nCompiler Configurations:")
            for key, config in configs.items():
                print(f"  {key}:")
                print(f"    Compiler: {config['impl']}")
                print(f"    Architecture: {config['bits']} bit")
                print(f"    Assembly Language: {config['lang']}")
                print(f"    Optimization Level: O{config['o']}")
            
            return configs
        else:
            print("No valid assembly information found in the provided JSON.")
            return None
    except json.JSONDecodeError:
        print("Invalid JSON format. Please check the input.")
        return None
    except Exception as e:
        print(f"Error analyzing JSON: {e}")
        return None
    

# Main script execution
if __name__ == "__main__":
    # Example usage
    # Automatically process all files in the specified folder
    folder_path = 'data/train_real_simple_io/'
    results = run_analysis(folder_path=folder_path)
    print(f"Analysis complete. Found {results.get('bulk_analysis', {}).get('total_entries', 0)} entries.")