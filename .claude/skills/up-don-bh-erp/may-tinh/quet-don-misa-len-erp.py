#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quét ĐƠN ĐẶT HÀNG trên MISA rồi dựng Sales Order trên ERP nhà thật — MỘT CHIỀU.

Thay luồng 9 bước bấm tay của sale admin (vào MISA → bấm 1 đơn → In theo lô → chọn
thời gian → Lấy dữ liệu → Chọn tất cả → Đồng ý → xuất Excel → gửi Claude đọc).

Sale vẫn lên đơn TAY trên MISA như cũ. Script chỉ chép sang ERP.
Cửa ngược ERP→MISA để trống — dây chuyền đó bỏ qua mọi đơn có `po_no`, nên hai chiều
không đánh nhau.

Hai cửa MISA (tìm 18/09/2026, KHÔNG phải Open API — Open API không cho đọc chứng từ):
    POST /g2/api/sa/v1/sa_order/paging_filter_v2   → danh sách đơn, filter property 3972
    POST /g2/api/sa/v1/sa_order/get_paging_detail  → dòng hàng, filter property 3993

MẶC ĐỊNH CHỈ XEM THỬ. Muốn ghi thật phải thêm --that.

Dùng:
    python3 quet-don-misa-len-erp.py --tu 2026-09-04 --den 2026-09-04
    python3 quet-don-misa-len-erp.py --tu 2026-09-04 --den 2026-09-04 --that
"""
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dong_bh   # rút gọn ghi chú (luật Tú 19/10/2026: mô tả ERP viết ngắn)

MISA = 'https://actapp.misa.vn'
HO_SO = Path.home() / '.ntv-secrets' / 'chrome-misa'

def khoa_file(duong):
    """Giữ khoá độc quyền trên một file (Mac: flock · Windows: msvcrt). Trả file đang giữ,
    hoặc None nếu tiến trình khác đang giữ. Khoá gắn TIẾN TRÌNH: chết là tự nhả."""
    Path(duong).parent.mkdir(mode=0o700, exist_ok=True)
    f = open(duong, 'a+')
    try:
        if os.name == 'nt':
            import msvcrt
            f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return f
    except OSError:
        f.close()
        return None


_khoa_ho_so = None


def giu_ho_so_misa(han=2700):
    """Xếp hàng dùng hồ sơ Chrome MISA — chạy tay mà đụng lượt job nền là cả hai cùng chết
    (ProcessSingleton, 27/09/2026). Khoá ĐÚNG file `chrome-misa.lock` mà `keo-misa.py`
    (kinh-doanh-dai-ly/07-du-lieu-misa, job kéo MISA 7h05) cũng flock → trên máy Công
    hai bên vẫn xếp hàng với nhau dù không còn import nhau (dời nhà 29/09/2026)."""
    global _khoa_ho_so
    import time
    if _khoa_ho_so:
        return
    t0, da_bao = time.time(), False
    while True:
        _khoa_ho_so = khoa_file(str(HO_SO) + '.lock')
        if _khoa_ho_so:
            return
        if time.time() - t0 > han:
            sys.exit('⛔ Hồ sơ Chrome MISA bận quá %d phút — bỏ lượt.' % (han // 60))
        if not da_bao:
            print('  (hồ sơ Chrome MISA đang có lượt khác dùng — xếp hàng đợi…)')
            da_bao = True
        time.sleep(15)


KHOA_ERP = Path.home() / '.ntv-secrets' / 'frappe-prod.env'

CUA_DS = MISA + '/g2/api/sa/v1/sa_order/paging_filter_v2'
CUA_CT = MISA + '/g2/api/sa/v1/sa_order/get_paging_detail'

CONG_TY = 'Nệm Thành Công'
KHO = 'Kho tổng bán hàng - TC'      # Công chốt 16/09/2026. ⛔ KHÔNG dùng Finished Goods - TC
BANG_GIA_LUI = 'Standard Selling'   # chỉ để đủ ô; rate từng dòng đã tường minh
MAU_THUE = {8: 'VAT 8% - TC', 10: 'Vietnam Tax - TC'}


def tham_so(ten, mac_dinh=None):
    return sys.argv[sys.argv.index(ten) + 1] if ten in sys.argv else mac_dinh


TU = tham_so('--tu', dt.date.today().strftime('%Y-%m-%d'))
DEN = tham_so('--den', TU)
GHI_THAT = '--that' in sys.argv
# Mặc định CHỈ lấy đơn MISA trạng thái 'Chưa thực hiện' (status=0).
LAY_HET = '--lay-het' in sys.argv
# Chạy đúng MỘT đơn — dùng khi thử lần đầu trên máy mới, hoặc khi chỉ cần bù một đơn sót.
# Thử cả lượt ngay lần đầu là đánh cược nhiều đơn vào một đường chưa ai chạy bao giờ.
CHI_MOT = tham_so('--chi')


# ── ERP ────────────────────────────────────────────────────────────────────────
# Máy Tú (29/09/2026): khoá ERP của Tú đã nằm trong khai báo kết nối MCP "frappe" của Claude.
# Không có file .env thì đọc thẳng từ đó (chỉ ĐỌC), khỏi chép khoá ra file thứ hai.
# Có .env thì .env vẫn ưu tiên. Máy khác để đường khác thì đặt biến môi trường NTV_MCP_JSON.
MCP_JSON = Path(os.environ.get('NTV_MCP_JSON') or r'C:\Claude Code\.mcp.json')


def khoa_tu_mcp_json():
    try:
        e = json.loads(MCP_JSON.read_text(encoding='utf-8'))['mcpServers']['frappe']['env']
    except Exception:
        return None
    url = (e.get('FRAPPE_URL') or '').rstrip('/')
    key, sec = e.get('FRAPPE_API_KEY'), e.get('FRAPPE_API_SECRET')
    return (url, 'token %s:%s' % (key, sec)) if (url and key and sec) else None


def khoa_erp():
    if not KHOA_ERP.exists() and khoa_tu_mcp_json():
        return khoa_tu_mcp_json()
    if not KHOA_ERP.exists():
        sys.exit('⛔ Chưa có %s — xin khoá ERP riêng của bạn (đừng dùng chung khoá '
                 'người khác, doanh số sẽ ghi sai tên).' % KHOA_ERP)
    d = {}
    for ln in KHOA_ERP.read_text(encoding='utf-8').splitlines():
        s = ln.strip()
        if s.startswith('export '):
            s = s[7:].strip()
        if s and not s.startswith('#') and '=' in s:
            k, v = s.split('=', 1)
            d[k.strip()] = v.strip().strip('"').strip("'")
    # Tên biến nhà mình dùng là FRAPPE_PROD_* ; giữ cả tên ngắn cho máy khác
    url = (d.get('FRAPPE_PROD_URL') or d.get('FRAPPE_URL')
           or d.get('ERP_URL') or '').rstrip('/')
    key = d.get('FRAPPE_PROD_API_KEY') or d.get('FRAPPE_API_KEY') or d.get('API_KEY')
    sec = (d.get('FRAPPE_PROD_API_SECRET') or d.get('FRAPPE_API_SECRET')
           or d.get('API_SECRET'))
    if not (url and key and sec):
        sys.exit('⛔ %s thiếu FRAPPE_PROD_URL / FRAPPE_PROD_API_KEY / '
                 'FRAPPE_PROD_API_SECRET.' % KHOA_ERP)
    return url, 'token %s:%s' % (key, sec)


ERP_URL, ERP_AUTH = None, None


def erp(path, method='GET', body=None, lan=3):
    """Gọi ERP, thử lại khi mạng/nhà thật chập. Đo 18/09/2026: prod timeout giữa lượt
    quét làm script chết nửa đường — chạy trên máy sale thì đó là hỏng việc, không phải
    một dòng lỗi đẹp."""
    import time
    loi = None
    for i in range(lan):
        req = urllib.request.Request(ERP_URL + path, method=method)
        req.add_header('Authorization', ERP_AUTH)
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(body).encode('utf-8') if body else None
        try:
            with urllib.request.urlopen(req, data, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            # Lỗi nghiệp vụ (4xx) thì thử lại vô ích — trả ngay cho người đọc
            noi_dung = e.read().decode('utf-8')[:400]
            if 400 <= e.code < 500 and e.code not in (408, 429):
                raise RuntimeError('ERP %s: %s' % (e.code, noi_dung))
            loi = RuntimeError('ERP %s: %s' % (e.code, noi_dung))
        except Exception as e:
            loi = RuntimeError('ERP không trả lời (%s)' % str(e)[:120])
        if i < lan - 1:
            time.sleep(3 * (i + 1))
    raise loi


def erp_ds(doctype, filters, fields, limit=20):
    import urllib.parse as up
    q = up.urlencode({'filters': json.dumps(filters), 'fields': json.dumps(fields),
                      'limit_page_length': limit})
    return erp('/api/resource/' + up.quote(doctype) + '?' + q).get('data', [])


# ── MISA ───────────────────────────────────────────────────────────────────────
def headers_misa():
    """Mở trang Đơn đặt hàng, mượn headers giao diện vừa dùng. Cần phiên đăng nhập sống."""
    from playwright.sync_api import sync_playwright
    bat = []
    with sync_playwright() as p:
        giu_ho_so_misa()
        ctx = p.chromium.launch_persistent_context(
            str(HO_SO), channel='chrome', headless=True,
            viewport={'width': 1600, 'height': 1000},
            args=['--disable-blink-features=AutomationControlled'])
        ctx.on('request', lambda r: bat.append(dict(r.headers))
               if 'sa_order/paging_filter_v2' in r.url else None)
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(MISA + '/app', wait_until='domcontentloaded', timeout=90000)
        pg.wait_for_timeout(5000)
        if '/login' in pg.url.lower():
            ctx.close()
            sys.exit('⛔ Phiên MISA đã hết. Chạy `quet-bh-misa-len-erp.py --dang-nhap` '
                     'rồi đăng nhập lại.')
        # Trang SAOrder chỉ gọi paging_filter_v2 khi lưới dữ liệu nạp xong — lúc MISA chậm
        # thì 8 giây là chưa tới. Đo 18/09/2026: đợi cứng 8s trượt 2 lần liền, trong khi
        # bản soi (đợi ~25s + tải lại) bắt được 4 lượt. ⇒ đợi CÓ KIỂM, tải lại nếu chưa thấy.
        for vong in range(3):
            pg.goto(MISA + '/app/SA/SAOrder', wait_until='domcontentloaded', timeout=60000)
            for _ in range(12):           # tối đa 12 × 2s = 24s mỗi vòng
                pg.wait_for_timeout(2000)
                if bat:
                    break
            if bat:
                break
            print('   (lượt %d chưa thấy lưới đơn nạp, tải lại…)' % (vong + 1))
        try:
            ctx.close()
        except Exception:
            pass
    if not bat:
        sys.exit('⛔ Không bắt được lượt gọi paging_filter_v2 sau 3 lần thử — MISA quá '
                 'chậm, hoặc giao diện đã đổi. Chạy soi-cua-don-dat-hang.py để soi lại cửa.')
    return bat[-1]


def misa(H, url, body):
    req = urllib.request.Request(url, method='POST',
                                 data=json.dumps(body).encode('utf-8'))
    for k, v in H.items():
        if k.lower() in ('content-length', 'host', 'connection', 'accept-encoding'):
            continue
        try:
            req.add_header(k, v)
        except Exception:
            pass
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode('utf-8'))


def mang_dong(d):
    g = d.get('Data', d) if isinstance(d, dict) else d
    if isinstance(g, list):
        return g
    if isinstance(g, dict):
        for k in ('PageData', 'Data', 'Items'):
            if isinstance(g.get(k), list):
                return g[k]
        for v in g.values():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
    return []


def utc(ngay, cuoi=False):
    """MISA nhận mốc UTC = giờ VN trừ 7. Gửi T00:00:00Z là lệch cả ngày."""
    t = dt.datetime.strptime(ngay, '%Y-%m-%d')
    t = (t + dt.timedelta(days=1) - dt.timedelta(hours=7, seconds=1)) if cuoi \
        else (t - dt.timedelta(hours=7))
    return t.strftime('%Y-%m-%dT%H:%M:%S.00Z')


def quet_don(H, tu, den):
    body = {
        "sort": '[{"property":3972,"desc":true,"data_type":3,"operand":1}]',
        "filter": [
            {"property": 3972, "value": utc(tu), "operator": 10,
             "operand": 1, "data_type": 3},
            {"property": 3972, "value": utc(den, True), "operator": 12,
             "operand": 1, "data_type": 3},
        ],
        "pageIndex": 1, "pageSize": 500, "useSp": False, "view": 22,
        "summaryColumns": [5127, 5126, 5069, 5068, 5047, 5039, 5097, 5094,
                           3938, 3937, 5124, 5123, 3944, 3943],
        "loadMode": 0,
    }
    return mang_dong(misa(H, CUA_DS, body))


def gom_dong(tho):
    """Gán mỗi dòng ghi chú (dòng không mang mã hàng) vào dòng hàng NGAY TRÊN nó —
    đúng cách MISA bày. Ảnh đơn ĐH03033 (Công gửi 22/09/2026): dòng 1 SORA20-8, ngay
    dưới là "Hạ size 169cm x 192cm x 20cm" không có số thứ tự, rồi dòng 2 SR310-1.

    Giữ được thứ tự gốc nhờ `quet_dong` sort theo một property RỖNG — đo 22/09/2026:
    với property 3876, `desc=true` cũng KHÔNG đảo thứ tự ⇒ field không có giá trị nên
    MISA bỏ qua sort và trả theo thứ tự nhập. Kiểm chéo hai đơn:
      · ĐH03033 → SORA20-8 · ‹ghi chú› · SR310-1, khớp từng dòng với ảnh.
      · ĐH03027 → ghi chú "Hạ size 100cm x 160cm x 15cm" rơi đúng sau SORA15-1
        (tấm 15cm/100x200): hạ chiều dài 200 xuống 160, cao 15 giữ nguyên.
    ⛔ Sort cũ (property 308) làm ghi chú nhảy lên ĐẦU danh sách, mất hẳn liên kết dòng.

    Trả (dòng hàng — mỗi dòng có `_ghi_chu` là list, ghi chú lạc đứng trước mọi dòng hàng).
    """
    ra, lac = [], []
    for x in tho:
        if (x.get('inventory_item_code') or '').strip():
            mot = dict(x)
            mot['_ghi_chu'] = []
            ra.append(mot)
        else:
            g = (x.get('description') or '').strip()
            if not g:
                continue
            if ra:
                ra[-1]['_ghi_chu'].append(g)
            else:
                lac.append(g)
    return ra, lac


def quet_dong(H, refid):
    body = {
        "columns": [2157, 1355, 5274, 3870, 3876, 5281, 5279, 308, 1464,
                    1455, 5364, 5350, 5936, 3404, 5476, 5575],
        # property 3876 RỖNG ⇒ MISA bỏ qua sort, trả theo thứ tự nhập (xem gom_dong).
        "sort": '[{"property":3876,"desc":false,"data_type":1,"operand":1}]',
        "filter": [{"property": 3993, "operator": 7, "operand": 1,
                    "value": refid, "data_type": 10}],
        "pageIndex": 1, "pageSize": 300, "useSp": False,
        "summaryColumns": [3488, 3870, 3878, 3879, 3876, 3877, 2717, 2719],
        "loadMode": 0,
    }
    return gom_dong(mang_dong(misa(H, CUA_CT, body)))


# ── ghép sang ERP ──────────────────────────────────────────────────────────────
_thue_cache = {}


def dong_thue(pt):
    """Đọc dòng thuế THẲNG từ mẫu trên ERP. Truyền mỗi tên mẫu là mất sạch VAT
    mà không báo lỗi — bẫy đã cắn 27/08/2026."""
    pt = int(round(pt or 0))
    if pt in _thue_cache:
        return _thue_cache[pt]
    if pt == 0:
        _thue_cache[0] = ('', [])
        return _thue_cache[0]
    ten = MAU_THUE.get(pt)
    if not ten:
        return None, None
    import urllib.parse as up
    d = erp('/api/resource/' + up.quote('Sales Taxes and Charges Template')
            + '/' + up.quote(ten)).get('data', {})
    dong = [{'charge_type': t.get('charge_type'), 'account_head': t.get('account_head'),
             'description': t.get('description'), 'rate': t.get('rate'),
             'cost_center': t.get('cost_center'),
             'included_in_print_rate': t.get('included_in_print_rate') or 0}
            for t in d.get('taxes', [])]
    _thue_cache[pt] = (ten, dong)
    return _thue_cache[pt]


def tim_customer(ma_so_thue, ten):
    """Khớp theo MÃ trước (mã đối tượng MISA = MST), tên chỉ là đường lùi."""
    for f in ([['tax_id', '=', ma_so_thue]] if ma_so_thue else []):
        ds = erp_ds('Customer', [f], ['name'], 5)
        if len(ds) == 1:
            return ds[0]['name'], 'tax_id'
    if ma_so_thue:
        # Tìm ĐÚNG NGUYÊN MÃ sau nhãn "mã MISA: " (29/09/2026). Kiểu cũ '%mã%' làm mã ngắn
        # KH00001 dính cả KH000012, KH000013… → ra nhiều bản → trượt về khớp tên.
        # Mã đứng cuối chuỗi thì không có ký tự theo sau, nên thử cả hai dạng.
        for mau in ('%mã MISA: ' + ma_so_thue + ' %', '%mã MISA: ' + ma_so_thue):
            ds = erp_ds('Customer', [['customer_details', 'like', mau]], ['name'], 5)
            if len(ds) == 1:
                return ds[0]['name'], 'mã MISA'
        ds = erp_ds('Customer', [['customer_details', 'like', '%' + ma_so_thue + '%']],
                    ['name'], 5)
        if len(ds) == 1:
            return ds[0]['name'], 'customer_details'
    ds = erp_ds('Customer', [['customer_name', '=', ten]], ['name'], 5)
    if len(ds) == 1:
        return ds[0]['name'], 'tên khớp đúng'
    return None, 'không tìm ra (%d ứng viên)' % len(ds)


def da_co_tren_erp(refno):
    """Tra po_no kèm docstatus [0,1] — thiếu docstatus là KHÔNG thấy đơn Nháp
    rồi tạo trùng (bẫy MCP/REST đã đo)."""
    ds = erp_ds('Sales Order', [['po_no', '=', refno], ['docstatus', 'in', [0, 1]]],
                ['name', 'docstatus'], 5)
    return ds[0] if ds else None


_sp_cache = {}
_item_cache = {}


def sales_person(ten):
    """Cache: một lượt quét có nhiều đơn cùng người bán, hỏi lại ERP mỗi đơn là phí."""
    if not ten:
        return None
    if ten not in _sp_cache:
        _sp_cache[ten] = ten if erp_ds('Sales Person', [['name', '=', ten]],
                                       ['name'], 1) else None
    return _sp_cache[ten]


def co_item(ma):
    if ma not in _item_cache:
        _item_cache[ma] = bool(erp_ds('Item', [['item_code', '=', ma]], ['name'], 1))
    return _item_cache[ma]


_ton_cache = {}


def ton_kho(ma):
    """(còn bán được, tồn vật lý, đã hứa) tại kho bán hàng. None nếu chưa có bản ghi Bin.

    ⚠️ Phải đọc `projected_qty`, KHÔNG phải `actual_qty`. `actual_qty` là hàng đang nằm
    trong kho, nó **không trừ những đơn đã Submit mà chưa giao** — hai người cùng bán một
    lô thì cả hai đều thấy đủ. Đo 18/09/2026 trên nhà mình: `SORA10-8` tồn 66 nhưng đã
    hứa 19, còn bán được 47. `reserved_qty` đang chạy thật, không phải lý thuyết.

    Thiếu hàng KHÔNG chặn tạo đơn: `Sales Order` không trừ kho (Delivery Note mới trừ),
    và sale đã hứa với khách từ lúc lên đơn bên MISA rồi. Nhưng phải NÓI RA để người đi
    giục sản xuất hoặc chuyển kho — im lặng là để kho phát hiện lúc đi lấy hàng.
    """
    if ma not in _ton_cache:
        ds = erp_ds('Bin', [['item_code', '=', ma], ['warehouse', '=', KHO]],
                    ['actual_qty', 'reserved_qty', 'projected_qty'], 1)
        if ds:
            b = ds[0]
            _ton_cache[ma] = (float(b.get('projected_qty') or 0),
                              float(b.get('actual_qty') or 0),
                              float(b.get('reserved_qty') or 0))
        else:
            _ton_cache[ma] = None
    return _ton_cache[ma]


def ngay_giao(d, ngay_don):
    """Luật Công đặt 18/09/2026: **ngày giao = ngày đơn + 2**.

    Đơn có ghi chú thời gian giao riêng thì theo ghi chú — nhưng ghi chú là câu chữ
    tiếng Việt ("giao đầu tuần sau", "giao gấp trong ngày"), máy đoán ngày từ đó là
    đoán bừa. Nên máy LUÔN đặt N+2 và **nói ra** khi thấy MISA có ngày giao khác, để
    người soát tự sửa nếu cần.

    ⚠️ Đừng lấy `ship_date` làm ngày giao: đo 18/09/2026, MISA tự đặt nó lệch 1 ngày so
    ngày đơn cho cả 7 đơn liền — tưởng "sale đã điền" là sai.

    ⚠️ Cửa `paging_filter_v2` KHÔNG trả ô "Ghi chú" của đơn (56 cột, không có cột nào là
    ghi chú). Nên máy không đọc được ghi chú thời gian giao — đơn nào khách đã hẹn riêng
    thì người sửa `delivery_date` trên ERP sau khi quét. Đừng để máy đoán.
    """
    try:
        n2 = (dt.datetime.strptime(ngay_don, '%Y-%m-%d')
              + dt.timedelta(days=2)).strftime('%Y-%m-%d')
    except Exception:
        return ngay_don, 'không đọc được ngày đơn'
    return n2, 'N+2'


def dung_don(d, dong, khach, ghi_chu_dong=None):
    ngay = (d.get('refdate') or '')[:10]
    giao, vi_sao_giao = ngay_giao(d, ngay)
    # ERPNext áp MỘT mẫu thuế cho cả đơn. Đơn trộn nhiều mức thuế mà lấy mức của dòng
    # đầu là tính sai tiền thuế mà không ai thấy — thà tắc, để người quyết cách tách.
    cac_muc = {round(float(x.get('vat_rate') or 0), 2) for x in dong}
    if len(cac_muc) > 1:
        raise ValueError('đơn có NHIỀU mức thuế (%s) — ERP áp một mẫu cho cả đơn, '
                         'người phải tự tách' % ', '.join('%g%%' % m for m in sorted(cac_muc)))
    vat_pt = cac_muc.pop() if cac_muc else 0
    ten_mau, dt_ = dong_thue(vat_pt)
    if vat_pt and not ten_mau:
        raise ValueError('chưa khai mẫu thuế VAT %g%% trên ERP (đang có: %s)'
                         % (vat_pt, ', '.join('%d%%' % k for k in sorted(MAU_THUE))))
    than = {
        'doctype': 'Sales Order', 'company': CONG_TY, 'customer': khach,
        'currency': d.get('currency_id') or 'VND',
        'po_no': d.get('refno'), 'po_date': ngay, 'transaction_date': ngay,
        'delivery_date': giao, 'order_type': 'Sales',
        'selling_price_list': BANG_GIA_LUI, 'set_warehouse': KHO,
        'items': [{'item_code': x.get('inventory_item_code'),
                   'qty': x.get('quantity') or 0,
                   'rate': x.get('unit_price') or 0,
                   'warehouse': KHO, 'delivery_date': giao,
                   'description': x.get('description') or None}
                  for x in dong],
    }
    if ten_mau and dt_:
        than['taxes_and_charges'] = ten_mau
        than['taxes'] = dt_
    # HAI nguồn ghi chú trên MISA, cả hai vào CỘT MÔ TẢ của dòng hàng — Công chốt
    # 22/09/2026: "đơn MISA trình bày sao thì đẩy qua y chang", "ai mà rảnh vào tab
    # điều khoản". Tab Điều khoản là tab KHÁC trên màn ERP, kho mở tab Chi tiết không
    # thấy gì (đo 18/09 và lại 22/09 với đơn 00114).
    #   (1) ghi chú của TỪNG dòng hàng — chỉ dẫn GIA CÔNG: "Hạ size 169cm x 192cm x
    #       20cm", "Lựa phôi cứng". Nay gắn đúng dòng của nó (xem gom_dong), y như MISA.
    #   (2) ô Diễn giải CẢ ĐƠN (journal_memo) — chỉ dẫn GIAO HÀNG: "ƯU TIÊN GIAO GẤP
    #       (22/09)", "Sắp xe công ty giao | TTIN NHẬN HÀNG: …". Thuộc cả đơn nên đặt ở
    #       DÒNG ĐẦU, không lặp xuống mọi dòng cho rối.
    # ⚠️ Ô Mô tả chỉ chứa GHI CHÚ, KHÔNG kèm tên hàng. Vì lưới Sales Order Item cắt ô
    # theo chiều cao, chỉ hiện ~dòng đầu: để tên hàng ở dòng đầu là ghi chú bị đẩy xuống
    # và Công KHÔNG THẤY GÌ — đo 22/09/2026 trên đơn 00154 (dữ liệu có đủ trong DB mà
    # lưới chỉ hiện "Nệm Foam Việt Nhật Sora"). Tên hàng đã có sẵn ở cột "Tên mặt hàng"
    # ngay cạnh, nên nhắc lại trong Mô tả là vừa thừa vừa che mất ghi chú.
    # Dòng KHÔNG có ghi chú thì để None cho Frappe tự điền như cũ.
    for n, (it, x) in enumerate(zip(than['items'], dong)):
        # Luật Tú 19/10/2026: BH có ghi chú thì ERP phải có, nhưng viết NGẮN (dong_bh.rut_gon);
        # dòng hàng nào cũng giữ riêng ghi chú của nó, KHÔNG cộng gộp mã.
        phan = [dong_bh.rut_gon(g) for g in (x.get('_ghi_chu') or []) if g and g.strip()]
        if n == 0:
            phan += [dong_bh.rut_gon(g) for g in (ghi_chu_dong or []) if g and g.strip()]
            memo = dong_bh.rut_gon((d.get('journal_memo') or '').strip())
            # Diễn giải mặc định của BH ("Bán hàng <khách>") chỉ lặp tên khách, bỏ cho gọn
            if memo and not re.match(r'^b[aá]n h[aà]ng\b', memo, re.I):
                phan.append(memo if re.match(r'^(ưu tiên )?giao\b', memo, re.I) else 'Giao: ' + memo)
        it['description'] = '\n'.join(p for p in phan if p) or None
    ck = float(d.get('total_discount_amount') or 0)
    if ck > 0:
        than['apply_discount_on'] = 'Net Total'
        than['discount_amount'] = ck
    nb = sales_person(d.get('employee_name'))
    if nb:
        than['sales_team'] = [{'sales_person': nb, 'allocated_percentage': 100}]
    return than, vat_pt, nb, giao, vi_sao_giao


def tien(x):
    return '{:,.0f}'.format(float(x or 0)).replace(',', '.')


def xu_ly_mot_don(H, d, refno, tao, bo, tac):
    cu = da_co_tren_erp(refno)
    if cu:
        bo.append((refno, cu['name'], 'Nháp' if cu['docstatus'] == 0 else 'đã Submit'))
        return
    khach, cach = tim_customer(d.get('account_object_code'),
                               d.get('account_object_name'))
    if not khach:
        tac.append((refno, 'khách chưa có trên ERP: %s (%s)'
                    % (d.get('account_object_name'), cach)))
        return
    dong, ghi_chu_dong = quet_dong(H, d.get('refid'))
    if not dong:
        tac.append((refno, 'MISA không trả dòng hàng nào'))
        return
    thieu = [x.get('inventory_item_code') for x in dong
             if not co_item(x.get('inventory_item_code'))]
    if thieu:
        tac.append((refno, 'mã chưa có trên ERP: ' + ', '.join(str(m) for m in thieu)))
        return

    # Đối chiếu tổng dòng với tiền hàng MISA TRƯỚC khi dựng đơn. MISA phân trang dòng
    # hàng; trả thiếu một dòng thì đơn vẫn "nhìn hợp lý" và lên ERP thiếu hàng mà không
    # ai thấy — đúng kiểu sai im lặng đắt nhất.
    tong_dong = sum(float(x.get('amount_oc') or 0) for x in dong)
    tien_hang = float(d.get('total_sale_amount') or 0)
    if tien_hang and abs(tong_dong - tien_hang) > 1:
        tac.append((refno, 'CỘNG DÒNG KHÔNG KHỚP: %d dòng cộng %s · MISA ghi tiền hàng %s '
                    '→ nghi thiếu dòng, KHÔNG tạo'
                    % (len(dong), tien(tong_dong), tien(tien_hang))))
        return
    than, vat_pt, nb, giao, vi_sao = dung_don(d, dong, khach, ghi_chu_dong)
    tao.append((refno, d, dong, than, vat_pt, nb, khach, giao, vi_sao))


def main():
    global ERP_URL, ERP_AUTH
    ERP_URL, ERP_AUTH = khoa_erp()
    print('Quét đơn MISA %s → %s   ·   ERP: %s' % (TU, DEN, ERP_URL))
    print('Chế độ: %s' % ('⚠️  GHI THẬT' if GHI_THAT else 'XEM THỬ (không ghi gì)'))

    H = headers_misa()
    don = quet_don(H, TU, DEN)
    print('\nMISA có %d đơn trong khoảng này.' % len(don))
    if CHI_MOT:
        don = [x for x in don if (x.get('refno') or '').strip() == CHI_MOT.strip()]
        print('Lọc còn ĐÚNG đơn %s → %d đơn.' % (CHI_MOT, len(don)))
        if not don:
            print('⛔ Không thấy đơn %s trong khoảng ngày này.' % CHI_MOT)
            return
    # ⛔ LUẬT anh Tùng (21/09/2026, nhóm Telegram): chỉ lên ERP đơn MISA CHƯA xử lý.
    # Đơn đã xử lý trên AMIS là hàng đã xuất đi rồi; tồn ERP đã đối soát về thực tế
    # của ngày, nên chép lại chỉ tạo đơn treo giữ tồn ảo và không đủ hàng để xuất.
    # status: 0 = Chưa thực hiện · 1 = Đã thực hiện · 3 = Huỷ bỏ (đo 21/09/2026).
    if not LAY_HET:
        truoc = len(don)
        don = [x for x in don if x.get('status') == 0]
        if truoc != len(don):
            print('Bỏ %d đơn MISA đã xử lý / huỷ — chỉ lên đơn "Chưa thực hiện" (luật '
                  'anh Tùng 21/09/2026). Muốn lấy hết thì thêm --lay-het.'
                  % (truoc - len(don)))
            print('Còn %d đơn cần lên ERP.' % len(don))

    print('')
    if not don:
        return

    tao, bo, tac = [], [], []
    for d in don:
        refno = d.get('refno')
        try:
            xu_ly_mot_don(H, d, refno, tao, bo, tac)
        except Exception as e:
            # Một đơn hỏng không được giết cả lượt quét — ghi lại rồi đi tiếp
            tac.append((refno, 'lỗi khi xử: %s' % str(e)[:160]))


    if bo:
        print('── ĐÃ CÓ TRÊN ERP, bỏ qua (%d) ──' % len(bo))
        for r, n, tt in bo:
            print('   %-10s → %s (%s)' % (r, n, tt))
    if tac:
        print('\n── TẮC, cần người xử (%d) ──' % len(tac))
        for r, ly in tac:
            print('   %-10s %s' % (r, ly))

    print('\n── SẼ TẠO (%d đơn) ──' % len(tao))
    for refno, d, dong, than, vat_pt, nb, khach, giao, vi_sao in tao:
        print('\n%s  %s  ·  %s' % (refno, (d.get('refdate') or '')[:10], khach))
        print('   người bán: %s%s  ·  VAT %s%%  ·  kho %s'
              % (d.get('employee_name') or '—',
                 '' if nb else ' ⚠️ KHÔNG có Sales Person → đơn sẽ không gán doanh số',
                 vat_pt, KHO))
        print('   ngày giao: %s  (%s)' % (giao, vi_sao))
        # In lại đúng những gì sẽ vào ô Mô tả, dòng nào ra dòng nào.
        for it in than['items']:
            phu = (it.get('description') or '').split('\n')
            for g in phu:
                print('   %-16s ô Mô tả thêm: %s' % (it['item_code'], g.lstrip('· ')))
        for x in dong:
            ma = x.get('inventory_item_code')
            can = float(x.get('quantity') or 0)
            t = ton_kho(ma)
            if t is None:
                dau = '  ⛔ kho chưa có mã này'
            else:
                con, thuc, hua = t
                if con < can:
                    dau = '  ⛔ CÒN %g, THIẾU %g' % (con, can - con)
                    if hua:
                        dau += ' (tồn %g, đã hứa %g)' % (thuc, hua)
                elif hua:
                    dau = '  (còn %g · tồn %g, đã hứa %g)' % (con, thuc, hua)
                else:
                    dau = '  (còn %g)' % con
            print('     %-14s %6s × %14s = %14s%s'
                  % (ma, x.get('quantity'), tien(x.get('unit_price')),
                     tien(x.get('amount_oc')), dau))
        if than.get('discount_amount'):
            print('     chiết khấu: %s' % tien(than['discount_amount']))
        print('     MISA: tiền hàng %s · VAT %s · TỔNG %s'
              % (tien(d.get('total_sale_amount')), tien(d.get('total_vat_amount')),
                 tien(d.get('total_amount'))))

    if not GHI_THAT:
        print('\n→ Chưa ghi gì. Soát bảng trên, đúng thì chạy lại kèm --that')
        return

    print('\n── GHI LÊN ERP ──')
    for refno, d, dong, than, vat_pt, nb, khach, giao, vi_sao in tao:
        try:
            r = erp('/api/resource/' + 'Sales%20Order', 'POST', than)
            ma = r['data']['name']
            tong_erp = float(r['data'].get('grand_total') or 0)
            tong_misa = float(d.get('total_amount') or 0)
            lech = abs(tong_erp - tong_misa)
            print('   ✅ %-10s → %s  · tổng ERP %s %s'
                  % (refno, ma, tien(tong_erp),
                     '(khớp MISA)' if lech <= 1 else
                     '⚠️ LỆCH %s so MISA %s' % (tien(lech), tien(tong_misa))))

            # Công dặn 18/09/2026: phải ĐÚNG KHO rồi mới Submit. Đọc lại đơn thật chứ
            # đừng tin payload vừa gửi — Submit xong là hết xoá, chỉ còn đường huỷ chứng từ.
            import urllib.parse as up
            ct = erp('/api/resource/Sales%20Order/' + up.quote(ma)).get('data', {})
            kho_don = ct.get('set_warehouse')
            dong_sai = [x.get('item_code') for x in ct.get('items', [])
                        if x.get('warehouse') != KHO]
            if kho_don != KHO or dong_sai:
                print('      ⛔ KHÔNG Submit — kho chưa đúng: header=%s%s'
                      % (kho_don, (' · dòng sai: ' + ', '.join(map(str, dong_sai)))
                         if dong_sai else ''))
                continue
            # Submit qua `frappe.client.submit` — cửa chính thức, chạy đủ validation và
            # hook on_submit (chỗ ERPNext sinh dữ liệu cho kho). Đo 18/09/2026:
            #   · PUT resource {docstatus:1} → endpoint có, nhưng chỉ ghi field
            #   · frappe.client.set_value docstatus → 417 "Không sửa được trường tiêu chuẩn"
            erp('/api/method/frappe.client.submit', 'POST', {'doc': json.dumps(ct)})
            lai = erp('/api/resource/Sales%20Order/' + up.quote(ma)).get('data', {})
            if lai.get('docstatus') == 1:
                print('      ✅ đã Submit · giao %s (%s) · kho %s'
                      % (lai.get('delivery_date'), vi_sao, kho_don))
            else:
                print('      ⚠️ gọi Submit xong nhưng đơn vẫn docstatus=%s — vào ERP kiểm tay'
                      % lai.get('docstatus'))
        except Exception as e:
            print('   ⛔ %-10s %s' % (refno, str(e)[:250]))


if __name__ == '__main__':
    main()
