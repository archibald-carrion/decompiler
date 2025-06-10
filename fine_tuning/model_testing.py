#!/usr/bin/env python3
"""
Assembly Decompiler Model Comparison Script
This script compares the performance of the base DistilGPT2 model vs the fine-tuned 
decompiler model using a separate validation dataset from data_validation folder.
"""

import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import argparse
import time
import json
import glob
from collections import defaultdict
import numpy as np
from datetime import datetime
import statistics

# Set local directory for model storage
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "distilgpt2")
FINETUNED_MODEL_DIR = os.path.join(SCRIPT_DIR, "models", "decompiler_model")
VALIDATION_DATA_DIR = os.path.join(SCRIPT_DIR, "data_validation")
RESULTS_DIR = os.path.join(SCRIPT_DIR, "test_results")

# Create directories if they don't exist
os.makedirs(RESULTS_DIR, exist_ok=True)

def check_requirements():
    """Check if required packages are installed"""
    try:
        import transformers
        print(f"✓ Transformers version: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not installed. Run: pip install transformers")
        return False
    
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        print(f"✓ CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"✓ CUDA device: {torch.cuda.get_device_name()}")
    except ImportError:
        print("❌ PyTorch not installed. Run: pip install torch")
        return False
    
    return True

def load_base_model():
    """Load base DistilGPT2 model and tokenizer"""
    if not os.path.exists(os.path.join(BASE_MODEL_DIR, "config.json")):
        print("❌ Base model not found. Please run the training script first to download it.")
        return None, None, None
    
    print("📥 Loading base DistilGPT2 model...")
    tokenizer = GPT2Tokenizer.from_pretrained(BASE_MODEL_DIR)
    model = GPT2LMHeadModel.from_pretrained(BASE_MODEL_DIR)
    
    # Set pad token
    tokenizer.pad_token = tokenizer.eos_token
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    print(f"✓ Base model loaded on {device}")
    return model, tokenizer, device

def load_finetuned_model():
    """Load the fine-tuned decompiler model"""
    if not os.path.exists(os.path.join(FINETUNED_MODEL_DIR, "config.json")):
        print("❌ Fine-tuned model not found. Please run training first.")
        return None, None, None
    
    print("📥 Loading fine-tuned decompiler model...")
    tokenizer = GPT2Tokenizer.from_pretrained(FINETUNED_MODEL_DIR)
    model = GPT2LMHeadModel.from_pretrained(FINETUNED_MODEL_DIR)
    
    # Move to GPU if available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    model.eval()
    
    print(f"✓ Fine-tuned model loaded on {device}")
    return model, tokenizer, device

def load_validation_data(data_dir=VALIDATION_DATA_DIR, use_all_optimizations=True, specific_optimization=None):
    """Load assembly-C code pairs from validation dataset"""
    print(f"📂 Loading validation data from {data_dir}...")
    
    c_dir = os.path.join(data_dir, "C")
    
    if not os.path.exists(c_dir):
        print(f"❌ Validation C directory not found: {c_dir}")
        return []
    
    all_pairs = []
    
    # Determine which optimization levels to process
    if use_all_optimizations:
        optimization_levels = ["O0", "Ofast", "Osize"]
        print("🔧 Processing ALL validation optimization levels (O0, Ofast, Osize)")
    elif specific_optimization:
        optimization_levels = [specific_optimization]
        print(f"🔧 Processing only {specific_optimization} validation optimization level")
    else:
        optimization_levels = ["O0"]  # Default fallback
        print("🔧 Processing only O0 validation optimization level (default)")
    
    # Get all C files first
    c_files = glob.glob(os.path.join(c_dir, "*.c"))
    print(f"📄 Found {len(c_files)} validation C files")
    
    if not c_files:
        print(f"❌ No validation C files found in {c_dir}")
        return []
    
    # Process each optimization level
    for opt_level in optimization_levels:
        asm_dir = os.path.join(data_dir, "ASM", opt_level)
        
        if not os.path.exists(asm_dir):
            print(f"⚠️  Validation assembly directory not found: {asm_dir}, skipping...")
            continue
        
        print(f"  📁 Processing {opt_level} validation optimization level...")
        pairs_for_this_opt = []
        
        for c_file in c_files:
            # Get base filename without extension
            base_name = os.path.splitext(os.path.basename(c_file))[0]
            
            # Look for corresponding assembly file
            asm_file = os.path.join(asm_dir, f"{base_name}.s")
            
            if os.path.exists(asm_file):
                try:
                    # Read C code
                    with open(c_file, 'r', encoding='utf-8') as f:
                        c_code = f.read().strip()
                    
                    # Read assembly code
                    with open(asm_file, 'r', encoding='utf-8') as f:
                        asm_code = f.read().strip()
                    
                    # Only add if both files have content
                    if c_code and asm_code:
                        pairs_for_this_opt.append({
                            'assembly': asm_code,
                            'c_code': c_code,
                            'filename': base_name,
                            'optimization': opt_level
                        })
                        
                except Exception as e:
                    print(f"    ⚠️  Error reading validation files {base_name}: {e}")
                    continue
            else:
                print(f"    ⚠️  Missing validation assembly file for {base_name} in {opt_level}")
        
        print(f"    ✓ Loaded {len(pairs_for_this_opt)} validation pairs from {opt_level}")
        all_pairs.extend(pairs_for_this_opt)
    
    print(f"✅ Total validation pairs loaded: {len(all_pairs)}")
    
    # Show statistics by optimization level
    if len(all_pairs) > 0:
        from collections import Counter
        opt_counts = Counter(pair['optimization'] for pair in all_pairs)
        print("📊 Validation pairs by optimization level:")
        for opt, count in sorted(opt_counts.items()):
            print(f"    {opt}: {count} pairs")
    
    return all_pairs

def generate_c_code(model, tokenizer, device, assembly_code, max_length=512, temperature=0.7, top_p=0.9):
    """Generate C code from assembly using the model"""
    # Format input with special token (for fine-tuned model) or plain prompt (for base model)
    prompt = f"<|assembly|>\n{assembly_code}\n<|c_code|>\n"
    
    # Encode the prompt
    inputs = tokenizer.encode(prompt, return_tensors='pt', truncation=True, max_length=512).to(device)
    attention_mask = torch.ones_like(inputs)
    
    # Generate C code
    start_time = time.time()
    
    try:
        with torch.no_grad():
            outputs = model.generate(
                inputs,
                attention_mask=attention_mask,
                max_length=len(inputs[0]) + max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
                num_return_sequences=1,
                repetition_penalty=1.1,
                early_stopping=True
            )
        
        generation_time = time.time() - start_time
        
        # Decode the generated text
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the C code part
        if "<|c_code|>" in generated_text:
            c_code = generated_text.split("<|c_code|>")[1].strip()
        else:
            c_code = generated_text[len(prompt):].strip()
        
        # Clean up common issues
        if "<|endoftext|>" in c_code:
            c_code = c_code.split("<|endoftext|>")[0].strip()
        if "<|assembly|>" in c_code:
            c_code = c_code.split("<|assembly|>")[0].strip()
        
        return c_code, generation_time, len(outputs[0]) - len(inputs[0])
        
    except Exception as e:
        print(f"    ⚠️  Generation error: {e}")
        return "", 0, 0

def calculate_similarity_metrics(generated_c, reference_c):
    """Calculate various similarity metrics between generated and reference C code"""
    metrics = {}
    
    # Basic length comparison
    gen_len = len(generated_c)
    ref_len = len(reference_c)
    metrics['length_ratio'] = gen_len / ref_len if ref_len > 0 else 0
    
    # Line count comparison
    gen_lines = len(generated_c.split('\n'))
    ref_lines = len(reference_c.split('\n'))
    metrics['line_ratio'] = gen_lines / ref_lines if ref_lines > 0 else 0
    
    # Simple token overlap (word-level)
    gen_tokens = set(generated_c.lower().split())
    ref_tokens = set(reference_c.lower().split())
    
    if len(ref_tokens) > 0:
        overlap = len(gen_tokens.intersection(ref_tokens))
        metrics['token_overlap'] = overlap / len(ref_tokens)
        metrics['token_precision'] = overlap / len(gen_tokens) if len(gen_tokens) > 0 else 0
    else:
        metrics['token_overlap'] = 0
        metrics['token_precision'] = 0
    
    # Check for common C keywords presence
    c_keywords = ['int', 'char', 'float', 'double', 'void', 'if', 'else', 'for', 'while', 'return', 'struct', 'typedef']
    gen_keywords = sum(1 for kw in c_keywords if kw in generated_c.lower())
    ref_keywords = sum(1 for kw in c_keywords if kw in reference_c.lower())
    
    metrics['keyword_coverage'] = gen_keywords / len(c_keywords)
    metrics['keyword_match_ratio'] = gen_keywords / ref_keywords if ref_keywords > 0 else 0
    
    # Simple structural similarity (braces, semicolons)
    gen_braces = generated_c.count('{') + generated_c.count('}')
    ref_braces = reference_c.count('{') + reference_c.count('}')
    gen_semicolons = generated_c.count(';')
    ref_semicolons = reference_c.count(';')
    
    metrics['brace_ratio'] = gen_braces / ref_braces if ref_braces > 0 else 0
    metrics['semicolon_ratio'] = gen_semicolons / ref_semicolons if ref_semicolons > 0 else 0
    
    return metrics

def test_model_on_validation_set(model, tokenizer, device, validation_pairs, model_name, max_samples=None):
    """Test a model on the validation dataset"""
    print(f"\n🧪 Testing {model_name} on validation set")
    print("=" * 60)
    
    if max_samples:
        validation_pairs = validation_pairs[:max_samples]
        print(f"Testing on first {max_samples} samples")
    
    results = []
    total_generation_time = 0
    total_tokens_generated = 0
    
    for i, pair in enumerate(validation_pairs):
        print(f"\n📄 Testing {i+1}/{len(validation_pairs)}: {pair['filename']} ({pair['optimization']})")
        
        try:
            # Generate C code
            generated_c, gen_time, tokens_gen = generate_c_code(
                model, tokenizer, device, pair['assembly']
            )
            
            total_generation_time += gen_time
            total_tokens_generated += tokens_gen
            
            # Calculate metrics
            metrics = calculate_similarity_metrics(generated_c, pair['c_code'])
            
            # Store results
            result = {
                'filename': pair['filename'],
                'optimization': pair['optimization'],
                'generated_c': generated_c,
                'reference_c': pair['c_code'],
                'assembly': pair['assembly'],
                'generation_time': gen_time,
                'tokens_generated': tokens_gen,
                'metrics': metrics
            }
            results.append(result)
            
            # Print brief metrics
            print(f"    Token overlap: {metrics['token_overlap']:.3f}")
            print(f"    Length ratio: {metrics['length_ratio']:.3f}")
            print(f"    Generation time: {gen_time:.3f}s")
            
        except Exception as e:
            print(f"    ❌ Error testing {pair['filename']}: {e}")
            continue
    
    # Calculate aggregate statistics
    if results:
        metrics_keys = results[0]['metrics'].keys()
        aggregate_metrics = {}
        
        for key in metrics_keys:
            values = [r['metrics'][key] for r in results if not np.isnan(r['metrics'].get(key, 0))]
            if values:
                aggregate_metrics[key] = {
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std': statistics.stdev(values) if len(values) > 1 else 0,
                    'min': min(values),
                    'max': max(values)
                }
            else:
                aggregate_metrics[key] = {'mean': 0, 'median': 0, 'std': 0, 'min': 0, 'max': 0}
        
        # Overall statistics
        overall_stats = {
            'model_name': model_name,
            'total_samples': len(results),
            'total_generation_time': total_generation_time,
            'avg_generation_time': total_generation_time / len(results),
            'total_tokens_generated': total_tokens_generated,
            'avg_tokens_per_sample': total_tokens_generated / len(results),
            'aggregate_metrics': aggregate_metrics,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"\n📊 {model_name} Performance Summary:")
        print(f"    Samples tested: {len(results)}")
        print(f"    Avg generation time: {overall_stats['avg_generation_time']:.3f}s")
        print(f"    Avg tokens generated: {overall_stats['avg_tokens_per_sample']:.1f}")
        print(f"    Token overlap (mean): {aggregate_metrics['token_overlap']['mean']:.3f}")
        print(f"    Length ratio (mean): {aggregate_metrics['length_ratio']['mean']:.3f}")
        print(f"    Keyword coverage (mean): {aggregate_metrics['keyword_coverage']['mean']:.3f}")
        
        return results, overall_stats
    
    return [], {}

def compare_models(base_results, finetuned_results, base_stats, finetuned_stats):
    """Compare performance between base and fine-tuned models"""
    print(f"\n🔍 Model Comparison Analysis")
    print("=" * 60)
    
    if not base_results or not finetuned_results:
        print("❌ Cannot compare - missing results from one or both models")
        return {}
    
    comparison = {
        'base_model': base_stats,
        'finetuned_model': finetuned_stats,
        'improvements': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Compare key metrics
    metrics_to_compare = ['token_overlap', 'length_ratio', 'keyword_coverage', 'token_precision']
    
    print(f"{'Metric':<20} {'Base Model':<12} {'Fine-tuned':<12} {'Improvement':<12}")
    print("-" * 60)
    
    for metric in metrics_to_compare:
        base_val = base_stats['aggregate_metrics'][metric]['mean']
        ft_val = finetuned_stats['aggregate_metrics'][metric]['mean']
        improvement = ((ft_val - base_val) / base_val * 100) if base_val > 0 else 0
        
        comparison['improvements'][metric] = {
            'base_value': base_val,
            'finetuned_value': ft_val,
            'improvement_percent': improvement
        }
        
        print(f"{metric:<20} {base_val:<12.3f} {ft_val:<12.3f} {improvement:>+7.1f}%")
    
    # Compare generation speed
    base_speed = base_stats['avg_generation_time']
    ft_speed = finetuned_stats['avg_generation_time']
    speed_change = ((ft_speed - base_speed) / base_speed * 100) if base_speed > 0 else 0
    
    comparison['improvements']['generation_speed'] = {
        'base_value': base_speed,
        'finetuned_value': ft_speed,
        'improvement_percent': -speed_change  # Negative because lower time is better
    }
    
    print(f"{'Generation Speed':<20} {base_speed:<12.3f} {ft_speed:<12.3f} {-speed_change:>+7.1f}%")
    
    # Overall assessment
    positive_improvements = sum(1 for imp in comparison['improvements'].values() 
                              if imp['improvement_percent'] > 0)
    total_metrics = len(comparison['improvements'])
    
    print(f"\n🎯 Overall Assessment:")
    print(f"   Metrics improved: {positive_improvements}/{total_metrics}")
    
    avg_improvement = statistics.mean([imp['improvement_percent'] 
                                     for imp in comparison['improvements'].values()])
    print(f"   Average improvement: {avg_improvement:+.1f}%")
    
    if avg_improvement > 5:
        print("   ✅ Fine-tuning shows significant improvement!")
    elif avg_improvement > 0:
        print("   ✓ Fine-tuning shows modest improvement")
    else:
        print("   ⚠️  Fine-tuning may need adjustment")
    
    return comparison

def save_detailed_results(base_results, finetuned_results, comparison, output_dir=RESULTS_DIR):
    """Save detailed test results to files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save individual results
    if base_results:
        base_file = os.path.join(output_dir, f"base_model_results_{timestamp}.json")
        with open(base_file, 'w') as f:
            json.dump(base_results, f, indent=2)
        print(f"💾 Base model results saved to: {base_file}")
    
    if finetuned_results:
        ft_file = os.path.join(output_dir, f"finetuned_model_results_{timestamp}.json")
        with open(ft_file, 'w') as f:
            json.dump(finetuned_results, f, indent=2)
        print(f"💾 Fine-tuned model results saved to: {ft_file}")
    
    # Save comparison
    if comparison:
        comp_file = os.path.join(output_dir, f"model_comparison_{timestamp}.json")
        with open(comp_file, 'w') as f:
            json.dump(comparison, f, indent=2)
        print(f"💾 Model comparison saved to: {comp_file}")
    
    # Create a summary report
    summary_file = os.path.join(output_dir, f"test_summary_{timestamp}.txt")
    with open(summary_file, 'w') as f:
        f.write("Assembly Decompiler Model Comparison Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if base_results and finetuned_results:
            f.write(f"Samples tested: {len(base_results)}\n")
            f.write(f"Base model avg token overlap: {comparison['base_model']['aggregate_metrics']['token_overlap']['mean']:.3f}\n")
            f.write(f"Fine-tuned avg token overlap: {comparison['finetuned_model']['aggregate_metrics']['token_overlap']['mean']:.3f}\n")
            f.write(f"Token overlap improvement: {comparison['improvements']['token_overlap']['improvement_percent']:+.1f}%\n\n")
            
            f.write("Key Improvements:\n")
            for metric, data in comparison['improvements'].items():
                f.write(f"  {metric}: {data['improvement_percent']:+.1f}%\n")
    
    print(f"📄 Summary report saved to: {summary_file}")

def show_sample_outputs(results, model_name, num_samples=3):
    """Show sample outputs from the model"""
    print(f"\n📋 Sample Outputs from {model_name}")
    print("=" * 80)
    
    # Sort by token overlap to show best and worst examples
    sorted_results = sorted(results, key=lambda x: x['metrics']['token_overlap'], reverse=True)
    
    # Show best examples
    print(f"\n🏆 Best Examples (highest token overlap):")
    for i, result in enumerate(sorted_results[:num_samples]):
        print(f"\n--- Example {i+1}: {result['filename']} ({result['optimization']}) ---")
        print(f"Token overlap: {result['metrics']['token_overlap']:.3f}")
        print(f"\nOriginal C:")
        print(result['reference_c'][:300] + "..." if len(result['reference_c']) > 300 else result['reference_c'])
        print(f"\nGenerated C:")
        print(result['generated_c'][:300] + "..." if len(result['generated_c']) > 300 else result['generated_c'])
    
    # Show worst examples
    print(f"\n🔍 Challenging Examples (lowest token overlap):")
    for i, result in enumerate(sorted_results[-num_samples:]):
        print(f"\n--- Example {i+1}: {result['filename']} ({result['optimization']}) ---")
        print(f"Token overlap: {result['metrics']['token_overlap']:.3f}")
        print(f"\nOriginal C:")
        print(result['reference_c'][:200] + "..." if len(result['reference_c']) > 200 else result['reference_c'])
        print(f"\nGenerated C:")
        print(result['generated_c'][:200] + "..." if len(result['generated_c']) > 200 else result['generated_c'])

def main():
    parser = argparse.ArgumentParser(description='Compare base and fine-tuned assembly decompiler models')
    parser.add_argument('--validation-dir', type=str, default=VALIDATION_DATA_DIR, 
                       help='Path to validation data directory')
    parser.add_argument('--optimization', choices=['O0', 'Ofast', 'Osize', 'all'], default='all',
                       help='Assembly optimization level to test (default: all)')
    parser.add_argument('--max-samples', type=int, help='Maximum number of samples to test')
    parser.add_argument('--base-only', action='store_true', help='Test only base model')
    parser.add_argument('--finetuned-only', action='store_true', help='Test only fine-tuned model')
    parser.add_argument('--show-samples', type=int, default=2, help='Number of sample outputs to show')
    parser.add_argument('--save-results', action='store_true', help='Save detailed results to files')
    
    args = parser.parse_args()
    
    print("🔍 Assembly Decompiler Model Comparison")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Missing requirements. Please install them and try again.")
        return
    
    # Load validation data
    use_all_optimizations = (args.optimization == 'all')
    specific_optimization = None if use_all_optimizations else args.optimization
    
    validation_pairs = load_validation_data(
        data_dir=args.validation_dir,
        use_all_optimizations=use_all_optimizations,
        specific_optimization=specific_optimization
    )
    
    if not validation_pairs:
        print("❌ No validation data found. Please check your data_validation directory structure.")
        print(f"Expected structure:")
        print(f"  {args.validation_dir}/")
        print(f"    C/")
        print(f"      <filename1>.c, <filename2>.c, ...")
        print(f"    ASM/")
        print(f"      O0/, Ofast/, Osize/")
        print(f"        <filename1>.s, <filename2>.s, ...")
        return
    
    base_results, base_stats = [], {}
    finetuned_results, finetuned_stats = [], {}
    
    # Test base model
    if not args.finetuned_only:
        base_model, base_tokenizer, base_device = load_base_model()
        if base_model:
            base_results, base_stats = test_model_on_validation_set(
                base_model, base_tokenizer, base_device, validation_pairs, 
                "Base DistilGPT2", args.max_samples
            )
            
            if args.show_samples > 0 and base_results:
                show_sample_outputs(base_results, "Base DistilGPT2", args.show_samples)
        else:
            print("⚠️  Skipping base model test - model not available")
    
    # Test fine-tuned model
    if not args.base_only:
        ft_model, ft_tokenizer, ft_device = load_finetuned_model()
        if ft_model:
            finetuned_results, finetuned_stats = test_model_on_validation_set(
                ft_model, ft_tokenizer, ft_device, validation_pairs, 
                "Fine-tuned Decompiler", args.max_samples
            )
            
            if args.show_samples > 0 and finetuned_results:
                show_sample_outputs(finetuned_results, "Fine-tuned Decompiler", args.show_samples)
        else:
            print("⚠️  Skipping fine-tuned model test - model not available")
    
    # Compare models
    comparison = {}
    if base_results and finetuned_results:
        comparison = compare_models(base_results, finetuned_results, base_stats, finetuned_stats)
    
    # Save results if requested
    if args.save_results:
        save_detailed_results(base_results, finetuned_results, comparison)
    
    print(f"\n✅ Model comparison completed!")
    if not args.save_results:
        print("💡 Use --save-results to save detailed results to files")

if __name__ == "__main__":
    main()