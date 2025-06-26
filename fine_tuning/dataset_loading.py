# See: https://docs.pytorch.org/tutorials/beginner/data_loading_tutorial.html

import pandas as pd # Dataframes
from os import path # Path resolution
from sys import stderr # Standard error file
import torch # PyTorch dataset interface
from transformers import PreTrainedTokenizerBase # Tokenization
from ..utils.model_loading import input_from_code 

class DecompilationDataset(torch.utils.data.Dataset):
    """
    C and x86 pairs instruction-for-decompilation dataset.
    Examples are in the following dictionary form constructed from a prompt fed to the tokenizer: 
    {"text": prompt}
    """

    def __init__(self, csv_mappings: str, root_dir: str, tokenizer: PreTrainedTokenizerBase):
        """
        Arguments:
            csv_mappings (string): Path to the csv file with mappings between source codes.
            root_dir (string): Parent directory to all source code paths.
            tokenizer: A HF tokenizer used to construct the dataset
        """
        # Validate root directory path
        assert isinstance(root_dir, str), "Dataset root directory path should be a string"
        root_dir = path.expanduser(root_dir)
        assert path.isdir(root_dir), "Invalid dataset root directory path"

        self.root_dir = root_dir

        # Validate sources directory paths
        self.c_dir = path.join(self.root_dir, "./c")
        self.asm_dir = path.join(self.root_dir, "./asm")

        assert path.isdir(self.c_dir), "Missing c directory for dataset"
        assert path.isdir(self.asm_dir), "Missing x86 directory for dataset"

        # Get and validate path to csv mappings
        assert isinstance(csv_mappings, str), "Mappings CSV table subpath should be a string"
        csv_mappings = path.join(root_dir, csv_mappings)
        assert path.isfile(csv_mappings), "Invalid mappings CSV table subpath for dataset"

        # Validate tokenizer
        assert isinstance(tokenizer, PreTrainedTokenizerBase), "Tokenizer should be a PreTrainedTokenizerBase"
        self.tokenizer = tokenizer

        # Load mapping into memory
        try:
            self.mappings = pd.read_csv(csv_mappings)
        except Exception as err:
            print(f"Unable to load dataset mappings file: {err}", file=stderr)
            raise Exception("Invalid mappings file for dataset")
        
        # Drop uneccesary features
        self.mappings = self.mappings.drop(columns=["Dataset", "Optimization level"])

    def __len__(self):
        """
        Returns the amount of elements in the dataset
        """
        return self.mappings.shape[0]

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

        # Construct tokenized prompt according to chat template
        # We need to have uniform embeddings / token sequences
        # See: https://huggingface.co/docs/transformers/en/chat_templating
        tokenized_prompt = input_from_code(self.tokenizer, asm_code, c_code, tokenize=True, pad=True)

        # Construct and return an ordered output
        # See: https://huggingface.co/docs/transformers/glossary#input-ids
        # See: https://huggingface.co/docs/transformers/glossary#attention-mask
        # See: https://huggingface.co/docs/transformers/glossary#labels
        # Often for causal language models, the 'labels' to predict are the 'input token ids'
        return {
            'input_ids': tokenized_prompt['input_ids'].flatten(),
            'attention_mask': tokenized_prompt['attention_mask'].flatten(),
            'labels': tokenized_prompt['input_ids'].flatten()
        }
