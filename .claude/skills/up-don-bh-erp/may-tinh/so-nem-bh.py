# -*- coding: utf-8 -*-
"""CHỈ ĐỌC MISA: đếm số tấm NỆM trong từng chứng từ BH (để điền cột Số lượng bảng kê chành).

Luật Tú dạy 30/10/2026: MISA › Bán hàng › Bán hàng › tìm số BH → mở đơn → đếm Số lượng các dòng
có tên hàng là "Nệm …" → điền vào cột Số lượng bảng kê. Gối, ga, phí… KHÔNG tính.

Dùng: python so-nem-bh.py --tu 2026-10-01 --den 2026-10-31 BH05036 BH05065 ...
In TSV: BH <tab> số tấm nệm <tab> chi tiết từng dòng. Không ghi gì lên MISA/ERP.
"""
import importlib.util
import os
import sys

for _l in (sys.stdout, sys.stderr):
    try:
        _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location('qb', os.path.join(HERE, 'quet-bh-misa-len-erp.py'))
qb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qb)


def la_nem(ten):
    return (ten or '').strip().lower().startswith('nệm')


def main():
    tu = qb.tham_so('--tu', '2026-10-01')
    den = qb.tham_so('--den', '2026-10-31')
    can = [a.strip().upper() for a in sys.argv[1:] if a.upper().startswith('BH')]
    H = qb.headers_misa()
    ds = {d['refno']: d for d in qb.quet_bh(H, tu, den)}
    print('BH\tso_tam_nem\tchi_tiet')
    for bh in can:
        d = ds.get(bh)
        if not d:
            print('%s\tKHONG_THAY\t' % bh)
            continue
        dong, _ = qb.quet_dong_bh(H, d.get('refid'))
        tong, ct = 0.0, []
        for x in dong:
            ten = (x.get('description') or x.get('inventory_item_name') or '').strip()
            sl = float(x.get('quantity') or 0)
            if la_nem(ten):
                tong += sl
            ct.append('%s%s x%g' % ('*' if la_nem(ten) else '', x.get('inventory_item_code'), sl))
        print('%s\t%g\t%s' % (bh, tong, ' ; '.join(ct)))


if __name__ == '__main__':
    main()
