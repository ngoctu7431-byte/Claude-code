# Luật dựng Sales Order trên ERP (company "Nệm Thành Công")

Gom từ memory erp-sales-order-entry-rules + misa-erp-sync-van-hanh (tới 26/10/2026).

## Khung đơn
```json
{
  "company": "Nệm Thành Công",
  "customer": "<name Customer ERP>",
  "order_type": "Sales",
  "transaction_date": "<Ngày hạch toán BH, yyyy-mm-dd>",
  "delivery_date": "<+7 ngày, xem dưới>",
  "po_no": "BHxxxxx",
  "po_date": "<Ngày hạch toán>",
  "selling_price_list": "Standard Selling",
  "set_warehouse": "Kho tổng bán hàng - TC",
  "taxes_and_charges": "VAT 8% - TC",
  "taxes": [ <chép NGUYÊN các dòng của mẫu "VAT 8% - TC"> ],
  "items": [
    {"item_code": "SORA10-6", "qty": 2, "rate": 746296.3,
     "warehouse": "Kho tổng bán hàng - TC", "delivery_date": "<như trên>",
     "description": "<ghi chú ngắn hoặc bỏ trống>"}
  ]
}
```

## Luật từng ô
1. **Kho** luôn `Kho tổng bán hàng - TC` cho `set_warehouse` VÀ từng dòng. ⛔ Không dùng "Finished Goods - TC"
   (lần đầu nhập sai, kế toán phải cancel + amend).
2. **delivery_date** = Ngày hạch toán **+ 7** (chốt 21/09/2026; KHÔNG dùng +2 nữa). Ngoại lệ: diễn giải ghi
   GẤP **kèm ngày cụ thể** ("giao gấp 3/10") → lấy đúng ngày đó. Chữ "gấp" trần ("Gấp gọn đóng bao") không tính.
   Ngày gấp sớm hơn ngày đơn → ERP chặn → báo Tú, không tự đổi.
3. **po_no** = số BH (vd "BH04842"), `po_date` = Ngày hạch toán. Kiểm trùng po_no NGAY trước khi tạo, kèm
   `docstatus: [0,1]`. Đơn đặt qua ảnh chat (không có số chứng từ) → po_no để trống, không bịa.
4. **rate** = đúng "Đơn giá" trước thuế trên MISA (không lấy theo bảng giá ERP). `selling_price_list`
   chỉ để đủ ô.
   Riêng đơn từ **ảnh chat Zalo không ghi giá**: `selling_price_list` = `default_price_list` của khách (giá ERP
   chưa VAT), không dùng Standard Selling; tạo Nháp → Tú xem → Tú gật mới Submit.
5. **Thuế**: đọc mẫu `Sales Taxes and Charges Template` "VAT 8% - TC" bằng `get_document`, chép NGUYÊN các
   dòng `taxes` (charge_type, account_head, description, rate, cost_center, included_in_print_rate).
   ⚠️ Chỉ truyền tên mẫu mà không chép dòng = mất sạch VAT, không báo lỗi (bẫy 27/08/2026).
   Mẫu 10% = "Vietnam Tax - TC". Một đơn trộn nhiều mức thuế → không tạo, báo Tú tách.
   Dòng MISA trống % thuế → không tạo, hỏi. Tú gật thì thuế "Actual" = đúng tiền thuế MISA (BH04917→00272).
6. **Chiết khấu** theo dòng trên MISA → KHÔNG dùng discount_percentage từng dòng. `rate` = đơn giá trước CK;
   cộng mọi "Tiền chiết khấu" → cấp đơn: `"apply_discount_on": "Net Total", "discount_amount": <tổng>`.
7. **KHÔNG CỘNG GỘP MÃ** (19/10/2026): mỗi dòng MISA = 1 dòng ERP, kể cả cùng mã (PVH10-6 ×6 và PVH10-6 ×1
   "Cắt dán" là hai dòng).
8. **Mô tả (description)** — BH có ghi chú thì ERP phải có, viết NGẮN (19/10/2026):
   - Ghi chú của từng dòng (Hạ size, Cắt dán, Lựa phôi cứng…) → vào đúng dòng đó, rút gọn:
     "Hạ size 169cm x 192cm x 20cm" → "Hạ size 169x192x20cm"; "Cắt dán: 250cm x 200cm x 10cm" → "Cắt dán 250x200x10cm".
   - Diễn giải cả đơn (chỉ dẫn giao hàng) → chỉ ở DÒNG ĐẦU: bắt đầu bằng "giao…/ưu tiên giao…" thì giữ nguyên,
     khác thì thêm "Giao: " phía trước. Diễn giải mặc định "Bán hàng <khách>" → bỏ.
   - Mô tả chỉ chứa ghi chú, KHÔNG nhắc tên hàng (lưới ERP chỉ hiện dòng đầu ô).
   - Dòng không có ghi chú → bỏ trống cho ERP tự điền.
9. **Người bán**: tên nhân viên trên BH có trong `Sales Person` → `sales_team: [{"sales_person": "<tên>",
   "allocated_percentage": 100}]`; không có thì bỏ.
10. **Kiểm sau khi tạo**: grand_total = tổng thanh toán MISA (±2đ, lệch vài đồng do làm tròn là thường, KHÔNG
    tự sửa số), total_qty = tổng SL, kho đúng → mới Submit. **Submit ngay, không để Draft** (trừ đơn từ ảnh chat
    không giá). Mở lại bản ghi vừa tạo trước khi báo xong.

## Khách chưa có trên ERP (Tú chốt 15/10/2026)
Lấy thông tin khách trên BH tạo sang ERP rồi up đơn, NHƯNG chống trùng trước:
- So tên bỏ dấu/bỏ tiền tố (Hộ kinh doanh, Công ty TNHH…) và số điện thoại (9+ chữ số) với mọi khách ERP.
  Có ứng viên na ná → **KHÔNG tạo**, dừng hỏi Tú (vụ trùng Lã Thị Kiều Oanh 21/09/2026).
- Tạo Customer: `customer_name` = tên MISA, `customer_type` "Company", `customer_group` "Khách lẻ B2C",
  `tax_id` nếu mã MISA là MST (10/13 số) hoặc CCCD 12 số, `mobile_no`/`email` nếu có,
  `customer_details` = "mã MISA: <mã> · Tạo tự động từ BHxxxxx". Kèm Address (Billing) + Contact nếu có SĐT.
- Trên điện thoại: trình Tú thông tin khách sẽ tạo, Tú gật mới tạo.
- Khách trùng SĐT → chọn khách đã có đơn trên ERP (Trần Quang Quyết → "Anh Quyết 0703955146").
- Tên trùng khác miền (TRẦN NHÃ PHƯƠNG Bắc / "… - 1" Trung; Nguyễn Quốc Linh Nam / "… - 1" Trung) → hỏi.

## Trùng & bỏ qua
- TRÙNG = đã có SO mang `po_no` = đúng số BH. Khác số BH thì VẪN up dù cùng khách/hàng/tiền (24/09/2026),
  TRỪ ca nghi trùng: cùng khách + cùng tổng tiền ±7 ngày + cùng {mã hàng, kích thước hạ size: SL} → dừng hỏi,
  so dòng hàng 2 đơn rồi báo rõ giống/khác (07/10/2026). Tấm nguyên ≠ tấm hạ size dù cùng mã.
- Đơn trùng mà MỌI đơn ERP trùng đã có Delivery Note chưa huỷ do `nvtungjob@gmail.com` tạo → BỎ, không hỏi (14/10/2026).
- Đơn ERP của BH bị anh Tùng huỷ → bỏ luôn, không up lại, không hỏi (05/10/2026). Người khác huỷ → hỏi.
- BH chỉ có dòng Phí → bỏ.
- Sàn tự up: BH có Ngày hạch toán từ **01/10/2026**. BH cũ hơn hôm qua → hỏi Tú trước khi up.

## Đổi mã MISA → ERP
`TPET169` → `TPET169*8` (05/10/2026). Chỉ thêm cặp khi Tú chốt cùng một hàng.

## Kỹ thuật connector
- `list_documents` của connector ERP áp filter đúng. (Connector "frappe" chạy cục bộ trên máy tính thì
  BỎ QUA filter — đừng dùng nó để kiểm trùng.)
- Connector không cancel được SO đã submit — sửa SO sai phải huỷ tay trên ERP (trình Tú).
- Sửa mặt hàng đơn đã Submit bằng `update_child_qty_rate` sẽ GHI ĐÈ mô tả mọi dòng → luôn truyền `description`.
- Đơn đã có phiếu giao mà bị sửa ngay trên ERP (MISA không đổi) → KỆ, không sửa lại cho giống MISA (15/10/2026).
