"""Kiểm thử đơn vị cho gói `nlpvi`, tính toàn vẹn dữ liệu và độ tái lập. Chạy:  pytest -q"""
import unicodedata

import pandas as pd
import pytest

from nlpvi import (DATA_DIR, LABELS, ViSegmenter, load_faq, load_hard, load_reviews, load_splits,
                   normalize, segment, split_sentences, strip_accents)
from nlpvi.retrieval import BM25, metrics_for, rank_from_scores, rrf, search_tokens


# ---------- văn bản ----------
def test_normalize_giu_nguyen_so():
    """Hồi quy: phiên bản đầu gộp chữ số lặp và biến 1000 thành 10."""
    assert "1000" in normalize("Giá 1000 đồng")
    assert "500000" in normalize("Tổng 500000 đồng")


def test_normalize_gop_chu_cai_keo_dai():
    assert normalize("ngonnnnn quááááá") == "ngon quá"


def test_normalize_dua_ve_nfc():
    nfd = unicodedata.normalize("NFD", "tiếng việt")
    assert nfd != "tiếng việt"
    assert normalize(nfd) == "tiếng việt"


def test_normalize_che_thong_tin_nhay_cam():
    out = normalize("Gọi 0912 345 678, mail abc@gmail.com, xem https://x.vn @shop")
    assert "0912" not in out and "abc@" not in out and "https" not in out and "@shop" not in out
    assert all(tok in out for tok in ["sdt", "email", "url", "user"])


def test_normalize_mo_rong_teencode():
    assert normalize("sp ko dc") == "sản phẩm không được"


def test_strip_accents():
    assert strip_accents("Đường Nguyễn Huệ") == "Duong Nguyen Hue"


def test_split_sentences():
    assert split_sentences("Tốt. Giao nhanh! Giá 3.5 triệu thôi.") == ["Tốt.", "Giao nhanh!", "Giá 3.5 triệu thôi."]


def test_split_sentences_khong_phu_thuoc_chu_hoa():
    """Hồi quy: phiên bản đầu dùng [A-ZÀ-Ỵ] (dải này chứa cả chữ thường có dấu) nên chỉ tách đúng khi câu sau viết hoa
    hoặc bắt đầu bằng chữ có dấu; văn bản đã hạ chữ thường bị tách sai/bỏ sót."""
    assert split_sentences("giao hàng nhanh. sẽ ủng hộ tiếp.") == ["giao hàng nhanh.", "sẽ ủng hộ tiếp."]
    assert split_sentences("tốt. đóng gói đẹp. mình hài lòng.") == ["tốt.", "đóng gói đẹp.", "mình hài lòng."]
    assert len(split_sentences(normalize("Mình dùng một tuần rồi. Giao hàng rất chậm. Đóng gói ẩu."))) == 3
    assert split_sentences("Giá 3.5 triệu, 1.500.000 đồng.") == ["Giá 3.5 triệu, 1.500.000 đồng."]       # dấu chấm trong số không tách


# ---------- tách từ ----------
def test_segment_ghep_tu():
    assert segment("Học sinh đang học xử lý ngôn ngữ tự nhiên .") == "Học_sinh đang học xử_lý ngôn_ngữ tự_nhiên ."


def test_segmenter_uu_tien_cum_dai_nhat():
    seg = ViSegmenter(["chăm_sóc", "chăm_sóc_khách_hàng", "khách_hàng"], max_syllables=5)
    assert seg.segment_tokens(["chăm", "sóc", "khách", "hàng"]) == ["chăm_sóc_khách_hàng"]
    assert ViSegmenter(["chăm_sóc"], 4).segment_tokens(["chăm", "sóc", "khách"]) == ["chăm_sóc", "khách"]


# ---------- dữ liệu ----------
def test_reviews_toan_ven():
    df = load_reviews()
    assert list(df.columns) == ["id", "text", "label", "domain", "split"]
    assert len(df) == 1800 and df["id"].is_unique and not df.isna().any().any()
    assert set(df["label"]) == set(LABELS)
    assert df["text"].str.count(r"\?").sum() == 0, "ký tự '?' hàng loạt = dấu hiệu hỏng mã hóa tiếng Việt"
    assert df["text"].map(lambda t: any(ord(c) > 127 for c in t)).mean() > 0.5, "thiếu ký tự tiếng Việt"


def test_chia_tap_khong_chong_lan():
    tr, va, te = load_splits()
    ids = [set(d["id"]) for d in (tr, va, te)]
    assert not (ids[0] & ids[1]) and not (ids[0] & ids[2]) and not (ids[1] & ids[2])
    assert len(tr) + len(va) + len(te) == 1800
    assert 0.65 < len(tr) / 1800 < 0.75


def test_van_ban_khong_co_ky_tu_dieu_khien_hay_cong_thuc_vo():
    """Hồi quy: viết "\\frac", "\\alpha", "\\text" trong chuỗi Python thường làm \\f, \\a, \\t thành ký tự điều khiển/tab, công thức LaTeX
    thành "rac{", "lpha"... (từng lọt vào docs/CAU_HOI_ON_TAP.md và một nguồn đáp án). Quét mọi tệp văn bản của kho."""
    import re
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    bo_qua = {".git", ".venv", "outputs", "__pycache__", ".pytest_cache"}
    dieu_khien = re.compile("[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
    manh_vo = re.compile(r"(?<![A-Za-z\\])(rac\{|lpha\b|ight[)\]|.]|imes\b|heta\b|ext\{|abla\b)")
    cong_thuc = re.compile(r"\$[^$\n]{1,300}\$")
    loi = []
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".md", ".nbsrc", ".py"} or any(x in bo_qua for x in p.parts):
            continue
        text = p.read_text(encoding="utf-8")
        if dieu_khien.search(text):
            loi.append(f"{p.relative_to(root)}: có ký tự điều khiển")
        for i, line in enumerate(text.split("\n"), 1):
            for m in cong_thuc.finditer(line):
                if "\t" in m.group() or "\r" in m.group() or manh_vo.search(m.group()):
                    loi.append(f"{p.relative_to(root)}:{i}: công thức nghi vấn {m.group()[:60]!r}")
    assert not loi, "\n".join(loi)


def test_du_lieu_bai_19_toan_ven():
    """Bộ tóm tắt và dịch mini (Bài 19): đủ số mẫu, id duy nhất, mỗi mẫu có đúng hai tham chiếu không rỗng, đúng 5 câu mỗi đoạn."""
    import json
    tt = json.loads((DATA_DIR / "tom_tat_mini.json").read_text(encoding="utf-8"))
    assert len(tt) == 16 and len({d["id"] for d in tt}) == 16
    for d in tt:
        assert len(split_sentences(d["text"])) == 5, d["id"]
        assert d["tom_tat_a"].strip() and d["tom_tat_b"].strip() and d["tom_tat_a"] != d["tom_tat_b"], d["id"]
        assert len(d["tom_tat_a"]) < len(d["text"]) / 2, d["id"]                      # tóm tắt thật sự ngắn hơn đoạn
    dich = json.loads((DATA_DIR / "dich_mini.json").read_text(encoding="utf-8"))
    assert len(dich) == 24 and len({d["id"] for d in dich}) == 24
    for d in dich:
        assert d["en"].strip() and len(d["vi"]) == 2 and all(v.strip() for v in d["vi"]), d["id"]
        assert not any(ord(c) > 0x2FFF for c in "".join(d["vi"])), d["id"]             # không lẫn chữ Hán/ký tự lạ
    assert all("?" not in "".join(d["vi"]) or d["en"].endswith("?") for d in dich)


def test_tap_cau_kho():
    h = load_hard()
    assert len(h) == 40 and set(h["label"]) <= set(LABELS) and h["hien_tuong"].notna().all()


def test_faq_dap_an_ton_tai():
    docs, queries = load_faq()
    ids = {d["id"] for d in docs}
    assert len(docs) == 24 and len(queries) == 33
    assert all(set(q["gold"]) <= ids for q in queries)


def test_tu_ghep_tep():
    words = (DATA_DIR / "tu_ghep_phobert.txt").read_text(encoding="utf-8").splitlines()
    assert len(words) > 20000 and all("_" in w for w in words)


def test_bo_sinh_du_lieu_tai_lap_duoc(tmp_path, monkeypatch):
    """Chạy lại tools/make_data.py (seed cố định) phải cho tệp y hệt tệp đang có."""
    import make_data
    out = tmp_path / "reviews_vi.csv"
    monkeypatch.setattr(make_data, "OUT", out)
    make_data.main()
    assert out.read_bytes() == (DATA_DIR / "reviews_vi.csv").read_bytes()


# ---------- truy hồi ----------
def test_metrics_for_vi_du_tay():
    m = metrics_for([0, 2, 1, 4, 3], gold=[2, 4], ks=(1, 3, 5))
    assert m["hit@1"] == 0 and m["hit@3"] == 1
    assert m["recall@3"] == pytest.approx(0.5) and m["recall@5"] == pytest.approx(1.0)
    assert m["mrr"] == pytest.approx(0.5)


def test_bm25_xep_dung_tai_lieu():
    docs = ["giao hàng nhanh đóng gói đẹp", "ứng dụng hay treo rất chậm", "món ăn ngon giá hợp lý"]
    bm = BM25([search_tokens(d, word_level=False) for d in docs])
    assert rank_from_scores(bm.scores(search_tokens("ứng dụng treo", word_level=False)))[0] == 1
    assert rank_from_scores(bm.scores(search_tokens("món ăn ngon", word_level=False)))[0] == 2


def test_rrf_hop_nhat_hang():
    assert rrf([[0, 1, 2], [1, 0, 2]])[:2] in ([0, 1], [1, 0])        # hai hạng đầu là 0 và 1 (đối xứng)
    assert rrf([[3, 1], [3, 2]])[0] == 3                                # đồng thuận ở hạng 1 thắng
