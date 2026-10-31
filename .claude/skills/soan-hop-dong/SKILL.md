---
name: soan-hop-dong
description: Soạn hợp đồng và phụ lục cho Nệm Thành Công (NTC) theo 10 file mẫu của Ngọc Tú — HĐ nguyên tắc (cá nhân / doanh nghiệp), HĐ mua bán, HĐ đại lý (cá nhân / doanh nghiệp), Phụ lục số 1, Phụ lục thay đổi thông tin, Phụ lục chính sách NPP, Biên bản thỏa thuận chiết khấu thanh toán; quy trình cấp số HĐ với sổ kế toán; luật riêng của Tú khi check hợp đồng (nơi lưu, đặt tên 3 file). Dùng khi Tú gửi thông tin khách và bảo soạn / lên hợp đồng, phụ lục, biên bản, hoặc check hợp đồng (dùng kèm skill checkhopdong).
---

# Soạn hợp đồng / phụ lục NTC

Đọc `references/luat-chung.md` trước. Chi tiết quy trình + lỗi sẵn có của mẫu: `references/quy-trinh-hop-dong.md`.

## Chọn mẫu (file ở `assets/mau-hop-dong/`, bản đã sửa theo chuẩn KTT 05/10/2026)

| Tú cần | File | Khối Bên B |
|---|---|---|
| HĐ nguyên tắc — công ty / HKD | `hd-nguyen-tac-doanh-nghiep.docx` | bảng 3, 6 dòng: Tên công ty · Địa chỉ · MST · Đại diện · SĐT · Email (đang trống, KHÔNG có dòng Chức vụ) |
| HĐ nguyên tắc — cá nhân | `hd-nguyen-tac-ca-nhan.docx` | bảng 3, 9 dòng: Cửa hàng/Đại lý · Địa chỉ · Chủ cửa hàng · CCCD · Cấp ngày · Nơi cấp · SĐT · Email · MST |
| HĐ mua bán | `hd-mua-ban.docx` | bảng 2 (6×6) = bảng hàng hoá, bảng 3 = chữ ký |
| HĐ đại lý — cá nhân | `hd-dai-ly-ca-nhan.docx` | |
| HĐ đại lý — doanh nghiệp | `hd-dai-ly-doanh-nghiep.docx` | bảng 3: 8 dòng × 3 cột, giá trị ở **cột 3** |
| Phụ lục số 1 — cá nhân | `pl1-dai-ly-ca-nhan.docx` | |
| Phụ lục số 1 — doanh nghiệp | `pl1-dai-ly-doanh-nghiep.docx` | bảng 3, cột 3 |
| Phụ lục thay đổi thông tin (cá nhân → HKD) | `pl-thay-doi-thong-tin.docx` | bảng 3 · 4 · 5 |
| Phụ lục chính sách NPP | `pl-chinh-sach-npp.docx` | chỗ trống nằm trong đoạn văn |
| Biên bản thỏa thuận chiết khấu TT | `bb-thoa-thuan-chiet-khau-tt.docx` | số dạng `…/2026-BBTT-NTC` |

## Các bước
1. **Thông tin vào**: Tú gửi thông tin khách (ảnh CCCD/ĐKKD, tin nhắn) + loại văn bản. Thiếu ô nào → **hỏi**,
   gom câu hỏi một lần. Không viết đại cho kín ô.
2. **Số văn bản**: số HĐ do sổ kế toán sinh (xem quy trình cấp số). Trên điện thoại: hỏi Tú số đã cấp, hoặc
   đọc sổ qua connector Google Drive để gợi ý số kế tiếp — **ghi vào sổ là việc Tú làm**. Số phụ lục độc lập
   số HĐ (HĐ 018/2026/HĐĐL-NTC → PL vẫn 01/2026/PLHĐ-NTC; PL thay đổi TT kế tiếp = 02/2026/PLHĐ-NTC).
3. **Xem chỗ cần điền**: `python scripts/liet-ke-o-vang.py assets/mau-hop-dong/<file>.docx` →
   danh sách ô bôi vàng + khối Bên B trong bảng ở trên. **Chỗ bôi vàng = chỗ thay** (Tú chốt 18/09/2026).
4. **Điền** bằng cách sửa `word/document.xml` (giải nén docx → sửa XML → nén lại). Giữ nguyên định dạng:
   chỉ thay chữ trong run, không đổi kiểu chữ. Điền xong **bỏ tô vàng**; chỉ giữ vàng ở ô còn thiếu dữ liệu.
   Nén lại bằng `zipfile` (đường dẫn trong zip dùng `/`, `[Content_Types].xml` đứng đầu).
5. **Luật bắt buộc** (mỗi lần):
   - Nơi ký luôn **"Tây Ninh"** (21/09/2026), không lấy "Tp Hồ Chí Minh" của mẫu.
   - Thay **toàn bộ dữ liệu khách mẫu còn sót**: NGUYỄN THANH TÂM, ngày 14/07/2026, số 019/020/2026,
     HKD ĐẠI LÝ NỆM THUẦN VIỆT / NGUYỄN HOÀNG THẢO MY (CCCD, MST, SĐT, biển số), HKD TỦ NHỰA MẠNH HÙNG /
     LẠI THỊ DIỄM HƯƠNG. Dò lại cả file sau khi điền, không còn tên nào trong số này.
   - **HĐ đại lý: thời hạn 2 năm** (Tú chọn 22/10/2026; mẫu ghi 1 năm). Khách khác thì hỏi.
   - Phụ lục thay đổi thông tin: cột "Thông tin cập nhật" luôn ghi **giá trị thật**; dòng không đổi thì **chép
     lại giá trị cũ**. **Tuyệt đối không** "Không thay đổi", "Không áp dụng", "N/A" (22/09/2026). Mục I Bên B =
     thông tin theo HĐ đã ký (giá trị CŨ). Khách vẫn là cá nhân → Mục 3 điền chính thông tin cá nhân đó.
   - Khối chữ ký: người ký thật là **PGĐ Lê Văn Quang** (UQ 01/2026/UQ-NTC ngày 01/01/2026) nhưng mẫu in
     "GIÁM ĐỐC" → hỏi Tú trước khi sửa. Điền tên vào dòng trống sẵn trong ô, không thêm dòng (đẩy sang trang trống).
   - Số tiền bằng chữ phải khớp số.
   - Mẫu HĐ mua bán và PL thay đổi TT có **content control khoá** (`<w:lock w:val="contentLocked"/>`) → gỡ thẻ
     lock trước khi sửa.
   - PL thay đổi TT có ô **trống mà dấu kết đoạn tô vàng** → chèn run mới sau `</w:pPr>` rồi gỡ highlight ở pPr.
6. **Soát từng ô** đã điền ngược lại với thông tin Tú gửi (kể cả ô không sửa lần này) rồi mới trả file.
   Mở lại file kiểm tra (đọc XML / python-docx; có LibreOffice thì xuất PDF xem số trang).
7. **Trả file .docx** để Tú tải về. Tên: `<số>.2026.<mã loại>-NTC — <TÊN KHÁCH>.docx`
   (vd `026.2026.HĐNT-NTC — HỘ KINH DOANH VIỆT NHẬT MATTRESS.docx`). Nơi lưu (Tú chốt 01/10/2026):
   `D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Hợp đồng tạm\` — khách có thêm phụ lục thì gom thư mục con tên khách.
   Không tự đẩy sang `HỒ SƠ KHÁCH HÀNG\Đại Lý\<NV>\<khách>\` (chỗ hồ sơ đã hoàn tất).

## Check hợp đồng (dùng skill `checkhopdong` của KTT Uyên + luật riêng của Tú)
Đọc thẳng SKILL.md + references của `checkhopdong`, đừng làm theo trí nhớ. Tú chốt đè lên skill đó (17/10/2026):
- **Nơi lưu**: `D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Hợp đồng tạm\Hợp đồng đã check\<tên khách>\` (thay PROMTAI/01_Draft).
  Trên điện thoại: trả 3 file cho Tú tải, nhắc thư mục này.
- **Tên 3 file** (loại đứng đầu, có dấu, ngắn, số HĐ đổi `/` thành `-`):
  `1. Báo cáo rà soát - <loại HĐ viết tắt> <số HĐ> <đối tác ngắn>.docx` · `2. Hợp đồng đã sửa - ….docx` ·
  `3. So sánh trước sau - ….docx`. Bộ nhiều văn bản → `2a.` `2b.`.
- Ghi `[Điền Nội dung]` / `[Xác nhận lại]` chữ đỏ chỉ khi **rà soát**; khi **soạn** thì hỏi Tú.
- Tô màu ĐÚNG cụm chữ đổi, không tô cả câu. Bảng bị cắt ngang trang → thêm `<w:cantSplit/>`.
- Soát luôn khối chữ ký, số tiền bằng chữ, và điều kiện hỗ trợ trong phụ lục so với đơn thực tế trên ERP
  (Sales Order theo khách). HĐ mua bán từng lần: tra Sales Order theo po_no (ĐH…/BH…) đối chiếu pháp nhân + MST.
- Công cụ trên máy tính (Node): `scripts/sua-docx-to-mau.js` + 2 file ví dụ + `scripts/mau-bao-cao-ra-soat.html`.
  Chi tiết thêm: `references/check-hop-dong-ghi-chu.md`.
