# -*- coding: utf-8 -*-
"""CHỈ ĐỌC. Tìm cặp Sales Order trùng: cùng khách + cùng dòng hàng (mã, SL, đơn giá) + cùng tổng tiền.
Tú yêu cầu 29/09/2026 sau khi thấy máy quét up BH mà ERP đã có đơn (đã xuất kho).
Dùng: python tim-don-trung.py [tu_ngay]
"""
import importlib.util
import json
import os
import sys
import urllib.parse as up

for _l in (sys.stdout, sys.stderr):
    try:
        _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
TU = sys.argv[1] if len(sys.argv) > 1 else '2026-09-15'
sys.argv = [sys.argv[0]]
s = importlib.util.spec_from_file_location('qd', os.path.join(HERE, 'quet-don-misa-len-erp.py'))
qd = importlib.util.module_from_spec(s)
s.loader.exec_module(qd)
qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()

ds = qd.erp_ds('Sales Order', [['docstatus', 'in', [0, 1]], ['transaction_date', '>=', TU],
                               ['company', '=', qd.CONG_TY]],
               ['name', 'customer', 'grand_total', 'po_no', 'transaction_date', 'per_delivered',
                'per_billed', 'owner', 'creation', 'docstatus', 'status'], 2000)
print('ERP có %d đơn (Nháp + đã duyệt) từ %s' % (len(ds), TU))

nhom = {}
for x in ds:
    nhom.setdefault((x['customer'], round(float(x['grand_total'] or 0))), []).append(x)


def dong(ten):
    d = qd.erp('/api/resource/Sales%20Order/' + up.quote(ten)).get('data', {})
    return sorted((i['item_code'], round(float(i['qty']), 3), round(float(i['rate']), 2))
                  for i in d.get('items', []))


cap = []
for (kh, tong), g in nhom.items():
    if len(g) < 2:
        continue
    theo_dong = {}
    for x in g:
        theo_dong.setdefault(tuple(dong(x['name'])), []).append(x)
    for d_, gg in theo_dong.items():
        if len(gg) >= 2:
            cap.append((kh, tong, d_, sorted(gg, key=lambda x: x['creation'])))

print('\nNHÓM TRÙNG (cùng khách + cùng dòng hàng + cùng tổng): %d nhóm' % len(cap))
for kh, tong, d_, gg in sorted(cap, key=lambda c: c[3][0]['transaction_date']):
    print('\n● %s · %s đ · %d dòng: %s' % (kh[:45], qd.tien(tong), len(d_),
          '; '.join('%s×%g' % (m, q) for m, q, r in d_)[:120]))
    for x in gg:
        print('   %s · po_no %-9s · ngày %s · tạo %s bởi %s · giao %s%% · HĐ %s%% · %s'
              % (x['name'], x.get('po_no') or '—', x['transaction_date'], x['creation'][:16],
                 (x['owner'] or '').split('@')[0], round(float(x['per_delivered'] or 0)),
                 round(float(x['per_billed'] or 0)), 'Nháp' if x['docstatus'] == 0 else x['status']))
json.dump([{'khach': kh, 'tong': tong, 'don': [x['name'] for x in gg]} for kh, tong, d_, gg in cap],
          open(os.path.join(HERE, 'log', 'don-trung.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
