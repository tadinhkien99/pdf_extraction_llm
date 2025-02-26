# #!/usr/bin/env python
# # -*- coding:utf-8 -*-
# # @Filename:    pdf_service.py
# # @Author:      Kuro
# # @Time:        11/7/2024 10:30 AM
from unsloth import FastLanguageModel

from configuration.config import Config


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
        self.system_message = "1. Goal\nYou are provided with the complete text extracted from an invoice PDF, which may span multiple pages. Your task is to extract key-value pairs strictly based on a list of keys supplied by the user. Focus on accurately retrieving values corresponding to each user-specified key (e.g., Invoice Number, Date, Total Amount) and ignore all extraneous content.\n-----------------------------------------------------\n2. Return Format\nOutput your results as a valid JSON object where each key from the user’s list is paired with its corresponding value extracted from the text. If a key is not found or is ambiguous, return a value of null. Do not include any additional text or commentary. For example:\n{\n  \"Invoice Number\": \"12345\",\n  \"Invoice Date\": \"2025-02-20\",\n  \"Total Amount\": \"$100.00\"\n}\n-----------------------------------------------------\n3. Warnings\nThe input text may contain noise such as headers, footers, page numbers, or OCR errors.\nOnly extract values for the keys explicitly provided by the user; do not infer or add any additional keys.\nIf a key appears multiple times, carefully decide whether to return the first occurrence, merge multiple values into an array, or set the value as null if ambiguous.\nEnsure that your output remains strictly in the specified JSON format without any extraneous explanations or notes.\n-----------------------------------------------------\n4. Context Dump\nUtilize the entire provided invoice text—across all pages—as your reference. This text is the sole source for extracting key-value pairs. Be mindful that the invoice may have multiple sections and formatting irregularities. All extractions should rely exclusively on the text context given, ensuring no data is assumed beyond what is provided.\n"

    async def generate_text(self, pdf_text, list_of_keys):
        list_of_keys_string = ", ".join(list_of_keys)
        user_message = f"""Extract the following key-value pairs from the invoice text:\n{list_of_keys_string}"""

        messages = [
            {"role": "system", "content": self.system_message},
            {"role": "user", "content": user_message}
        ]

        inputs = self.tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")

        outputs = self.model.generate(input_ids=inputs, min_p=self.min_p, temperature=self.temperature, max_new_tokens=self.max_tokens, use_cache=True)
        generated_text = self.tokenizer.batch_decode(outputs)[0]
        return generated_text
