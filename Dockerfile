# Python gọn nhẹ
FROM python:3.11-slim

# Tăng tốc & gọn pip cache
ENV PIP_NO_CACHE_DIR=1

# Thư mục làm việc
WORKDIR /app

# Cài công cụ build + git (cần để pip clone repo private)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
 && rm -rf /var/lib/apt/lists/*

# Cài Python deps trước để tận dụng cache
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# --- CÀI FiinQuantX (PRIVATE) BẰNG TOKEN) ---
# Render sẽ cung cấp biến môi trường trong lúc build, ta map sang ARG rồi dùng
ARG GITHUB_TOKEN
ENV GITHUB_TOKEN=${GITHUB_TOKEN}

# Fail sớm nếu thiếu token; sau đó cài từ private repo
RUN test -n "$GITHUB_TOKEN" \
 && pip install "git+https://${GITHUB_TOKEN}@github.com/fiinlab/fiinquantx.git@main#egg=FiinQuantX"

# Copy toàn bộ code app
COPY . .

# Cổng chuẩn cho Render
ENV PORT=10000
EXPOSE 10000

# Chạy app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
