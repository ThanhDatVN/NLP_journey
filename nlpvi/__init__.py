"""Tiện ích dùng chung cho giáo trình NLP tiếng Việt.

Mỗi hàm ở đây đều được xây dần, từng bước, trong notebook tương ứng; gói này
chỉ giữ bản hoàn chỉnh để các bài sau không phải chép lại.
"""
from .data import (DATA_DIR, LABELS, ROOT, load_faq, load_hard, load_reviews,
                   load_splits, set_seed)
from .diacritics import DiacriticRestorer, tach_token
from .segment import ViSegmenter, get_segmenter, segment
from .text import (TEENCODE, normalize, normalize_unicode, split_sentences,
                   strip_accents, tokenize_surface)

__all__ = [
    "DATA_DIR", "LABELS", "ROOT", "load_faq", "load_hard", "load_reviews",
    "load_splits", "set_seed", "ViSegmenter", "get_segmenter", "segment",
    "TEENCODE", "normalize", "normalize_unicode", "split_sentences",
    "strip_accents", "tokenize_surface", "DiacriticRestorer", "tach_token",
]
