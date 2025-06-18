# See: https://docs.pytorch.org/tutorials/beginner/data_loading_tutorial.html

import pandas as pd # Dataframes
from os import path # Path resolution
from sys import stderr # Standard error file
import torch # PyTorch dataset interface
from sklearn.model_selection import train_test_split # Stratified split

class DecompilationDataset(torch.utils.data.Dataset):
    """
    C and x86 pairs decompilation dataset.

    Examples are in the dictionary form:
    \{"c": c_code, "asm": asm_code, "opt": opt_level, "dataset": og_dataset\}
    """

    def __init__(self, csv_mappings: str, root_dir: str):
        """
        Arguments:
            csv_mappings (string): Path to the csv file with mappings between source codes.
            root_dir (string): Parent directory to all source code paths.
        """
        # Validate root directory path
        if not path.isdir(root_dir):
            raise Exception("Invalid root directory for dataset")

        self.root_dir = root_dir

        # Get path to csv mappings
        csv_mappings = path.join(root_dir, csv_mappings)

        # Validate mapping path
        if not path.isfile(csv_mappings):
            raise Exception("Invalid mappings file for dataset") 
        
        # Load mapping into memory
        try:
            self.mappings = pd.read_csv(csv_mappings)

            # Fix field types
            self.mappings["Dataset"] = self.mappings["Dataset"].astype('category')
            self.mappings["Optimization level"] = self.mappings["Optimization level"].astype('category')
        except Exception as err:
            print(f"Unable to load dataset mappings file: {err}", file=stderr)
            raise Exception("Invalid mappings file for dataset")

    def __len__(self):
        """
        Returns the amount of elements in the dataset
        """
        return len(self.mappings.shape[0])

    def __getitem__(self, idx: int):
        """
        Get the items described by the index from memory
        Arguments:
            idx (int): Index refering to the example to collect 
        """
        # Validate index
        if not isinstance(idx, int):
            print(f"Invalid index type: Only integers supported", file=stderr)
            raise Exception("Invalid index for dataset")

        if not (0 <= idx and idx < self.mappings.shape[0]):
            print(f"Index out of range for dataset entry", file=stderr)
            raise Exception("Index out of range for dataset entry")

        # Collect the respective entry in the mapping
        try:
            mapping = self.mappings.iloc[idx]
        except Exception as err:
            print(f"Unable to load dataset mapping entry: {err}", file=stderr)
            raise Exception("Missing entry for dataset")
        
        # Collect the paths to the source codes, as well as other features,
        # according to the entry
        try:
            c_path = path.join(self.root_dir, mapping["C filename"])
            asm_path = path.join(self.root_dir, mapping["x86 filename"])
            opt_level = path.join(self.root_dir, mapping["Optimization level"])
            og_dataset = path.join(self.root_dir, mapping["Dataset"])
        except Exception as err:
            print(f"Unable to load fields in dataset mapping entry: {err}", file=stderr)
            raise Exception("Invalid entry for dataset")

        # Load the contents of the x86 assembly and C source codes
        try:
            with open(c_path, "r", encoding="UTF-8") as f:
                c_code = f.read()
            
            with open(asm_path, "r", encoding="UTF-8") as f:
                asm_code = f.read() 
        except Exception as err:
            print(f"Unable to load source codes from files: {err}", file=stderr)
            raise Exception("Invalid source code file")

        # Construct and return an ordered output
        return {"c": c_code, "asm": asm_code, "opt": opt_level, "dataset": og_dataset}
    
def gen_splits(root_dir: str, csv_mappings: str, random_state: int):
    # Validate root directory path
    if not path.isdir(root_dir):
        raise Exception("Invalid root directory for dataset")
    
    # Get the path of original mapping and the resulting mappings
    mappings_path = path.join(root_dir, csv_mappings)
    
    train_path = path.join(root_dir, "./train.csv")
    validation_path = path.join(root_dir, "./validation.csv")
    test_path = path.join(root_dir, "./test.csv")

    # If the splits already exist, dont generate them
    if path.exists(train_path) and path.exists(validation_path) and path.exists(test_path):
        print(f"Splits already exist at '{train_path}', '{validation_path}', '{test_path}'"
        + "Skipping generation...")
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

    # The sizes are fixed
    # Train -> 80%
    # Test -> 10%
    # Validation -> 10%

    # Split on [test and validation] and [train] sets
    X_train, X_testval, y_train, y_testval = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=random_state)
    
    # Split [test and validation] set on [test-only] and [validation-only] sets
    X_test, X_val, y_test, y_val = train_test_split(
        X_testval, y_testval, test_size=0.5, stratify=y_train, random_state=random_state)
    
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