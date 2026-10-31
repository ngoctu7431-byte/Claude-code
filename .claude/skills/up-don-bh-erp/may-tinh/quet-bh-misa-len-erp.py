#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Quét CHỨNG TỪ BÁN HÀNG (BH) trên MISA rồi dựng Sales Order trên ERP nhà thật.

Vì sao có file này (29/09/2026)
    Routine của Tú đọc BH bằng Claude in Chrome: bấm từng dòng rồi đọc chữ trên màn.
    Ngày 28/09 gãy 4 kiểu: đọc nhầm chi tiết BH trước (bảng hiện chậm), hai lượt chạy
    chồng, Chrome tắt giữa chừng, tự up cả BH tồn ngày cũ → 20 đơn phải huỷ.
    Chính trang BH lấy dữ liệu qua 2 cửa JSON (bắt được 29/09/2026):
        POST /g1/api/sa/v1/sa_voucher_get/paging_filter_v2   → danh sách BH, lọc property 3654
        POST /g1/api/sa/v1/sa_voucher_get/get_paging_detail  → dòng hàng theo refid (3993)
    Chi tiết lấy THEO MÃ BH nên không thể lẫn sang BH khác. Không bấm, không đọc màn hình.

Nhà: `apps-ntv/Nghiệp Vụ ERP/cong-cu/misa-len-erp/` (nghiệp vụ lên đơn, dời từ
kinh-doanh-dai-ly/07-du-lieu-misa 29/09/2026). Cài sang máy khác (máy Tú): `goi-quet-bh/`.

Dùng lại TOÀN BỘ phần ERP của `quet-don-misa-len-erp.py` (tìm khách, thuế, kho, submit,
kiểm kho trước khi submit) — đừng viết đường tạo đơn thứ hai.

LUẬT (lấy từ routine của Tú + bài học 28/09/2026)
    · "BH ngày X" = Ngày hạch toán (posted_date) = X. Ngày đơn ERP = ngày hạch toán.
    · Chống trùng bằng số BH ở ô po_no (kể cả đơn Nháp).
    · Cùng khách + cùng tổng tiền với một đơn ERP khác trong 7 ngày → TẮC, hỏi người.
      (28/09: kế toán lập lại BH04880 ngày 26 thành BH04901 ngày 28.)
    · Cộng dòng hàng phải khớp tiền hàng BH; cộng VAT dòng phải khớp VAT BH; dòng nào
      để trống thuế → TẮC. Không tự điền thuế.
    · Chế độ --tu-dong: chỉ TẠO BH hôm nay + hôm qua. BH 2–7 ngày trước mà chưa có
      trên ERP thì chỉ BÁO (tồn cũ), không tự up.
    · Khoá chạy một lượt: lượt trước chưa xong thì lượt này thoát ngay.
    · BH đã có trên ERP: so lại tổng tiền, kế toán sửa BH thì BÁO, không tự sửa.
    · Ngày giao = ngày đơn + 7.

MẶC ĐỊNH CHỈ XEM THỬ. Muốn ghi thật phải thêm --that.

Dùng:
    python quet-bh-misa-len-erp.py --tu-dong                 # xem thử: hôm qua + hôm nay
    python quet-bh-misa-len-erp.py --tu-dong --that          # ghi thật (routine gọi dòng này)
    python quet-bh-misa-len-erp.py --tu 2026-09-28 --den 2026-09-28
    python quet-bh-misa-len-erp.py --tu 2026-09-28 --chi BH04920 --that   # đúng một BH
    ... --bo-qua ~/misa-bh-sync-bo-qua.md       # sổ BH không đụng (mọi chữ BHxxxxx trong file)
    python quet-bh-misa-len-erp.py --tu 2026-09-28 --chi BH04901 --cho-trung --that
                                                # người đã xác nhận "nghi trùng" là đơn thật
    python quet-bh-misa-len-erp.py --dang-nhap  # mở Chrome riêng để đăng nhập MISA (1 lần)

CHẠY ĐƯỢC CẢ MAC LẪN WINDOWS (máy Tú là Windows — 29/09/2026). Khoá, hồ sơ Chrome nằm ở
<thư mục người dùng>/.ntv-secrets/, không nằm trong thư mục script.
"""
import datetime as dt
import importlib.util
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse as up
from pathlib import Path

# Windows: màn hình mặc định không in được tiếng Việt/emoji → UnicodeEncodeError giữa lượt.
for _luong in (sys.stdout, sys.stderr):
    try:
        _luong.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location(
    'qd', os.path.join(HERE, 'quet-don-misa-len-erp.py'))
qd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(qd)

MISA = qd.MISA
CUA_DS = MISA + '/g1/api/sa/v1/sa_voucher_get/paging_filter_v2'
CUA_CT = MISA + '/g1/api/sa/v1/sa_voucher_get/get_paging_detail'
KHOA_CHAY = Path.home() / '.ntv-secrets' / 'quet-bh.lock'
NGAY_GIAO_CONG = 7


def tham_so(ten, mac_dinh=None):
    return sys.argv[sys.argv.index(ten) + 1] if ten in sys.argv else mac_dinh


HOM_NAY = dt.date.today()
TU_DONG = '--tu-dong' in sys.argv
GHI_THAT = '--that' in sys.argv
CHI_MOT = tham_so('--chi')
# Tự bù ngày lỡ (Tú làm 29/09/2026: "lỡ quên đăng nhập hay off 1–2 ngày thì sao, xử lý triệt để").
# File mốc ghi lúc của lượt GHI THẬT gần nhất đã quét trọn MISA. Máy nghỉ / MISA đăng xuất bao lâu
# thì BH những ngày đó CHƯA TỪNG được lượt nào xét → tự up như BH mới. TỒN CŨ chỉ còn nghĩa: đã có
# lượt thấy mà vẫn chưa lên ERP.
# TRẦN_BU (em thêm khi gộp): bù tối đa 7 ngày. Máy nghỉ lâu hơn thì phần xa hơn vẫn là TỒN CŨ, người
# duyệt — 28/09 dồn 3 ngày đã up nhầm, dồn cả tháng không ai soát kịp.
MOC_FILE = Path(HERE) / 'log' / 'lan-quet-thanh-cong.txt'
SAN_MOC = '2026-10-01'          # routine của Tú chỉ up BH từ ngày này (Tú chốt 01/10/2026; trước là 2026-09-24)
TRAN_BU = 7


def doc_moc():
    try:
        m = MOC_FILE.read_text(encoding='utf-8').strip()[:10]
        dt.date.fromisoformat(m)
        return m
    except Exception:
        return None


if TU_DONG:
    _hom_qua = (HOM_NAY - dt.timedelta(days=1)).isoformat()
    _moc = doc_moc()
    MOC_TAO = max(min(_hom_qua, _moc) if _moc else _hom_qua, SAN_MOC,
                  (HOM_NAY - dt.timedelta(days=TRAN_BU)).isoformat())      # TẠO từ ngày này
    TU = min((HOM_NAY - dt.timedelta(days=7)).isoformat(), MOC_TAO)       # quét rộng để thấy tồn cũ
    DEN = HOM_NAY.isoformat()
    BU_NGAY = MOC_TAO < _hom_qua
    # --chi BHxxxxx --tu <ngày HT>: up đúng một BH cũ hơn hôm qua (người đã duyệt, hoặc routine thử lại BH
    # thiếu mã/khách sau khi ERP đã bổ sung). Trước 03/10/2026 --tu bị bỏ qua ở chế độ --tu-dong. Vẫn giữ sàn.
    if CHI_MOT and '--tu' in sys.argv:
        MOC_TAO = max(SAN_MOC, min(MOC_TAO, tham_so('--tu')))
        TU = min(TU, MOC_TAO)
        BU_NGAY = False
else:
    TU = tham_so('--tu', HOM_NAY.isoformat())
    DEN = tham_so('--den', TU)
    MOC_TAO = TU
    BU_NGAY = False
FILE_BO_QUA = tham_so('--bo-qua')
# Người đã xác nhận BH "nghi trùng" là đơn thật → cho qua. Chỉ nhận khi đi kèm --chi,
# để không ai lỡ tay tắt luật chống trùng cho cả lượt.
CHO_TRUNG = '--cho-trung' in sys.argv
# BH từng có đơn nhưng đơn đã bị HUỶ → mặc định TẮC, không tự tạo lại (24/09: 11 đơn bị huỷ, sổ theo
# dõi không biết; da_co_tren_erp chỉ tính docstatus 0/1 nên máy sẽ up lại). Người xác nhận thì
# --chi BHxxxxx --tao-lai.
TAO_LAI = '--tao-lai' in sys.argv
if TAO_LAI and not CHI_MOT:
    sys.exit('⛔ --tao-lai chỉ dùng kèm --chi BHxxxxx (một BH đã có người xác nhận).')
if CHO_TRUNG and not CHI_MOT:
    sys.exit('⛔ --cho-trung chỉ dùng kèm --chi BHxxxxx (một BH đã có người xác nhận).')


# ── khoá ───────────────────────────────────────────────────────────────────────
khoa_file = qd.khoa_file
giu_ho_so = qd.giu_ho_so_misa


def giu_khoa_chay():
    """Một lượt một lúc. Script không bao giờ ngồi chờ người trả lời, nên không còn kiểu
    'đang chờ anh thì không tính là đang chạy' như routine cũ."""
    f = khoa_file(KHOA_CHAY)
    if not f:
        print('⏭  Lượt trước còn đang chạy — bỏ lượt này (không tạo gì).')
        sys.exit(0)
    return f


def dang_nhap():
    """Mở Chrome RIÊNG (hồ sơ ~/.ntv-secrets/chrome-misa, tách khỏi Chrome hằng ngày) để
    người đăng nhập MISA một lần. Đóng cửa sổ là xong."""
    from playwright.sync_api import sync_playwright
    giu_ho_so()
    print('Mở Chrome để đăng nhập MISA. Vào được trang chủ MISA thì ĐÓNG CỬA SỔ đó.')
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            str(qd.HO_SO), channel='chrome', headless=False,
            viewport={'width': 1400, 'height': 900},
            args=['--disable-blink-features=AutomationControlled'])
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(MISA + '/app', timeout=90000)
        het = time.time() + 900
        while time.time() < het:
            try:
                if not ctx.pages:
                    break
                ctx.pages[0].wait_for_timeout(2000)
            except Exception:
                break
        try:
            ctx.close()
        except Exception:
            pass
    print('Đã lưu phiên đăng nhập vào', qd.HO_SO)


# ── MISA ───────────────────────────────────────────────────────────────────────
def headers_misa():
    """Mở trang Bán hàng, mượn headers mà chính giao diện vừa dùng."""
    from playwright.sync_api import sync_playwright
    bat = []
    with sync_playwright() as p:
        qd.giu_ho_so_misa()
        ctx = p.chromium.launch_persistent_context(
            str(qd.HO_SO), channel='chrome', headless=True,
            viewport={'width': 1600, 'height': 1000},
            args=['--disable-blink-features=AutomationControlled'])
        ctx.on('request', lambda r: bat.append(dict(r.headers))
               if 'sa_voucher_get/paging_filter_v2' in r.url else None)
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        for vong in range(3):
            pg.goto(MISA + '/app/SA/SAVoucher', wait_until='domcontentloaded',
                    timeout=90000)
            het_phien = False
            for _ in range(15):
                pg.wait_for_timeout(2000)
                if bat:
                    break
                # MISA chuyển sang amisapp.misa.vn/login SAU vài giây, không phải ngay lúc
                # goto — kiểm một lần đầu vòng là trượt (đo 29/09/2026 trên máy trắng).
                if '/login' in pg.url.lower():
                    het_phien = True
                    break
                # Cùng tài khoản MISA đang mở ở chỗ khác (người mở MISA trên Chrome thường) →
                # MISA hỏi "Tiếp tục đăng nhập?". Máy KHÔNG tự bấm: bấm là đá người kia ra
                # giữa lúc đang làm (đo 29/09/2026: tưởng "giao diện đã đổi" suốt 3 lượt).
                try:
                    if 'người dùng khác sử dụng tài khoản' in pg.inner_text('body'):
                        ctx.close()
                        sys.exit('⛔ TÀI KHOẢN MISA ĐANG MỞ Ở CHỖ KHÁC — MISA hỏi "Tiếp tục đăng '
                                 'nhập?". Đóng MISA trên Chrome kia (hoặc dùng tài khoản khác cho '
                                 'máy quét) rồi lượt sau chạy lại. Máy không tự bấm để khỏi đá người ra.')
                except SystemExit:
                    raise
                except Exception:
                    pass
            if het_phien:
                ctx.close()
                sys.exit('⛔ PHIÊN MISA ĐÃ HẾT — chạy quet-bh-misa-len-erp.py --dang-nhap '
                         'rồi đăng nhập lại.')
            if bat:
                break
            print('   (lượt %d chưa thấy danh sách BH nạp, tải lại…)' % (vong + 1))
        try:
            ctx.close()
        except Exception:
            pass
    if not bat:
        sys.exit('⛔ Không bắt được cửa danh sách BH sau 3 lần — MISA chậm hoặc '
                 'giao diện đã đổi.')
    return bat[-1]


def quet_bh(H, tu, den):
    body = {
        "sort": '[{"property":3654,"desc":true,"data_type":3,"operand":1}]',
        "filter": [
            {"property": 3654, "value": qd.utc(tu), "operator": 10,
             "operand": 1, "data_type": 3},
            {"property": 3654, "value": qd.utc(den, True), "operator": 12,
             "operand": 1, "data_type": 3},
        ],
        "pageIndex": 1, "pageSize": 500, "useSp": False, "view": 1,
        "summaryColumns": [5126, 5068, 5141, 5039], "loadMode": 2,
    }
    ra = qd.mang_dong(qd.misa(H, CUA_DS, body))
    if len(ra) >= 500:
        sys.exit('⛔ Chạm trần 500 BH một trang — thu hẹp --tu/--den.')
    # Chuẩn hoá về đúng tên trường phần ERP của quet-don đang đọc.
    for d in ra:
        d['refno'] = (d.get('refno_finance') or '').strip()
        d['refdate'] = (d.get('posted_date') or d.get('refdate') or '')[:10]
    return ra


def quet_dong_bh(H, refid):
    body = {
        "columns": [2157, 1355, 5274, 3870, 2326, 1195, 1065, 5281, 5279, 308, 5364,
                    5350, 5347, 1464, 1455, 1671, 3334, 1452, 3404, 5476, 2358],
        "sort": '[{"property":4555,"desc":false,"data_type":4,"operand":1}]',
        "filter": [{"property": 3993, "operator": 7, "operand": 1,
                    "value": refid, "data_type": 10}],
        "pageIndex": 1, "pageSize": 300, "useSp": False, "view": 96,
        "summaryColumns": [3870, 1032, 308, 3488, 5350, 1455], "loadMode": 2,
    }
    tho = qd.mang_dong(qd.misa(H, CUA_CT, body))
    if len(tho) >= 300:
        raise ValueError('chạm trần 300 dòng — nghi thiếu dòng')
    return doi_ma(qd.gom_dong(tho))


# Mã MISA ≠ mã ERP mà Tú đã chốt là cùng một hàng (vd 05/10/2026: TPET169 → TPET169*8). Chỉ thêm vào file
# này khi Tú chốt, không tự đoán. Áp cho cả máy quét lẫn máy sửa đơn lệch (cùng gọi quet_dong_bh).
FILE_DOI_MA = Path(HERE) / 'doi-ma-misa-erp.json'


def doi_ma(kq):
    """kq = (dòng hàng, ghi chú lạc) như gom_dong trả về; chỉ đổi mã ở dòng hàng."""
    try:
        bang = json.loads(FILE_DOI_MA.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return kq
    for x in (kq[0] if isinstance(kq, tuple) else kq):
        ma = x.get('inventory_item_code')
        if ma in bang:
            x['inventory_item_code'] = bang[ma]
    return kq


def ngay_gap(memo, ngay_don):
    """Luật của Tú: Diễn giải ghi GẤP kèm ngày cụ thể (dd/mm) thì giao đúng ngày đó.
    Chỉ chữ "gấp" trần thì KHÔNG tính — "Gấp gọn đóng bao kiện" là gấp nệm, không phải
    giao gấp (bắt nhầm lượt thử 29/09/2026)."""
    if not re.search(r'(?i)g[aấ]p', memo or ''):
        return None
    m = re.search(r'(?<!\d)(\d{1,2})/(\d{1,2})(?:/(\d{4}))?(?!\d)', memo)
    if not m:
        return None
    nam = int(m.group(3) or ngay_don[:4])
    try:
        return dt.date(nam, int(m.group(2)), int(m.group(1))).isoformat()
    except ValueError:
        return None


def ngay_giao_bh(d, ngay_don):
    g = ngay_gap(d.get('journal_memo'), ngay_don)
    if g and g >= ngay_don:
        return g, 'GẤP ghi ở Diễn giải'
    try:
        return ((dt.datetime.strptime(ngay_don, '%Y-%m-%d')
                 + dt.timedelta(days=NGAY_GIAO_CONG)).strftime('%Y-%m-%d'),
                'N+%d' % NGAY_GIAO_CONG)
    except Exception:
        return ngay_don, 'không đọc được ngày đơn'


# Cắm phần BH vào đúng chỗ phần ERP của quet-don gọi tới
qd.quet_dong = quet_dong_bh
qd.ngay_giao = ngay_giao_bh


# ── luật thêm cho BH ───────────────────────────────────────────────────────────
def doc_bo_qua():
    if not FILE_BO_QUA:
        return set()
    p = Path(os.path.expanduser(FILE_BO_QUA))
    if not p.exists():
        sys.exit('⛔ Không thấy sổ bỏ qua %s' % p)
    return set(re.findall(r'BH\d{4,}', p.read_text(encoding='utf-8')))


def kich_thuoc_cat(chu):
    """Kích thước hạ size/cắt trong ghi chú dòng ("Hạ size 169cm x 192cm x 20cm") → ((169, 192), …).
    Tấm nguyên (không ghi chú cắt) → (). Tú sửa 07/10/2026: BH04986 tấm nguyên NA10-6 và BH05092 tấm cắt
    hạ size cùng mã, cùng tiền — KHÔNG phải trùng."""
    chu = (chu or '').lower()
    if not re.search(r'h[aạ]\s*size|c[aắ]t|size', chu):
        return ()
    return tuple(sorted(set((int(a), int(b)) for a, b in
                            re.findall(r'(\d{2,3})\s*(?:cm)?\s*[x×*]\s*(\d{2,3})', chu))))


def bo_hang(bo):
    """{(mã, kích thước cắt): tổng SL} để so hai đơn có cùng hàng không. bo = [(mã, SL, ghi chú)]."""
    gom = {}
    for ma, sl, chu in bo:
        if ma:
            k = (ma, kich_thuoc_cat(chu))
            gom[k] = round(gom.get(k, 0) + float(sl or 0), 3)
    return gom


def nghi_trung(khach, tong, refno, ngay, dong_bh=None):
    """Đơn ERP khác (khác po_no) cùng khách, cùng tổng tiền trong ±7 ngày, VÀ cùng mã hàng + số lượng
    + cùng kích thước hạ size (tấm nguyên ≠ tấm cắt).
    Tú sửa 07/10/2026 ("sản phẩm của 2 đơn có giống nhau đâu"): BH05092 bị chặn oan vì chỉ trùng khách + tiền,
    hàng khác hẳn. Khác hàng thì KHÔNG phải trùng, cứ up."""
    a = (dt.datetime.strptime(ngay, '%Y-%m-%d') - dt.timedelta(days=7)).strftime('%Y-%m-%d')
    b = (dt.datetime.strptime(ngay, '%Y-%m-%d') + dt.timedelta(days=7)).strftime('%Y-%m-%d')
    ds = qd.erp_ds('Sales Order', [['customer', '=', khach], ['docstatus', 'in', [0, 1]],
                                   ['transaction_date', 'between', [a, b]],
                                   ['grand_total', 'between', [tong - 1, tong + 1]]],
                   ['name', 'po_no', 'transaction_date'], 10)
    ds = [x for x in ds if (x.get('po_no') or '') != refno]
    if not ds or dong_bh is None:
        return ds
    hang_bh = bo_hang((x.get('inventory_item_code'), x.get('quantity'),
                       ' '.join(x.get('_ghi_chu') or [])) for x in dong_bh)
    giong = []
    for x in ds:
        so = qd.erp('/api/resource/Sales%20Order/' + up.quote(x['name'])).get('data', {})
        if bo_hang((i.get('item_code'), i.get('qty'), i.get('description'))
                   for i in so.get('items', [])) == hang_bh:
            giong.append(x)
    return giong


NGUOI_XUAT_PHIEU = 'nvtungjob@gmail.com'   # anh Tùng (kho)
DA_GIAO = []                                # (số BH, lý do): BH bỏ vì đơn trùng đã có phiếu giao của anh Tùng


def phieu_giao_cua_tung(ten_so):
    """Phiếu giao hàng (Delivery Note, chưa huỷ) trỏ tới đơn này mà anh Tùng đã bấm xuất.
    Tú chốt 14/10/2026: đơn nào anh Tùng đã Xuất phiếu giao hàng thì đừng up BH của đơn đó nữa."""
    q = up.urlencode({'parent': 'Delivery Note',
                      'filters': json.dumps([['against_sales_order', '=', ten_so]]),
                      'fields': json.dumps(['parent']), 'limit_page_length': 20})
    ct = qd.erp('/api/resource/Delivery%20Note%20Item?' + q).get('data', [])
    kq = []
    for ma in sorted({x['parent'] for x in ct}):
        p = qd.erp('/api/resource/Delivery%20Note/' + up.quote(ma)).get('data', {})
        if p.get('docstatus') in (0, 1) and p.get('owner') == NGUOI_XUAT_PHIEU:
            kq.append(ma)
    return kq


def kiem_thue(d, dong):
    """Trả lý do tắc, hoặc None nếu thuế ổn."""
    trong = [x.get('inventory_item_code') for x in dong if x.get('vat_rate') is None]
    if trong:
        return 'dòng để TRỐNG thuế: %s — hỏi kế toán, không tự điền' % ', '.join(trong)
    vat_dong = sum(float(x.get('vat_amount_oc') or 0) for x in dong)
    vat_bh = float(d.get('total_vat_amount') or 0)
    if abs(vat_dong - vat_bh) > 2:
        return ('VAT cộng dòng %s ≠ VAT BH %s' % (qd.tien(vat_dong), qd.tien(vat_bh)))
    return None


def don_da_huy(refno):
    return qd.erp_ds('Sales Order', [['po_no', '=', refno], ['docstatus', '=', 2]],
                     ['name', 'modified'], 5)


KHACH_MOI = []   # (số BH, tên khách, ĐÃ TẠO / SẼ TẠO): khách lấy từ MISA tạo sang ERP (Tú chốt 15/10/2026)
_DS_KHACH_ERP = None
_TIEN_TO_TEN = ('doanh nghiep tu nhan', 'cong ty co phan', 'ho kinh doanh', 'cong ty tnhh', 'cong ty', 'dntn', 'hkd')


def _bo_dau(s):
    s = unicodedata.normalize('NFD', (s or '').lower().replace('đ', 'd'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def _loi_ten(s):
    t = _bo_dau(s)
    for p in _TIEN_TO_TEN:
        if t.startswith(p + ' '):
            return t[len(p) + 1:]
    return t


def khach_nghi_trung(d):
    """Khách ERP có thể chính là khách này (khác cách viết/dấu, hoặc trùng số điện thoại trong tên).
    Có ứng viên thì KHÔNG tạo mới (đã từng lỡ tạo trùng "Lã Thị Kiều Oanh", 21/09/2026)."""
    global _DS_KHACH_ERP
    if _DS_KHACH_ERP is None:
        _DS_KHACH_ERP = [(x['name'], x.get('mobile_no') or '') for x in
                         qd.erp_ds('Customer', [], ['name', 'mobile_no'], 20000)]
    ten = (d.get('account_object_name') or '').strip()
    loi = _loi_ten(ten)
    so = set(re.findall(r'\d{9,}', ten)) | {re.sub(r'\D', '', d.get('tel') or '')}
    so.discard('')
    kq = []
    for name, mobile in _DS_KHACH_ERP:
        so_erp = re.sub(r'\D', '', name)
        if (loi and _loi_ten(name) == loi) or any(s in so_erp or s == re.sub(r'\D', '', mobile) for s in so):
            kq.append(name)
    return sorted(set(kq))


def tao_khach_tu_misa(d, refno):
    """Tạo Customer (+ Address, Contact) trên ERP từ thông tin khách trên BH MISA. Trả tên khách."""
    global _DS_KHACH_ERP
    ten = (d.get('account_object_name') or '').strip()
    ma = (d.get('account_object_code') or '').strip()
    tel = (d.get('tel') or '').strip()
    mail = (d.get('email_address') or '').strip()
    dc = (d.get('account_object_address') or '').strip()
    than = {'customer_name': ten, 'customer_type': 'Company', 'customer_group': 'Khách lẻ B2C',
            'territory': 'Vietnam', 'language': 'vi',
            'customer_details': ('mã MISA: %s · ' % ma if ma else '') +
                                'Tạo tự động từ %s (ngày HT %s) theo lệnh Tú 15/10/2026.' % (refno, d.get('refdate'))}
    if re.fullmatch(r'\d{10}(-\d{3})?|\d{12}', ma):
        than['tax_id'] = ma
    if tel:
        than['mobile_no'] = tel
    if mail:
        than['email_id'] = mail
    ten_erp = qd.erp('/api/resource/Customer', 'POST', than)['data']['name']
    if _DS_KHACH_ERP is not None:
        _DS_KHACH_ERP.append((ten_erp, tel))
    try:
        if dc:
            tinh = (d.get('province_or_city') or '').strip()
            if not tinh:
                parts = [p.strip() for p in dc.split(',') if p.strip() and p.strip().lower() not in ('việt nam', 'vietnam')]
                tinh = parts[-1] if parts else 'Vietnam'
            qd.erp('/api/resource/Address', 'POST', {
                'address_title': ten, 'address_type': 'Billing', 'address_line1': dc,
                'address_line2': (d.get('ward_or_commune') or '').strip() or None, 'city': tinh, 'state': tinh,
                'country': 'Vietnam', 'phone': tel or None, 'email_id': mail or None, 'is_primary_address': 1,
                'links': [{'link_doctype': 'Customer', 'link_name': ten_erp}]})
        if tel or mail:
            lh = {'first_name': ten, 'is_primary_contact': 1,
                  'links': [{'link_doctype': 'Customer', 'link_name': ten_erp}]}
            if tel:
                lh['phone_nos'] = [{'phone': tel, 'is_primary_phone': 1, 'is_primary_mobile_no': 1}]
            if mail:
                lh['email_ids'] = [{'email_id': mail, 'is_primary': 1}]
            qd.erp('/api/resource/Contact', 'POST', lh)
    except Exception as e:
        print('   ⚠️ khách %s đã tạo nhưng thiếu địa chỉ/liên hệ: %s' % (ten_erp, str(e)[:120]))
    return ten_erp


def xu_ly_bh(H, d, tao, bo, tac):
    refno = d['refno']
    cu = qd.da_co_tren_erp(refno)
    if cu:
        bo.append((refno, cu['name'], 'Nháp' if cu['docstatus'] == 0 else 'đã Submit'))
        return
    huy = [] if TAO_LAI else don_da_huy(refno)
    if huy:
        tac.append((refno, 'từng có đơn nhưng ĐÃ HUỶ: %s — hỏi người vì sao huỷ; up lại thì '
                    '--chi %s --tao-lai' % (', '.join(x['name'] for x in huy), refno)))
        return
    khach, cach = qd.tim_customer(d.get('account_object_code'), d.get('account_object_name'))
    if not khach and '(0 ứng viên)' in cach:
        # Tú chốt 15/10/2026: BH tắc vì ERP chưa có khách → lấy thông tin khách ở MISA tạo sang ERP rồi up đơn.
        # Chỉ tạo khi KHÔNG có khách nào na ná; có ứng viên thì dừng hỏi người, đừng tạo trùng.
        na_na = khach_nghi_trung(d)
        if na_na:
            tac.append((refno, 'khách chưa có trên ERP nhưng NGHI TRÙNG khách đã có: %s — hỏi người, không tự tạo'
                        % ', '.join(na_na[:3])))
            return
        if not GHI_THAT:
            KHACH_MOI.append((refno, (d.get('account_object_name') or '').strip(), 'SẼ TẠO'))
            return
        try:
            khach = tao_khach_tu_misa(d, refno)
            KHACH_MOI.append((refno, khach, 'ĐÃ TẠO'))
        except Exception as e:
            tac.append((refno, 'khách chưa có trên ERP, tự tạo từ MISA bị lỗi: %s' % str(e)[:150]))
            return
    if not khach:
        tac.append((refno, 'khách chưa có trên ERP: %s (%s)'
                    % (d.get('account_object_name'), cach)))
        return
    trung = [] if CHO_TRUNG else nghi_trung(khach, float(d.get('total_amount') or 0), refno, d['refdate'])
    if trung:   # cùng khách + tiền → mới tốn công đọc dòng hàng để so (07/10/2026)
        trung = nghi_trung(khach, float(d.get('total_amount') or 0), refno, d['refdate'],
                           quet_dong_bh(H, d.get('refid'))[0])
    if trung:   # Tú chốt 14/10/2026: đơn trùng mà anh Tùng đã xuất phiếu giao → bỏ BH này, không hỏi
        try:
            giao = {x['name']: phieu_giao_cua_tung(x['name']) for x in trung}
        except Exception:
            giao = {}   # tra phiếu giao lỗi thì giữ cách cũ: dừng hỏi người
        if giao and all(giao.values()):
            DA_GIAO.append((refno, 'tổng %s · trùng %s, anh Tùng đã xuất phiếu giao %s'
                            % (qd.tien(d.get('total_amount')),
                               ', '.join('%s (%s)' % (x['name'], x.get('po_no') or '—') for x in trung),
                               ', '.join(m for v in giao.values() for m in v))))
            return
    if trung:
        tac.append((refno, 'NGHI TRÙNG: cùng khách, cùng tổng %s, cùng mã hàng + số lượng với %s — hỏi người'
                    % (qd.tien(d.get('total_amount')),
                       ', '.join('%s (%s, %s)' % (x['name'], x.get('po_no') or '—',
                                                  x['transaction_date']) for x in trung))))
        return
    n_tac = len(tac)
    n_tao = len(tao)
    qd.xu_ly_mot_don(H, d, refno, tao, bo, tac)   # cộng dòng khớp tiền hàng nằm ở đây
    if len(tao) > n_tao:
        ly = kiem_thue(d, tao[-1][2])
        if ly:
            tao.pop()
            tac.append((refno, ly))
    return len(tac) == n_tac


def erp_sua_da_giao(refno, ten_so, d_misa):
    """Tú chốt 15/10/2026: đơn đã có phiếu giao mà bị sửa mặt hàng ngay trên ERP (MISA không đổi kể từ lần
    ERP còn khớp, mốc do cap-nhat-lech-bh.py ghi) thì KỆ, không báo lệch tiền. Lỗi tra cứu → coi như không phải."""
    try:
        mo = json.loads((Path(HERE) / 'log' / 'cap-nhat-lech-trang-thai.json').read_text(encoding='utf-8'))
        cu = mo.get(refno)
        if not cu or cu.get('so') != ten_so or cu.get('ver') != str(d_misa.get('edit_version') or ''):
            return False
        q = up.urlencode({'parent': 'Delivery Note',
                          'filters': json.dumps([['against_sales_order', '=', ten_so]]),
                          'fields': json.dumps(['parent']), 'limit_page_length': 50})
        for x in qd.erp('/api/resource/Delivery%20Note%20Item?' + q).get('data', []):
            p = qd.erp('/api/resource/Delivery%20Note/' + up.quote(x['parent'])).get('data', {})
            if p.get('docstatus') in (0, 1):
                return True
    except Exception:
        pass
    return False


def so_lai_tien(ds_misa, bo):
    """BH đã có trên ERP: tổng ERP phải khớp tổng MISA. Lệch = kế toán đã sửa BH."""
    lech = []
    theo_so = {d['refno']: d for d in ds_misa}
    for refno, ten, _ in bo:
        r = qd.erp('/api/resource/Sales%20Order/' + up.quote(ten)).get('data', {})
        a, b = float(r.get('grand_total') or 0), float(theo_so[refno].get('total_amount') or 0)
        if abs(a - b) > 1:
            if erp_sua_da_giao(refno, ten, theo_so[refno]):
                continue
            lech.append((refno, ten, a, b))
    return lech


def main():
    if '--dang-nhap' in sys.argv:
        dang_nhap()
        return
    _khoa = giu_khoa_chay()  # noqa: F841 — giữ tới hết tiến trình
    qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()
    print('Quét BH MISA %s → %s   ·   ERP: %s' % (TU, DEN, qd.ERP_URL))
    print('Chế độ: %s%s' % ('⚠️  GHI THẬT' if GHI_THAT else 'XEM THỬ (không ghi gì)',
                            ' · tự động: chỉ tạo BH từ %s' % MOC_TAO if TU_DONG else ''))
    if BU_NGAY:
        print('BÙ NGÀY LỠ: lượt quét thành công gần nhất là %s → tự up BH từ %s (máy nghỉ/MISA '
              'đăng xuất trong khoảng đó).' % (doc_moc(), MOC_TAO))

    H = headers_misa()
    ds = [d for d in quet_bh(H, TU, DEN) if d['refno']]
    print('\nMISA có %d BH (theo Ngày hạch toán).' % len(ds))
    if CHI_MOT:
        ds = [d for d in ds if d['refno'] == CHI_MOT.strip()]
        if not ds:
            sys.exit('⛔ Không thấy %s trong khoảng ngày này.' % CHI_MOT)

    bo_qua = doc_bo_qua()
    bo_so = [d['refno'] for d in ds if d['refno'] in bo_qua]
    ds = [d for d in ds if d['refno'] not in bo_qua]

    tao, bo, tac, ton_cu = [], [], [], []
    for d in sorted(ds, key=lambda x: x['refno']):
        try:
            if d['refdate'] < MOC_TAO:
                cu = qd.da_co_tren_erp(d['refno'])
                if cu:
                    bo.append((d['refno'], cu['name'],
                               'Nháp' if cu['docstatus'] == 0 else 'đã Submit'))
                else:
                    ton_cu.append(d)
                continue
            xu_ly_bh(H, d, tao, bo, tac)
        except Exception as e:
            tac.append((d['refno'], 'lỗi khi xử: %s' % str(e)[:160]))

    lech = so_lai_tien(ds, [x for x in bo if x[0] in {d['refno'] for d in ds
                                                    if d['refdate'] >= MOC_TAO}])

    if bo_so:
        print('── TRONG SỔ BỎ QUA (%d): %s' % (len(bo_so), ', '.join(sorted(bo_so))))
    if bo:
        print('── ĐÃ CÓ TRÊN ERP (%d)' % len(bo))
        for r, n, tt in bo:
            print('   %-9s → %s (%s)' % (r, n, tt))
    if KHACH_MOI:
        print('── KHÁCH LẤY TỪ MISA TẠO SANG ERP (%d) — Tú chốt 15/10/2026' % len(KHACH_MOI))
        for r, k, tt in KHACH_MOI:
            print('   %-9s %s · %s' % (r, k, tt))
    if DA_GIAO:
        print('── BỎ QUA vì đơn trùng đã có phiếu giao của anh Tùng (%d)' % len(DA_GIAO))
        for r, ly in DA_GIAO:
            print('   %-9s %s' % (r, ly))
    if lech:
        print('\n── ⚠️ TIỀN LỆCH SO MISA — kế toán đã sửa BH? KHÔNG tự sửa (%d)' % len(lech))
        for r, n, a, b in lech:
            print('   %-9s %s  ERP %s · MISA %s' % (r, n, qd.tien(a), qd.tien(b)))
    if ton_cu:
        print('\n── ⚠️ TỒN CŨ chưa có trên ERP — KHÔNG tự up, hỏi người (%d)' % len(ton_cu))
        theo_ngay = {}
        for d in ton_cu:
            theo_ngay.setdefault(d['refdate'], []).append(d)
        for ngay in sorted(theo_ngay):
            g = theo_ngay[ngay]
            print('   %s: %d BH · %s · %s' % (
                ngay, len(g), qd.tien(sum(float(x.get('total_amount') or 0) for x in g)),
                ' '.join(x['refno'] for x in g)))
        print('   → BH nào cố ý không up thì thêm số BH vào sổ bỏ qua (--bo-qua).')
    if tac:
        print('\n── ⛔ TẮC, cần người xử (%d)' % len(tac))
        ngay_ht = {d['refno']: d['refdate'] for d in ds}
        for r, ly in tac:
            # kèm ngày HT để routine tự thử lại BH thiếu mã/khách bằng --chi ... --tu (03/10/2026)
            print('   %-9s %s · ngày HT %s' % (r, ly, ngay_ht.get(r, '?')))

    print('\n── SẼ TẠO (%d đơn)' % len(tao))
    for refno, d, dong, than, vat_pt, nb, khach, giao, vi_sao in tao:
        print('   %-9s %s  %-40s tổng %s · %d dòng · VAT %s%% · giao %s%s'
              % (refno, d['refdate'], khach[:40], qd.tien(d.get('total_amount')),
                 len(dong), vat_pt, giao, '' if nb else ' · ⚠️ không có Sales Person'))
        if vi_sao != 'N+%d' % NGAY_GIAO_CONG:
            print('             ngày giao theo %s: %s' % (vi_sao, (d.get('journal_memo') or '')[:80]))

    tao_xong = []
    if GHI_THAT and tao:
        print('\n── GHI LÊN ERP')
        for refno, d, dong, than, vat_pt, nb, khach, giao, vi_sao in tao:
            try:
                r = qd.erp('/api/resource/Sales%20Order', 'POST', than)
                ma = r['data']['name']
                ct = qd.erp('/api/resource/Sales%20Order/' + up.quote(ma)).get('data', {})
                kho_sai = [x.get('item_code') for x in ct.get('items', [])
                           if x.get('warehouse') != qd.KHO]
                sl_erp = sum(float(x.get('qty') or 0) for x in ct.get('items', []))
                sl_misa = sum(float(x.get('quantity') or 0) for x in dong)
                tong_erp = float(ct.get('grand_total') or 0)
                tong_misa = float(d.get('total_amount') or 0)
                sai = []
                if ct.get('set_warehouse') != qd.KHO or kho_sai:
                    sai.append('kho sai')
                if abs(sl_erp - sl_misa) > 0.001:
                    sai.append('số lượng ERP %g ≠ MISA %g' % (sl_erp, sl_misa))
                if abs(tong_erp - tong_misa) > 1:
                    sai.append('tổng ERP %s ≠ MISA %s' % (qd.tien(tong_erp), qd.tien(tong_misa)))
                if sai:
                    print('   ⛔ %-9s → %s để NHÁP, không Submit: %s' % (refno, ma, '; '.join(sai)))
                    tac.append((refno, '%s nháp: %s' % (ma, '; '.join(sai))))
                    continue
                qd.erp('/api/method/frappe.client.submit', 'POST', {'doc': json.dumps(ct)})
                lai = qd.erp('/api/resource/Sales%20Order/' + up.quote(ma)).get('data', {})
                if lai.get('docstatus') == 1:
                    print('   ✅ %-9s → %s · tổng %s khớp · SL %g khớp · đã Submit'
                          % (refno, ma, qd.tien(tong_erp), sl_erp))
                    tao_xong.append((refno, ma))
                else:
                    print('   ⚠️ %-9s → %s gọi Submit xong vẫn docstatus=%s'
                          % (refno, ma, lai.get('docstatus')))
                    tac.append((refno, '%s chưa Submit được' % ma))
            except Exception as e:
                print('   ⛔ %-9s %s' % (refno, str(e)[:250]))
                tac.append((refno, str(e)[:120]))
    elif tao:
        print('\n→ Chưa ghi gì. Đúng thì chạy lại kèm --that')

    # Lượt GHI THẬT quét trọn (không lọc --chi) → dời mốc "đã quét tới" sang hôm nay.
    if GHI_THAT and TU_DONG and not CHI_MOT:
        MOC_FILE.parent.mkdir(exist_ok=True)
        MOC_FILE.write_text(dt.datetime.now().strftime('%Y-%m-%d %H:%M') + '\n', encoding='utf-8')
    if BU_NGAY:
        print('\n(Lượt này đã bù ngày lỡ từ %s.)' % MOC_TAO)

    # Một dòng cuối cho routine đọc
    print('\nTÓM TẮT: %s · tạo %d · đã có %d · tắc %d · tồn cũ %d · lệch tiền %d'
          % ('GHI THẬT' if GHI_THAT else 'XEM THỬ',
             len(tao_xong) if GHI_THAT else len(tao), len(bo), len(tac),
             len(ton_cu), len(lech)))


if __name__ == '__main__':
    main()
