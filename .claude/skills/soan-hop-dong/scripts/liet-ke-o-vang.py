# -*- coding: utf-8 -*-
"""Liệt kê mọi chỗ BÔI VÀNG (= chỗ cần điền) trong một file .docx mẫu.

    python scripts/liet-ke-o-vang.py "<file.docx>"

In ra: số thứ tự đoạn · (bảng b, dòng d, ô o nếu nằm trong bảng) · chữ đang tô vàng · cả đoạn văn.
Bắt cả ô TRỐNG mà dấu kết đoạn bị tô vàng (highlight nằm trong w:pPr/w:rPr) — mẫu Phụ lục thay đổi
thông tin có kiểu này, chỉ quét run có chữ là sót.
Chỉ dùng thư viện chuẩn, chạy được trên máy Tú lẫn claude.ai.
"""
import sys, zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def vang(rpr):
    if rpr is None:
        return False
    h = rpr.find(W + "highlight")
    return h is not None and h.get(W + "val") not in (None, "none")


def chu(p):
    return "".join(t.text or "" for t in p.iter(W + "t"))


def main(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")
    vitri = {}
    for bi, tbl in enumerate(body.iter(W + "tbl"), start=1):
        for di, tr in enumerate(tbl.findall(W + "tr"), start=1):
            for oi, tc in enumerate(tr.findall(W + "tc"), start=1):
                for p in tc.iter(W + "p"):
                    vitri.setdefault(id(p), (bi, di, oi))
    dem = 0
    for n, p in enumerate(body.iter(W + "p"), start=1):
        phan = [ "".join(t.text or "" for t in r.iter(W + "t"))
                 for r in p.findall(W + "r") if vang(r.find(W + "rPr")) ]
        ppr = p.find(W + "pPr")
        trong_vang = ppr is not None and vang(ppr.find(W + "rPr")) and not chu(p).strip()
        if not phan and not trong_vang:
            continue
        dem += 1
        vt = vitri.get(id(p))
        o = "bảng %d dòng %d ô %d" % vt if vt else "đoạn văn"
        vang_txt = " | ".join(x for x in phan if x) or "(ô trống, dấu kết đoạn tô vàng)"
        print("[%d] đoạn %d · %s\n    VÀNG: %s\n    CẢ ĐOẠN: %s" % (dem, n, o, vang_txt, chu(p)[:300]))
    print("\nTổng: %d chỗ bôi vàng." % dem)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
