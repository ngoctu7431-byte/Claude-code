---
name: bao-gia-ton-kho
description: Báo giá đại lý chính xác từng sản phẩm nệm Thuần Việt / Việt Nhật / King Home (bảng giá 2026 gồm VAT 8%, theo miền khách) KÈM số tồn kho trên ERP, giống phiên "Lên đơn hàng" của Ngọc Tú. Dùng khi Tú gửi ảnh chat Zalo, ảnh lưới MISA hoặc file đơn và hỏi giá, check giá, check tồn, "giá miền X", "giá anh Thảo", quy đổi giá chưa thuế, phí tăng/hạ size, nệm gấp, tính khối vận chuyển.
---

# Báo giá + tồn kho đơn đại lý

Đọc `references/luat-chung.md` trước (xưng hô "công chúa – em", luật cứng).

## Việc
Tú gửi đơn (ảnh chat Zalo, ảnh lưới MISA, file) → em trả **một bảng giá + tồn** cho từng dòng.
**Mọi lần báo giá đều kèm tồn** (Tú chốt 12/10 và 14/10/2026). Ngoại lệ duy nhất: câu chỉ hỏi quy đổi số
(vd "160k chưa thuế là bao nhiêu" → 160.000 ÷ 1,08 = 148.148).

## Các bước
1. **Đọc đơn.** Tách từng dòng: sản phẩm · rộng · dài · dày · số lượng. Quy ước viết tắt ở
   `references/quy-uoc-doc-don.md`. Ảnh lưới MISA có dòng tổng số lượng (vd "11,00") → cộng SL các dòng
   em đọc **phải khớp** tổng đó rồi mới báo; lệch thì đọc lại từng ô, vẫn lệch thì nói rõ với Tú.
2. **Chọn bảng** (`references/bang-gia-2026.md`):
   - Thuần Việt → 1 bảng chung mọi miền (từ 31/10/2026 = PDF "GLOBAL 2025").
   - Việt Nhật → theo **miền của khách** (Nam/Bắc/Trung). Miền lấy theo thứ tự: Tú nói trong tin → sổ
     `references/khach-mien.md` (nói rõ "theo sổ, ghi ngày …") → không có thì **HỎI**, không đoán theo địa chỉ,
     không tự lấy miền ERP.
   - King Home → bảng riêng.
   - Size/sản phẩm không có ("—") hoặc tên mơ hồ ("Latex" trần, "3 zone 20p") → hỏi, kèm giá các phương án.
3. **Tính giá** theo luật ở `references/luat-tinh-gia.md` (phí tăng size, hạ size, nệm gấp +150k,
   ngoại lệ khách Nguyễn Hữu Thảo, độ dày vượt bảng, quà gối, mặc định 10cm…).
4. **Tra tồn trên ERP** (connector ERP Frappe; nếu chưa bật thì nói thẳng, vẫn báo giá):
   - Mã hàng ERP: xem `references/quy-uoc-ma-hang.md`; không chắc mã → `list_documents` doctype `Item`
     lọc `item_name` like `%Sora%`… rồi chọn đúng dày + rộng.
   - `list_documents` doctype **`Bin`**, lọc `{"item_code": "<mã>"}`, fields
     `["warehouse","actual_qty","reserved_qty","projected_qty"]`.
   - Cột chính = kho **"Kho tổng bán hàng - TC"**: **còn bán được = `projected_qty`** (tồn thực − đã giữ cho
     đơn khác). KHÔNG dùng `actual_qty` làm số bán được. Kho khác (Tổ Nệm Mút, Tổ Cao Su) ghi phụ; bỏ Kho bảo hành.
   - Hết hàng → gợi ý size/độ dày cùng dòng còn tồn.
   - Ghi **ngày giờ lấy số tồn**.
5. **Đối chiếu miền ERP** (chỉ hàng Việt Nhật): `list_documents` doctype `Customer` lọc
   `customer_name` like `%tên%`, field `default_price_list`. Báo 1 dòng: ✅ khớp / ❌ lệch (ERP ghi X, Tú báo Y) /
   ⚠️ ERP chưa gán / ⚠️ không thấy khách. **Không tự sửa Customer.** Tên trùng khác miền → hỏi khách nào.
   Kết quả đối chiếu mới → nhắc Tú thêm dòng vào sổ khách-miền (xem luật chung, mục góp ý).

## Mẫu trả lời
```
Đơn <khách> · giá miền <X> (theo Tú/ theo sổ dd/MM/yyyy) · ERP: ✅ khớp
| # | Sản phẩm | Size | SL | Đơn giá (gồm VAT) | Thành tiền | Chưa VAT (÷1,08) | Còn bán được* |
|---|---|---|---|---|---|---|---|
...
Tổng: … tấm · … đ (gồm VAT)
*Tồn Kho tổng bán hàng - TC lúc hh:mm dd/MM/yyyy. Hết hàng: … → gợi ý …
Quà: … gối CS 45×65 (CTKM)
Cần công chúa chốt: … (nếu có)
```
- Cột chưa VAT dùng khi lên ERP hoặc so với đơn MISA (đơn giá MISA = chưa VAT).
- Phí tăng size ghi **một dòng riêng**.

## Tính khối vận chuyển (khi Tú hỏi)
Xem `references/tinh-khoi.md`.

## Bảng giá mới
Tú gửi bảng giá mới (PDF/ảnh) → đọc, so với `bang-gia-2026.md`, báo **chỗ đổi** (sản phẩm · size · cũ → mới)
và ngày áp dụng. Trong phiên dùng bảng mới; nhắc Tú cập nhật skill. PDF gốc thắng nếu lệch.
