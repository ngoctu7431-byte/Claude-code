> Chép từ bộ nhớ Claude trên máy tính của Ngọc Tú ngày 31/10/2026. Đường dẫn `C:\…`, `D:\…` là của
> máy tính đó; trên iPad/iPhone thì dữ liệu do Tú gửi kèm. Chữ "anh Tú"/"chị" = công chúa (Tú).

Chỉ ảnh hưởng hàng **Việt Nhật** (Thuần Việt dùng chung một bảng). Cách dùng: `kiem-gia-don-hang-theo-bang-gia`.

**Giai đoạn đầu (chốt 30/09/2026): miền do anh Tú báo là chuẩn — ERP chỉ để đối chiếu.**
Anh chưa chắc miền gán trên ERP có đúng không. Nên mỗi lần anh gửi đơn kèm miền:
1. Dùng **miền anh báo** để lấy giá, kể cả khi ERP ghi khác.
2. Tra ERP ngay: Customer `default_price_list` ("Giá đại lý - Miền Nam/Bắc/Trung"), tìm bằng
   `mcp__0f3084c7-...__list_documents` (doctype Customer, lọc `customer_name` like). Ngày 30/09/2026 có 133 khách đã gán.
3. **Báo anh một dòng ngay trong câu trả lời**: ERP ghi miền gì → ✅ khớp / ❌ lệch (ERP ghi X, anh báo Y) /
   ⚠️ ERP chưa gán / ⚠️ không tìm thấy khách. Lệch thì **anh tự sửa ERP** — em không tự sửa Customer.
4. Ghi/cập nhật dòng khách vào sổ bên dưới (miền anh báo + kết quả đối chiếu ERP + ngày).
Anh quên báo miền → tra sổ này trước; khách có trong sổ thì dùng luôn nhưng nói rõ "theo sổ, ghi ngày …";
không có trong sổ → hỏi anh, **không** tự lấy miền trên ERP.
Khi nào anh bảo "ERP đã chuẩn" thì mới chuyển sang tra ERP trước.

**Why:** hai bên mới làm task này, anh cần thấy chỗ ERP gán sai miền để sửa dần.

Cẩn thận: ERP có khách **trùng tên nhưng khác miền** (30/09/2026): "HỘ KINH DOANH TRẦN NHÃ PHƯƠNG" = Bắc,
"… - 1" = Trung; "Nguyễn Quốc Linh" = Nam, "… - 1" = Trung. Gặp tên trùng → hỏi anh là khách nào.
Tên Zalo có thể khác tên ERP — ghi cả hai khi biết.

Sổ bổ sung:
| Khách (tên ERP / tên hay gọi) | Nơi | Miền anh báo | ERP ghi | Khớp? | Ghi ngày | Nguồn |
|---|---|---|---|---|---|---|
| Bá Trung | Đà Nẵng | Trung | chưa tra | — | 28/09/2026 | kiểm đơn ĐH03108 |
| MAI THỊ KIM NGÂN (A. Tài Việt Nhật - 0708885677) / "Mai Thị Kim Ngân" | — | Nam | "Giá riêng theo khách - TC" (có 21 giá riêng từ 08/09/2026, vd NA10-8 4.937.500 chưa VAT, thấp hơn bảng Nam) | ⚠️ không phải bảng miền | 30/09/2026 | báo giá đơn ảnh |
| HỘ KINH DOANH 608 AN PHÁT (?) / chat "608 An Lộc Phát" | — | Bắc | chưa gán | ⚠️ ERP chưa gán; tên ERP thiếu chữ "Lộc" — chưa xác nhận cùng khách | 30/09/2026 | báo giá đơn chat |
| Zalo "Nệm Việt Nhật Buôn Ma Thuột Đắk Lắk" (tên ERP chưa rõ) | Buôn Ma Thuột, Đắk Lắk | Trung | chưa tra | — | 26/10/2026 | báo giá đơn Zalo 26/10 |
| Zalo "Tiên Nguyễn" (tên ERP chưa rõ) | — | Trung | chưa tra | — | 16/10/2026 | báo giá đơn Grey + TV latex |
| CÔNG TY TNHH NỆM THẢO NGUYÊN (MST 0318844615, Bà Điểm HCM; đơn ĐH03221 tính giá Nam) — ⚠️ khác "Hộ Kinh Doanh Nệm Thảo Nguyên" (066302012102, ERP "Giá riêng theo khách") | HCM | Nam (theo ERP + ĐH03221, Tú chưa nói miền) | Nam | ✅ | 12/10/2026 | báo giá |
| Nguyễn Thị Thu Hương (MISA mã 083185020028, Bình Đại, Vĩnh Long; gửi chành Tám Lệ) | Vĩnh Long | Trung | không tìm thấy trên ERP (tên/MST) | ⚠️ | 08/10/2026 | ĐH03269 |
| HỘ KINH DOANH HUỲNH THẾ HẬU / Zalo "Phi Trần" | — | Trung | Trung | ✅ | 02/10/2026 | báo giá đơn Zalo |
| Nguyễn Hồng Thắng (MISA mã 049098010826, tên MISA "HỘ KINH DOANH NỆM VIỆT NHẬT - NỆM THUẦN VIỆT"; Zalo "Nệm Thuần Việt - Việt Nhật (Ng Hồng Thắng)") | Pleiku, Gia Lai | Trung | Trung | ✅ | 01/10/2026 | lên ĐH MISA |
| Hoàng My – đại lý Quảng Ngãi (Zalo "Nệm Thuần Việt - Hoàng My (Quảng Ngãi)"; ERP có "HỘ KINH DOANH NỆM THUẦN VIỆT QUẢNG NGÃI"; MISA mã 051302000333, người nhận Nguyễn Hoàng Thảo My) | Quảng Ngãi | Trung | Trung | ✅ | 01/10/2026 | lên ĐH MISA |
| HUỲNH TẤN NHÂN (ERP có 2 bản: "HUỲNH TẤN NHÂN" và "HỘ KINH DOANH NỆM VIỆT NHẬT - HUỲNH TẤN NHÂN", cùng SĐT 0967954750) / Zalo "Nệm Việt Nhật - Nệm Thuần Việt - Cần Đước", chat ghi "21 cần đước" | Cần Đước | Nam | Nam (cả 2) | ✅ | 01/10/2026 | lên ĐH MISA thử |
| HỘ KINH DOANH NỆM VIỆT NHẬT - LÊ NGUYỄN QUANG ĐẠT / Zalo "Nệm Thuần Việt - Việt Nhật (Quang Đạt)" | — | Trung | Trung | ✅ | 30/09/2026 | báo giá đơn Zalo |
| HỘ KINH DOANH NỆM VIỆT NHẬT - NGUYỄN HỮU THẢO / Zalo "Nệm Thắng Lợi - Chính Hãng - Anh Hữu Thảo" — **Nano gấp chỉ +100.000** (Sora gấp +150.000), chốt 08/10/2026; **chỉ mua hàng Việt Nhật → "Cstn" = Natural (NA…)**, chốt 18/10/2026 | — | Nam | Nam | ✅ | 30/09/2026 | báo giá đơn Zalo |
