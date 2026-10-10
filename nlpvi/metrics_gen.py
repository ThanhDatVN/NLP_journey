"""Độ đo đánh giá sinh văn bản, cài từ đầu: ROUGE-N, ROUGE-L, BLEU (nhiều tham chiếu, có làm mịn) và chrF.

Bản hoàn chỉnh của những gì Bài 19 xây từng bước. Đầu vào ROUGE/BLEU là danh sách *token đã tách sẵn* (cách tách token
quyết định điểm số! xem Bài 19); chrF làm việc trên chuỗi ký tự. BLEU và chrF trả về thang 0–100 như thông lệ, ROUGE thang 0–1.
Đã đối chiếu số liệu với `sacrebleu` và `rouge-score` (xem tests/test_metrics_gen.py).
"""
import math
from collections import Counter


def ngrams(tokens, n: int) -> Counter:
    """Đếm n-gram (tuple) của một danh sách token."""
    return Counter(tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1))


def _prf(match: int, n_hyp: int, n_ref: int, beta: float = 1.0) -> dict:
    p = match / n_hyp if n_hyp else 0.0
    r = match / n_ref if n_ref else 0.0
    b2 = beta ** 2
    f = (1 + b2) * p * r / (b2 * p + r) if (b2 * p + r) else 0.0
    return {"p": p, "r": r, "f": f}


def rouge_n(ref, hyp, n: int = 1) -> dict:
    """ROUGE-N giữa một tham chiếu và một đầu ra (đều là list token): precision, recall, F1 của số n-gram trùng (có cắt theo số lần xuất hiện)."""
    gr, gh = ngrams(ref, n), ngrams(hyp, n)
    match = sum(min(c, gr[g]) for g, c in gh.items())
    return _prf(match, sum(gh.values()), sum(gr.values()))


def lcs_length(a, b) -> int:
    """Độ dài chuỗi con chung dài nhất (không nhất thiết liên tiếp), quy hoạch động O(len(a)·len(b))."""
    if not a or not b:
        return 0
    truoc = [0] * (len(b) + 1)
    for x in a:
        hien = [0]
        for j, y in enumerate(b):
            hien.append(truoc[j] + 1 if x == y else max(truoc[j + 1], hien[j]))
        truoc = hien
    return truoc[-1]


def rouge_l(ref, hyp) -> dict:
    """ROUGE-L (mức câu): dựa trên chuỗi con chung dài nhất, nên nhạy với *thứ tự* từ."""
    return _prf(lcs_length(ref, hyp), len(hyp), len(ref))


def rouge_nhieu_tham_chieu(refs, hyp, ham=rouge_n, **kw) -> dict:
    """Với nhiều tham chiếu, lấy tham chiếu cho F1 cao nhất (cách của `rouge-score`)."""
    return max((ham(r, hyp, **kw) for r in refs), key=lambda d: d["f"])


# ---------------- BLEU ----------------
def bleu(refs, hyps, max_n: int = 4, smooth: str = "none") -> dict:
    """BLEU mức *corpus*. refs[i] là list các tham chiếu của câu i (mỗi tham chiếu là list token); hyps[i] là list token.

    smooth: "none" (không làm mịn: bằng 0 nếu một bậc n-gram không trùng) hoặc "exp" (làm mịn kiểu NIST/mteval, mặc định của sacreBLEU).
    Trả về dict: score (0–100), precisions (%), bp (phạt ngắn), sys_len, ref_len.
    """
    dung, tong = [0] * max_n, [0] * max_n
    sys_len = ref_len = 0
    for rs, h in zip(refs, hyps):
        sys_len += len(h)
        ref_len += min((abs(len(r) - len(h)), len(r)) for r in rs)[1]          # độ dài tham chiếu gần nhất (hòa → ngắn hơn)
        for n in range(1, max_n + 1):
            gh = ngrams(h, n)
            tran = Counter()
            for r in rs:
                for g, c in ngrams(r, n).items():
                    tran[g] = max(tran[g], c)                                   # cắt theo số lần tối đa ở bất kỳ tham chiếu nào
            dung[n - 1] += sum(min(c, tran[g]) for g, c in gh.items())
            tong[n - 1] += sum(gh.values())
    bp = 1.0 if sys_len >= ref_len else (math.exp(1 - ref_len / sys_len) if sys_len else 0.0)
    prec = [0.0] * max_n
    if any(dung):
        mu = 1.0
        for i in range(max_n):
            if tong[i] == 0:
                break
            if dung[i] == 0:
                if smooth == "exp":
                    mu *= 2
                    prec[i] = 100.0 / (mu * tong[i])
            else:
                prec[i] = 100.0 * dung[i] / tong[i]
        score = bp * math.exp(sum(math.log(p) if p > 0 else -9999999999 for p in prec) / max_n)
    else:
        score = 0.0
    return {"score": score, "precisions": prec, "bp": bp, "sys_len": sys_len, "ref_len": ref_len}


# ---------------- chrF ----------------
def _thong_ke_chrf(ref: str, hyp: str, bac_ky_tu: int) -> list:
    r, h = "".join(ref.split()), "".join(hyp.split())                           # bỏ khoảng trắng như sacreBLEU mặc định
    out = []
    for n in range(1, bac_ky_tu + 1):
        gr, gh = ngrams(list(r), n), ngrams(list(h), n)
        out.append((sum(gh.values()), sum(gr.values()), sum(min(c, gr[g]) for g, c in gh.items())))
    return out


def _f_chrf(thong_ke, beta: float) -> float:
    """F-beta của precision và recall *trung bình qua các bậc* n-gram (chỉ tính bậc mà cả hai phía còn n-gram), đúng định nghĩa chrF gốc."""
    b2, tp, tr, k = beta ** 2, 0.0, 0.0, 0
    for n_hyp, n_ref, n_khop in thong_ke:
        if n_hyp > 0 and n_ref > 0:
            tp += n_khop / n_hyp
            tr += n_khop / n_ref
            k += 1
    if k == 0:
        return 0.0
    p, r = tp / k, tr / k
    return 100.0 * (1 + b2) * p * r / (b2 * p + r) if (p + r) else 0.0


def chrf(refs, hyps, bac_ky_tu: int = 6, beta: float = 2.0) -> float:
    """chrF mức corpus (0–100): F-beta của precision/recall trung bình theo bậc n-gram *ký tự* (beta = 2: recall quan trọng gấp đôi precision).
    refs[i] là list các tham chiếu (chuỗi) của câu i; mỗi câu chọn tham chiếu cho điểm cao nhất."""
    tong = [(0, 0, 0)] * bac_ky_tu
    for rs, h in zip(refs, hyps):
        tk = max((_thong_ke_chrf(r, h, bac_ky_tu) for r in rs), key=lambda s: _f_chrf(s, beta))
        tong = [(a[0] + b[0], a[1] + b[1], a[2] + b[2]) for a, b in zip(tong, tk)]
    return _f_chrf(tong, beta)
