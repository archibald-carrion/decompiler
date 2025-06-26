# LLM Causal model
from transformers import PreTrainedModel, PreTrainedTokenizerBase # Models
from torch import no_grad, ones_like # Disable gradient tracking, quick linear algebra

# Input/output parsing from prompts
from time import time_ns # Timing
from .model_loading import input_from_code, output_from_response

# Cuda availability

# Logging
from sys import stderr

def decompile(model: PreTrainedModel, tokenizer: PreTrainedTokenizerBase, asm_code: str, 
    top_p: float = 0.5, temperature: float = 0.5) -> tuple[str | None, int]:
    # Validate arguments
    assert isinstance(model, PreTrainedModel), "Invalid model"
    assert isinstance(tokenizer, PreTrainedTokenizerBase), "Invalid tokenizer"
    assert isinstance(asm_code, str), "x86 code should be a string"
    assert isinstance(top_p, float) and top_p >= 0 and top_p <= 1, "Top-P sampling parameter should be a float between 0 and 1"
    assert isinstance(temperature, float) and temperature >= 0 and temperature <= 1, "Temperature parameter should be a float between 0 and 1"

    # Construct prompt
    tokenized_prompt = input_from_code(tokenizer, asm_code, tokenize=True).to("cuda")

    # Collect best prediction as response
    start_time = time_ns()
    with no_grad():
        try:
            output = model.generate(
                **tokenized_prompt,
                tokenizer=tokenizer,
                do_sample=True,
                top_p=top_p,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=tokenizer.pad_token_type_id,
                stop_strings=["<|im_end|>"],
            )[0]
        except Exception as err:
            print(f"Unable to predict best response: {err}", file=stderr)
            raise Exception("Invalid model prediction")
    
    generation_time = time_ns() - start_time
    
    # Decode the generated text
    response = tokenizer.decode(output, skip_special_tokens=False)

    # Parse the output from it
    c_code = output_from_response(tokenizer, asm_code, response)

    # All is done
    return (c_code, generation_time)