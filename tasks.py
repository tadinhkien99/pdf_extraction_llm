#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    tasks.py
# @Author:      Kuro
# @Time:        2/19/2025 10:15 AM

from celery_app import celery_app


@celery_app .task()
def test():
    pass
