"""Liên kết nội bộ trong Markdown/notebook phải trỏ tới tệp có thật và mọi notebook phải hợp lệ theo nbformat. Chạy:  pytest -q"""
import pytest

import check_links as cl


def test_bo_kiem_tra_bat_duoc_lien_ket_hong(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("[có](b.md) [hỏng](khong_co.md) [web](https://example.com) [neo](#muc) ![anh](hinh_khong_co.png)", encoding="utf-8")
    (tmp_path / "b.md").write_text("x", encoding="utf-8")
    hong, http = cl.kiem_tra(f.read_text(encoding="utf-8"), f)
    assert hong == ["khong_co.md", "hinh_khong_co.png"] and http == ["https://example.com"]


def test_bo_kiem_tra_bo_qua_ma_mau(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("Ví dụ `[x](khong_co.md)` và\n```\n[y](khong_co2.md)\n```\n", encoding="utf-8")
    assert cl.kiem_tra(f.read_text(encoding="utf-8"), f)[0] == []


def test_lien_ket_noi_bo_cua_giao_trinh_khong_hong():
    loi = []
    for p, txt in cl.tep_markdown():
        loi += [f"{p.relative_to(cl.ROOT)}: {x}" for x in cl.kiem_tra(txt, p)[0]]
    for p, i, txt in cl.o_markdown_notebook():
        loi += [f"{p.relative_to(cl.ROOT)} (ô {i}): {x}" for x in cl.kiem_tra(txt, p)[0]]
    assert not loi, "\n".join(loi)


def test_moi_notebook_hop_le_theo_nbformat():
    nbformat = pytest.importorskip("nbformat")
    loi = []
    for p in cl.ROOT.rglob("*.ipynb"):
        if any(x in cl.BO_QUA for x in p.parts):
            continue
        try:
            nbformat.validate(nbformat.read(p, as_version=4))
        except Exception as e:                                       # noqa: BLE001
            loi.append(f"{p.name}: {type(e).__name__}")
    assert not loi, loi
