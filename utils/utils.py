#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    utils.py
# @Author:      Kuro
# @Time:        1/18/2025 11:05 AM

import re


def extract_fields(text):
    try:
        pattern = r"<\|im_start\|>assistant<\|im_sep\|>(.*?)<\|im_end\|>"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            extracted_text = match.group(1).strip()
            return extracted_text
        else:
            return text
    except Exception as e:
        return text
