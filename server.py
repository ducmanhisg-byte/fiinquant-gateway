
import os
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import JSONResponse
import uvicorn
import FiinQuantX as fq

APP_API_KEY = os.environ.get("APP_API_KEY")
FIIN_USER = os.environ.get("FIIN_USER")
FIIN_PASS = os.environ.get("FIIN_PASS")

if not APP_API_KEY or not FIIN_USER or not FIIN_PASS:
    raise RuntimeError("Missing required environment variables: APP_API_KEY, FIIN_USER, FIIN_PASS")

app = FastAPI(title="FiinQuant Mini Gateway", version="1.0.0")

# Login once when server starts
client = fq.FiinSession(username=FIIN_USER, password=FIIN_PASS).login()

def check_key(x_api_key: str | None):
    if (APP_API_KEY and (not x_api_key or x_api_key != APP_API_KEY)):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/history")
def history(symbol: str, period: int = 30, x_api_key: str | None = Header(default=None)):
    """
    Get daily history for a symbol (last N sessions).
    Use request header: x-api-key: <APP_API_KEY>
    Example: /history?symbol=HPG&period=30
    """
    check_key(x_api_key)
    try:
        df = client.Fetch_Trading_Data(
            realtime=False,
            tickers=[symbol.upper()],
            fields=['open','high','low','close','volume'],
            by='1d',
            period=period
        ).get_data()
        return JSONResponse(content=df.to_dict(orient="records"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")), reload=False)
