"""Kiểm thử mô hình khôi phục dấu (Bài 17) trên một kho đồ chơi nhỏ, chạy trong chớp mắt. Chạy:  pytest -q"""
import pytest

from nlpvi import strip_accents
from nlpvi.diacritics import DiacriticRestorer, tach_token

CAU = ["tôi bán hàng", "bạn mua hàng", "bạn bè của tôi", "mua bán online", "tôi mua bán hàng",
       "bàn ghế rất đẹp", "tôi bán bàn ghế", "bạn bè rất tốt", "cửa hàng của bạn"]
CORPUS = [tach_token(s) for s in CAU]


@pytest.fixture(scope="module")
def mo_hinh():
    return DiacriticRestorer(bac=3).fit(CORPUS)


def test_tach_token_giu_dau_cau_va_ve_chu_thuong():
    assert tach_token("Tôi  muốn ĐỔI hàng, được không?") == ["tôi", "muốn", "đổi", "hàng", ",", "được", "không", "?"]


def test_tach_token_dua_ve_nfc():
    import unicodedata
    nfd = unicodedata.normalize("NFD", "tiếng việt")
    assert tach_token(nfd) == ["tiếng", "việt"]


def test_ngu_canh_phan_biet_cac_dang_cua_ban(mo_hinh):
    """Cùng dạng không dấu "ban": bán / bạn / bàn, chọn theo ngữ cảnh."""
    assert mo_hinh.restore("toi ban hang") == "tôi bán hàng"
    assert mo_hinh.restore("ban be cua toi") == "bạn bè của tôi"
    assert mo_hinh.restore("ban ghe rat dep") in ("bàn ghế rất đẹp", "bạn ghế rất đẹp")      # chỉ yêu cầu dạng có trong kho


def test_giu_khoang_trang_dau_cau_va_viet_hoa(mo_hinh):
    assert mo_hinh.restore("Toi ban hang!") == "Tôi bán hàng!"
    assert mo_hinh.restore("TOI BAN HANG") == "TÔI BÁN HÀNG"
    assert mo_hinh.restore("toi  ban\nhang .") == "tôi  bán\nhàng ."


def test_khoi_phuc_roi_bo_dau_lai_ra_dung_dau_vao(mo_hinh):
    """Tính chất kênh nhiễu: bỏ dấu của kết quả phải trả đúng văn bản đầu vào (dù đoán sai dấu)."""
    for x in ["toi mua ban hang", "xyz abc 123 toi", "cua hang cua ban!"]:
        assert strip_accents(mo_hinh.restore(x)) == x


def test_am_tiet_chua_thay_duoc_giu_nguyen(mo_hinh):
    assert mo_hinh.restore("xyz 123") == "xyz 123"


def test_bac_1_chon_dang_pho_bien_nhat():
    corpus = [tach_token(s) for s in ["bán bán bán", "bạn"]]
    m = DiacriticRestorer(bac=1).fit(corpus)
    assert m.restore("ban") == "bán"


def test_tu_dien_bo_sung_mo_rong_ung_vien():
    m = DiacriticRestorer().fit(CORPUS)
    assert "chuyển" not in m.candidates("chuyen")
    m2 = DiacriticRestorer().fit(CORPUS, extra_syllables=["chuyển", "chuyên"])
    assert {"chuyển", "chuyên"} <= set(m2.candidates("chuyen"))


def test_nho_lai_cau_da_hoc(mo_hinh):
    """Trên chính kho huấn luyện, trigram phải khôi phục đúng mọi câu (đây là kiểm tra cài đặt, không phải đánh giá)."""
    for s in CORPUS:
        assert mo_hinh.restore_tokens([strip_accents(w) for w in s]) == s


def test_logp_la_xac_suat_hop_le(mo_hinh):
    import math
    for u, v in [("<s>", "<s>"), ("tôi", "bán"), ("chưa", "thấy")]:
        tong = sum(math.exp(mo_hinh.logp(u, v, w)) for w in set(mo_hinh.uni) | {"</s>"})
        assert tong <= 1.0 + 1e-9, (u, v, tong)
