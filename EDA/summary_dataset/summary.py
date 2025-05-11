import zstandard as zstd
import json
import os

def print_first_n_json_entries(filepath, n=5):
    """Reads a .jsonl.zst file and prints the first N JSON entries."""
    print(f"First {n} entries from: {filepath}")
    try:
        with open(filepath, 'rb') as f:
            dctx = zstd.ZstdDecompressor()
            stream_reader = dctx.stream_reader(f)
            text_stream = stream_reader.read().decode('utf-8')
            lines = text_stream.strip().split('\n')
            count = 0
            for line in lines:
                try:
                    obj = json.loads(line)
                    print(f"--- Entry {count + 1} ---")
                    print(json.dumps(obj, indent=2))
                    count += 1
                    if count >= n:
                        break
                except json.JSONDecodeError:
                    print(f"Could not decode line: {line}")
                except Exception as e:
                    print(f"Error processing line: {e}")
            if count == 0:
                print("No valid JSON entries found in the file.")
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
    print("-" * 30)

if __name__ == "__main__":
    folder_path = 'data/train_real_simple_io/'
    filepaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.jsonl.zst')]

    if not filepaths:
        print(f"Error: No .jsonl.zst files found in the folder {folder_path}")
    else:
        for filepath in filepaths:
            print_first_n_json_entries(filepath, n=3) # You can change 'n' to the desired number of entries