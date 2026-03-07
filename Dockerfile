FROM python:3.12-slim

WORKDIR /app

# Docling needs libxcb, libGL, and libglib for headless rendering (matplotlib, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# docling[vlm] for VlmPipeline with remote RunPod Granite serverless (no local OCR)
RUN pip install --no-cache-dir "docling[vlm]" fastapi uvicorn

COPY extract.py app.py /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
