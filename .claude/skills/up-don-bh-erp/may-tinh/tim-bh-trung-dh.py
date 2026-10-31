# -*- coding: utf-8 -*-
"""CHỈ ĐỌC (29/09/2026). Tìm Sales Order của BH (po_no BH…) trùng với Sales Order ĐH đã có trên ERP.
Khớp khi: cùng khách, mọi dòng BH (mã hàng + đơn giá ±1đ) đều có trong đơn ĐH với SL ĐH ≥ SL BH.
Chấm thêm: Diễn giải MISA ghi 'ĐHxxxx' trùng po_no đơn ĐH; cùng tổng tiền; ĐH đã giao."""
import importlib.util, json, os, re, sys, datetime as dt, urllib.parse as up
for _l in (sys.stdout, sys.stderr):
    try: _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], '--tu', '2026-09-20', '--den', dt.date.today().isoformat()]
s = importlib.util.spec_from_file_location('bh', os.path.join(HERE, 'quet-bh-misa-len-erp.py'))
bh = importlib.util.module_from_spec(s); s.loader.exec_module(bh); qd = bh.qd
qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()
H = bh.headers_misa()
memo = {d['refno']: (d.get('journal_memo') or '') for d in bh.quet_bh(H, bh.TU, bh.DEN)}
F = ['name', 'customer', 'grand_total', 'po_no', 'transaction_date', 'per_delivered', 'owner', 'creation', 'docstatus']
so_bh = qd.erp_ds('Sales Order', [['docstatus', 'in', [0, 1]], ['po_no', 'like', 'BH%']], F, 1000)
so_dh = qd.erp_ds('Sales Order', [['docstatus', 'in', [0, 1]], ['po_no', 'is', 'not set'], ['transaction_date', '>=', '2026-09-10']], F, 2000) + qd.erp_ds('Sales Order', [['docstatus', 'in', [0, 1]], ['po_no', 'not like', 'BH%'],
                                  ['transaction_date', '>=', '2026-09-10']], F, 2000)
_c = {}
def dong(t):
    if t not in _c:
        d = qd.erp('/api/resource/Sales%20Order/' + up.quote(t)).get('data', {})
        _c[t] = [(i['item_code'], float(i['qty']), float(i['rate'])) for i in d.get('items', [])]
    return _c[t]
theo_kh = {}
for x in so_dh: theo_kh.setdefault(x['customer'], []).append(x)
kq = []
for b in sorted(so_bh, key=lambda x: x['po_no']):
    ung = theo_kh.get(b['customer'], [])
    if not ung: continue
    db = dong(b['name'])
    for d in ung:
        dd = dong(d['name'])
        ok = all(any(m == m2 and abs(r - r2) <= 1 and q2 + 1e-9 >= q for m2, q2, r2 in dd) for m, q, r in db)
        if not ok: continue
        dh_memo = re.findall(r'ĐH\d+', memo.get(b['po_no'], ''))
        kq.append({'bh': b['po_no'], 'so_bh': b['name'], 'ngay_bh': b['transaction_date'], 'tong_bh': b['grand_total'],
                   'giao_bh': b['per_delivered'], 'so_dh': d['name'], 'po_dh': d['po_no'], 'ngay_dh': d['transaction_date'],
                   'tong_dh': d['grand_total'], 'giao_dh': d['per_delivered'], 'khach': b['customer'],
                   'cung_tong': abs(float(b['grand_total']) - float(d['grand_total'])) <= 2,
                   'memo_khop': (d.get('po_no') in dh_memo), 'memo': memo.get(b['po_no'], '')[:60],
                   'nguoi_bh': b['owner'].split('@')[0], 'tao_bh': b['creation'][:16]})
print('Đơn BH đang hiệu lực: %d · đơn ĐH/khác từ 10/09: %d · cặp nghi trùng: %d' % (len(so_bh), len(so_dh), len(kq)))
for k in kq:
    print('%s %s (%s, %s đ, giao %d%%) ⇄ %s %s (%s, %s đ, giao %d%%) · %s%s%s · %s'
          % (k['bh'], k['so_bh'], k['ngay_bh'], qd.tien(k['tong_bh']), round(float(k['giao_bh'] or 0)),
             k['po_dh'], k['so_dh'], k['ngay_dh'], qd.tien(k['tong_dh']), round(float(k['giao_dh'] or 0)),
             'CÙNG TỔNG ' if k['cung_tong'] else '', 'MEMO KHỚP ' if k['memo_khop'] else '',
             k['khach'][:28], k['memo']))
json.dump(kq, open(os.path.join(HERE, 'log', 'bh-trung-dh.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
