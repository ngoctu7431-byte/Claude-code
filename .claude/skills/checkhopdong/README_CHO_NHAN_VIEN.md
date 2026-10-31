# Hướng dẫn dùng skill rà soát hợp đồng

## Skill này làm gì

Rà soát hợp đồng, phụ lục, biên bản thanh lý của 3 công ty **Nệm Thành Công · Thuần Việt Global · Thuần Việt Digital** dưới góc nhìn kế toán trưởng, rồi xuất ra báo cáo và file hợp đồng đã chỉnh.

---

## Cách dùng

### Bước 1 — Cài skill

Giải nén rồi copy thư mục `checkhopdong` vào:

```
C:\Users\<tên người dùng Windows>\.claude\skills\checkhopdong\
```

Nếu chưa có thư mục `.claude\skills` thì tạo mới. Sau khi copy, cấu trúc phải là:

```
.claude\skills\checkhopdong\
    ├── SKILL.md
    ├── README_CHO_NHAN_VIEN.md
    └── references\   (9 file)
```

Cài xong, mở lại Claude cho nhận skill.

> **Không cần khai báo đường dẫn.** Skill tự tìm thư mục hồ sơ `PROMTAI` trên OneDrive công ty theo tên đăng nhập Windows của máy. Chỉ khi không tìm được nó mới hỏi một lần.

### Bước 2 — Gửi hợp đồng

Kéo file `.docx` hoặc `.pdf` vào Claude rồi gõ một câu là đủ:

```
Rà soát hợp đồng này giúp tôi
```

Skill tự nhận ra công ty nào, mua vào hay bán ra, rồi làm theo quy trình.

### Bước 3 — Chọn chế độ (không bắt buộc)

| Gõ | Nghĩa | Nhận được |
|---|---|---|
| *(không gõ gì)* | Mặc định | Báo cáo + file hợp đồng đã chỉnh + báo cáo so sánh |
| `chế độ A` | Rà soát nhanh | Chỉ báo cáo rà soát |
| `chế độ C` | Chốt trình ký | Thêm phiếu trình ký 1 trang + ghi nhật ký |
| `làm bảng gửi đối tác` | | Bảng đề nghị điều chỉnh để gửi nhà cung cấp / khách hàng |

---

## Anh chị nhận được gì

| Sản phẩm | Nội dung |
|---|---|
| **Báo cáo rà soát** | Bảng 9 cột, đặt **nội dung theo mẫu cạnh hiện trạng hợp đồng** để so ngang, có sẵn **cột trống để Kế toán trưởng ghi phản hồi**. Mỗi lỗi đều có sẵn câu sửa để dán thẳng vào hợp đồng |
| **File hợp đồng đã chỉnh** | Bản Word đã sửa, tô màu đúng chỗ thay đổi |
| **Báo cáo so sánh** | Bảng trước – sau, chỉ ghi thay đổi về nội dung |

Bốn mức độ: **BẮT BUỘC SỬA** (đỏ) · **NÊN SỬA** (cam) · **CÓ THỂ GIỮ** (xanh) · **CHỈ HÌNH THỨC** (xám).

---

## Bảy việc phải trình Kế toán trưởng

Skill sẽ tự dừng và ghi cảnh báo, nhưng anh chị cũng cần biết:

1. Thay đổi **giá trị hợp đồng**
2. Thay đổi **điều khoản thanh toán, thời hạn thanh toán**
3. Thay đổi **điều khoản phạt, bồi thường, chấm dứt**
4. Thay đổi **số tài khoản ngân hàng** khác bảng chuẩn
5. Hợp đồng giữa **2 công ty trong hệ thống**
6. Hợp đồng dùng **mẫu chưa có** trong thư mục mẫu đã phê duyệt
7. Có điều khoản bị đánh mức **BẮT BUỘC SỬA**

Gặp mấy trường hợp này: cứ để skill làm xong báo cáo, rồi **gửi Kế toán trưởng duyệt trước khi phản hồi đối tác**.

---

## Bốn điều tuyệt đối không làm

1. **Không xóa file** — kể cả bản nháp. Muốn dọn thì xin phép Kế toán trưởng từng lần.
2. **Không ghi đè file đã có** — luôn lưu bản mới.
3. **Không tự lưu vào thư mục hồ sơ final** khi Kế toán trưởng chưa xác nhận "đây là bản cuối cùng".
4. **Không tạo folder mới trùng với folder đã có** của cùng một đối tác.

---

## Khi skill hỏi

Skill được thiết kế để hỏi **tối đa 3 câu, gộp một lần ở đầu**. Nếu thấy nó hỏi nhiều hơn hoặc hỏi rải rác, nghĩa là thiếu dữ liệu chuẩn — báo lại Kế toán trưởng để bổ sung vào thư mục `references`, đừng trả lời thủ công mãi.

---

## Khi kết quả chưa đúng

Skill dựa trên dữ liệu trong thư mục `references`. Sai ở đâu thì sửa đúng file đó, đừng sửa tay từng lần:

| Sai chỗ nào | Sửa file |
|---|---|
| Thông tin công ty, địa chỉ, email | `references/01-cong-ty.md` |
| Tài khoản ngân hàng | `references/02-tai-khoan.md` |
| Ngưỡng điều khoản | `references/03-chuan-dieu-khoan.md` |
| Hình thức trình bày | `references/04-the-thuc-dau-ra.md` |
| Cách đọc công nợ khi thanh lý | `references/05-cong-no-131-331.md` |
| Căn cứ pháp luật | `references/06-can-cu-phap-ly.md` |
| Đặt tên file, thư mục lưu | `references/07-luu-tru-dat-ten.md` |
| Phân quyền | `references/08-phan-quyen-nhan-vien.md` |
| Danh mục mẫu | `references/09-mau-da-phe-duyet.md` |

Sửa file tham chiếu = sửa một lần, dùng mãi.
