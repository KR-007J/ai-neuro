# Multi-stage build for smaller image size
FROM python:3.10-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

COPY . .

ENV PATH=/root/.local/bin:$PATH

RUN mkdir -p app/models data/raw data/processed

EXPOSE 10000

# ✅ Use curl instead of requests (lighter, already available in slim)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# ✅ Port changed to 10000 for Render
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]