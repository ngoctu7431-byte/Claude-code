# -*- coding: utf-8 -*-
"""CHỈ ĐỌC (29/09/2026). So đơn BH (Sales Order po_no BH…) với phiếu xuất (Delivery Note) trên ERP."""
import importlib.util, json, os, sys, urllib.parse as up
for _l in (sys.stdout, sys.stderr):
    try: _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv = [sys.argv[0]]
s = importlib.util.spec_from_file_location('qd', os.path.join(HERE, 'quet-don-misa-len-erp.py'))
qd = importlib.util.module_from_spec(s); s.loader.exec_module(qd); qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()
dn = qd.erp_ds('Delivery Note', [['docstatus', 'in', [0, 1]], ['posting_date', '>=', '2026-09-20']],
               ['name', 'customer', 'grand_total', 'po_no', 'posting_date', 'owner', 'creation', 'docstatus'], 2000)
print('Phiếu xuất từ 20/09: %d' % len(dn))
lk = {}
for d in dn:
    x = qd.erp('/api/resource/Delivery%20Note/' + up.quote(d['name'])).get('data', {})
    d['so'] = sorted({i.get('against_sales_order') or '—' for i in x.get('items', [])})
    d['hang'] = sorted((i['item_code'], float(i['qty']), round(float(i['rate']), 2)) for i in x.get('items', []))
khong_so = [d for d in dn if d['so'] == ['—']]
print('Phiếu xuất KHÔNG gắn đơn bán: %d' % len(khong_so))
so_bh = qd.erp_ds('Sales Order', [['docstatus', 'in', [0, 1]], ['po_no', 'like', 'BH%']],
                  ['name', 'customer', 'grand_total', 'po_no', 'transaction_date', 'per_delivered'], 1000)
_c = {}
def dong(t):
    if t not in _c:
        x = qd.erp('/api/resource/Sales%20Order/' + up.quote(t)).get('data', {})
        _c[t] = sorted((i['item_code'], float(i['qty']), round(float(i['rate']), 2)) for i in x.get('items', []))
    return _c[t]
kq = []
for b in so_bh:
    for d in khong_so:
        if d['customer'] != b['customer']: continue
        if dong(b['name']) == d['hang'] or abs(float(b['grand_total']) - float(d['grand_total'])) <= 2:
            kq.append((b, d, dong(b['name']) == d['hang']))
print('Cặp đơn BH ⇄ phiếu xuất không gắn đơn (cùng khách + cùng hàng hoặc cùng tiền): %d' % len(kq))
for b, d, cung_hang in sorted(kq, key=lambda k: k[0]['po_no']):
    print('%s %s (%s, %s đ, giao %d%%) ⇄ %s (po_no %s, %s, %s đ, bởi %s, %s)%s'
          % (b['po_no'], b['name'], b['transaction_date'], qd.tien(b['grand_total']), round(float(b['per_delivered'] or 0)),
             d['name'], d.get('po_no') or '—', d['posting_date'], qd.tien(d['grand_total']), d['owner'].split('@')[0],
             'Nháp' if d['docstatus'] == 0 else 'đã duyệt', ' · CÙNG HÀNG' if cung_hang else ''))
print('\nMẫu phiếu xuất không gắn đơn (10 phiếu mới nhất):')
for d in sorted(khong_so, key=lambda d: d['creation'], reverse=True)[:10]:
    print('  %s · %s · %s · %s đ · po_no %s · bởi %s' % (d['name'], d['posting_date'], d['customer'][:30],
          qd.tien(d['grand_total']), d.get('po_no') or '—', d['owner'].split('@')[0]))
