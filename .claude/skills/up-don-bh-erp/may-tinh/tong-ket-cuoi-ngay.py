"""Tổng kết BH cuối ngày → Telegram cho Tú, rồi ghi mốc log\bao-cuoi-ngay.txt. Dựng 06/10/2026.

Routine gọi tong-ket-cuoi-ngay.cmd KHÔNG kèm tham số (lệnh kèm nội dung tin nhắn bị hỏi quyền, phiên nền treo
từ 19:16 ngày 05/10 tới 16:58 ngày 06/10/2026). Script tự đếm, tự gửi, tự ghi mốc; mỗi ngày gửi một lần.
"""
import datetime as dt
import importlib.util
import os
import re
import sys
from pathlib import Path

for _l in (sys.stdout, sys.stderr):
    try:
        _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
MOC = HERE / 'log' / 'bao-cuoi-ngay.txt'
MOC_QUET = HERE / 'log' / 'lan-quet-thanh-cong.txt'
SO = Path(r'C:\Claude Code\routines\misa-bh-sync-bo-qua.md')


def nap(ten, file):
    s = importlib.util.spec_from_file_location(ten, str(HERE / file))
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def main():
    hom_nay = dt.date.today()
    try:
        if MOC.read_text(encoding='utf-8').strip()[:10] == hom_nay.isoformat():
            print('Tổng kết %s đã gửi rồi, bỏ qua.' % hom_nay.strftime('%d/%m/%Y'))
            return 0
    except FileNotFoundError:
        pass

    qd = nap('qd', 'quet-don-misa-len-erp.py')
    qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()
    don = qd.erp_ds('Sales Order', [['po_no', 'like', 'BH%'],
                                    ['creation', '>=', hom_nay.isoformat() + ' 00:00:00'],
                                    ['docstatus', 'in', [0, 1, 2]]],
                    ['name', 'po_no', 'docstatus', 'grand_total'], 500)
    sub = [d for d in don if d['docstatus'] == 1]
    nhap = [d for d in don if d['docstatus'] == 0]
    tong = sum(float(d['grand_total'] or 0) for d in sub)

    cho, trong = 0, False
    for dong in SO.read_text(encoding='utf-8').splitlines():
        if dong.startswith('## '):
            trong = dong.startswith('## Chờ Ngọc Tú quyết')
        elif trong and re.match(r'^- BH\d', dong):
            cho += 1
    try:
        tot = MOC_QUET.read_text(encoding='utf-8').strip()[-5:]
    except FileNotFoundError:
        tot = '?'

    tin = ('🕔 Tổng kết BH %s: up %d đơn (tổng %s đ) · Nháp %d · chờ công chúa quyết %d · lượt quét tốt gần nhất %s'
           % (hom_nay.strftime('%d/%m/%Y'), len(sub), '{:,.0f}'.format(tong).replace(',', '.'), len(nhap), cho, tot))
    print(tin)
    tele = nap('tele', 'tele.py')
    if tele.gui(tin):
        MOC.write_text(hom_nay.isoformat() + '\n', encoding='utf-8')
        print('Đã ghi mốc', hom_nay.isoformat())
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
