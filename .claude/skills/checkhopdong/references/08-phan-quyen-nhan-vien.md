# 08 · Phân quyền nhân viên

Người dùng skill này là **nhân viên kế toán**. Kế toán trưởng là kế toán trưởng, người duyệt cuối.

---

## Nhân viên ĐƯỢC tự làm

| Việc |
|---|
| Rà soát và lập báo cáo SP1 |
| Lập báo cáo so sánh SP3 |
| Chỉnh lỗi chính tả, trình bày, thể thức trong file SP2 |
| Chỉnh tên công ty, MST, địa chỉ cho khớp dữ liệu chuẩn tại `01-cong-ty.md` |
| Bổ sung tài khoản ngân hàng theo bảng tra tại `02-tai-khoan.md` |
| **Đề xuất** sửa điều khoản theo chuẩn tại `03-chuan-dieu-khoan.md` — chỉ đề xuất, không tự chốt |
| Ghi dòng nhật ký SP6 |

---

## Bắt buộc TRÌNH CHỊ UYÊN — không được tự quyết

| Trường hợp |
|---|
| Thay đổi **giá trị hợp đồng** |
| Thay đổi **điều khoản thanh toán, thời hạn thanh toán** |
| Thay đổi **điều khoản phạt, bồi thường, chấm dứt** |
| Thay đổi **số tài khoản ngân hàng** khác bảng tra |
| Hợp đồng giữa **2 công ty trong hệ thống** (giao dịch liên kết) |
| Hợp đồng dùng **mẫu chưa có** trong `02_Mau_da_phe_duyet` |
| Văn bản có điều khoản bị đánh mức **BẮT BUỘC SỬA** |
| Hợp đồng do **ông Lê Văn Quang** ký, giá trị **trên 500.000.000 đồng** |
| Đối tác nhất quyết dùng **trọng tài VIAC** thay vì Tòa án tại TP.HCM |

Khi gặp các trường hợp trên: **vẫn hoàn thành báo cáo SP1 đầy đủ**, nhưng ghi rõ ở đầu báo cáo:

> "⚠️ CẦN TRÌNH KẾ TOÁN TRƯỞNG TRƯỚC KHI PHẢN HỒI ĐỐI TÁC — lý do: [nêu lý do]"

Không tự gửi SP4 cho đối tác, không tự lưu vào hồ sơ final.

*(Ghi chú: hợp đồng do **Giám đốc** ký thì không đặt ngưỡng giá trị. Ngưỡng 500 triệu **chỉ áp dụng cho ông Lê Văn Quang** và là quy định nội bộ, không phải khiếm khuyết pháp lý — xem `03-chuan-dieu-khoan.md`.)*

---

## Chỉ Kế toán trưởng được quyết

| Việc |
|---|
| Xác nhận **"đây là bản cuối cùng"** trước khi lưu vào `03_Ho_so_final` |
| Công nhận một file là **mẫu đã phê duyệt** |
| Cho phép **xóa** bất kỳ file nào |
| Xác nhận hồ sơ phê duyệt đã chốt, và cho phép dọn folder `01_Trao_doi_Phe_duyet` |
| Cho phép **ghi đè** lên file đã có |
| Thay đổi bất kỳ ngưỡng điều khoản nào tại `03-chuan-dieu-khoan.md` |
| Quyết định với các điều khoản nhóm 👁️ *"theo từng hợp đồng"* — nhân viên chỉ trích ra, không tự chốt |

---

## Bốn điều tuyệt đối không làm

1. **Không xóa file** — kể cả bản nháp, kể cả khi nhân viên yêu cầu. Muốn dọn bản nháp thì theo đúng quy trình 5 bước tại `07-luu-tru-dat-ten.md`.
2. **Không ghi đè file đã có** — luôn lưu bản mới.
3. **Không bịa căn cứ pháp luật.**
4. **Không suy đoán khi thiếu dữ liệu** — ghi rõ thiếu gì.

---

## Dữ liệu nhân viên không được xem

Kế toán trưởng đã chốt: nhân viên **không xem** danh sách đầy đủ tài khoản ngân hàng của 3 công ty và hạn mức ký.

- Skill chỉ cung cấp **tài khoản cần dùng theo từng loại hợp đồng** tại `02-tai-khoan.md`, không liệt kê toàn bộ tài khoản.
- Danh sách đầy đủ nằm ở `_CHI_UYEN_ONLY\du-lieu-han-che.md` — **không phát kèm** khi gửi skill cho nhân viên.
- Nhân viên hỏi tài khoản khác ngoài bảng tra → trả lời: *"Nội dung này cần Kế toán trưởng xác nhận."* Không liệt kê.
