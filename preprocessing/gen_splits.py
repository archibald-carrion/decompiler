import pandas as pd # Dataframes
from os import path # Path resolution / manipulation
from sys import stderr # Standard error file
from sklearn.model_selection import train_test_split # Stratified split
from numbers import Number

def gen_splits(root_dir: str, csv_mappings: str, seed: Number, p_train: Number, p_val: Number):
    # Check valid parameters
    # Root directory path
    assert isinstance(root_dir, str), "Dataset root directory path should be a string"
    root_dir = path.expanduser(root_dir)
    assert path.isdir(root_dir), "Invalid root directory for dataset"

    # Split percentages
    assert isinstance(p_train, Number) and p_train >= 0, "Train split percentage should be a non-negative percent number"
    assert isinstance(p_val, Number) and p_val >= 0, "Validation split percentage should be a non-negative percent number"
    assert p_train + p_val <= 1, "Split percentages must sum at most 100%"

    # Get the path of original mapping and the resulting mappings
    mappings_path = path.join(root_dir, csv_mappings)
    
    train_path = path.join(root_dir, "./train.csv")
    validation_path = path.join(root_dir, "./validation.csv")
    test_path = path.join(root_dir, "./test.csv")

    # If the splits already exist, dont generate them
    if path.exists(train_path) and path.exists(validation_path) and path.exists(test_path):
        print(f"Splits already exist at '{train_path}', '{validation_path}', '{test_path}'"
        + " Skipping generation...")
        pass

    # Otherwise, load the original mappings and then generate the splits in files
    try:
        mappings = pd.read_csv(mappings_path)
        # Fix field types
        mappings["Dataset"] = mappings["Dataset"].astype('category')
        mappings["Optimization level"] = mappings["Optimization level"].astype('category')
    except Exception as err:
        print(f"Unable to load dataset mappings file: {err}", file=stderr)
        raise Exception("Invalid mappings file for dataset")

    # The splits will be stratified according to the optimization level and the dataset
    X = mappings[["C filename", "x86 filename"]]
    y = mappings[["Optimization level", "Dataset"]]

    # Split on [test and validation] and [train] sets
    p_test = 1 - p_train - p_val
    X_train, X_testval, y_train, y_testval = train_test_split(
        X, y, test_size=p_test+p_val, stratify=y, random_state=seed)
    
    # Split [test and validation] set on [test-only] and [validation-only] sets
    X_test, X_val, y_test, y_val = train_test_split(
        X_testval, y_testval, test_size=p_val/(p_test+p_val), stratify=y_testval, random_state=seed)
    
    # Rebuild dataframes
    train = X_train.join(y_train, how="outer")
    train.index.name = "Index"
    test = X_test.join(y_test, how="outer")
    test.index.name = "Index"
    val = X_val.join(y_val, how="outer")
    val.index.name = "Index"

    # Save them to file
    try:
        train.to_csv(path_or_buf=train_path, mode="w")
        test.to_csv(path_or_buf=test_path, mode="w")
        val.to_csv(path_or_buf=validation_path, mode="w")
    except Exception as err:
        print(f"Unable to save split mappings: {err}", file=stderr)
        raise Exception("Unable to save mappings splits")
    
    # All is done
    print("Split mappings saved to disk")