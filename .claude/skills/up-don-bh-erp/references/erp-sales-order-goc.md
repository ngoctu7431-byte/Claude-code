> Chép từ bộ nhớ Claude trên máy tính của Ngọc Tú ngày 31/10/2026. Đường dẫn `C:\…`, `D:\…` là của
> máy tính đó; trên iPad/iPhone thì dữ liệu do Tú gửi kèm. Chữ "anh Tú"/"chị" = công chúa (Tú).

> **Từ 24/09/2026: KHÔNG đưa Đơn đặt hàng (ĐHxxxxx trên MISA) lên ERP nữa** — Ngọc Tú chốt, đã
> tắt tác vụ tự động `misa-order-sync`. Chỉ nhập khi Ngọc Tú yêu cầu lại rõ ràng; quy tắc dưới
> đây giữ lại để dùng lúc đó. Xem `misa-erp-sync-van-hanh`.

Khi nhập "Đơn đặt hàng" (PDF/chứng từ ĐHxxxxx) thành Sales Order trong ERP (company "Nệm Thành Công"):

1. **Kho (warehouse)**: luôn dùng `Kho tổng bán hàng - TC` cho cả `set_warehouse` (cấp đơn) lẫn từng dòng `items[].warehouse`. KHÔNG dùng "Finished Goods - TC" (đã nhập sai lần đầu, bị đồng nghiệp kế toán tự sửa lại qua thao tác cancel+amend).
2. **Ngày giao hàng (`delivery_date`)**: mặc định (từ 2026-09-21) là **n+7** — ngày đặt hàng (`transaction_date`) + 7 ngày, áp dụng cho đơn thường (không ghi chú gấp, hoặc ghi chú không nêu deadline cụ thể). (Trước 2026-09-21 dùng n+2 — đã đổi, không dùng n+2 nữa.)
   - **Ngoại lệ (từ 2026-09-18)**: nếu Ghi chú trên chứng từ nêu rõ là đơn **gấp** kèm **deadline/ngày giao cụ thể** (vd "ĐƠN GẤP GIAO HÔM NAY 18/09", "giao gấp ngày X") → **ưu tiên lấy đúng ngày đó làm `delivery_date`**, bỏ qua công thức n+7. Chỉ ghi chú "gấp" chung chung mà không có ngày cụ thể thì vẫn dùng n+7.
   - Nếu ngày trong ghi chú gấp lại SỚM HƠN `transaction_date` (đặt hàng ngày sau nhưng đòi giao trước) thì ERPNext sẽ chặn (delivery_date phải >= transaction_date) — báo người dùng, không tự ý đổi ngày.
3. **Sau khi tạo xong đơn phải Submit ngay** (docstatus 0 → 1) để kho tiếp nhận xử lý — không để ở trạng thái Draft chờ.
4. **Thuế**: thêm dòng `taxes` thủ công (không dùng `taxes_and_charges` template): `{charge_type: "On Net Total", account_head: "VAT - TC", description: "VAT @ 8.0", cost_center: "Main - TC", rate: 8}`.
5. **po_no**: lưu mã đơn gốc (vd "ĐH02977") vào field `po_no` (+ `po_date` = ngày đặt) để đối chiếu, tránh nhập trùng — luôn kiểm tra `po_no` đã tồn tại trong Sales Order trước khi tạo mới.
6. **selling_price_list**: dùng "Standard Selling" cho khách lẻ B2C thông thường; `rate` mỗi dòng lấy trực tiếp từ đơn giá trên chứng từ (override price list, không phụ thuộc giá niêm yết).
7. Nếu thiếu Customer hoặc Item trong ERP: được phép tự tạo mới theo đúng thông tin trên chứng từ (đã được người dùng xác nhận chủ trương này), theo mẫu field của các bản ghi tương tự đã có (item_group, brand, product_line, thickness_size, width_size...). Field `width_size` là select cố định, không tự bịa giá trị ngoài danh sách hợp lệ.
8. **Đơn đặt qua chat (ảnh chụp Zalo/Facebook), không có chứng từ ĐHxxxxx** (chốt 22/09/2026):
   - `po_no` để **trống** — không bịa mã. Hỏi người dùng nếu cần ghi gì vào đó.
   - Chat thường không ghi giá → lấy `selling_price_list` = **`default_price_list` của Customer**
     (vd đại lý Miền Nam dùng "Giá đại lý - Miền Nam"), KHÔNG dùng "Standard Selling" — đó là
     giá khách lẻ B2C. Giá trong Item Price là giá **chưa VAT**.
   - Quy cách trong chat: "1m6 x 15p" = rộng 160cm × dày 15cm → item `SORA15-6`
     (mã dạng `<DÒNG><dày><-mã rộng>`); "sl 10t" = 10 Tấm.
   - Tên hiển thị trên Zalo có thể khác tên khách trong ERP (vd Zalo "Nệm Thắng Lợi - Chính Hãng
     - Anh Hữu Thảo" ↔ ERP "HỘ KINH DOANH NỆM VIỆT NHẬT - NGUYỄN HỮU THẢO"). Dò theo tên người,
     rồi **trình lại cho người dùng xác nhận trước khi submit**.
   - Quy trình đã chốt: tạo Draft → gửi PDF/ảnh đơn cho người dùng coi → người dùng gật → submit.

9. **Kỹ thuật**: tool `mcp__frappe__list_documents` **bỏ qua filters** (trả về dữ liệu không liên
   quan). Dùng `mcp__0f3084c7-...__list_documents` / `search_link` — mấy tool này áp filter đúng.
   Lấy PDF đơn: `GET /api/method/frappe.utils.print_format.download_pdf?doctype=Sales Order&name=<mã>`
   kèm header `Authorization: token <key>:<secret>` (khoá trong `C:\Claude Code\.mcp.json`).

10. **Chiết khấu theo dòng hàng trên MISA** (mỗi dòng có % CK riêng, hoặc quà tặng CK 100%):
    KHÔNG dùng `discount_percentage` trên từng dòng `items`. Thay vào đó: `rate` mỗi dòng = đúng
    "Đơn giá" (giá trước chiết khấu) trên MISA; cộng dồn toàn bộ "Tiền chiết khấu" các dòng lại
    thành một số, đưa vào cấp đơn: `apply_discount_on: "Net Total"`, `discount_amount: <tổng>`.
    Đã đối chiếu khớp `grand_total` với "Tổng tiền thanh toán" MISA theo đúng cách này (chốt
    23/09/2026, xác nhận lại qua đơn ĐH02959/SAL-ORD-2026-00096 đã có từ trước — cùng một kiểu).
11. **Item có sẵn nhưng `is_sales_item = 0`**: gặp lại đúng trường hợp SKILL.md cảnh báo (vd
    `TSR234`, 23/09/2026) — bật lại `is_sales_item: 1` bằng `update_document` trước khi thêm vào
    đơn, không tự tạo item trùng mã.
12. **Đơn cũ có nhiều dòng vẫn tự đối chiếu lại `grand_total`** với "Tổng tiền thanh toán" MISA
    trước khi Submit (chênh vài đồng do làm tròn là bình thường, KHÔNG tự sửa số).

**Why**: Người dùng (ngoctu@nemvietnhat.com) trực tiếp chỉnh sửa quy trình sau khi phát hiện tôi dùng sai kho "Finished Goods - TC" thay vì kho chuẩn, và để đơn ở Draft thay vì submit — gây thêm việc cho kế toán phải tự sửa lại.

**How to apply**: Áp dụng mọi lúc nhập Sales Order từ chứng từ PDF/AMIS vào ERP này, kể cả các phiên làm việc sau.
