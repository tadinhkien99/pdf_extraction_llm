# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # @Filename:    pdf_service.py
# # @Author:      Kuro
# # @Time:        11/7/2024 10:30 AM
from unsloth import FastLanguageModel

from configuration.config import Config
from utils.utils import extract_fields


class PDFService:
    def __init__(self):
        max_seq_length = 2048  # Choose any! We auto support RoPE Scaling internally!
        dtype = None  # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
        load_in_4bit = True  # Use 4bit quantization to reduce memory usage. Can be False.
        self.model_name = Config.llm_model
        self.min_p = Config.min_p
        self.temperature = Config.temperature
        self.max_tokens = Config.max_tokens

        self.model, self.tokenizer = FastLanguageModel.from_pretrained(model_name=self.model_name, max_seq_length=max_seq_length, dtype=dtype, load_in_4bit=load_in_4bit)
        FastLanguageModel.for_inference(self.model)  # Enable native 2x faster inference

    async def generate_text(self, pdf_text, list_of_keys, system_message):
        list_of_keys_string = "\n".join(list_of_keys)
        user_message = f"""Extract the following key-value pairs from the invoice text:\n{list_of_keys_string}"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]

        inputs = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")

        outputs = self.model.generate(input_ids=inputs, min_p=self.min_p, temperature=self.temperature, max_new_tokens=self.max_tokens, use_cache=True)
        generated_text = self.tokenizer.batch_decode(outputs)[0]
        generated_text = extract_fields(generated_text)
        return generated_text
