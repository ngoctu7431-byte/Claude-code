# -*- coding: utf-8 -*-
"""Cài máy quét BH MISA → ERP lên một máy mới (Windows hoặc Mac). Chạy trong thư mục gói:
    python cai-quet-bh.py                 # Windows: cài vào C:\\Claude Code\\routines\\quet-bh
    python cai-quet-bh.py --dich <thư mục>

Không đụng gì trên MISA hay ERP. Chỉ: chép 2 script, dựng môi trường Python, cất khoá ERP
vào <thư mục người dùng>/.ntv-secrets/frappe-prod.env (ngoài thư mục script).
"""
import getpass
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

for _luong in (sys.stdout, sys.stderr):
    try:
        _luong.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

WIN = os.name == 'nt'
NGUON = Path(__file__).resolve().parent
MAC_DINH = Path(r'C:\Claude Code\routines\quet-bh') if WIN else Path.home() / 'ntv-quet-bh'
DICH = Path(sys.argv[sys.argv.index('--dich') + 1]) if '--dich' in sys.argv else MAC_DINH
KHO_KHOA = Path.home() / '.ntv-secrets'
KHOA = KHO_KHOA / 'frappe-prod.env'
SCRIPT = ['quet-don-misa-len-erp.py', 'quet-bh-misa-len-erp.py']


def dung(msg):
    print('⛔ ' + msg)
    if WIN:
        input('Bấm Enter để đóng…')
    sys.exit(1)


def co_chrome():
    if WIN:
        goc = [os.environ.get(k, '') for k in ('ProgramFiles', 'ProgramFiles(x86)', 'LOCALAPPDATA')]
        return any(Path(g, 'Google', 'Chrome', 'Application', 'chrome.exe').exists()
                   for g in goc if g)
    return Path('/Applications/Google Chrome.app').exists()


print('== 1/4 Kiểm máy')
if sys.version_info < (3, 9):
    dung('Python cũ hơn 3.9 — cài Python mới rồi chạy lại.')
if not co_chrome():
    dung('Chưa cài Google Chrome — cài xong chạy lại.')
print('   Chrome ✓  Python %d.%d ✓' % sys.version_info[:2])

print('== 2/4 Chép script vào %s' % DICH)
DICH.mkdir(parents=True, exist_ok=True)
for f in SCRIPT:
    if not (NGUON / f).exists():
        dung('Thiếu %s trong gói — giải nén lại đủ file.' % f)
    shutil.copy2(NGUON / f, DICH / f)
print('   %d file ✓' % len(SCRIPT))

print('== 3/4 Dựng môi trường Python + Playwright (dùng Chrome có sẵn, không tải trình duyệt)')
PY = DICH / '.venv' / ('Scripts/python.exe' if WIN else 'bin/python')
if not PY.exists():
    subprocess.check_call([sys.executable, '-m', 'venv', str(DICH / '.venv')])
# Python 3.9 chỉ chạy tới Playwright 1.60 (bản cuối còn hỗ trợ 3.9).
goi = 'playwright==1.60.0' if sys.version_info < (3, 10) else 'playwright'
subprocess.check_call([str(PY), '-m', 'pip', 'install', '-q', '--upgrade', 'pip'])
subprocess.check_call([str(PY), '-m', 'pip', 'install', '-q', goi])
print('   playwright ✓')

print('== 4/4 Khoá ERP (của CHÍNH người dùng máy này — đừng dùng khoá người khác)')
KHO_KHOA.mkdir(exist_ok=True)
if not WIN:
    os.chmod(KHO_KHOA, 0o700)
if KHOA.exists() and KHOA.stat().st_size:
    print('   Đã có %s — giữ nguyên.' % KHOA)
else:
    k = input('   API Key: ').strip()
    s = getpass.getpass('   API Secret (gõ/dán không hiện chữ, xong bấm Enter): ').strip()
    KHOA.write_text('FRAPPE_PROD_URL=https://platform.nguoithuanviet.com\n'
                    'FRAPPE_PROD_API_KEY=%s\nFRAPPE_PROD_API_SECRET=%s\n' % (k, s),
                    encoding='utf-8')
    if not WIN:
        os.chmod(KHOA, 0o600)
    print('   Cất vào %s ✓' % KHOA)

d = {}
for ln in KHOA.read_text(encoding='utf-8').splitlines():
    if '=' in ln and not ln.startswith('#'):
        a, b = ln.strip().split('=', 1)
        d[a] = b.strip().strip('"').strip("'")
req = urllib.request.Request(d.get('FRAPPE_PROD_URL', '') + '/api/method/frappe.auth.get_logged_user')
req.add_header('Authorization', 'token %s:%s' % (d.get('FRAPPE_PROD_API_KEY'), d.get('FRAPPE_PROD_API_SECRET')))
try:
    ai = json.loads(urllib.request.urlopen(req, timeout=30).read())['message']
    print('   Khoá ERP chạy được — tài khoản: %s' % ai)
except Exception as e:
    print('   ⛔ Khoá ERP KHÔNG chạy được (%s).\n      Xoá file %s rồi chạy lại bộ cài với khoá đúng.'
          % (e, KHOA))

chay = '"%s" "%s"' % (PY, DICH / 'quet-bh-misa-len-erp.py')
lenh = '''LỆNH MÁY QUÉT BH (bộ cài ghi ra)

Đăng nhập MISA (1 lần, và mỗi khi báo PHIÊN MISA ĐÃ HẾT):
  {c} --dang-nhap

Chạy thử CHỈ XEM:
  {c} --tu-dong --bo-qua "<đường dẫn sổ bỏ qua>"

Routine gọi (ghi thật):
  {c} --tu-dong --that --bo-qua "<đường dẫn sổ bỏ qua>"
'''.format(c=chay)
(DICH / 'LENH.txt').write_text(lenh, encoding='utf-8')
print('\nXong phần cài. Các lệnh dùng tiếp đã ghi vào %s:\n' % (DICH / 'LENH.txt'))
print(lenh)
if WIN:
    input('Bấm Enter để đóng…')
