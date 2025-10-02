FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential gcc g++ \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip

# Cài các gói KHÔNG bao gồm dòng git của FiinQuantX trong requirements.txt
# (Hãy xóa dòng git đó khỏi requirements.txt, chỉ giữ các lib khác: fastapi, uvicorn, plotly, stumpy, v.v.)
RUN pip install -r requirements.txt

# Cài FiinQuantX từ GitHub private bằng token build-time
ARG GITHUB_TOKEN
# Render sẽ đưa env vào build-time; để chắc ăn, ta tham chiếu cả ENV lẫn ARG
ENV GITHUB_TOKEN=${GITHUB_TOKEN}
RUN test -n "$GITHUB_TOKEN" && \
    pip install "git+https://${GITHUB_TOKEN}@github.com/fiinlab/fiinquantx.git@main#egg=FiinQuantX"

COPY . .
ENV PORT=10000
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "${PORT}"]
