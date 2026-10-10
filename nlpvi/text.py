"""Chuẩn hóa và tách văn bản tiếng Việt bằng Python thuần (không phụ thuộc thư viện nặng)."""
import re
import unicodedata

# Viết tắt / teencode phổ biến. Lưu ý: ánh xạ này MANG TÍNH TÌNH HUỐNG,
# ví dụ "k" có thể là "không" hoặc "nghìn". Hãy kiểm tra trên dữ liệu của bạn.
TEENCODE = {
    "ko": "không", "k": "không", "hok": "không", "hông": "không",
    "dc": "được", "đc": "được", "sp": "sản phẩm", "nv": "nhân viên",
    "mik": "mình", "mn": "mọi người", "ok": "ổn", "oke": "ổn",
    "thanks": "cảm ơn", "cám": "cảm",
}

URL_RE = re.compile(r"https?://\S+|www\.\S+")
USER_RE = re.compile(r"(?<!\w)@\w+")
PHONE_RE = re.compile(r"(?<!\d)(?:\+?84|0)(?:[\s.\-]?\d){9}(?!\d)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
REPEAT_CHAR_RE = re.compile(r"([^\W\d_])\1{2,}")  # ngonnnn -> ngon (chỉ chữ cái, giữ nguyên số 1000)
REPEAT_PUNCT_RE = re.compile(r"([!?.])\1{1,}")  # !!! -> !
# Khối emoji chính (U+1F300-1FAFF), ký hiệu linh tinh/dingbats (U+2600-27BF), ❤ (U+2764)
# và bộ chọn biến thể U+FE0F. Viết bằng chr() để mã nguồn không chứa ký tự vô hình.
EMOJI_RE = re.compile(
    "[" + chr(0x1F300) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + chr(0x2764) + "]" + chr(0xFE0F) + "?"
)
TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def normalize_unicode(text: str) -> str:
    """Đưa về dạng dựng sẵn NFC để cùng một chữ luôn có cùng chuỗi byte."""
    return unicodedata.normalize("NFC", str(text))


def strip_accents(text: str) -> str:
    """Bỏ dấu tiếng Việt. Chỉ để thử nghiệm: thường làm MẤT thông tin."""
    text = text.replace("đ", "d").replace("Đ", "D")
    nfd = unicodedata.normalize("NFD", text)
    return unicodedata.normalize("NFC", "".join(c for c in nfd if unicodedata.category(c) != "Mn"))


def normalize(text: str, *, lower=True, mask_url=True, mask_user=True, mask_phone=True,
              mask_email=True, squeeze_repeats=True, expand_teencode=True, emoji="keep") -> str:
    """Chuỗi chuẩn hóa dùng cho các bài phân loại.

    Giữ nguyên dấu tiếng Việt, từ phủ định và dấu ! ? (thường mang cảm xúc).
    emoji: "keep" giữ nguyên, "drop" xóa.
    """
    text = normalize_unicode(text)
    if mask_email:
        text = EMAIL_RE.sub(" EMAIL ", text)   # trước USER để không nhầm @tên-miền
    if mask_url:
        text = URL_RE.sub(" URL ", text)
    if mask_user:
        text = USER_RE.sub(" USER ", text)
    if mask_phone:
        text = PHONE_RE.sub(" SDT ", text)
    if lower:
        text = text.lower()
    if emoji == "drop":
        text = EMOJI_RE.sub(" ", text)
    else:
        text = EMOJI_RE.sub(lambda m: f" {m.group(0)} ", text)
    if squeeze_repeats:
        text = REPEAT_CHAR_RE.sub(r"\1", text)
        text = REPEAT_PUNCT_RE.sub(r"\1", text)
    if expand_teencode:
        text = " ".join(TEENCODE.get(w, w) for w in text.split())
    return re.sub(r"\s+", " ", text).strip()


def tokenize_surface(text: str):
    """Tách chuỗi thành âm tiết/số/dấu câu (chưa ghép từ)."""
    return TOKEN_RE.findall(text)


# Tách sau dấu kết câu + khoảng trắng khi từ kế tiếp bắt đầu bằng chữ/số/dấu mở. KHÔNG dựa vào chữ hoa:
# văn bản có thể đã hạ chữ thường, và dải [À-Ỵ] của Unicode chứa cả chữ thường có dấu (nên không dùng để bắt "chữ hoa").
_SENT_END_RE = re.compile(r"(?<=[.!?…])\s+(?=[\w\"“(])")


def split_sentences(text: str):
    """Tách câu bằng quy tắc: sau . ! ? … + khoảng trắng + chữ/số (không phụ thuộc chữ hoa/thường). Chưa xử lý viết tắt như 'TP. HCM'."""
    text = normalize_unicode(text).strip()
    return [s.strip() for s in _SENT_END_RE.split(text) if s.strip()]
