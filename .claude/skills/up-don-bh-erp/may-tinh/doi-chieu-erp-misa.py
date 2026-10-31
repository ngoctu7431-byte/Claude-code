# -*- coding: utf-8 -*-
"""CHỈ ĐỌC. Đối chiếu Sales Order đang hiệu lực (po_no = BH) với BH đang có trên MISA.
Tìm đơn ERP mà số BH của nó KHÔNG còn trên MISA (kế toán đã xoá/lập lại BH) → nghi trùng.
Dùng: python doi-chieu-erp-misa.py 2026-09-20
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
_dt = __import__('datetime')
# Mặc định: 10 ngày gần nhất, nhưng không trước 24/09/2026 (routine chỉ up BH từ ngày đó).
tu = sys.argv[1] if len(sys.argv) > 1 else max(
    '2026-09-24', (_dt.date.today() - _dt.timedelta(days=10)).isoformat())
sys.argv = [sys.argv[0], '--tu', tu, '--den', __import__('datetime').date.today().isoformat()]
s = importlib.util.spec_from_file_location('bh', os.path.join(HERE, 'quet-bh-misa-len-erp.py'))
bh = importlib.util.module_from_spec(s)
s.loader.exec_module(bh)
qd = bh.qd
qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()

H = bh.headers_misa()
misa = {d['refno']: d for d in bh.quet_bh(H, bh.TU, bh.DEN) if d['refno']}
so = qd.erp_ds('Sales Order', [['po_no', 'like', 'BH%'], ['docstatus', '=', 1],
                               ['transaction_date', '>=', tu]],
               ['name', 'po_no', 'customer', 'grand_total', 'transaction_date'], 500)
print('MISA %d BH · ERP %d đơn hiệu lực có po_no BH (từ %s)' % (len(misa), len(so), tu))
mo_coi = [x for x in so if x['po_no'] not in misa]
lech = [x for x in so if x['po_no'] in misa
        and abs(float(x['grand_total']) - float(misa[x['po_no']].get('total_amount') or 0)) > 2]
# Ngưỡng 2đ như cap-nhat-lech-bh.py: ERP làm tròn VAT từng dòng nên lệch 1–2đ là thường (00229, 00230).
print('\n── ĐƠN ERP MÀ SỐ BH KHÔNG CÒN TRÊN MISA (%d)' % len(mo_coi))
for x in sorted(mo_coi, key=lambda x: x['po_no']):
    cung = [d['refno'] for d in misa.values()
            if abs(float(d.get('total_amount') or 0) - float(x['grand_total'])) <= 1]
    print('   %s → %s · %s · %s · %s · BH cùng tiền trên MISA: %s'
          % (x['po_no'], x['name'], x['transaction_date'], x['customer'][:35],
             qd.tien(x['grand_total']), ', '.join(cung) or '—'))
print('\n── ĐƠN ERP LỆCH TIỀN SO BH MISA (%d)' % len(lech))
for x in sorted(lech, key=lambda x: x['po_no']):
    print('   %s → %s · ERP %s · MISA %s' % (x['po_no'], x['name'], qd.tien(x['grand_total']),
                                            qd.tien(misa[x['po_no']].get('total_amount'))))
