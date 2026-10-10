"""Nạp dữ liệu của giáo trình. Mọi tệp đều là UTF-8."""
import json
import os
import random
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
LABELS = ["tích cực", "tiêu cực", "trung tính"]


def set_seed(seed: int = 42) -> None:
    """Cố định seed cho random, NumPy và (nếu có) PyTorch."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    except ImportError:
        pass


def load_reviews() -> pd.DataFrame:
    """Bộ đánh giá tổng hợp: id, text, label, domain, split."""
    return pd.read_csv(DATA_DIR / "reviews_vi.csv", encoding="utf-8-sig")


def load_splits():
    """Trả về (train, valid, test) theo cột `split` đã cố định sẵn."""
    df = load_reviews()
    return tuple(df[df.split == s].reset_index(drop=True) for s in ("train", "valid", "test"))


def load_hard() -> pd.DataFrame:
    """40 câu khó viết tay (phủ định, đối lập, mỉa mai, không dấu...)."""
    return pd.read_csv(DATA_DIR / "reviews_hard.csv", encoding="utf-8")


def load_faq():
    """Trả về (docs, queries) cho bài tìm kiếm / RAG."""
    docs = json.loads((DATA_DIR / "faq_docs.json").read_text(encoding="utf-8"))
    queries = json.loads((DATA_DIR / "faq_queries.json").read_text(encoding="utf-8"))
    return docs, queries
