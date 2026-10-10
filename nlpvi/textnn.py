"""Hàm dùng lại cho các bài mạng nơ-ron văn bản (đã viết từng bước ở Bài 6)."""
import copy

import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader, Dataset

from .data import set_seed
from .segment import segment
from .text import normalize

PAD, UNK = 0, 1


def tach_tu(text: str):
    """Chuẩn hóa rồi tách từ."""
    return segment(normalize(text)).split()


def build_vocab(texts, min_freq: int = 2):
    """Từ điển chỉ xây từ tập train. Trả về (itos, stoi) với <pad>=0, <unk>=1."""
    from collections import Counter
    dem = Counter(w for t in texts for w in tach_tu(t))
    itos = ["<pad>", "<unk>"] + sorted(w for w, c in dem.items() if c >= min_freq)
    return itos, {w: i for i, w in enumerate(itos)}


class TextDS(Dataset):
    def __init__(self, df, stoi, class2idx, max_len: int = 40):
        self.x = [[stoi.get(w, UNK) for w in tach_tu(t)][:max_len] for t in df["text"]]
        self.y = [class2idx[l] for l in df["label"]]

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        return self.x[i], self.y[i]


def collate(batch):
    xs, ys = zip(*batch)
    out = torch.zeros(len(xs), max(len(x) for x in xs), dtype=torch.long)
    for i, x in enumerate(xs):
        out[i, :len(x)] = torch.tensor(x)
    return out, torch.tensor(ys)


def evaluate(model, ds, device="cpu", bs: int = 256):
    """Trả về (loss, macro-F1, dự đoán)."""
    model.eval()
    P, Y, L = [], [], 0.0
    with torch.no_grad():
        for xb, yb in DataLoader(ds, batch_size=bs, collate_fn=collate):
            out = model(xb.to(device))
            L += F.cross_entropy(out, yb.to(device), reduction="sum").item()
            P.append(out.argmax(1).cpu())
            Y.append(yb)
    P, Y = torch.cat(P).numpy(), torch.cat(Y).numpy()
    return L / len(ds), f1_score(Y, P, average="macro"), P


def fit(model, ds_tr, ds_va, epochs=25, lr=3e-3, wd=1e-4, bs=64, seed=0, patience=6,
        clip=None, device="cpu"):
    """Huấn luyện với AdamW + dừng sớm theo macro-F1 trên valid; nạp lại trọng số tốt nhất."""
    set_seed(seed)
    model.to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=wd)
    dl = DataLoader(ds_tr, batch_size=bs, shuffle=True, collate_fn=collate)
    best, best_state, wait, hist = -1.0, None, 0, []
    for ep in range(1, epochs + 1):
        model.train()
        tl = 0.0
        for xb, yb in dl:
            xb, yb = xb.to(device), yb.to(device)
            loss = F.cross_entropy(model(xb), yb)
            opt.zero_grad()
            loss.backward()
            if clip:
                torch.nn.utils.clip_grad_norm_(model.parameters(), clip)
            opt.step()
            tl += loss.item() * len(xb)
        vl, vf, _ = evaluate(model, ds_va, device)
        hist.append({"epoch": ep, "loss_train": tl / len(ds_tr), "loss_valid": vl, "f1_valid": vf})
        if vf > best:
            best, best_state, wait = vf, copy.deepcopy(model.state_dict()), 0
        else:
            wait += 1
            if wait >= patience:
                break
    model.load_state_dict(best_state)
    return pd.DataFrame(hist)
