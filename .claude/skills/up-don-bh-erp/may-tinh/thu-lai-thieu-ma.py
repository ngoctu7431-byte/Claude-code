"""Thử lại BH tắc vì THIẾU MÃ HÀNG / THIẾU KHÁCH trên ERP (Tú chốt 03/10/2026).

Đọc mục "## Chờ bổ sung mã (máy tự thử lại mỗi lượt)" trong sổ bỏ qua. Mỗi dòng
    - BHxxxxx · ngày HT yyyy-mm-dd · thiếu mã: A, B
    - BHxxxxx · ngày HT yyyy-mm-dd · mã chưa bật bán: X
    - BHxxxxx · ngày HT yyyy-mm-dd · thiếu khách: Tên khách
ERP đã bổ sung đủ → xoá dòng khỏi sổ, gọi chay-routine.cmd --chi BHxxxxx --tu <ngày HT> (vẫn qua đủ luật
kiểm trùng + kiểm tiền). Vẫn tắc → ghi BH vào "## Chờ Ngọc Tú quyết" kèm lý do mới.

Routine gọi file .cmd cùng tên, KHÔNG kèm tham số, để khớp đúng quyền đã cho phép sẵn (lệnh kèm số BH
bị hỏi quyền → phiên nền treo, 03/10/2026 20:08).
"""
import datetime as dt
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

for _l in (sys.stdout, sys.stderr):
    try:
        _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
SO = Path(r'C:\Claude Code\routines\misa-bh-sync-bo-qua.md')
MUC_THU = '## Chờ bổ sung mã (máy tự thử lại mỗi lượt)'
MUC_CHO = '## Chờ Ngọc Tú quyết'
DONG = re.compile(r'^- (BH\d+) · ngày HT (\d{4}-\d{2}-\d{2}) · (thiếu mã|mã chưa bật bán|thiếu khách): (.+?)\s*$')

_s = importlib.util.spec_from_file_location('qd', os.path.join(HERE, 'quet-don-misa-len-erp.py'))
qd = importlib.util.module_from_spec(_s)
_s.loader.exec_module(qd)
qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()


def da_bo_sung(loai, gia_tri):
    if loai == 'thiếu khách':
        # Tú chốt 15/10/2026: thiếu khách thì máy quét tự lấy khách từ MISA tạo sang ERP, nên luôn sẵn sàng
        # để thử lại (vẫn tắc, vd khách nghi trùng, thì lại ghi vào "Chờ Ngọc Tú quyết").
        return True
    ma = [m.strip() for m in gia_tri.split(',') if m.strip()]
    loc = [['item_code', 'in', ma], ['disabled', '=', 0]]
    if loai == 'mã chưa bật bán':
        loc.append(['is_sales_item', '=', 1])
    co = {d['name'] for d in qd.erp_ds('Item', loc, ['name'], 50)}
    return all(m in co for m in ma)


def main():
    noi_dung = SO.read_text(encoding='utf-8').splitlines()
    try:
        dau = noi_dung.index(MUC_THU)
    except ValueError:
        print('⛔ Sổ không có mục "%s"' % MUC_THU)
        return 1
    cuoi = next((i for i in range(dau + 1, len(noi_dung)) if noi_dung[i].startswith('## ')), len(noi_dung))
    cho, san_sang = 0, []
    for i in range(dau + 1, cuoi):
        m = DONG.match(noi_dung[i])
        if not m:
            continue
        bh, ngay, loai, gia_tri = m.groups()
        if da_bo_sung(loai, gia_tri):
            san_sang.append((i, bh, ngay, loai, gia_tri))
        else:
            cho += 1

    print('Thử lại BH thiếu mã/khách · %s' % dt.datetime.now().strftime('%d/%m/%Y %H:%M'))
    if not san_sang:
        print('TÓM TẮT THỬ LẠI: up 0 · vẫn tắc 0 · còn chờ ERP bổ sung %d' % cho)
        return 0

    # Xoá các dòng đã sẵn sàng khỏi sổ TRƯỚC khi up (máy quét bỏ qua mọi BH có trong sổ).
    bo = {x[0] for x in san_sang}
    noi_dung = [d for i, d in enumerate(noi_dung) if i not in bo]
    SO.write_text('\n'.join(noi_dung) + '\n', encoding='utf-8')

    up, tac = 0, []
    for _, bh, ngay, loai, gia_tri in san_sang:
        print('\n→ ERP đã bổ sung %s "%s" → up lại %s (ngày HT %s)' % (loai.replace('thiếu ', ''), gia_tri, bh, ngay))
        kq = subprocess.run(['cmd', '/c', os.path.join(HERE, 'chay-routine.cmd'), '--chi', bh, '--tu', ngay],
                            capture_output=True, text=True, encoding='utf-8', errors='replace')
        ra = kq.stdout + kq.stderr
        dong_ok = [d.strip() for d in ra.splitlines() if d.strip().startswith('✅ ' + bh)]
        da_co = [d.strip() for d in ra.splitlines() if re.match(r'^%s\s+→ SAL-ORD-' % bh, d.strip())]
        if dong_ok:
            up += 1
            print('   ✅ THỬ LẠI ĐÃ UP: ' + dong_ok[0][2:].strip())
        elif da_co:
            # Có người đã up tay trong lúc chờ → không làm gì thêm, không ghi sổ.
            print('   ☑️ ĐÃ CÓ SẴN TRÊN ERP: ' + da_co[0])
        else:
            ly = next((d.strip() for d in ra.splitlines() if d.strip().startswith(bh)), '')
            ly = ly[len(bh):].strip() if ly else (ra.strip().splitlines() or ['không rõ'])[-1]
            tac.append((bh, ly))
            print('   ⛔ THỬ LẠI VẪN TẮC: %s · %s' % (bh, ly))

    if tac:
        noi_dung = SO.read_text(encoding='utf-8').splitlines()
        j = noi_dung.index(MUC_CHO) + 1
        hom_nay = dt.date.today().strftime('%d/%m/%Y')
        for bh, ly in reversed(tac):
            noi_dung.insert(j, '- %s · thử lại sau khi ERP bổ sung mã/khách vẫn tắc: %s (%s)' % (bh, ly, hom_nay))
        SO.write_text('\n'.join(noi_dung) + '\n', encoding='utf-8')

    print('\nTÓM TẮT THỬ LẠI: up %d · vẫn tắc %d · còn chờ ERP bổ sung %d' % (up, len(tac), cho))
    return 0


if __name__ == '__main__':
    sys.exit(main())
