# See: https://docs.pytorch.org/tutorials/beginner/data_loading_tutorial.html

import pandas as pd # Dataframes
from os import path # Path resolution
from sys import stderr # Standard error file
import torch # PyTorch dataset interface

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

        # Validate sources directory paths
        self.c_dir = path.join(self.root_dir, "./c")
        self.asm_dir = path.join(self.root_dir, "./asm")

        if not path.isdir(self.c_dir):
            raise Exception("Missing c directory for dataset")
        
        if not path.isdir(self.asm_dir):
            raise Exception("Missing x86 directory for dataset")

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
            c_path = path.join(self.c_dir, mapping["C filename"])
            asm_path = path.join(self.asm_dir, mapping["x86 filename"])
            opt_level = mapping["Optimization level"]
            og_dataset = mapping["Dataset"]
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
