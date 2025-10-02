FROM python:3.11-slim

# Cài hệ thống cơ bản
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Cấu hình pip dùng index của FiinQuant
RUN python -m pip install --upgrade pip
RUN pip config set global.extra-index-url https://fiinquant.github.io/fiinquantx/simple

# Cài thư viện
RUN pip install fastapi==0.115.0 uvicorn[standard]==0.30.6 \
    numpy==1.26.4 pandas==2.2.2 fastdtw fiinquantx

# Sao chép app
WORKDIR /app
COPY server.py /app/server.py

# Thông số chạy
ENV PORT=8000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]
