FROM python:3.12-slim

WORKDIR /app

# Docling needs libxcb for headless rendering (matplotlib, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxcb1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir docling fastapi uvicorn

COPY extract.py app.py /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
