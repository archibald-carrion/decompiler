# See: https://docs.pytorch.org/tutorials/beginner/data_loading_tutorial.html

import pandas as pd
from os import path
from sys import stderr
import torch

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

        # Validate root directory path
        if not path.isdir(root_dir):
            raise Exception("Invalid root directory for dataset")

        self.root_dir = root_dir

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