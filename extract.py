#!/usr/bin/env python3
"""
Docling PDF/document extraction.
Converts PDF to DoclingDocument, exports to JSON and Markdown.
"""
from __future__ import annotations

from pathlib import Path

from docling.document_converter import DocumentConverter


def extract(pdf_path: str) -> dict:
    """
    Convert PDF to DoclingDocument; export to JSON and Markdown.
    Returns dict with docling_document (dict) and docling_markdown (str).
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))

    if not result.document:
        raise RuntimeError(f"Docling conversion failed for {pdf_path}")

    doc = result.document
    docling_document = doc.export_to_dict() if hasattr(doc, "export_to_dict") else doc.model_dump()
    docling_markdown = doc.export_to_markdown()

    return {
        "docling_document": docling_document,
        "docling_markdown": docling_markdown,
    }
