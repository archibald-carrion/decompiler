#!/usr/bin/env bash
# Downloads, collects and decompresses the files for splits in the exebench dataset
# Run with sh collect.sh 
# You may use these to generate examples later via the 'preprocessing' python module CLI

# Use the following script filenames. Change at your own discretion
declare -a splits=("valid_real" "test_real" "train_real_compilable")

# Create a directory to store the split contents on
declare contents_root_dir=~/exebench_splits
mkdir -p $contents_root_dir

# Process each file
for split in "${splits[@]}"
do
    echo "== Processing split $split ..."

    # Download the compressed contents
    declare split_filename=${split}.tar.gz
    declare split_filepath=${contents_root_dir}/$split_filename
    echo ">> Downloading $split_filename into $split_filepath ..."
    wget -O $split_filepath "https://huggingface.co/datasets/jordiae/exebench/resolve/main/$split_filename" \
        -q --show-progress

    # Decompress them
    declare split_directory=${contents_root_dir}/$split
    echo ">> Decompressing contents into $split_directory ..."
    mkdir -p $split_directory
    tar -xzf $split_filepath --directory $split_directory

    # Keep only the split files on split directory, delete all others
    echo ">> Purging unnecessary contents from $split_directory ..."
    find ${split_directory}/ -type f \! \( -name \*.jsonl.zst \) -exec sh -c 'rm "$1"' _ {} \;

    # Remove compressed contents, we don't need them anymore
    echo ">> Purging unnecessary $split_filepath ..."
    rm $split_filepath

    echo ">> Done processing split!"
done

echo "Done processing all splits!"
