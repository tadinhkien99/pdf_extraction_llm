#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    config.py
# @Author:      Kuro
# @Time:        1/18/2025 11:05 AM
import yaml


class Config:
    with open("./configuration/config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, yaml.SafeLoader)
        llm_model = cfg["llm_model"]
        min_p = cfg["min_p"]
        temperature = cfg["temperature"]
        max_tokens = cfg["max_tokens"]
