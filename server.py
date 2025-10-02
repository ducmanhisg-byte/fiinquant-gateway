from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

# Import FiinQuantX sau khi container đã cài xong package
try:
    import FiinQuantX as fq  # noqa: F401
except Exception as e:
    # Không crash app nếu import lỗi, để còn đọc log
    print("Warning: cannot import FiinQuantX:", e)

@app.get("/")
def root():
    return {"message": "FiinQuant API is alive"}
