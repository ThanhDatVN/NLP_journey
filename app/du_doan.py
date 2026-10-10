"""Lõi dự đoán dùng chung cho API và demo (Bài 14).

Mô hình mặc định: TF-IDF + Logistic Regression do notebook Bài 14 huấn luyện và lưu ở
outputs/tfidf_lr.joblib. Để dùng PhoBERT đã tinh chỉnh ở Bài 10, thay `_load_model` và
`predict` bằng phiên bản gọi `AutoModelForSequenceClassification` (xem Bài 10, mục 10).
"""
import re
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from nlpvi import normalize  # noqa: E402

MODEL_PATH = ROOT / "outputs" / "tfidf_lr.joblib"
MAX_CHARS = 2000      # giới hạn đầu vào: tránh văn bản quá dài làm chậm/đổ vỡ dịch vụ


class ModelNotFound(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _load_model():
    if not MODEL_PATH.exists():
        raise ModelNotFound(f"Chưa có mô hình tại {MODEL_PATH}. Hãy chạy notebook Bài 14 (mục 5) để huấn luyện và lưu.")
    import joblib
    return joblib.load(MODEL_PATH)


def predict(text: str) -> dict:
    """Trả về {'nhan': ..., 'xac_suat': {lớp: p}, 'do_tin_cay': p cao nhất}."""
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Văn bản rỗng")
    text = text[:MAX_CHARS]
    pipe = _load_model()
    probs = pipe.predict_proba([normalize(text)])[0]
    classes = list(pipe.classes_)
    best = max(range(len(classes)), key=lambda i: probs[i])
    return {"nhan": classes[best], "xac_suat": {c: round(float(p), 4) for c, p in zip(classes, probs)},
            "do_tin_cay": round(float(probs[best]), 4)}


def che_pii_de_ghi_log(text: str) -> str:
    """Che số điện thoại, email, dãy số dài (ghi log KHÔNG được chứa dữ liệu cá nhân thô)."""
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<EMAIL>", text)
    text = re.sub(r"(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){9}(?!\d)", "<SDT>", text)
    return re.sub(r"\d{9,}", "<SO_DAI>", text)
