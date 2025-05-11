"""
Module for analyzing cyclomatic complexity of C functions.
"""
import lizard

def analyze_cyclomatic_complexity(function_definitions):
    """
    Analyzes the cyclomatic complexity directly using lizard without writing to files.
    
    Args:
        function_definitions: List of C function definitions
        
    Returns:
        tuple: (list of complexity values, list of (function, complexity) tuples)
    """
    complexities = []
    functions_with_complexity = []
    error_count = 0
    success_count = 0
    
    print(f"Processing {len(function_definitions)} functions...")
    
    for i, func in enumerate(function_definitions):
        if i % 1000 == 0 and i > 0:
            print(f"Processed {i} functions. Success: {success_count}, Errors: {error_count}")
        
        # Add necessary headers and wrap the function in a complete file
        full_code = f"""
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

{func}
"""
        try:
            # Clean code of any non-ASCII characters
            clean_code = ''.join(c if ord(c) < 128 else ' ' for c in full_code)
            
            # Use lizard to analyze the code string directly
            analysis = lizard.analyze_file.analyze_source_code("temp_func.c", clean_code)
            
            # Extract complexity for each function found
            for func_info in analysis.function_list:
                complexity = func_info.cyclomatic_complexity
                complexities.append(complexity)
                functions_with_complexity.append((func, complexity))
                success_count += 1
                
        except Exception as e:
            error_count += 1
            if error_count % 1000 == 0:
                print(f"Error in function {i}: {type(e).__name__}")
    
    print(f"Analysis complete. Successfully analyzed: {success_count}, Errors: {error_count}")
    return complexities, functions_with_complexity