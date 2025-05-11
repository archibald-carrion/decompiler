"""
Module for extracting function definitions from .jsonl.zst files.
"""
import zstandard as zstd
import json

def extract_function_definitions(filepath):
    """
    Reads a .jsonl.zst file and extracts C function definitions.
    
    Args:
        filepath: Path to the .jsonl.zst file
        
    Returns:
        list: List of function definitions (strings)
    """
    function_definitions = []
    
    try:
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
    except Exception as e:
        print(f"Error opening file {filepath}: {e}")
        
    return function_definitions