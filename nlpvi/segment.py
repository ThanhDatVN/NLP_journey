"""Tách từ tiếng Việt: ghép các âm tiết thành từ ("học sinh" -> "học_sinh").

Mặc định dùng thuật toán khớp tối đa từ trái sang phải (forward maximum matching)
với từ điển các từ ghép trích từ từ vựng của PhoBERT (data/tu_ghep_phobert.txt).
Cách này thuần Python nên chạy được mọi nơi, và khớp với từ vựng lúc tiền huấn luyện.

Với sản phẩm thật, hãy dùng bộ tách từ có huấn luyện: RDRSegmenter (VnCoreNLP, cần Java),
hoặc Underthesea. `get_segmenter("underthesea")` thử dùng nó và tự lùi về từ điển nếu lỗi.
"""
from functools import lru_cache

from .data import DATA_DIR
from .text import normalize_unicode, tokenize_surface


class ViSegmenter:
    """Forward maximum matching trên từ điển từ ghép."""

    def __init__(self, compounds, max_syllables: int = 4):
        self.max_n = max_syllables
        self.dict = {c.lower() for c in compounds}

    @classmethod
    def from_file(cls, path=None):
        path = path or DATA_DIR / "tu_ghep_phobert.txt"
        words = [w for w in path.read_text(encoding="utf-8").splitlines() if w]
        return cls(words)

    def segment_tokens(self, tokens):
        out, i = [], 0
        while i < len(tokens):
            for n in range(min(self.max_n, len(tokens) - i), 1, -1):
                chunk = tokens[i:i + n]
                if all(t.isalpha() for t in chunk) and "_".join(chunk).lower() in self.dict:
                    out.append("_".join(chunk))
                    i += n
                    break
            else:
                out.append(tokens[i])
                i += 1
        return out

    def segment(self, text: str) -> str:
        return " ".join(self.segment_tokens(tokenize_surface(normalize_unicode(text))))


@lru_cache(maxsize=None)
def get_segmenter(backend: str = "dictionary"):
    """Trả về hàm `f(text) -> 'chuỗi đã ghép từ'`.

    backend: "dictionary" (mặc định, thuần Python) hoặc "underthesea".
    Nếu Underthesea không import/chạy được (thiếu gói, bị chính sách bảo mật chặn DLL...),
    tự lùi về "dictionary" và in một dòng cảnh báo.
    """
    if backend == "underthesea":
        try:
            from underthesea import word_tokenize
            word_tokenize("Thử nghiệm")  # ép nạp mô hình ngay để lỗi lộ ra sớm
            return lambda t: word_tokenize(normalize_unicode(t), format="text")
        except Exception as e:  # noqa: BLE001 - cố ý bắt rộng: ImportError, OSError, ...
            print(f"[nlpvi] Underthesea không dùng được ({type(e).__name__}); lùi về từ điển.")
    return ViSegmenter.from_file().segment


def segment(text: str) -> str:
    """Tách từ bằng backend mặc định."""
    return get_segmenter("dictionary")(text)
