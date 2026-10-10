"""Kiểm thử hành vi (CheckList) cho bộ phân loại cảm xúc TF-IDF của Bài 14. Chạy:  pytest -q

Cần mô hình đã lưu bởi notebook Bài 14: outputs/tfidf_lr.joblib (tự bỏ qua nếu chưa có).
Ngưỡng = mức hiện tại cộng biên an toàn. Các ca đã biết là yếu (phủ định) KHÔNG đưa vào đây.
"""
import numpy as np
import pytest

from nlpvi import ROOT

MODEL_PATH = ROOT / "outputs" / "tfidf_lr.joblib"
NGUONG = {"khen đơn giản": 0.15, "chê đơn giản": 0.20, "thêm 'ạ'": 0.02, "thêm 'luôn'": 0.02}


@pytest.fixture(scope="module")
def mo_hinh():
    if not MODEL_PATH.exists():
        pytest.skip("chưa có outputs/tfidf_lr.joblib — hãy chạy notebook Bài 14 (mục 2)")
    import joblib
    return joblib.load(MODEL_PATH)


def _cap():
    from make_data import ASPECTS
    return [(s, pa, na) for dom in ASPECTS.values() for s, pa, na in dom]


def test_khen_don_gian(mo_hinh):
    khen = [f"{s} {a}" for s, pa, _ in _cap() for a in pa]
    assert np.mean(mo_hinh.predict(khen) != "tích cực") <= NGUONG["khen đơn giản"]


def test_che_don_gian(mo_hinh):
    che = [f"{s} {a}" for s, _, na in _cap() for a in na]
    assert np.mean(mo_hinh.predict(che) != "tiêu cực") <= NGUONG["chê đơn giản"]


@pytest.mark.parametrize("hau_to", ["ạ", "luôn"])
def test_bat_bien_hau_to(mo_hinh, hau_to):
    goc = [f"{s} {a}" for s, pa, na in _cap() for a in pa + na]
    doi = np.mean(mo_hinh.predict(goc) != mo_hinh.predict([f"{x} {hau_to}" for x in goc]))
    assert doi <= NGUONG[f"thêm '{hau_to}'"]


def test_du_doan_hop_le(mo_hinh):
    """Mọi nhãn dự đoán thuộc tập nhãn đã biết và xác suất cộng bằng 1."""
    p = mo_hinh.predict_proba(["giao hàng nhanh", "ứng dụng hay treo", "mình mới nhận hàng"])
    assert set(mo_hinh.classes_) == {"tích cực", "tiêu cực", "trung tính"}
    assert np.allclose(p.sum(axis=1), 1.0)
