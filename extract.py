#!/usr/bin/env python3
"""
Docling PDF/document extraction via RunPod Granite serverless.
Converts PDF to DoclingDocument, exports to JSON and Markdown.
Requires RUNPOD_API_KEY and RUNPOD_GRANITE_ENDPOINT_ID (deploy via docker/runpod/granite-docling/).
"""
from __future__ import annotations

import os
from pathlib import Path

from docling.document_converter import DocumentConverter


def _make_runpod_converter() -> DocumentConverter:
    """Build DocumentConverter with VlmPipeline pointing at RunPod Granite serverless."""
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import (
        VlmConvertOptions,
        VlmPipelineOptions,
    )
    from docling.datamodel.vlm_engine_options import ApiVlmEngineOptions, VlmEngineType
    from docling.document_converter import PdfFormatOption
    from docling.pipeline.vlm_pipeline import VlmPipeline

    api_key = os.environ.get("RUNPOD_API_KEY", "")
    endpoint_id = os.environ.get("RUNPOD_GRANITE_ENDPOINT_ID", "")
    if not api_key or not endpoint_id:
        raise ValueError(
            "RUNPOD_API_KEY and RUNPOD_GRANITE_ENDPOINT_ID must be set for RunPod serverless mode"
        )

    url = f"https://api.runpod.ai/v2/{endpoint_id}/openai/v1/chat/completions"
    vlm_options = VlmConvertOptions.from_preset(
        "granite_docling",
        engine_options=ApiVlmEngineOptions(
            runtime_type=VlmEngineType.API,
            url=url,
            headers={"Authorization": f"Bearer {api_key}"},
            params={
                "model": "ibm-granite/granite-docling-258M",
                "max_tokens": 4096,
                "skip_special_tokens": True,
            },
            timeout=360,  # Allow cold start (worker spin-up can take 3-5 min)
        ),
    )
    pipeline_options = VlmPipelineOptions(
        vlm_options=vlm_options,
        enable_remote_services=True,
    )
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
                pipeline_cls=VlmPipeline,
            )
        }
    )


def extract(pdf_path: str) -> dict:
    """
    Convert PDF to DoclingDocument; export to JSON and Markdown.
    Returns dict with docling_document (dict) and docling_markdown (str).
    Requires RUNPOD_API_KEY and RUNPOD_GRANITE_ENDPOINT_ID.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    api_key = os.environ.get("RUNPOD_API_KEY", "")
    endpoint_id = os.environ.get("RUNPOD_GRANITE_ENDPOINT_ID", "")
    if not api_key or not endpoint_id:
        raise ValueError(
            "RUNPOD_API_KEY and RUNPOD_GRANITE_ENDPOINT_ID must be set. "
            "Deploy the Granite Docling endpoint via docker/runpod/granite-docling/."
        )

    converter = _make_runpod_converter()
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
