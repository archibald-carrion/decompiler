import json
import difflib
import re
from collections import Counter
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def normalize_code(code):
    # Remove comments and extra whitespace for fairer comparison
    code = re.sub(r'//.*|/\\*.*?\\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'\\s+', ' ', code)
    return code.strip()

def levenshtein(a, b):
    # Simple Levenshtein distance implementation
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous[j] + 1, current[j - 1] + 1, previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current[j] = min(add, delete, change)
    return current[n]

def token_overlap(a, b):
    tokens_a = set(a.split())
    tokens_b = set(b.split())
    return len(tokens_a & tokens_b) / max(1, len(tokens_a | tokens_b))

def exact_match(a, b):
    return int(a.strip() == b.strip())

def main():
    with open('decompiler_comparison_results_v2.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    model_keys = [
        ('base_model_output', 'Base'),
        ('finetuned_model_output', 'Finetuned'),
        ('finetuned_model_v2_output', 'Finetuned_v2'),
    ]
    metrics = {name: [] for _, name in model_keys}
    for entry in data:
        ref = entry.get('correct_c') or entry.get('reference') or ''
        if not ref:
            continue
        ref_norm = normalize_code(ref)
        for key, name in model_keys:
            gen = entry.get(key, '')
            if not gen:
                continue
            gen_norm = normalize_code(gen)
            lev = levenshtein(ref_norm, gen_norm)
            bleu = sentence_bleu([ref_norm.split()], gen_norm.split(), smoothing_function=SmoothingFunction().method1)
            em = exact_match(ref_norm, gen_norm)
            overlap = token_overlap(ref_norm, gen_norm)
            line_diff = abs(len(ref_norm.splitlines()) - len(gen_norm.splitlines()))
            char_diff = abs(len(ref_norm) - len(gen_norm))
            metrics[name].append({
                'filename': entry.get('filename', ''),
                'levenshtein': lev,
                'bleu': bleu,
                'exact_match': em,
                'token_overlap': overlap,
                'line_diff': line_diff,
                'char_diff': char_diff,
            })

    # Print summary for each model
    for name in metrics:
        print(f'\n=== Metrics for {name} ===')
        for m in metrics[name]:
            print(m)
        if metrics[name]:
            print(f'--- Averages for {name} ---')
            for key in ['levenshtein', 'bleu', 'exact_match', 'token_overlap', 'line_diff', 'char_diff']:
                avg = sum(m[key] for m in metrics[name]) / len(metrics[name])
                print(f'{key}: {avg:.4f}')

if __name__ == '__main__':
    main()