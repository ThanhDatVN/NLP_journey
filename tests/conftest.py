"""Thêm thư mục gốc và tools/ vào đường dẫn import cho mọi kiểm thử."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "tools"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
