# -*- coding: utf-8 -*-
"""Gửi thông báo Telegram cho Tú (dựng 29/09/2026).

Mã bot và chat_id cất ở <thư mục người dùng>\\.ntv-secrets\\telegram.env, NGOÀI thư mục script.
Claude không đọc, không in, không chép mã bot.

Dùng:
    python tele.py --cai               # Tú tự dán mã bot (không hiện chữ), rồi nhắn /start cho bot
    python tele.py "nội dung"          # gửi một tin
    python tele.py --tu-log <file>     # đọc log máy quét, có chuyện đáng báo thì gửi
"""
import getpass
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

for _l in (sys.stdout, sys.stderr):
    try:
        _l.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

KHOA = Path.home() / '.ntv-secrets' / 'telegram.env'


def doc():
    d = {}
    if KHOA.exists():
        for ln in KHOA.read_text(encoding='utf-8').splitlines():
            if '=' in ln:
                a, b = ln.split('=', 1)
                d[a.strip()] = b.strip()
    return d


def ghi(d):
    KHOA.parent.mkdir(exist_ok=True)
    KHOA.write_text(''.join('%s=%s\n' % kv for kv in d.items()), encoding='utf-8')
    try:
        KHOA.chmod(0o600)       # Mac/Linux; Windows bỏ qua
    except Exception:
        pass


def api(token, ham, **tham):
    url = 'https://api.telegram.org/bot%s/%s' % (token, ham)
    data = urllib.parse.urlencode(tham).encode('utf-8') if tham else None
    with urllib.request.urlopen(url, data, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))


def gui(noi_dung):
    d = doc()
    if not d.get('TOKEN') or not d.get('CHAT_ID'):
        print('⛔ Chưa cài Telegram — chạy cai-tele.cmd')
        return False
    loi = 'Telegram trả ok=false'
    for i in range(3):
        try:
            r = api(d['TOKEN'], 'sendMessage', chat_id=d['CHAT_ID'], text=noi_dung[:4000])
            if r.get('ok'):
                print('✅ đã gửi Telegram')
                return True
        except Exception as e:
            loi = str(e)[:120]
        time.sleep(3 * (i + 1))
    print('⛔ gửi Telegram không được: %s' % loi)
    return False


DA_GUI = Path(__file__).resolve().parent / 'log' / 'tele-da-gui.json'


def gui_moi(kenh, tieu_de, than):
    """Chống lặp: cùng kênh mà nội dung y như lần gửi trước (vd đơn 00228 chờ kho, lượt nào
    cũng thấy) thì KHÔNG gửi lại. Nội dung đổi, hoặc qua ngày mới, thì gửi."""
    try:
        cu = json.loads(DA_GUI.read_text(encoding='utf-8'))
    except Exception:
        cu = {}
    dau = time.strftime('%Y-%m-%d') + '|' + than
    if cu.get(kenh) == dau:
        print('(Telegram: giống tin trước, không gửi lại)')
        return
    if gui(tieu_de + ' · ' + time.strftime('%d/%m/%Y %H:%M') + '\n\n' + than):
        cu[kenh] = dau
        DA_GUI.parent.mkdir(exist_ok=True)
        DA_GUI.write_text(json.dumps(cu, ensure_ascii=False), encoding='utf-8')


def cai():
    print('== Cài thông báo Telegram ==')
    tok = getpass.getpass('Dán MÃ BOT (BotFather đưa, dạng 123456:ABC...) rồi Enter (không hiện chữ): ').strip()
    try:
        me = api(tok, 'getMe')['result']
    except Exception as e:
        print('⛔ Mã bot không đúng (%s). Chạy lại và dán lại.' % str(e)[:80])
        input('Enter để đóng…')
        return
    print('Bot: @%s' % me.get('username'))
    print('\nBây giờ mở Telegram, tìm @%s, bấm START (hoặc nhắn "hi"). Em chờ tối đa 3 phút…' % me.get('username'))
    # Chỉ nhận tin nhắn gửi SAU lúc bắt đầu cài, và bắt người cài xác nhận đúng tên — không thì
    # ai từng nhắn bot trước đó (tin cũ còn trong getUpdates) sẽ nhận hết số nội bộ (sửa khi gộp 29/09).
    bat_dau = int(time.time()) - 5
    chat, ten = None, ''
    het = time.time() + 180
    while time.time() < het and not chat:
        try:
            for u in api(tok, 'getUpdates', timeout=20).get('result', []):
                m = u.get('message') or {}
                if m.get('chat', {}).get('type') == 'private' and int(m.get('date') or 0) >= bat_dau:
                    c = m['chat']
                    ten = ('%s %s @%s' % (c.get('first_name', ''), c.get('last_name', ''),
                                          c.get('username', '—'))).strip()
                    if input('Thấy tin của: %s — đúng người nhận báo cáo chưa? (c/k): ' % ten
                             ).strip().lower().startswith('c'):
                        chat = c['id']
                        break
                    print('Bỏ qua, chờ tin khác…')
        except Exception:
            time.sleep(3)
    if not chat:
        print('⛔ Chưa thấy tin nhắn nào gửi cho bot. Chạy lại rồi bấm START trong Telegram.')
        input('Enter để đóng…')
        return
    ghi({'TOKEN': tok, 'CHAT_ID': str(chat)})
    print('Đã nối với khung chat của %s.' % ten)
    gui('✅ Bot đã nối xong. Từ nay máy quét BH MISA → ERP báo anh qua đây.')
    input('\nXong. Enter để đóng…')


def tu_log(file):
    """Đọc log một lượt máy quét. Báo khi: tạo đơn, bù ngày lỡ, tắc, tồn cũ, lệch, nháp, lỗi, MISA đăng xuất."""
    t = Path(file).read_text(encoding='utf-8', errors='replace')
    if 'TÓM TẮT CẬP NHẬT' in t or 'cap-nhat-lech' in t.splitlines()[0]:
        return tu_log_lech(t)
    tom = re.findall(r'TÓM TẮT: (.*)', t)
    dong_tom = tom[-1] if tom else ''
    so = {k: int(v) for k, v in re.findall(r'(tạo|tắc|tồn cũ|lệch tiền) (\d+)', dong_tom)}
    tin = []
    if 'PHIÊN MISA ĐÃ HẾT' in t:
        # Nhắc MỖI lượt (không chống lặp) cho tới khi Tú đăng nhập lại.
        try:
            moc = (Path(__file__).resolve().parent / 'log' / 'lan-quet-thanh-cong.txt').read_text().strip()
        except Exception:
            moc = '?'
        gui('⚠️ MISA đăng xuất — chưa quét được BH từ %s. Cửa sổ đăng nhập đã mở sẵn trên máy, anh '
            'đăng nhập rồi đóng cửa sổ. BH những giờ lỡ máy sẽ tự bù.' % moc)
        return
    if 'Lượt trước còn đang chạy' in t:
        return
    if 'TÀI KHOẢN MISA ĐANG MỞ Ở CHỖ KHÁC' in t:
        gui_moi('dung-chung', 'BH MISA → ERP', '⚠️ Máy quét chưa chạy được: tài khoản MISA đang mở ở '
                'Chrome khác. Đóng MISA ở đó (hoặc dùng tài khoản riêng cho máy quét), lượt sau tự chạy lại.')
        return
    if 'Traceback' in t or ('⛔' in t and not tom and 'PHIÊN MISA ĐÃ HẾT' not in t):
        tin.append('⛔ Máy quét lỗi:\n' + '\n'.join(t.strip().splitlines()[-6:]))
    if 'BÙ NGÀY LỠ' in t:
        tin.append('↩️ ' + re.search(r'BÙ NGÀY LỠ[^\n]*', t).group(0))
    ok = re.findall(r'✅ (BH\d+)\s+→ (SAL-ORD-\S+) · tổng ([\d.]+)', t)
    if ok:
        tin.append('✅ Đã up %d đơn:\n' % len(ok) + '\n'.join('%s → %s · %s đ' % x for x in ok))
    for nhom, bieu in (('TẮC', 'tắc'), ('TỒN CŨ', 'tồn cũ'), ('TIỀN LỆCH', 'lệch tiền')):
        if so.get(bieu):
            m = re.search(r'── [^\n]*%s[^\n]*\n((?:   [^\n]*\n?)+)' % nhom, t)
            tin.append('⚠️ %s (%d):\n%s' % (nhom, so[bieu], (m.group(1).rstrip() if m else '')[:1500]))
    nhap = re.findall(r'⛔ (BH\d+)\s+→ (SAL-ORD-\S+) để NHÁP[^\n]*', t)
    if nhap:
        tin.append('⛔ Để NHÁP, cần xem: ' + ', '.join('%s→%s' % x for x in nhap))
    if tin:
        gui_moi('quet', 'BH MISA → ERP', '\n\n'.join(tin))


def tu_log_lech(t):
    """Log của cap-nhat-lech (sửa đơn ERP cho khớp BH kế toán đã sửa)."""
    if 'PHIÊN MISA ĐÃ HẾT' in t or 'Lượt trước còn đang chạy' in t:
        return      # máy quét chính đã báo
    tom = re.findall(r'TÓM TẮT CẬP NHẬT: (.*)', t)
    if not tom:
        if 'Traceback' in t or '⛔' in t:
            gui('⛔ Bước sửa lệch ERP lỗi:\n' + '\n'.join(t.strip().splitlines()[-6:]))
        return
    so = {k: int(v) for k, v in re.findall(r'(sửa|không tự sửa được|lỗi) (\d+)', tom[-1])}
    tin = []
    for nhom, k in (('SỬA CHO KHỚP MISA', 'sửa'), ('LỆCH MÀ KHÔNG TỰ SỬA ĐƯỢC', 'không tự sửa được'),
                    ('LỖI', 'lỗi')):
        if so.get(k):
            m = re.search(r'── [^\n]*%s[^\n]*\n((?:    ?[^\n]*\n?)+)' % re.escape(nhom), t)
            tin.append('%s (%d):\n%s' % (nhom, so[k], (m.group(1).rstrip() if m else '')[:1500]))
    if tin:
        if so.get('sửa'):
            tin.append('Phần hàng thêm hiện "chưa giao" trên ERP — kho làm thêm phiếu giao nếu đã giao thật.')
        gui_moi('lech', 'Sửa đơn ERP theo BH MISA', '\n\n'.join(tin))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        print(__doc__)
    elif a[0] == '--cai':
        cai()
    elif a[0] == '--tu-log':
        tu_log(a[1])
    else:
        gui(' '.join(a))
