# -*- coding: utf-8 -*-
"""Rà BH trên MISA, kế toán sửa BH SAU khi đã up thì sửa lại Sales Order trên ERP cho khớp.

Vì sao có file này (29/09/2026)
    Tú dặn: "tự động rà soát các phiếu BH trên misa nếu có thay đổi và cập nhật lại trên ERP
    để khớp số liệu". Đối chiếu 29/09 thấy 5 đơn lệch vì kế toán thêm dòng / tăng số lượng /
    đổi mã hàng sau khi máy quét đã up.

Cách sửa: nút "Cập nhật mặt hàng" (Update Items) của ERP, tức
    erpnext.controllers.accounts_controller.update_child_qty_rate.
    KHÔNG Cancel, KHÔNG Amend, KHÔNG đụng phiếu giao hàng.

CHỈ TỰ SỬA khi an toàn:
    · đơn đã Submit, chưa xuất hoá đơn (per_billed = 0), không Closed/Completed;
    · không dòng nào phải giảm xuống DƯỚI số đã giao (đổi mã hàng đã giao, bớt hàng đã giao
      → phải huỷ/trả phiếu giao trước — việc của kho → chỉ BÁO);
    · mã hàng mới có sẵn trên ERP; thuế dòng MISA = thuế của đơn;
    · tính trước tổng sau khi sửa phải khớp tổng BH MISA (lệch ≤ 2 đồng).
    Sửa xong đọc lại đơn: tổng phải khớp MISA, không thì báo.
Chỉ xét BH có Ngày hạch toán từ 24/09/2026 và đang có đúng một đơn Submit mang po_no = số BH.
BH không còn trên MISA thì doi-chieu-erp-misa.py báo, file này không đụng.

MẶC ĐỊNH CHỈ XEM. Muốn sửa thật thêm --that.
Dùng:
    python cap-nhat-lech-bh.py                    # xem: 14 ngày gần nhất (không trước 24/09/2026)
    python cap-nhat-lech-bh.py --that             # sửa thật (routine gọi dòng này)
    python cap-nhat-lech-bh.py --tu 2026-09-24 --chi BH04836 --that
"""
import datetime as dt
import importlib.util
import json
import os
import sys
import urllib.parse as up

for _luong in (sys.stdout, sys.stderr):
    try:
        _luong.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import dong_bh
SAN = '2026-09-24'


def tham_so(ten, mac_dinh=None):
    return sys.argv[sys.argv.index(ten) + 1] if ten in sys.argv else mac_dinh


HOM_NAY = dt.date.today()
TU = max(SAN, tham_so('--tu', (HOM_NAY - dt.timedelta(days=14)).isoformat()))
DEN = tham_so('--den', HOM_NAY.isoformat())
GHI_THAT = '--that' in sys.argv
GIEO = '--gieo' in sys.argv           # chỉ ghi mốc "ERP đang khớp MISA", không sửa gì
CHI_MOT = tham_so('--chi')
FILE_TT = os.path.join(HERE, 'log', 'cap-nhat-lech-trang-thai.json')

# Nạp máy quét BH (không sửa file gốc). Đổi argv để phần đầu file đó không hiểu nhầm tham số.
_argv = sys.argv
sys.argv = [_argv[0], '--tu', TU, '--den', DEN]
_s = importlib.util.spec_from_file_location('bh', os.path.join(HERE, 'quet-bh-misa-len-erp.py'))
bh = importlib.util.module_from_spec(_s)
_s.loader.exec_module(bh)
sys.argv = _argv
qd = bh.qd


def f(x):
    return float(x or 0)


def doc_so(ten):
    return qd.erp('/api/resource/Sales%20Order/' + up.quote(ten)).get('data', {})


def doc_tt():
    """Mốc mỗi BH: phiên bản BH trên MISA (edit_version) lần cuối ERP còn khớp MISA."""
    try:
        with open(FILE_TT, encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}


def ghi_tt(tt):
    os.makedirs(os.path.dirname(FILE_TT), exist_ok=True)
    with open(FILE_TT, 'w', encoding='utf-8') as fh:
        json.dump(tt, fh, ensure_ascii=False, indent=1, sort_keys=True)


def phieu_giao_con_hieu_luc(ten_so):
    """Phiếu giao hàng (Delivery Note chưa huỷ, kể cả phiếu trả hàng) trỏ tới đơn này."""
    q = up.urlencode({'parent': 'Delivery Note',
                      'filters': json.dumps([['against_sales_order', '=', ten_so]]),
                      'fields': json.dumps(['parent']), 'limit_page_length': 50})
    ct = qd.erp('/api/resource/Delivery%20Note%20Item?' + q).get('data', [])
    kq = []
    for ma in sorted({x['parent'] for x in ct}):
        p = qd.erp('/api/resource/Delivery%20Note/' + up.quote(ma)).get('data', {})
        if p.get('docstatus') in (0, 1):
            kq.append(ma)
    return kq


def thue_don(so):
    """Tổng % thuế 'On Net Total' của đơn. Cấu trúc khác thì None (không tự tính được)."""
    ts = so.get('taxes') or []
    if not ts or any(t.get('charge_type') != 'On Net Total' for t in ts):
        return None
    return sum(f(t.get('rate')) for t in ts)


def du_tong(so, dong_moi, pt):
    """Tính trước grand_total sau khi thay dòng hàng (giữ nguyên chiết khấu cả đơn)."""
    tong_hang = sum(round(q * r, 2) for q, r in dong_moi)
    ck = f(so.get('discount_amount'))
    if ck and so.get('apply_discount_on') == 'Grand Total':
        return tong_hang * (1 + pt / 100) - ck
    return (tong_hang - ck) * (1 + pt / 100)


def mo_ta_moi(r, x):
    """Mô tả dòng sau khi đồng bộ (luật Tú 19/10/2026: BH có ghi chú thì ERP phải có, viết ngắn).
    Giữ nguyên chữ đang có trên ERP; chỉ nối thêm ghi chú MISA mà ERP chưa có."""
    cu = (r.get('description') or '').strip()
    if cu and cu.lower() == (r.get('item_name') or '').strip().lower():
        cu = ''                                   # chữ mặc định = tên hàng, coi như trống
    if cu.startswith('Nguồn: MISA CRM') and '\n' not in cu and '|' not in cu:
        cu = ''                                   # chữ mặc định của danh mục hàng (nhập từ MISA CRM), không phải ghi chú
    them = [g for g in dong_bh.cac_ghi_chu(x) if dong_bh.chuan(g) not in dong_bh.chuan(cu)]
    if not them:
        return cu or None
    return (cu + ' | ' if cu else '') + ' / '.join(them)


def lap_ke_hoach(so, dong_misa, bh_misa, chi_khi_lech=False):
    """Trả (trans_items, mô tả thay đổi) hoặc (None, lý do không tự sửa được).
    KHÔNG gộp mã: mỗi dòng MISA ↔ một dòng ERP (dong_bh.lap_plan). description luôn được truyền
    (update_child_qty_rate ghi đè Mô tả của MỌI dòng nếu thiếu — sự cố BH05237 15/10/2026).
    chi_khi_lech=True: tổng đã khớp, chỉ xem cấu trúc/mô tả có lệch không → trả ([], []) nếu y hệt."""
    if so.get('per_billed') and f(so['per_billed']) > 0:
        return None, 'đơn đã xuất hoá đơn %s%% — không tự sửa' % so['per_billed']
    if so.get('status') in ('Closed', 'Completed', 'On Hold'):
        return None, 'đơn đang %s — không tự sửa' % so['status']
    pt = thue_don(so)
    if pt is None:
        return None, 'thuế của đơn không phải dạng "On Net Total" — không tự tính được'
    for x in dong_misa:
        ma = (x.get('inventory_item_code') or '').strip()
        if x.get('vat_rate') is None or abs(f(x.get('vat_rate')) - pt) > 0.001:
            return None, 'dòng %s thuế %s%% ≠ thuế đơn %g%%' % (ma, x.get('vat_rate'), pt)

    kh = dong_bh.lap_plan(dong_misa, so.get('items') or [], f)
    trans, doi, dong_moi = [], [], []
    for r, x in kh['giu']:
        ma = r['item_code']
        sl, gm = f(x.get('quantity')), f(x.get('unit_price'))
        da_giao = f(r.get('delivered_qty'))
        if sl + 1e-9 < da_giao:
            return None, ('%s: MISA %g < đã giao %g — phải trả/huỷ phiếu giao trước (việc của kho)'
                          % (ma, sl, da_giao))
        gia = f(r['rate']) if (abs(f(r['rate']) - gm) < 0.01 or abs(f(r['rate']) - gm) * sl <= 1) else gm
        if abs(sl - f(r['qty'])) > 1e-9:
            doi.append('%s: SL %g → %g' % (ma, f(r['qty']), sl))
        if gia != f(r['rate']):
            doi.append('%s: đơn giá %s → %s' % (ma, qd.tien(r['rate']), qd.tien(gia)))
        mt = mo_ta_moi(r, x)
        if (mt or '') != (r.get('description') or '').strip() and mt:
            doi.append('%s: ghi mô tả "%s"' % (ma, mt))
        trans.append({'docname': r['name'], 'item_code': ma, 'qty': sl, 'rate': gia,
                      'uom': r.get('uom'), 'conversion_factor': f(r.get('conversion_factor')) or 1,
                      'delivery_date': r.get('delivery_date') or so.get('delivery_date'),
                      'description': mt})
        dong_moi.append((sl, gia))
    for r in kh['xoa']:
        if f(r.get('delivered_qty')) > 0:
            return None, ('%s × %g có trên ERP (đã giao %g) nhưng MISA không còn dòng đó — '
                          'phải huỷ phiếu giao trước (việc của kho)'
                          % (r['item_code'], f(r['qty']), f(r['delivered_qty'])))
        doi.append('bỏ dòng %s × %g (chưa giao)' % (r['item_code'], f(r['qty'])))
        # không đưa vào trans_items = ERP xoá dòng (chỉ cho khi chưa giao)
    for x in kh['them']:
        ma = x['_ma']
        if not qd.co_item(ma):
            return None, 'mã hàng %s chưa có trên ERP — báo người phụ trách danh mục' % ma
        mt = dong_bh.ghi_chu_misa(x)
        doi.append('thêm %s × %g · đơn giá %s%s' % (ma, f(x.get('quantity')), qd.tien(x.get('unit_price')),
                                                     (' · mô tả "%s"' % mt) if mt else ''))
        trans.append({'item_code': ma, 'qty': f(x.get('quantity')), 'rate': f(x.get('unit_price')),
                      'conversion_factor': 1, 'delivery_date': so.get('delivery_date'),
                      'description': mt or None})
        dong_moi.append((f(x.get('quantity')), f(x.get('unit_price'))))

    if not doi:
        if chi_khi_lech:
            return [], []
        return None, 'dòng hàng giống hệt MISA mà tổng vẫn lệch (chiết khấu/thuế đổi?) — người xem'
    du = du_tong(so, dong_moi, pt)
    tong_bh = f(bh_misa.get('total_amount'))
    if abs(du - tong_bh) > 2:
        return None, ('sửa dòng hàng xong vẫn lệch: dự tính %s · MISA %s (chiết khấu/thuế đổi?) '
                      '— không tự sửa. Cần đổi: %s' % (qd.tien(du), qd.tien(tong_bh), '; '.join(doi)))
    return trans, doi


def main():
    qd.ERP_URL, qd.ERP_AUTH = qd.khoa_erp()
    print('Rà BH đã sửa trên MISA %s → %s · %s' % (TU, DEN,
          '⚠️  SỬA THẬT' if GHI_THAT else 'XEM THỬ (không ghi gì)'))
    H = bh.headers_misa()
    misa = {d['refno']: d for d in bh.quet_bh(H, TU, DEN) if d['refno'] and d['refdate'] >= SAN}
    so_ds = qd.erp_ds('Sales Order', [['po_no', 'like', 'BH%'], ['docstatus', '=', 1],
                                      ['transaction_date', '>=', TU]],
                      ['name', 'po_no', 'grand_total'], 1000)
    theo_bh = {}
    for x in so_ds:
        theo_bh.setdefault(x['po_no'], []).append(x)

    tt = doc_tt()
    bo_qua_erp = []
    sua, khong, loi = [], [], []
    for refno in sorted(theo_bh):
        if CHI_MOT and refno != CHI_MOT:
            continue
        if refno not in misa:
            continue                      # BH mất trên MISA: doi-chieu báo, ở đây không đụng
        ds = theo_bh[refno]
        if len(ds) > 1:
            khong.append((refno, ', '.join(x['name'] for x in ds), 'có %d đơn Submit cùng số BH' % len(ds)))
            continue
        x = ds[0]
        tong_bh = f(misa[refno].get('total_amount'))
        ver = str(misa[refno].get('edit_version') or '')
        if abs(f(x['grand_total']) - tong_bh) <= 2:
            # Tổng khớp nhưng MISA vừa được sửa (edit_version đổi) → soi từng dòng + mô tả, vì đổi cấu trúc
            # (tách/gộp dòng, đổi ghi chú cắt/hạ size) có thể không làm đổi tổng.
            cu = tt.get(refno)
            if ver and cu and cu.get('so') == x['name'] and cu.get('ver') != ver and not GIEO:
                try:
                    so = doc_so(x['name'])
                    dong, _ = bh.quet_dong_bh(H, misa[refno].get('refid'))
                    trans, doi = lap_ke_hoach(so, dong, misa[refno], chi_khi_lech=True)
                except Exception as e:
                    loi.append((refno, x['name'], 'soi cấu trúc: ' + str(e)[:200]))
                    continue
                if trans is None:
                    # Tổng đã khớp mà dòng/mô tả không tự đồng bộ được (vd dòng quà tặng giá 0 trên ERP,
                    # dòng đã giao) → không ghi gì, không báo oan; ghi mốc để khỏi soi lại mỗi lượt.
                    tt[refno] = {'ver': ver, 'so': x['name']}
                    continue
                if trans:
                    if not GHI_THAT:
                        sua.append((refno, x['name'], doi, 'SẼ SỬA (tổng khớp, lệch dòng/mô tả)'))
                        continue
                    try:
                        qd.erp('/api/method/erpnext.controllers.accounts_controller.update_child_qty_rate',
                               'POST', {'parent_doctype': 'Sales Order', 'parent_doctype_name': x['name'],
                                        'child_docname': 'items', 'trans_items': json.dumps(trans)})
                        lai = doc_so(x['name'])
                    except Exception as e:
                        loi.append((refno, x['name'], str(e)[:250]))
                        continue
                    thieu_mt = [t['item_code'] for t in trans if t.get('description') and not any(
                        (r.get('description') or '').strip() for r in lai.get('items', [])
                        if r['item_code'] == t['item_code'])]
                    if abs(f(lai.get('grand_total')) - tong_bh) <= 2 and lai.get('docstatus') == 1 and not thieu_mt:
                        tt[refno] = {'ver': ver, 'so': x['name']}
                        sua.append((refno, x['name'], doi, 'ĐÃ SỬA · tổng %s khớp MISA' % qd.tien(lai['grand_total'])))
                    else:
                        loi.append((refno, x['name'], 'đã sửa nhưng tổng %s / mô tả mất %s — người xem'
                                    % (qd.tien(lai.get('grand_total')), ', '.join(thieu_mt) or '-')))
                    continue
            if ver:
                tt[refno] = {'ver': ver, 'so': x['name']}
            continue
        if GIEO:
            continue
        # Tú chốt 15/10/2026: đơn ERP đã có phiếu giao mà bị sửa mặt hàng ngay trên ERP (anh Tùng trả hàng,
        # giảm SL…) thì KỆ, không sửa lại cho giống MISA. MISA đổi thì vẫn cập nhật về ERP.
        # "Sửa từ ERP" = MISA không đổi (edit_version y như lần cuối ERP còn khớp) mà ERP đã lệch.
        cu = tt.get(refno)
        if cu and cu.get('ver') == ver and cu.get('so') == x['name']:
            try:
                pg = phieu_giao_con_hieu_luc(x['name'])
            except Exception:
                pg = []     # tra phiếu giao lỗi thì giữ cách cũ, không bỏ oan
            if pg:
                bo_qua_erp.append((refno, x['name'], 'ERP %s · MISA %s · phiếu giao %s'
                                   % (qd.tien(x['grand_total']), qd.tien(tong_bh), ', '.join(pg))))
                continue
        try:
            so = doc_so(x['name'])
            dong, _ = bh.quet_dong_bh(H, misa[refno].get('refid'))
            trans, doi = lap_ke_hoach(so, dong, misa[refno])
            if trans is None:
                khong.append((refno, x['name'], doi))
                continue
            if not GHI_THAT:
                sua.append((refno, x['name'], doi, 'SẼ SỬA'))
                continue
            qd.erp('/api/method/erpnext.controllers.accounts_controller.update_child_qty_rate',
                   'POST', {'parent_doctype': 'Sales Order', 'parent_doctype_name': x['name'],
                            'child_docname': 'items', 'trans_items': json.dumps(trans)})
            lai = doc_so(x['name'])
            # Dòng THÊM qua Update Items lấy kho từ set_warehouse của đơn — kiểm lại chứ đừng
            # tin (luật "đúng kho" của quet-don, thêm khi gộp 29/09/2026).
            kho_sai = [r.get('item_code') for r in lai.get('items', []) if r.get('warehouse') != qd.KHO]
            if kho_sai:
                loi.append((refno, x['name'], 'đã sửa nhưng dòng %s KHÔNG ở kho %s — người sửa kho'
                            % (', '.join(kho_sai), qd.KHO)))
                continue
            mat_mt = [t['item_code'] for t in trans if t.get('description') and not any(
                (r.get('description') or '').strip() for r in lai.get('items', []) if r['item_code'] == t['item_code'])]
            if mat_mt:
                loi.append((refno, x['name'], 'đã sửa nhưng Mô tả dòng %s bị mất — người xem' % ', '.join(mat_mt)))
                continue
            if abs(f(lai.get('grand_total')) - tong_bh) <= 2 and lai.get('docstatus') == 1:
                if ver:
                    tt[refno] = {'ver': ver, 'so': x['name']}
                sua.append((refno, x['name'], doi, 'ĐÃ SỬA · tổng %s khớp MISA' % qd.tien(lai['grand_total'])))
            else:
                loi.append((refno, x['name'], 'đã gọi sửa nhưng tổng ERP %s ≠ MISA %s — người xem'
                            % (qd.tien(lai.get('grand_total')), qd.tien(tong_bh))))
        except Exception as e:
            loi.append((refno, x['name'], str(e)[:250]))

    if GHI_THAT or GIEO:
        try:
            ghi_tt(tt)
        except Exception as e:
            print('⚠️ không ghi được mốc %s: %s' % (FILE_TT, str(e)[:120]))
    if GIEO:
        print('GIEO: đã ghi mốc cho %d BH (ERP đang khớp MISA).' % len(tt))
    if bo_qua_erp:
        print('\n── BỎ QUA vì đơn đã có phiếu giao và sửa ngay trên ERP, MISA không đổi (%d)' % len(bo_qua_erp))
        for r, n, ly in bo_qua_erp:
            print('   %-9s → %s · %s' % (r, n, ly))

    print('\n── SỬA CHO KHỚP MISA (%d)' % len(sua))
    for r, n, doi, tt in sua:
        print('   ✅ %-9s → %s · %s' % (r, n, tt))
        for d in doi:
            print('        %s' % d)
    if khong:
        print('\n── ⛔ LỆCH MÀ KHÔNG TỰ SỬA ĐƯỢC — cần người (%d)' % len(khong))
        for r, n, ly in khong:
            print('   %-9s → %s · %s' % (r, n, ly))
    if loi:
        print('\n── ⚠️ LỖI (%d)' % len(loi))
        for r, n, ly in loi:
            print('   %-9s → %s · %s' % (r, n, ly))
    print('\nTÓM TẮT CẬP NHẬT: %s · sửa %d · không tự sửa được %d · lỗi %d'
          % ('GHI THẬT' if GHI_THAT else 'XEM THỬ', len(sua), len(khong), len(loi)))


if __name__ == '__main__':
    main()
