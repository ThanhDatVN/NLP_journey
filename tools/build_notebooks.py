"""Dựng notebook từ nguồn văn bản `tools/notebook_src/*.nbsrc` (và tuỳ chọn chạy để lưu kết quả).

Vì sao có bước này: tệp .ipynb là JSON khó đọc/khó so sánh. Nguồn `.nbsrc` là văn bản thuần,
dễ sửa lời văn, dễ xem khác biệt (diff). Mỗi dòng bắt đầu bằng `@@@ md` hoặc `@@@ code` mở một ô mới.

Dùng:
    python tools/build_notebooks.py 03                 # chỉ dựng bài 03 (không chạy)
    python tools/build_notebooks.py 03 05 --run        # dựng rồi chạy, lưu kết quả vào notebook
    python tools/build_notebooks.py --all --run        # tất cả (rất lâu: cần Internet/GPU)
    python tools/build_notebooks.py --dap-an 03 --run  # dựng/chạy notebook ĐÁP ÁN của bài 03 (notebooks/dap_an/)
    python tools/build_notebooks.py 03 --sync-text     # chỉ cập nhật LỜI VĂN từ nguồn, GIỮ NGUYÊN kết quả đã chạy

Lưu ý quan trọng:
  * Nguồn là `tools/notebook_src/*.nbsrc`; `notebooks/*.ipynb` là sản phẩm dựng ra. Nếu bạn sửa trực tiếp
    .ipynb, hãy sửa cả .nbsrc tương ứng (hoặc chấp nhận rằng lần dựng sau sẽ ghi đè).
  * Sau khi sửa lời văn có chứa số liệu, hãy chạy lại (--run) và đối chiếu số liệu với lời văn.
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
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tools" / "notebook_src"
OUT = ROOT / "notebooks"


def parse(path: Path):
    cells, kind, buf = [], None, []

    def flush():
        if kind is None:
            return
        text = "\n".join(buf).strip("\n")
        if text.strip():
            cells.append(new_markdown_cell(text) if kind == "md" else new_code_cell(text))

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("@@@ "):
            flush()
            kind, buf = line[4:].strip(), []
        else:
            buf.append(line)
    flush()
    return cells


def sync_text(src: Path, out_dir: Path) -> bool:
    """Cập nhật các ô markdown của notebook đã chạy theo nguồn mà KHÔNG chạy lại. Từ chối nếu mã (ô code) đã thay đổi."""
    out = out_dir / (src.stem + ".ipynb")
    if not out.exists():
        print(f"[{src.stem[:2]}] chưa có {out.name}; hãy dựng với --run trước")
        return False
    nb = nbformat.read(out, as_version=4)
    moi = parse(src)
    code_cu = [c for c in nb.cells if c.cell_type == "code"]
    code_moi = [c for c in moi if c.cell_type == "code"]
    if len(code_cu) != len(code_moi):
        print(f"[{src.stem[:2]}] số ô code đã đổi ({len(code_cu)} → {len(code_moi)}) — cần chạy lại (--run)")
        return False
    doi_code = [i for i, (a, b) in enumerate(zip(code_moi, code_cu)) if a.source != b.source]
    if doi_code:
        print(f"[{src.stem[:2]}] mã ở ô code thứ {doi_code} đã đổi — kết quả cũ không còn hợp lệ, cần chạy lại (--run)")
        return False
    # Dãy ô code giữ nguyên ⇒ kết quả cũ còn hợp lệ: cho phép sửa/thêm/bớt ô markdown, ô code mang theo kết quả cũ theo thứ tự.
    md_cu = {c.source for c in nb.cells if c.cell_type == "markdown"}
    n = sum(c.source not in md_cu for c in moi if c.cell_type == "markdown")
    it = iter(code_cu)
    for c in moi:
        if c.cell_type == "code":
            cu = next(it)
            c.outputs, c.execution_count, c.metadata = cu.outputs, cu.execution_count, cu.metadata
    nb.cells = moi
    nbformat.write(nb, out)
    print(f"[{src.stem[:2]}] đã cập nhật {n} ô văn bản (mới/đổi), giữ nguyên kết quả đã chạy của {len(code_moi)} ô code")
    return True


def build(src: Path, run: bool, timeout: int, out_dir: Path = OUT) -> bool:
    OUT_ = out_dir
    OUT_.mkdir(parents=True, exist_ok=True)      # thư mục làm việc của kernel phải tồn tại
    nb = new_notebook(cells=parse(src))
    nb.metadata["kernelspec"] = {"display_name": "Python 3", "language": "python", "name": "python3"}
    nb.metadata["language_info"] = {"name": "python"}
    out = OUT_ / (src.stem + ".ipynb")
    if run:
        t0 = time.time()
        client = NotebookClient(nb, timeout=timeout, kernel_name="python3", resources={"metadata": {"path": str(OUT_)}})
        try:
            client.execute()
            print(f"[{src.stem[:2]}] chạy OK trong {time.time() - t0:.0f}s")
        except Exception:  # noqa: BLE001
            traceback.print_exc(limit=0)
            failed = out.with_suffix(".failed.ipynb")
            nbformat.write(nb, failed)
            print(f"[{src.stem[:2]}] LỖI — đã lưu bản chạy dở: {failed.name} (xoá sau khi gỡ lỗi)")
            return False
    OUT_.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, out)
    print(f"[{src.stem[:2]}] ghi {out.name} ({out.stat().st_size // 1024} KB, {len(nb.cells)} ô)")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bai", nargs="*", help="tiền tố số của bài, ví dụ 03 05")
    ap.add_argument("--all", action="store_true", help="dựng mọi bài")
    ap.add_argument("--run", action="store_true", help="chạy notebook và lưu kết quả")
    ap.add_argument("--sync-text", action="store_true", help="chỉ cập nhật lời văn từ nguồn, giữ kết quả đã chạy (từ chối nếu mã đổi)")
    ap.add_argument("--dap-an", action="store_true", help="dựng notebook đáp án (tools/notebook_src/dap_an -> notebooks/dap_an)")
    ap.add_argument("--timeout", type=int, default=3000, help="giới hạn thời gian mỗi ô (giây)")
    args = ap.parse_args()

    src_dir, out_dir = (SRC / "dap_an", OUT / "dap_an") if args.dap_an else (SRC, OUT)
    nguon = sorted(src_dir.glob("[0-9][0-9]_*.nbsrc"))
    if not args.all:
        if not args.bai:
            ap.error("hãy nêu số bài (ví dụ 03) hoặc dùng --all")
        nguon = [p for p in nguon if p.name[:2] in set(args.bai)]
    if not nguon:
        sys.exit("Không tìm thấy nguồn phù hợp trong " + str(SRC))
    if args.sync_text:
        ok = all([sync_text(p, out_dir) for p in nguon])
    else:
        ok = all([build(p, args.run, args.timeout, out_dir) for p in nguon])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
