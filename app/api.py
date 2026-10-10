"""API phân loại cảm xúc bằng FastAPI.

Chạy:   uvicorn app.api:app --port 8000
Thử:    curl -X POST localhost:8000/du-doan -H "Content-Type: application/json" -d '{"van_ban": "Giao hàng nhanh, rất hài lòng"}'
Yêu cầu: pip install -r app/requirements-app.txt
"""
import logging
import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.du_doan import ModelNotFound, che_pii_de_ghi_log, predict

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("api")

app = FastAPI(title="API phân loại cảm xúc tiếng Việt", version="1.0")


class YeuCau(BaseModel):
    van_ban: str = Field(..., min_length=1, max_length=2000, description="Đánh giá cần phân loại")


@app.get("/suc-khoe")
def suc_khoe():
    return {"trang_thai": "ok"}


@app.post("/du-doan")
def du_doan(req: YeuCau):
    t0 = time.perf_counter()
    try:
        kq = predict(req.van_ban)
    except ModelNotFound as e:
        raise HTTPException(status_code=503, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    # Ghi log: KHÔNG ghi văn bản gốc (có thể chứa dữ liệu cá nhân); chỉ ghi bản đã che và số liệu vận hành.
    log.info("du_doan nhan=%s tin_cay=%.3f do_dai=%d ms=%.1f van_ban_da_che=%r", kq["nhan"], kq["do_tin_cay"],
             len(req.van_ban), (time.perf_counter() - t0) * 1000, che_pii_de_ghi_log(req.van_ban)[:80])
    return kq
