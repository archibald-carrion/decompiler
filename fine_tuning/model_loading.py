# Path resolution / manipulation
from os import path, makedirs

# Import system
from sys import stderr

# PyTorch support
from torch import float16, float32
from torch.cuda import is_available as is_cuda_available 

# (Down)loadLM Models
from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import snapshot_download

def load_model(model_path: str):
    """ Download the OpenCoder-1.5B-Instruct model and tokenizer to local folder without cache.
    Then, load it into memory
    ### Arguments:
        model_path (str): Directory to store / load the model from
    ### Returns:
        (model, tokenizer)
    """
    MODEL_REPO = "distilbert/distilgpt2"
    
    # Validate local directory path
    assert isinstance(model_path, str), "Local model directory path should be a string"
    model_path = path.expanduser(model_path)

    # Download model
    print(f"Downloading model from {MODEL_REPO} to {model_path}...")
    
    # Create model directory if it doesn't exist
    try:
        makedirs(model_path, exist_ok=True)
    except Exception as err:
        print(f"Unable to create output directory for model: {err}", file=stderr)
        raise Exception("Invalid output directory for model")
    
    # Download model files to local directory (no cache)
    try:
        snapshot_download(
            repo_id=MODEL_REPO,
            local_dir=model_path,
            cache_dir=None,  # Disable cache
            local_dir_use_symlinks=False  # Ensure files are copied, not symlinked
        )
    except Exception as err:
        print(f"Unable to download model from {MODEL_REPO} into {model_path}: {err}")
        raise Exception("Model download failure")
    
    print(f"Model downloaded successfully to {model_path}")

    # Load the model and its tokenizer to memory 
    print(f"Loading model and tokenizer from {model_path}")
    try:
        # Load model
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            # TODO: The alternative line below won't work. Can't finetune models loaded with FP16?
            # See: https://github.com/huggingface/transformers/issues/23165#issuecomment-1536439098
            # torch_dtype=float16 if is_cuda_available() else float32,
            torch_dtype=float32, # Always loading model with FP32 for now
            device_map="auto" if is_cuda_available() else None,
            trust_remote_code=True
        )

        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        
        # Add BOS, EOS and padding tokens if none are provided
        if None in [tokenizer.bos_token, tokenizer.eos_token, tokenizer.pad_token]: 
            tokenizer.add_special_tokens(
                # Provided from OpenCoder
                # See https://huggingface.co/infly/OpenCoder-1.5B-Instruct/blob/d1d1fec467bb8cb9cb1b9bd8b5267fabac284df9/tokenizer_config.json
                special_tokens_dict={
                    'eos_token': "<|im_start|>", 'bos_token': "<|im_end|>", "pad_token": "<pad>"},
                replace_additional_special_tokens=False
            )

            # Resize embeddings appropiately
            model.resize_token_embeddings(len(tokenizer))

        # Add a chat template if none are provided
        tokenizer.chat_template = (
            tokenizer.chat_template if tokenizer.chat_template is not None 
            # Provided from OpenCoder
            # See https://huggingface.co/infly/OpenCoder-1.5B-Instruct/blob/d1d1fec467bb8cb9cb1b9bd8b5267fabac284df9/tokenizer_config.json
            else "{% for message in messages %}{% if loop.first and messages[0]['role'] != 'system' %}{{ '<|im_start|>system\nYou are OpenCoder, created by OpenCoder Team.<|im_end|>\n' }}{% endif %}{{'<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n'}}{% endfor %}{% if add_generation_prompt %}{{ '<|im_start|>assistant\n' }}{% endif %}"
        )

    except Exception as err:
        print(f"Unable to load model and tokenizer into memory from {model_path}: {err}")
        raise Exception("Model load failure")
    
    print(f"Model and tokenizer loaded succesfully")
    return (model, tokenizer)
