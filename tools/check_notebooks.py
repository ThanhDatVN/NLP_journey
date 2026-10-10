"""Kiểm tra giáo trình: mã hóa tiếng Việt còn nguyên không, và notebook có chạy lại không lỗi không.

Ví dụ:
    python tools/check_notebooks.py                 # chạy các bài chỉ cần CPU: 00-07 và 14 (vài phút)
    python tools/check_notebooks.py --only 03 05    # chỉ các bài chỉ định
    python tools/check_notebooks.py --all           # thêm 08-19 (cần Internet/GPU, lâu: > 60 phút)
    python tools/check_notebooks.py --encoding-only # chỉ kiểm tra mã hóa (vài giây)
    python tools/check_notebooks.py --save          # ghi kết quả chạy lại vào notebook (cẩn thận: ghi đè)

Notebook chạy trong bản sao ở bộ nhớ; mặc định KHÔNG ghi đè tệp. Thoát với mã 1 nếu có lỗi.
"""
import argparse
import os
import sys
import time
import traceback
from pathlib import Path

os.environ.setdefault("PYTHONUTF8", "1")
os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")

import nbformat  # noqa: E402
from nbclient import NotebookClient  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"
CPU_ONLY = {"00", "01", "02", "03", "04", "05", "06", "07", "14"}


def kiem_tra_ma_hoa(paths):
    """Phát hiện tệp bị ghi sai mã hóa: nhiều dấu '?' mà gần như không có ký tự tiếng Việt."""
    loi = []
    for p in paths:
        text = p.read_text(encoding="utf-8-sig", errors="replace")
        non_ascii = sum(ord(c) > 127 for c in text)
        qmarks = text.count("?")
        if text.count("�") > 20 or (non_ascii < 20 and qmarks > 50):   # vài ký tự � có thể là lời văn cố ý nhắc tới
            loi.append(f"{p.relative_to(ROOT)}: nghi hỏng mã hóa (ký tự '?' = {qmarks}, non-ASCII = {non_ascii})")
    return loi


def chay(path: Path, save: bool, timeout: int):
    nb = nbformat.read(path, as_version=4)
    for c in nb.cells:                      # xóa kết quả cũ để chắc chắn chạy lại thật
        if c.cell_type == "code":
            c.outputs, c.execution_count = [], None
    client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(NB_DIR)}})
    t0 = time.time()
    client.execute()
    if save:
        nbformat.write(nb, path)
    return time.time() - t0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="chạy cả bài cần Internet/GPU (08-19)")
    ap.add_argument("--only", nargs="+", metavar="NN", help="chỉ chạy các bài có tiền tố số này, ví dụ 03 05")
    ap.add_argument("--encoding-only", action="store_true", help="chỉ kiểm tra mã hóa")
    ap.add_argument("--save", action="store_true", help="ghi kết quả chạy lại vào notebook")
    ap.add_argument("--timeout", type=int, default=3000, help="giới hạn thời gian mỗi ô (giây)")
    args = ap.parse_args()

    notebooks = sorted(NB_DIR.glob("[0-9][0-9]_*.ipynb"))
    notebooks = [p for p in notebooks if not p.name.endswith(".failed.ipynb")]
    if args.only:
        notebooks = [p for p in notebooks if p.name[:2] in set(args.only)]
    elif not args.all:
        notebooks = [p for p in notebooks if p.name[:2] in CPU_ONLY]

    # 1) mã hóa
    tep = list(ROOT.glob("*.md")) + list((ROOT / "docs").glob("*.md")) + list((ROOT / "data").glob("*"))
    tep = [p for p in tep if p.suffix in {".md", ".csv", ".json", ".txt"}] + sorted(NB_DIR.glob("*.ipynb"))
    loi = kiem_tra_ma_hoa(tep)
    print(f"[mã hóa] kiểm tra {len(tep)} tệp: " + ("OK" if not loi else f"{len(loi)} tệp nghi hỏng"))
    for l in loi:
        print("   ", l)
    if args.encoding_only:
        sys.exit(1 if loi else 0)

    # 2) chạy notebook
    that_bai = list(loi)
    for p in notebooks:
        try:
            dt = chay(p, args.save, args.timeout)
            print(f"[chạy] {p.name}: OK ({dt:.0f}s)")
        except Exception as e:  # noqa: BLE001
            print(f"[chạy] {p.name}: LỖI — {type(e).__name__}: {str(e).splitlines()[-1][:200] if str(e) else ''}")
            traceback.print_exc(limit=0)
            that_bai.append(p.name)
    print("\nKẾT QUẢ:", "TẤT CẢ ĐỀU TỐT" if not that_bai else f"{len(that_bai)} vấn đề: {that_bai}")
    sys.exit(1 if that_bai else 0)


if __name__ == "__main__":
    main()
