"""Kiểm thử lõi dự đoán và API của Bài 14 (app/). Không cần mô hình thật: dùng một pipeline nhỏ huấn luyện ngay trong kiểm thử.
Phần API tự bỏ qua nếu chưa cài fastapi/httpx.  Chạy:  pytest -q"""
import pytest

from app import du_doan


@pytest.fixture()
def mo_hinh_nho(tmp_path, monkeypatch):
    """Huấn luyện TF-IDF + LR trên 6 câu, lưu ra tệp tạm và trỏ MODEL_PATH tới đó."""
    try:                                   # bắt cả lỗi nạp DLL (ví dụ bị Application Control chặn), không chỉ thiếu gói
        import joblib
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
    except ImportError as e:
        pytest.skip(f"không nạp được scikit-learn/joblib: {e}")
    texts = ["giao hàng nhanh rất tốt", "sản phẩm tuyệt vời", "hài lòng", "giao hàng chậm rất tệ", "sản phẩm lỗi thất vọng", "quá tệ"]
    y = ["tích cực", "tích cực", "tích cực", "tiêu cực", "tiêu cực", "tiêu cực"]
    pipe = make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=200)).fit(texts, y)
    f = tmp_path / "tfidf_lr.joblib"
    joblib.dump(pipe, f)
    monkeypatch.setattr(du_doan, "MODEL_PATH", f)
    du_doan._load_model.cache_clear()
    yield f
    du_doan._load_model.cache_clear()


def test_che_pii_de_ghi_log():
    out = du_doan.che_pii_de_ghi_log("Gọi 0912 345 678 hoặc mail lan.nguyen@gmail.com, mã đơn 1234567890123")
    assert "0912" not in out and "lan.nguyen" not in out and "1234567890123" not in out
    assert "<SDT>" in out and "<EMAIL>" in out and "<SO_DAI>" in out


def test_predict_khi_chua_co_mo_hinh(tmp_path, monkeypatch):
    monkeypatch.setattr(du_doan, "MODEL_PATH", tmp_path / "khong_co.joblib")
    du_doan._load_model.cache_clear()
    with pytest.raises(du_doan.ModelNotFound):
        du_doan.predict("giao hàng nhanh")
    du_doan._load_model.cache_clear()


def test_predict_tra_ve_nhan_va_xac_suat(mo_hinh_nho):
    kq = du_doan.predict("giao hàng nhanh rất tốt")
    assert kq["nhan"] == "tích cực"
    assert set(kq["xac_suat"]) == {"tích cực", "tiêu cực"} and abs(sum(kq["xac_suat"].values()) - 1) < 1e-3
    assert kq["do_tin_cay"] == max(kq["xac_suat"].values())


@pytest.mark.parametrize("vao", ["", "   ", None, 123])
def test_predict_tu_choi_dau_vao_rong_hoac_sai_kieu(mo_hinh_nho, vao):
    with pytest.raises(ValueError):
        du_doan.predict(vao)


def test_predict_cat_van_ban_qua_dai(mo_hinh_nho):
    kq = du_doan.predict("tệ " * 5000)                      # 15.000 ký tự > MAX_CHARS, không được đổ vỡ
    assert kq["nhan"] in ("tích cực", "tiêu cực")


# ---------- API ----------
@pytest.fixture()
def client():
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient
    from app.api import app
    return TestClient(app)


def test_api_suc_khoe(client):
    r = client.get("/suc-khoe")
    assert r.status_code == 200 and r.json() == {"trang_thai": "ok"}


def test_api_du_doan_thanh_cong(client, mo_hinh_nho):
    r = client.post("/du-doan", json={"van_ban": "sản phẩm tuyệt vời, hài lòng"})
    assert r.status_code == 200
    assert r.json()["nhan"] == "tích cực" and "xac_suat" in r.json()


def test_api_503_khi_chua_co_mo_hinh(client, tmp_path, monkeypatch):
    monkeypatch.setattr(du_doan, "MODEL_PATH", tmp_path / "khong_co.joblib")
    du_doan._load_model.cache_clear()
    assert client.post("/du-doan", json={"van_ban": "giao hàng nhanh"}).status_code == 503
    du_doan._load_model.cache_clear()


@pytest.mark.parametrize("body", [{"van_ban": ""}, {"van_ban": "x" * 2001}, {}, {"khac": "gì đó"}])
def test_api_422_khi_dau_vao_khong_hop_le(client, mo_hinh_nho, body):
    assert client.post("/du-doan", json=body).status_code == 422


def test_api_khong_ghi_van_ban_goc_chua_so_dien_thoai(client, mo_hinh_nho, caplog):
    import logging
    with caplog.at_level(logging.INFO, logger="api"):
        client.post("/du-doan", json={"van_ban": "giao hàng nhanh, gọi 0912345678"})
    nhat_ky = " ".join(r.getMessage() for r in caplog.records)
    assert "0912345678" not in nhat_ky and "<SDT>" in nhat_ky
