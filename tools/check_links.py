"""Kiểm tra liên kết nội bộ (đường dẫn tương đối) trong các tệp Markdown và ô markdown của notebook, và kiểm tra notebook hợp lệ theo nbformat.

    python tools/check_links.py            # in mọi liên kết hỏng, thoát mã 1 nếu có
    python tools/check_links.py --http     # liệt kê thêm các URL http(s) (không kiểm tra mạng)

Chỉ kiểm tra *sự tồn tại của tệp đích*; không kiểm tra neo `#...` và không gọi mạng.
"""
import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent.parent
BO_QUA = {".git", ".venv", "venv", "outputs", "__pycache__", ".pytest_cache", ".ipynb_checkpoints"}
LIEN_KET = re.compile(r"(?<!!)\[[^\]\n]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)|!\[[^\]\n]*\]\(([^)\s]+)\)")
KHOI_MA = re.compile(r"```.*?```", re.S)
MA_DONG = re.compile(r"`[^`\n]*`")


def tep_markdown():
    for p in ROOT.rglob("*.md"):
        if not any(x in BO_QUA for x in p.parts):
            yield p, p.read_text(encoding="utf-8")


def o_markdown_notebook():
    for p in ROOT.rglob("*.ipynb"):
        if any(x in BO_QUA for x in p.parts):
            continue
        nb = json.loads(p.read_text(encoding="utf-8"))
        for i, c in enumerate(nb["cells"]):
            if c["cell_type"] == "markdown":
                yield p, i, "".join(c["source"])


def kiem_tra(van_ban, goc: Path):
    van_ban = MA_DONG.sub("", KHOI_MA.sub("", van_ban))                 # bỏ mã mẫu: ví dụ `[x](y)` trong khối mã không phải liên kết thật
    hong, http = [], []
    for m in LIEN_KET.finditer(van_ban):
        url = (m.group(1) or m.group(2)).strip("<>")
        if url.startswith(("http://", "https://")):
            http.append(url)
            continue
        if url.startswith(("mailto:", "#", "data:")):
            continue
        dich = (goc.parent / unquote(url.split("#")[0])).resolve()
        if not dich.exists():
            hong.append(url)
    return hong, http


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--http", action="store_true", help="liệt kê thêm các URL http(s) (không kiểm tra mạng)")
    args = ap.parse_args()
    loi, tong_http, so_lk = [], [], 0
    for p, txt in tep_markdown():
        h, u = kiem_tra(txt, p)
        loi += [(p.relative_to(ROOT), None, x) for x in h]; tong_http += u
    for p, i, txt in o_markdown_notebook():
        h, u = kiem_tra(txt, p)
        loi += [(p.relative_to(ROOT), i, x) for x in h]; tong_http += u
    try:
        import nbformat
        for p in ROOT.rglob("*.ipynb"):
            if any(x in BO_QUA for x in p.parts):
                continue
            try:
                nbformat.validate(nbformat.read(p, as_version=4))
            except Exception as e:                                   # noqa: BLE001
                loi.append((p.relative_to(ROOT), None, f"notebook không hợp lệ: {type(e).__name__}: {str(e)[:80]}"))
    except ImportError:
        print("(bỏ qua kiểm tra nbformat: chưa cài nbformat)")
    for f, i, x in loi:
        print(f"HỎNG: {f}" + (f" (ô {i})" if i is not None else "") + f" -> {x}")
    if args.http:
        print(f"\n{len(set(tong_http))} URL http(s) khác nhau (chưa kiểm tra mạng).")
    print(f"Kết quả: {len(loi)} vấn đề.")
    sys.exit(1 if loi else 0)


if __name__ == "__main__":
    main()
