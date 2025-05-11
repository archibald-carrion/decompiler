"""
Module for exporting analysis results to CSV format.
"""
import csv
import os

def export_to_csv(functions_with_complexity, output_file_name):
    """
    Exports function complexity data to a CSV file in the same folder as the script.
    
    Args:
        functions_with_complexity: List of (function, complexity) tuples
        output_file_name: Name of the output file
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, output_file_name)
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        writer.writerow(['Function Name', 'Cyclomatic Complexity', 'First Line', 'Function Length (lines)'])
        
        # Write data rows
        for func, complexity in functions_with_complexity:
            lines = func.strip().split('\n')
            function_name = extract_function_name(lines[0])
            first_line = lines[0].strip()
            line_count = len(lines)
            
            writer.writerow([function_name, complexity, first_line, line_count])

def extract_function_name(function_signature):
    """
    Extracts function name from its signature.
    
    Args:
        function_signature: First line of the function definition
        
    Returns:
        str: Extracted function name or "Unknown" if not found
    """
    # Remove leading/trailing whitespace and split by spaces
    parts = function_signature.strip().split()
    
    if len(parts) < 2:
        return "Unknown"
    
    # Find the part that contains the function name (with parentheses)
    for part in parts:
        if '(' in part:
            # Extract just the name (before the parentheses)
            return part.split('(')[0]
    
    # If no parentheses found, use the last part before any semicolon
    if ';' in parts[-1]:
        return parts[-1].split(';')[0]
    
    return parts[-1]