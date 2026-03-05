# docker-docling

Docling PDF/document extraction API. FastAPI service that converts PDFs to DoclingDocument and exports JSON and Markdown. RunPod-friendly.

## API

- **POST /extract** – JSON body `{filename, document_id}`. Expects PDF at `DATA_DIR/filename`, returns `docling_document` and `docling_markdown`.
- **GET /health** – Health check.

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `DOCLING_DATA_DIR` | `/workspace` | Directory containing PDFs (mount volume here) |

## Build

```bash
docker build --platform linux/amd64 -t ghcr.io/christhompsontldr/docker-docling:latest .
```

## Run (local)

```bash
docker run -p 8000:8000 \
  -v /path/to/pdfs:/workspace:ro \
  ghcr.io/christhompsontldr/docker-docling:latest
```

## License

MIT
