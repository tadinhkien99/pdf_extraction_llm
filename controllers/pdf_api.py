#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    pdf_api.py
# @Author:      Kuro
# @Time:        11/29/2024 11:28 AM
import json
from typing import List

import fitz
from fastapi import APIRouter, UploadFile, File, HTTPException, Form

from services.pdf_service import PDFService

pdf_router = APIRouter()
pdf_service = PDFService()


@pdf_router.post("/pdf-extraction")
async def pdf_extraction(file: UploadFile = File(...), system_msg: str = Form(...), fields: List[str] = Form(...)):
    try:
        # Read file data as bytes
        data = await file.read()
        # Open the PDF from bytes using PyMuPDF
        doc = fitz.open(stream=data, filetype="pdf")
        text = ""
        # Iterate over each page and extract text
        for page in doc:
            text += page.get_text() + "\n----------------------------------------\n"
        doc.close()
        system_msg_json = json.dumps(system_msg, ensure_ascii=False)
        if system_msg_json.startswith('"') and system_msg_json.endswith('"'):
            system_msg_json = system_msg_json[1:-1]
        # Pass the extracted text along with the system message and fields list
        output_llm = await pdf_service.generate_text(text, fields, system_msg_json)
        return {"status": 200, "data": output_llm}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error. Please try again. {str(e)}")
