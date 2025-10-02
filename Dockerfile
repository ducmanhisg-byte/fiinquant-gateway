FROM python:3.11-slim

# Cài công cụ build cơ bản
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Nâng pip và cấu hình index của FiinQuant
RUN python -m pip install --upgrade pip
RUN pip config set global.extra-index-url https://fiinquant.github.io/fiinquantx/simple

# Cài thư viện cần thiết
# Cài thư viện cần thiết (đã ghim phiên bản để tương thích)
RUN pip install \
    fastapi==0.115.0 \
    uvicorn[standard]==0.30.6 \
    numpy==1.26.4 \
    pandas==2.2.2 \
    scipy==1.11.4 \
    numba==0.58.1 \
    llvmlite==0.41.1 \
    fastdtw \
    stumpy==1.12.0 \
    fiinquantx

# Chép mã ứng dụng
WORKDIR /app
COPY server.py /app/server.py

# Cổng & lệnh chạy
ENV PORT=8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
