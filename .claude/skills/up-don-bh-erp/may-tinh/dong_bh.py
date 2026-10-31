# -*- coding: utf-8 -*-
"""So dòng hàng BH (MISA) ↔ Sales Order (ERP) THEO TỪNG DÒNG, không cộng gộp mã hàng.

Luật Tú chốt 19/10/2026:
  1. Không được cộng gộp mã hàng: mỗi dòng MISA là một dòng ERP (vd PVH10-6 ×6 và PVH10-6 ×1 "Cắt dán" là HAI dòng).
  2. BH có mô tả/ghi chú thì dòng ERP cũng phải có, nhưng viết ngắn gọn.
(Trước đó cap-nhat-lech-bh.py gộp theo mã nên mất ghi chú cắt/hạ size: đơn 00678/BH05304, 19/10/2026.)
"""
import re


def rut_gon(chu):
    """Ghi chú dòng MISA → bản ngắn. "Cắt dán: 250cm x 200cm x 10cm" → "Cắt dán 250x200x10cm"."""
    chu = re.sub(r'\s+', ' ', (chu or '').strip())
    if not chu:
        return ''

    def kt(m):
        so = [s for s in m.groups() if s]
        return 'x'.join(so) + 'cm'

    chu = re.sub(r'(\d{1,3})\s*(?:cm)?\s*[x×*]\s*(\d{1,3})\s*(?:cm)?(?:\s*[x×*]\s*(\d{1,3})\s*(?:cm)?)?', kt, chu,
                 flags=re.I)
    chu = re.sub(r'\b(h[aạ] size|c[aắ]t d[aá]n|c[aắ]t)\s*:\s*', lambda m: m.group(1) + ' ', chu, flags=re.I)
    return chu.strip()


def khoa_cat(chu):
    """Kích thước cắt trong ghi chú → khoá so sánh (không phân biệt rộng×dài đảo chiều). Tấm nguyên → ()."""
    chu = (chu or '').lower()
    if not re.search(r'h[aạ]\s*size|c[aắ]t|size', chu):
        return ()
    cap = re.findall(r'(\d{2,3})\s*(?:cm)?\s*[x×*]\s*(\d{2,3})', chu)
    return tuple(sorted(tuple(sorted((int(a), int(b)))) for a, b in cap))


def chuan(chu):
    """Chuẩn hoá để so ghi chú: rút gọn, bỏ tiền tố "GIAO HÀNG:"/"Giao:", thường hoá, bỏ dấu câu thừa."""
    chu = rut_gon(chu).lower()
    chu = re.sub(r'giao( h[aà]ng)?s*:s*', '', chu)
    return re.sub(r'[s|/·,;:.-]+', ' ', chu).strip()


def cac_ghi_chu(x):
    """Các ghi chú của MỘT dòng MISA (x['_ghi_chu'] là list), đã rút gọn, bỏ trùng."""
    kq, thay = [], set()
    for g in (x.get('_ghi_chu') or []):
        g = rut_gon(g)
        k = chuan(g)
        if g and k not in thay:
            thay.add(k)
            kq.append(g)
    return kq


def ghi_chu_misa(x):
    """Ghi chú của MỘT dòng MISA → chuỗi ngắn."""
    return ' / '.join(cac_ghi_chu(x))


def lap_plan(dong_misa, dong_erp, f=float):
    """Ghép từng dòng, KHÔNG gộp.
    dong_misa: list dict MISA (inventory_item_code, quantity, unit_price, _ghi_chu).
    dong_erp : list dict ERP (name, item_code, qty, rate, delivered_qty, description).
    Trả dict: giu (cặp ERP↔MISA, kể cả cần đổi SL/giá), xoa (dòng ERP thừa), them (dòng MISA chưa có)."""
    m = [dict(x, _ma=(x.get('inventory_item_code') or '').strip(), _khoa=None) for x in dong_misa]
    for x in m:
        x['_khoa'] = (x['_ma'], khoa_cat(' '.join(x.get('_ghi_chu') or [])))
    e = [dict(r, _khoa=(r['item_code'], khoa_cat(r.get('description')))) for r in dong_erp]
    da_m, da_e, giu = set(), set(), []
    # Lượt 1: cùng khoá + cùng SL + cùng giá → ghép trước (đơn không đổi thì không bị xê dịch)
    # Lượt 2: cùng khoá, khác SL/giá → ghép theo thứ tự, chỉ đổi SL/giá
    for luot in (1, 2):
        for i, r in enumerate(e):
            if i in da_e:
                continue
            for j, x in enumerate(m):
                if j in da_m or x['_khoa'] != r['_khoa']:
                    continue
                if luot == 1 and not (abs(f(x.get('quantity')) - f(r['qty'])) < 1e-9
                                      and abs(f(x.get('unit_price')) - f(r['rate'])) < 0.01):
                    continue
                giu.append((r, x))
                da_e.add(i)
                da_m.add(j)
                break
    # Lượt 3: cùng MÃ, chưa ghép, mà MỘT bên không có thông tin cắt (vd ERP mất ghi chú) → vẫn là cùng dòng
    # (ghép 1-1, không gộp). Tránh báo oan "dòng đã giao biến mất" khi ERP chỉ thiếu Mô tả.
    for i, r in enumerate(e):
        if i in da_e:
            continue
        for j, x in enumerate(m):
            if j in da_m or x['_ma'] != r['item_code'] or (x['_khoa'][1] and r['_khoa'][1]):
                continue
            giu.append((r, x))
            da_e.add(i)
            da_m.add(j)
            break
    xoa = [r for i, r in enumerate(e) if i not in da_e]
    them = [x for j, x in enumerate(m) if j not in da_m]
    return {'giu': giu, 'xoa': xoa, 'them': them}
