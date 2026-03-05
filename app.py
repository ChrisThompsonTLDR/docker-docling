#!/usr/bin/env python3
"""
Docling extraction HTTP service for RunPod.
POST /extract with JSON {filename, document_id} -> converts PDF, returns docling_document + docling_markdown.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from extract import extract

app = FastAPI()

DATA_DIR = Path(os.environ.get("DOCLING_DATA_DIR", "/workspace"))


class ExtractRequest(BaseModel):
    filename: str
    document_id: int


@app.post("/extract")
def extract_endpoint(req: ExtractRequest) -> dict:
    pdf_path = DATA_DIR / req.filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found: {req.filename}")

    try:
        result = extract(str(pdf_path))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
