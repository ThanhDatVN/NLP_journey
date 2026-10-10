"""Khôi phục dấu tiếng Việt bằng mô hình kênh nhiễu: ŷ = argmax_y P(y) với y_i thuộc các dạng có dấu của âm tiết i.

Bản hoàn chỉnh của những gì Bài 17 xây từng bước: từ điển ứng viên (dạng không dấu → các dạng có dấu đã gặp),
mô hình ngôn ngữ trigram nội suy trên âm tiết và giải mã Viterbi trên lưới ứng viên.
"""
import math
import re
from collections import Counter, defaultdict

from .text import normalize_unicode, strip_accents

TOKEN_RE = re.compile(r"\w+|[^\w\s]")


def tach_token(text: str) -> list:
    """Tách thành âm tiết/số/dấu câu, đã đưa về NFC và chữ thường (khớp cách tách của dữ liệu huấn luyện)."""
    return TOKEN_RE.findall(normalize_unicode(text).lower())


def _giu_hoa_thuong(goc: str, moi: str) -> str:
    if goc.isupper() and len(goc) > 1:
        return moi.upper()
    if goc[:1].isupper():
        return moi[:1].upper() + moi[1:]
    return moi


class DiacriticRestorer:
    """Mô hình khôi phục dấu.

    lam: trọng số nội suy (unigram, bigram, trigram); k: hằng số làm mịn add-k cho unigram;
    bac: 1 = chỉ dạng phổ biến nhất của từng âm tiết, 2 = bigram, 3 = trigram.
    """

    def __init__(self, lam=(0.1, 0.4, 0.5), k: float = 0.01, bac: int = 3):
        assert bac in (1, 2, 3)
        self.lam, self.k, self.bac = lam, k, bac
        self.cands = defaultdict(Counter)          # dạng không dấu -> Counter(dạng có dấu)
        self.uni, self.bi, self.tri = Counter(), Counter(), Counter()
        self.bi_ctx, self.tri_ctx = Counter(), Counter()
        self.N = 0
        self.extra = {}                            # từ điển bổ sung (không có tần suất): dạng không dấu -> set(dạng có dấu)

    # ---------- học ----------
    def fit(self, sentences, extra_syllables=()):
        """sentences: danh sách câu, mỗi câu là list âm tiết CÓ DẤU (chữ thường). extra_syllables: âm tiết bổ sung chỉ để mở rộng ứng viên."""
        for s in sentences:
            for w in s:
                self.cands[strip_accents(w)][w] += 1
            p = ["<s>", "<s>"] + list(s) + ["</s>"]
            for i in range(2, len(p)):
                self.uni[p[i]] += 1
                self.bi[(p[i - 1], p[i])] += 1
                self.tri[(p[i - 2], p[i - 1], p[i])] += 1
                self.bi_ctx[p[i - 1]] += 1
                self.tri_ctx[(p[i - 2], p[i - 1])] += 1
        self.N = sum(self.uni.values())
        extra = defaultdict(set)
        for w in extra_syllables:
            w = normalize_unicode(w).lower()
            extra[strip_accents(w)].add(w)
        self.extra = extra
        self.V = len(self.uni) + sum(len(v) for v in extra.values()) + 1
        return self

    # ---------- ứng viên ----------
    def candidates(self, base: str) -> list:
        c = [w for w, _ in self.cands[base].most_common()] if base in self.cands else []
        for w in sorted(self.extra.get(base, ())):
            if w not in c:
                c.append(w)
        return c or [base]                          # chưa từng thấy: giữ nguyên

    # ---------- xác suất ----------
    def logp(self, u: str, v: str, w: str) -> float:
        p1 = (self.uni[w] + self.k) / (self.N + self.k * self.V)
        l1, l2, l3 = self.lam
        t = self.tri_ctx[(u, v)] if self.bac >= 3 else 0
        b = self.bi_ctx[v] if self.bac >= 2 else 0
        w3, w2 = (l3 if t else 0.0), (l2 if b else 0.0)
        z = l1 + w2 + w3                            # bỏ bậc không có ngữ cảnh rồi chuẩn hóa lại trọng số
        p = l1 * p1
        if w2:
            p += w2 * self.bi[(v, w)] / b
        if w3:
            p += w3 * self.tri[(u, v, w)] / t
        return math.log(p / z)

    # ---------- giải mã ----------
    def restore_tokens(self, bases: list) -> list:
        """bases: list dạng không dấu (chữ thường). Trả về list dạng có dấu."""
        C = [self.candidates(b) for b in bases]
        if self.bac == 1:
            return [c[0] for c in C]
        prev = {("<s>", "<s>"): (0.0, None)}
        back = []
        for ci in C:
            cur = {}
            for (u, v), (sc, _) in prev.items():
                for w in ci:
                    s2 = sc + self.logp(u, v, w)
                    key = (v, w)
                    if key not in cur or s2 > cur[key][0]:
                        cur[key] = (s2, (u, v))
            back.append(cur)
            prev = cur
        best, best_sc = None, -1e18
        for (u, v), (sc, _) in prev.items():
            s2 = sc + self.logp(u, v, "</s>")
            if s2 > best_sc:
                best, best_sc = (u, v), s2
        out, key = [], best
        for i in range(len(C) - 1, -1, -1):
            out.append(key[1])
            key = back[i][key][1]
        return out[::-1]

    def restore(self, text: str) -> str:
        """Khôi phục dấu cho một chuỗi bất kỳ, giữ nguyên khoảng trắng, dấu câu và kiểu viết hoa của từng âm tiết."""
        spans = list(TOKEN_RE.finditer(normalize_unicode(text)))
        bases = [strip_accents(m.group().lower()) for m in spans]
        pred = self.restore_tokens(bases)
        src = normalize_unicode(text)
        out, pos = [], 0
        for m, p in zip(spans, pred):
            out.append(src[pos:m.start()])
            out.append(_giu_hoa_thuong(m.group(), p))
            pos = m.end()
        out.append(src[pos:])
        return "".join(out)
