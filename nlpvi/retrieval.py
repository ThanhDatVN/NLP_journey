"""Truy hồi văn bản: BM25, embedding câu (dense), hợp nhất xếp hạng và các độ đo.

Mã được xây từng bước trong Bài 12 và dùng lại ở Bài 13 (RAG).
"""
import math
from collections import Counter

import numpy as np

from .segment import segment
from .text import normalize


def search_tokens(text: str, word_level: bool = True):
    """Chuẩn hóa → (tùy chọn) ghép từ → chữ thường → bỏ dấu câu."""
    t = normalize(text, expand_teencode=False, emoji="drop")
    if word_level:
        t = segment(t)
    return [w for w in t.split() if any(ch.isalnum() for ch in w)]


class BM25:
    """Okapi BM25 cài đặt thuần Python.

    score(q, d) = Σ_t idf(t) · tf(t,d)·(k1+1) / (tf(t,d) + k1·(1 − b + b·|d|/avgdl))
    """

    def __init__(self, docs_tokens, k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs_tokens]
        self.dl = np.array([len(d) for d in docs_tokens], dtype=float)
        self.avgdl = self.dl.mean()
        df = Counter(t for d in self.tf for t in d)
        n = len(docs_tokens)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, q_tokens):
        out = np.zeros(len(self.tf))
        for t in set(q_tokens):
            if t not in self.idf:
                continue
            for i, tf in enumerate(self.tf):
                f = tf.get(t, 0)
                if f:
                    out[i] += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.dl[i] / self.avgdl))
        return out


class Embedder:
    """Embedding câu = trung bình các vector token (có mặt nạ), chuẩn hóa L2.

    query_prefix / passage_prefix: các mô hình họ E5 yêu cầu tiền tố "query: " / "passage: ".
    segment_input: True với mô hình dựa trên PhoBERT (cần văn bản đã tách từ).
    """

    def __init__(self, name, query_prefix="", passage_prefix="", segment_input=False, max_length=256, device=None):
        import torch
        from transformers import AutoModel, AutoTokenizer
        self.torch = torch
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tok = AutoTokenizer.from_pretrained(name)
        self.model = AutoModel.from_pretrained(name).to(self.device).eval()
        self.qp, self.pp = query_prefix, passage_prefix
        self.seg, self.max_length = segment_input, max_length

    def encode(self, texts, kind="passage", batch_size=32):
        torch = self.torch
        prefix = self.qp if kind == "query" else self.pp
        texts = [prefix + (segment(t) if self.seg else t) for t in texts]
        out = []
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                enc = self.tok(texts[i:i + batch_size], padding=True, truncation=True,
                               max_length=self.max_length, return_tensors="pt").to(self.device)
                h = self.model(**enc).last_hidden_state
                m = enc["attention_mask"].unsqueeze(-1).to(h.dtype)
                v = (h * m).sum(1) / m.sum(1)
                out.append(torch.nn.functional.normalize(v, dim=-1).float().cpu())
        return torch.cat(out).numpy()


def rank_from_scores(scores):
    """Chỉ số tài liệu theo điểm giảm dần."""
    return list(np.argsort(-np.asarray(scores), kind="stable"))


def rrf(rankings, k: int = 60):
    """Reciprocal Rank Fusion: điểm(d) = Σ_r 1/(k + hạng_r(d)), hạng bắt đầu từ 1."""
    score = Counter()
    for r in rankings:
        for pos, d in enumerate(r, 1):
            score[d] += 1.0 / (k + pos)
    return [d for d, _ in score.most_common()]


def metrics_for(ranking, gold, ks=(1, 3, 5)):
    """Độ đo cho một truy vấn. gold: tập chỉ số tài liệu liên quan."""
    gold = set(gold)
    res = {}
    for k in ks:
        top = ranking[:k]
        res[f"hit@{k}"] = float(any(d in gold for d in top))
        res[f"recall@{k}"] = len(gold & set(top)) / len(gold)
    rr = 0.0
    for pos, d in enumerate(ranking, 1):
        if d in gold:
            rr = 1.0 / pos
            break
    res["mrr"] = rr
    dcg = sum(1.0 / math.log2(pos + 1) for pos, d in enumerate(ranking[:10], 1) if d in gold)
    idcg = sum(1.0 / math.log2(pos + 1) for pos in range(1, min(len(gold), 10) + 1))
    res["ndcg@10"] = dcg / idcg
    return res


def evaluate_rankings(rankings, golds, ks=(1, 3, 5)):
    """Trung bình độ đo trên mọi truy vấn."""
    per_q = [metrics_for(r, g, ks) for r, g in zip(rankings, golds)]
    return {k: float(np.mean([m[k] for m in per_q])) for k in per_q[0]}, per_q
