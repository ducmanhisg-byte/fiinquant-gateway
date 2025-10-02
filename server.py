# server.py
import os
import importlib
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Header, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

APP_NAME = "fiinquant-api"

# Đặt API key:
# - Bạn có thể set biến môi trường API_KEY trên Render
# - Nếu chưa set, mặc định dùng key bạn đưa: "MyFiin-Key_2025_x3W9pQ"
API_KEY = os.getenv("API_KEY", "MyFiin-Key_2025_x3W9pQ")

app = FastAPI(title=APP_NAME, version="1.0.0")

# CORS (tuỳ chỉnh domain của bạn nếu cần)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nên hạn chế origin trong production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Healthcheck cực nhẹ (Render gọi endpoint này khi khởi động) ----
@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME}

# ---- Root ----
@app.get("/")
def root():
    return {"message": f"Welcome to {APP_NAME}. See /docs for OpenAPI UI."}

# ---- API-Key guard ----
def require_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-KEY")
    return True

# ---- Lazy import FiinQuantX để tránh timeout khi khởi động ----
_fq = None
def get_fq():
    """
    Import FiinQuantX khi CẦN DÙNG (lazy-load).
    Lần gọi đầu có thể chậm hơn, nhưng app đã sẵn sàng và không bị Render cắt.
    """
    global _fq
    if _fq is None:
        _fq = importlib.import_module("FiinQuantX")
    return _fq

# =============== Demo Endpoints ===============

@app.get("/similar-chart")
def similar_chart(
    symbol: str = Query(..., description="Mã cổ phiếu, ví dụ: VNM"),
    _=Depends(require_api_key),
):
    """
    Ví dụ endpoint gọi chức năng SimilarChart trong FiinQuantX.
    Tùy bản FiinQuantX, đổi tên hàm/param tương ứng nếu cần.
    """
    fq = get_fq()
    try:
        # Ví dụ minh hoạ: tuỳ vào API thực tế của FiinQuantX bạn đang dùng
        result = fq.SimilarChart(symbol)
        return JSONResponse({"symbol": symbol, "data": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SimilarChart error: {e}")

@app.get("/ohlcv")
def ohlcv(
    symbol: str = Query(..., description="Mã cổ phiếu"),
    start: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end: Optional[str] = Query(None, description="YYYY-MM-DD"),
    _=Depends(require_api_key),
):
    """
    Ví dụ endpoint lấy OHLCV. Thay nội dung cho khớp FiinQuantX của bạn.
    """
    fq = get_fq()
    try:
        # Ví dụ: giả sử FiinQuantX có hàm FiinQuant.get_ohlcv(symbol, start, end)
        if hasattr(fq, "FiinQuant"):
            data = fq.FiinQuant.get_ohlcv(symbol, start_date=start, end_date=end)
        else:
            # Fallback placeholder nếu API khác
            data = {"note": "Please replace with actual FiinQuantX OHLCV function."}
        return JSONResponse({"symbol": symbol, "start": start, "end": end, "data": data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OHLCV error: {e}")
