import argparse
import logging

import numpy as np
import torch

from collections import Counter
from transformers import (
    CTRLLMHeadModel,
    CTRLTokenizer,
    GPT2LMHeadModel,
    GPT2Tokenizer,
    OpenAIGPTLMHeadModel,
    OpenAIGPTTokenizer,
    TransfoXLLMHeadModel,
    TransfoXLTokenizer,
    XLMTokenizer,
    XLMWithLMHeadModel,
    XLNetLMHeadModel,
    XLNetTokenizer,
)


# logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s", datefmt="%m/%d/%Y %H:%M:%S", level=logging.INFO)
# logger = logging.getLogger(__name__)


def adjust_length_to_model(length, max_sequence_length):
    if length < 0 and max_sequence_length > 0:
        length = max_sequence_length
    elif 0 < max_sequence_length < length:
        length = max_sequence_length  # No generation bigger than model size
    elif length < 0:
        length = int(10000)  # avoid infinite loop
    return length


def load_distilgpt2(device, model_path):
    # Initialize the model and tokenizer
    model_class, tokenizer_class = (GPT2LMHeadModel, GPT2Tokenizer)
    tokenizer = tokenizer_class.from_pretrained(model_path)
    model = model_class.from_pretrained(model_path)
    model.to(device)
    return model_class, tokenizer_class, tokenizer, model


def generate(prompt_text):
    # Encode prompt sequences
    encoded_prompt = tokenizer.encode(prompt_text, add_special_tokens=False, return_tensors="pt")
    encoded_prompt = encoded_prompt.to(device)

    if encoded_prompt.size()[-1] == 0:
        input_ids = None
    else:
        input_ids = encoded_prompt

    # Generate sequences
    length = 1
    length = adjust_length_to_model(length, max_sequence_length=model.config.max_position_embeddings)

    output_sequences = model.generate(
        input_ids=input_ids,
        max_length=length + len(encoded_prompt[0]),
        temperature=.7,
        top_k=0,
        top_p=0.9,
        repetition_penalty=2,
        do_sample=True,
        num_return_sequences=10,
    )

    # Remove the batch dimension when returning multiple sequences
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()

    generated_sequences = []
    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)

        # Remove all text after the stop token
        # stop_token = "<end>"
        # text = text[: text.find(stop_token) if stop_token else None]

        # Add the prompt at the beginning of the sequence. Remove the excess text that was used for pre-processing
        total_sequence = (text[len(tokenizer.decode(encoded_prompt[0], clean_up_tokenization_spaces=True)) :]        )
        generated_sequences.append(total_sequence[1:])

    # Return sorted words with most occurance
    suggestions = Counter(generated_sequences).most_common(5)
    print(prompt_text)
    print(suggestions)
    return [elem for elem, n in suggestions]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_class, tokenizer_class, tokenizer, model = load_distilgpt2(device, "server/model/gpt2/distilgpt2")

# preds_all = generate("clustering solves gaps")
# print(preds_all)