#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    pdf_api.py
# @Author:      Kuro
# @Time:        11/29/2024 11:28 AM
import fitz
from fastapi import APIRouter, UploadFile, File, HTTPException

from services.pdf_service import PDFService

pdf_router = APIRouter()
pdf_service = PDFService()


@pdf_router.post("/pdf-extraction")
async def pdf_extraction(file: UploadFile = File(...)):
    try:
        # Read file data as bytes
        data = await file.read()
        # Open the PDF from bytes using PyMuPDF
        doc = fitz.open(stream=data, filetype="pdf")
        text = ""
        # Iterate over each page and extract text
        for page in doc:
            # print("Page number: ", page.number)
            # print("Page text: ", page.get_text())
            # print("-------------------------------------------------")
            text += page.get_text() + "\n----------------------------------------\n"
        doc.close()
        output_llm = await pdf_service.generate_text(text, ["Address", "Partner name", "Partner code"])
        return {"status": 200, "data": output_llm}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error. Please try again. {str(e)}")
