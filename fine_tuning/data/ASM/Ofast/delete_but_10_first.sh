#!/bin/bash

# Script to delete all files in the current folder except the first 10 (alphabetically sorted),
# and never delete itself (the script file), even if it is in the first 10.

SCRIPT_NAME=$(basename "$0")
TARGET_DIR="."

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

cd "$TARGET_DIR" || exit 1

file_count=$(find . -maxdepth 1 -type f | wc -l)
echo "Found $file_count files in directory: $(pwd)"

if [ "$file_count" -le 10 ]; then
    echo "10 or fewer files found. Nothing to delete."
    exit 0
fi

# Get all files sorted alphabetically
all_files=($(find . -maxdepth 1 -type f -printf '%f\n' | sort))

# Find the index of the script itself in the sorted list
script_index=-1
for i in "${!all_files[@]}"; do
    if [[ "${all_files[$i]}" == "$SCRIPT_NAME" ]]; then
        script_index=$i
        break
    fi
done

# Determine how many files to keep at the start
if [[ $script_index -ge 0 && $script_index -lt 10 ]]; then
    keep_count=11
else
    keep_count=10
fi

# Build the list of files to keep
files_to_keep=("${all_files[@]:0:$keep_count}")

# Remove the script from the delete list if present
files_to_delete=()
for file in "${all_files[@]:$keep_count}"; do
    if [[ "$file" != "$SCRIPT_NAME" ]]; then
        files_to_delete+=("$file")
    fi
done

if [ ${#files_to_delete[@]} -gt 0 ]; then
    echo "Files to be deleted:"
    for file in "${files_to_delete[@]}"; do
        echo "$file"
    done
    echo
    read -p "Are you sure you want to delete these files? (y/N): " confirm
    if [[ $confirm =~ ^[Yy]$ ]]; then
        for file in "${files_to_delete[@]}"; do
            if [ -f "$file" ]; then
                rm "$file"
                echo "Deleted: $file"
            fi
        done
        echo "Deletion complete."
    else
        echo "Operation cancelled."
    fi
else
    echo "No files to delete."
fi