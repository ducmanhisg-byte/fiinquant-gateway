
# FiinQuant Mini Gateway (không cần biết code)

Mục tiêu: Tạo 1 "cầu nối" nho nhỏ giữa ChatGPT và FiinQuant. Bạn deploy 1 lần,
sau đó đưa cho mình (ChatGPT) **URL** và **APP_API_KEY** là xong.

## 1) Chuẩn bị
- Tài khoản FiinQuant (username/password).
- Tạo 1 **APP_API_KEY** (chuỗi bí mật, ví dụ: `my-key-123`).
- Hai file: `server.py`, `requirements.txt` (đã kèm ở đây).

## 2) Deploy trên Render (miễn phí)
1. Vào https://render.com → Log in → New → **Web Service**.
2. Kết nối repo GitHub có chứa 2 file này (hoặc tạo repo mới và push 2 file).
3. Thiết lập:
   - **Runtime**: Python 3.x
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. **Environment Variables**:
   - `APP_API_KEY` = chuỗi bí mật bạn tự đặt
   - `FIIN_USER`   = username FiinQuant
   - `FIIN_PASS`   = password FiinQuant
5. Deploy → nhận URL dạng `https://<ten-dich-vu>.onrender.com`

## 3) Kiểm tra nhanh
- `GET /health` → `{ "ok": true }`
- `GET /history?symbol=HPG&period=5` (kèm header `x-api-key: <APP_API_KEY>`)
  - Dùng Postman hoặc:
    ```bash
    curl -H "x-api-key: YOUR_APP_API_KEY" "https://<your-url>/history?symbol=HPG&period=5"
    ```

## 4) Dùng với ChatGPT
Bạn gửi cho mình URL + APP_API_KEY (một lần). Khi bạn hỏi
“HPG hôm nay thế nào?”, mình sẽ gọi endpoint `/history` tương ứng để lấy dữ liệu
và trả lời bạn trong chat.
