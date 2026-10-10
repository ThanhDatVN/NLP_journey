"""Kiểm thử độ đo sinh văn bản (Bài 19). Các giá trị chuẩn lấy từ `sacrebleu` / `rouge-score` (đã đối chiếu 200 trường hợp ngẫu nhiên
nhiều tham chiếu, sai khác ≈ 1e-14) hoặc tính tay. Chạy:  pytest -q"""
import pytest

from nlpvi.metrics_gen import bleu, chrf, lcs_length, ngrams, rouge_l, rouge_n, rouge_nhieu_tham_chieu

REF = "tôi muốn đổi trả hàng".split()
HYP = "tôi muốn trả hàng".split()


def test_ngrams_dem_dung():
    assert ngrams("a b a b".split(), 2) == {("a", "b"): 2, ("b", "a"): 1}
    assert ngrams(["a"], 2) == {}


def test_rouge_n_tinh_tay():
    r1, r2 = rouge_n(REF, HYP, 1), rouge_n(REF, HYP, 2)
    assert (r1["p"], r1["r"], r1["f"]) == pytest.approx((1.0, 0.8, 8 / 9))
    assert (r2["p"], r2["r"], r2["f"]) == pytest.approx((2 / 3, 0.5, 4 / 7))


def test_rouge_cat_theo_so_lan_xuat_hien():
    """Đầu ra lặp một từ nhiều lần không được tính trùng quá số lần từ đó có trong tham chiếu."""
    r = rouge_n("tốt".split(), "tốt tốt tốt tốt".split(), 1)
    assert r["p"] == pytest.approx(0.25) and r["r"] == pytest.approx(1.0)


def test_rouge_l_nhay_voi_thu_tu():
    xuoi = rouge_l("a b c d".split(), "a b c d".split())["f"]
    nguoc = rouge_l("a b c d".split(), "d c b a".split())["f"]
    assert xuoi == 1.0 and nguoc == pytest.approx(0.25)                 # LCS của chuỗi đảo ngược chỉ dài 1
    assert rouge_n("a b c d".split(), "d c b a".split(), 1)["f"] == 1.0   # ROUGE-1 thì không thấy gì


def test_lcs_khong_lien_tiep():
    assert lcs_length("a x b y c".split(), "a b c".split()) == 3
    assert lcs_length([], ["a"]) == 0


def test_rouge_rong_khong_loi():
    assert rouge_n(REF, [], 1)["f"] == 0.0 and rouge_l([], HYP)["f"] == 0.0


def test_rouge_nhieu_tham_chieu_lay_tot_nhat():
    refs = ["a b c d".split(), "x y".split()]
    assert rouge_nhieu_tham_chieu(refs, "x y".split(), rouge_n, n=1)["f"] == 1.0


def test_bleu_giong_het_la_100():
    assert bleu([[REF]], [REF])["score"] == pytest.approx(100.0)


def test_bleu_khong_lam_min_bang_0_khi_thieu_bac_4():
    """Hồi quy kinh điển: câu ngắn thiếu 4-gram trùng cho BLEU = 0 nếu không làm mịn (giá trị từ sacreBLEU)."""
    ref, hyp = "the cat sat on the mat".split(), "the cat is on the mat".split()
    assert bleu([[ref]], [hyp], smooth="none")["score"] == 0.0
    assert bleu([[ref]], [hyp], smooth="exp")["score"] == pytest.approx(37.99178428257963)


def test_bleu_nhieu_tham_chieu_cao_hon():
    r1, r2 = "the cat sat on the mat".split(), "there is a cat on the mat".split()
    hyp = "the cat is on the mat".split()
    assert bleu([[r1, r2]], [hyp], smooth="exp")["score"] == pytest.approx(39.76353643835254)
    assert bleu([[r1, r2]], [hyp], smooth="exp")["score"] > bleu([[r1]], [hyp], smooth="exp")["score"]


def test_bleu_phat_do_dai_ngan():
    out = bleu([["the cat sat on the mat".split()]], ["the cat sat".split()], smooth="none")
    assert out["bp"] == pytest.approx(__import__("math").exp(1 - 6 / 3)) and out["score"] == 0.0     # thiếu 4-gram nên 0


def test_bleu_khong_trung_chu_nao_la_0():
    assert bleu([["v w x y z".split()]], ["a b c d e".split()])["score"] == 0.0


def test_chrf_gia_tri_chuan():
    assert chrf([["tôi muốn đổi trả hàng"]], ["tôi muốn trả hàng"]) == pytest.approx(62.658927057569116)
    assert chrf([["tôi muốn đổi trả hàng", "tôi muốn trả hàng nhanh"]], ["tôi muốn trả hàng"]) == pytest.approx(73.89345307771646)
    assert chrf([["tôi muốn trả hàng"]], ["tôi muốn trả hàng"]) == pytest.approx(100.0)


def test_chrf_bo_qua_khoang_trang():
    assert chrf([["a b c"]], ["abc"]) == pytest.approx(100.0)


def test_bay_tokenizer_ascii_pha_huy_tieng_viet():
    """Tokenizer mặc định của `rouge-score` chỉ giữ [a-z0-9]: tiếng Việt vỡ thành mảnh vô nghĩa, hai câu khác nghĩa vẫn 'trùng'."""
    import re
    tach = lambda t: re.sub(r"[^a-z0-9]+", " ", t.lower()).split()
    assert tach("Người dùng đổi trả hàng trong 7 ngày") == ["ng", "i", "d", "ng", "i", "tr", "h", "ng", "trong", "7", "ng", "y"]
    assert rouge_n(tach("Tôi thích phở"), tach("Tôi ghét bún"), 1)["f"] > 0.3          # hai câu khác nghĩa mà điểm 0,36
