import zstandard as zstd
import json

def read_jsonl_zst(filepath, max_lines=10):
    """Reads a .jsonl.zst compressed file and prints a summary of the first few entries."""
    # Open the compressed file
    with open(filepath, 'rb') as f:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(f)
        
        # Read the decompressed bytes
        text_stream = stream_reader.read().decode('utf-8')
        
        # Each line is a JSON object
        lines = text_stream.strip().split('\n')
        
        print(f"Total lines: {len(lines)}")
        print(f"Showing first {min(max_lines, len(lines))} lines summary:\n")
        
        for i, line in enumerate(lines[:max_lines]):
            obj = json.loads(line)
            print(f"Entry {i+1}:")
            print(json.dumps(obj, indent=2))  # Pretty print JSON
            print("-" * 40)

def read_and_write_function_definitions(filepath, output_txt):
    """Reads a .jsonl.zst compressed file and writes function definitions to a .txt file."""
    with open(filepath, 'rb') as f:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(f)

        text_stream = stream_reader.read().decode('utf-8')
        lines = text_stream.strip().split('\n')

        with open(output_txt, 'w', encoding='utf-8') as out_file:
            for line in lines:
                try:
                    obj = json.loads(line)
                    # The function definition is nested within the "text" field
                    if "text" in obj and "func_def" in obj["text"]:
                        func_def = obj["text"]["func_def"]
                        out_file.write(func_def + '\n\n' + '-'*40 + '\n\n')  # Add separator for readability
                except json.JSONDecodeError:
                    # Skip lines that aren't valid JSON
                    continue
                except Exception as e:
                    # Log other errors but continue processing
                    print(f"Error processing line: {e}")

# TODO: export eahc function in a separate file instead of one txt file

read_and_write_function_definitions(
    'data/train_synth_compilable/data_0_time1677787985_default.jsonl.zst',
    'function_definitions_output.txt'
)