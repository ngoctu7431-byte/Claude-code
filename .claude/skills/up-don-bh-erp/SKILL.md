---
name: up-don-bh-erp
description: Up Chứng từ bán hàng BH (MISA AMIS) thành Sales Order trên ERP Frappe của Nệm Thành Công theo đúng luật của Ngọc Tú — kiểm trùng po_no, tìm khách, kho "Kho tổng bán hàng - TC", ngày giao +7, thuế VAT 8%, chiết khấu, mô tả dòng ngắn, không gộp mã, đối chiếu tổng tiền rồi Submit. Dùng khi Tú nói "up đơn", "up BH", "lên đơn ERP", gửi ảnh chụp/ file xuất danh sách BH từ MISA, hoặc hỏi vì sao BH chưa lên ERP.
---

# Up đơn BH (MISA) → Sales Order (ERP)

Đọc `references/luat-chung.md` trước. Luật nhập đơn chi tiết: `references/luat-sales-order.md`.

## Hai cách chạy — chọn theo thiết bị

| Đang ở | Cách |
|---|---|
| **iPad / iPhone / claude.ai** (không có máy quét) | Tú gửi **ảnh chụp chi tiết BH** (MISA › Bán hàng › Bán hàng › bấm số BH, thấy bảng Mã hàng · SL · Đơn giá · Thành tiền · % thuế) hoặc **file Excel** xuất từ MISA. Em đọc → tạo SO qua **connector ERP**. Các bước dưới. |
| **Máy tính Windows có Claude Code + máy quét đã cài** | Chạy máy quét: xem `may-tinh/LENH.txt` và `may-tinh/HUONG-DAN-CAI-QUET-BH.md`. Từ 26/10/2026 Tú KHÔNG bật routine tự động: Tú kêu "up đơn" thì chạy **đúng một lượt** (`xem-thu.cmd` xem trước, rồi `chay-routine.cmd`) và báo kết quả. |

Cả hai cách đều phải đúng bộ luật trong `luat-sales-order.md`.

## Các bước (iPad / iPhone)
0. Kiểm connector ERP đang bật (thử `list_documents` doctype `Company`, limit 1). Không có → dừng, báo
   "chưa bật connector ERP", không làm tiếp.
1. **Đọc từng BH** từ ảnh/file: số BH · **Ngày hạch toán** · khách (tên + mã MISA/MST) · diễn giải ·
   từng dòng: mã hàng, tên, SL, đơn giá (trước thuế), thành tiền, % thuế, tiền CK, ghi chú dòng (Hạ size…) ·
   tổng tiền hàng, tổng thuế, tổng CK, **tổng thanh toán**.
   - Tự cộng: Σ(thành tiền) phải = tiền hàng; Σ(thành tiền − CK + thuế) phải = tổng thanh toán (±2đ).
     Lệch → ảnh thiếu dòng / đọc sai → hỏi Tú chụp lại, KHÔNG tạo.
   - "BH ngày X" = Ngày hạch toán = X (chốt 29/09/2026).
2. **Kiểm trùng**: `list_documents` doctype `Sales Order`, filters
   `{"po_no": "BHxxxxx", "docstatus": [0, 1]}` (phải có docstatus để thấy cả nháp). Có rồi → bỏ, báo số SO.
   Nghi trùng (cùng khách + cùng tổng ±7 ngày **và cùng mã hàng/hạ size/SL**) → dừng hỏi, kèm so sánh dòng hàng.
3. **Bỏ qua** (không hỏi): BH chỉ có dòng Phí (Phi1, Phi2…); BH mà đơn ERP trùng đã bị anh Tùng
   (nvtungjob@gmail.com) huỷ; BH trùng đơn anh Tùng đã có Delivery Note. Người khác huỷ → hỏi.
4. **Tìm khách** theo thứ tự: `tax_id` = mã MISA/MST → `customer_details` like `%mã MISA: <mã>%` →
   `customer_name` = đúng tên. Nhiều ứng viên / tên na ná → hỏi. Không có khách → xem mục tạo khách trong
   `luat-sales-order.md` (chống trùng trước, có ứng viên na ná thì DỪNG hỏi).
5. **Kiểm mã hàng**: mỗi mã có trong `Item` (đổi mã theo bảng đổi mã trước). Thiếu mã → không tạo, báo
   "thiếu mã: X" (KHÔNG tự tạo mã hàng). `is_sales_item = 0` → báo Tú (có thể bật lại khi Tú gật).
   Dòng để trống % thuế → không tạo, hỏi Tú.
6. **Dựng đơn** theo `luat-sales-order.md` → `create_document` với `validate_only: true` trước.
7. Tạo thật (Nháp) → `get_document` đọc lại: kho, **grand_total = tổng thanh toán MISA (±2đ)**,
   **total_qty = tổng SL**, mô tả còn đủ. Khớp → `submit_document`. Lệch → để Nháp, báo Tú.
8. Báo kết quả theo bảng: `BH → SAL-ORD-… · khách · tổng · SL · đã Submit / để Nháp vì …`
   + danh sách BH bị bỏ qua / tắc kèm lý do (thiếu mã, thiếu khách, nghi trùng, thuế trống…).

## Không làm trên điện thoại
- Sửa đơn đã Submit cho khớp MISA (cập nhật mặt hàng) → để máy tính (script `cap-nhat-lech-bh.py`) hoặc Tú
  bấm tay. Cancel/amend → trình Tú, việc của kế toán.
- Đăng nhập MISA, quét MISA tự động.
