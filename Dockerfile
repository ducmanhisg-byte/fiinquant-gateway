# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Thêm gói hệ thống tối thiểu (nếu cần cho numpy/scipy). Thử tối giản trước:
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cài dependencies trước để tận dụng layer cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy code
COPY . .

# Render sẽ set biến PORT. Mặc định local 8000
CMD sh -c 'uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}'
