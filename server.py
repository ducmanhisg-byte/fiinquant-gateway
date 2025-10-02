# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

# Healthcheck siêu nhẹ cho Render
@app.get("/health")
def health():
    return {"status": "ok"}

# Biến toàn cục để lưu module sau khi import
_fq = None
def get_fq():
    global _fq
    if _fq is None:
        import importlib
        _fq = importlib.import_module("FiinQuantX")  # <- import tại đây
    return _fq

# Ví dụ 1 endpoint dùng FiinQuantX
@app.get("/similar-chart")
def similar_chart(symbol: str):
    fq = get_fq()
    try:
        # gọi hàm của FiinQuantX như bình thường
        data = fq.SimilarChart(symbol)  # ví dụ minh họa
        return JSONResponse({"symbol": symbol, "data": data})
    except Exception as e:
        raise HTTPException(500, f"SimilarChart error: {e}")
