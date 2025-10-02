FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Cài system deps cần cho build từ source & git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential gcc g++ \
 && rm -rf /var/lib/apt/lists/*

# Cài Python deps trước để tận dụng cache
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code
COPY . .

# Render sẽ đặt PORT, đừng hardcode
ENV PORT=10000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "${PORT}"]
