> Chép từ bộ nhớ Claude trên máy tính của Ngọc Tú ngày 31/10/2026. Đường dẫn `C:\…`, `D:\…` là của
> máy tính đó; trên iPad/iPhone thì dữ liệu do Tú gửi kèm. Chữ "anh Tú"/"chị" = công chúa (Tú).

Quy trình Ngọc Tú giao ngày 18/09/2026 (làm lần đầu hôm đó, chạy được):

1. **Nguồn khách hàng:** file `DANH SÁCH HỢP ĐỒNG KHÁCH HÀNG 2026 (1).xlsx`
   (id `1CH_51IaGUApuIKnRQetDvH95cKt2Hssg`, trong Drive `Nệm Thành Công\WORKING\HỒ SƠ KHÁCH HÀNG`).
   6 tab: Hợp đồng kí cá nhân · Phụ lục 01 Cá nhân · Hợp đồng kí doanh nghiệp ·
   Phụ lục 01 Doanh nghiệp · Hợp đồng nguyên tắc-Cá nhân (gid 1525188771) ·
   Hợp đồng nguyên tắc-Doanh nghiệp (gid 1726758049). **Cột A = SỐ HĐ, để trống = chưa cấp số.**
2. **Sổ cấp số:** Google Sheet `NTC Danh mục hợp đồng bán ra`
   (id `1NLRFLD2xoYo7F0aYJobxGYu10MKXy39OjVV1NrrAkGY`, chủ sở hữu là **kế toán** ktnemthanhcong@gmail.com).
   Tab: Đại lý · HĐ Nguyên tắc (gid 1863446417) · HĐ mua bán · Gia công · KH gia công.
   Cột: A STT · B TIỀN TỐ · C KÝ HIỆU · **D SỐ HỢP ĐỒNG = công thức**, chỉ cần điền B ·
   E ngày ký · F từ ngày · G đến ngày · H tên · I MST/CCCD · J ngày cấp · K nơi cấp ·
   L địa chỉ ĐKKD · M người đại diện · P NV kinh doanh.
3. **Soạn HĐ:** mẫu ở `03 Hợp đồng\Hợp đồng mẫu\Nguyên tắc\` —
   `HĐ Nguyên tắc — bản 21.07.2026.docx` = bản **cá nhân/hộ KD**,
   `HĐ Nguyên tắc — ký doanh nghiệp.docx` = bản **doanh nghiệp**.
   **Chỗ bôi vàng trong mẫu = chỗ cần thay thông tin** (Ngọc Tú chốt 18/09/2026).
   Bảng 3 trong file Word là khối BÊN B; bảng 4 ô (3,2) là chỗ ghi tên ký.
4. **Lưu:** bản mới lưu vào `Tủ hồ sơ\HỒ SƠ KHÁCH HÀNG\Đại Lý\Hợp đồng tạm`.
   Đặt tên kiểu `019.2026.HĐNT-NTC — TÊN KHÁCH.docx` (theo nếp file đã ký).

Mẹo kỹ thuật:
- Máy **không có Python**; đọc/ghi Excel và Word bằng **COM qua PowerShell** (Excel 16.0, Word 16.0).
- Tên sheet trong .xlsx bị cắt còn 31 ký tự → `Worksheets.Item("Hợp đồng nguyên tắc-Doanh nghiệp")` lỗi, phải dùng **index**.
- Ghi vào Google Sheet: dùng **Claude in Chrome** (đã đăng nhập), `Ctrl+J` → gõ ô → Enter, gõ giá trị,
  bấm **Delete trước Tab/Enter** để huỷ gợi ý autocomplete. MST/CCCD có số 0 đầu phải gõ `'` phía trước.
- Locale sheet là **dd/mm/yyyy**.

Xem thêm `drive-kd-dai-ly-b2b-layout`, `drive-thao-tac-qua-o-g`.

Bổ sung 21/09/2026 (soạn HĐ Đại lý 018/2026 cho anh Nguyễn Đắc Khởi):
- **Bộ HĐ Đại lý** (khác HĐ Nguyên tắc) nằm ở
  `D:\Ngọc Tú\WORKING\CHỨNG TỪ\[MẪU] HỢP ĐỒNG ĐẠI LÝ\[MẪU] BỘ HỢP ĐỒNG ĐẠI LÝ-Chị Uyên (1)\`
  — `[MẪU] Hợp đồng ĐẠI LÝ.docx` + `[MẪU] Phụ lục HD Đại lý.docx` (bản cá nhân),
  và 2 file `...2026 ... kí doanh nghiệp` cho bản doanh nghiệp.
  Bản soạn xong lưu ở `D:\Ngọc Tú\WORKING\CHỨNG TỪ\HỢP ĐỒNG ĐẠI LÝ ĐÃ SOẠN\<số HĐ> - <TÊN KHÁCH>\`.
- Số phụ lục **độc lập** với số hợp đồng (HĐ 018/2026/HĐĐL-NTC nhưng phụ lục vẫn 01/2026/PLHĐ-NTC).
- Máy **không có pandoc, LibreOffice, Python**. Sửa .docx nhanh nhất: `unzip` bằng Git Bash →
  sửa `word/document.xml` bằng script **Node** (node có sẵn) → đóng gói lại.
- Đóng gói lại **không dùng** `ZipFile::CreateFromDirectory` / `Compress-Archive`:
  PowerShell 5.1 ghi tên entry bằng dấu `\` → Word không mở được. Phải tự tạo entry bằng
  `System.IO.Compression.ZipArchive` và `.Replace('\','/')`, đặt `[Content_Types].xml` lên đầu.
- Ghi file mới vào scratchpad rồi `Copy-Item -Force` sang đích; `Remove-Item` trên đường dẫn
  có dấu tiếng Việt hay bị sandbox chặn.
- Chỗ bôi vàng sau khi điền thì **bỏ tô vàng**; chỉ giữ tô vàng ở ô còn thiếu dữ liệu.
- Kiểm lại bằng Word COM: `ComputeStatistics(2)` = số trang, `(0)` = số từ — mở được là file lành.
- Kế toán có thể **cấp số trước** và điền sẵn ngày ký/thời hạn vào sổ trước khi mình soạn HĐ.
  Nếu ngày trong sổ vênh với ngày chị Tú chốt cho hợp đồng → **trình chị chọn, đừng tự sửa**.
  Chốt 21/09/2026: lần đó chị chọn **sửa sổ theo hợp đồng**.
- Sheet `Đại lý` đang bật bộ lọc (hiện 16/30 hàng) → số dòng trên màn hình không liền mạch.
  Ghi bằng `Ctrl+J` → gõ địa chỉ ô → Enter thì không bị ảnh hưởng.
- Cột N = THƯƠNG HIỆU NỆM THUẦN VIỆT, O = THƯƠNG HIỆU NỆM VIỆT NHẬT (checkbox, gõ `TRUE` để tích).
- Đọc lại giá trị ô mà không cần nhìn màn hình: chạy JS
  `document.querySelector('#t-name-box').value` và `#t-formula-bar-input` .innerText.

Bổ sung 21/09/2026 — LUẬT: **mọi hợp đồng/phụ lục Ngọc Tú giao soạn đều ký tại "Tây Ninh"**
(trụ sở Bên A ở Tây Ninh). Không lấy "Tp Hồ Chí Minh" của file mẫu. Chị chốt 21/09/2026.

Bổ sung 21/09/2026 — phụ lục thay đổi thông tin cá nhân → hộ kinh doanh:
- Mẫu: `[MẪU] PHU LUC THAY DOI THONG TIN HOP DONG - CO SO CA NHAN SANG HO KINH DOANH (1).docx`
  (cùng thư mục bộ HĐ Đại lý). Thư mục mẫu đã đổi tên thành `[MẪU] HỢP ĐỒNG` (bỏ chữ ĐẠI LÝ).
- Đánh số tiếp theo trong cùng hợp đồng: PL số 1 = `01/2026/PLHĐ-NTC`, PL thay đổi TT = `02/2026/PLHĐ-NTC`.
- Trong mẫu này, nhiều ô bảng **trống nhưng dấu kết đoạn bị tô vàng** (`<w:highlight>` nằm
  trong `w:pPr/w:rPr`), không phải run có chữ → script chỉ thay run tô vàng sẽ bỏ sót.
  Phải xử lý riêng: chèn run mới sau `</w:pPr>` rồi gỡ highlight ở pPr.
- Mẫu này đại diện Bên A là **Ông Lê Văn Quang - Phó Giám đốc** (uỷ quyền 01/2026/UQ-NTC
  ngày 01/01/2026), khác hợp đồng gốc (Ông Phạm Văn Bình - Giám đốc). Khối chữ ký trong mẫu
  vẫn in "GIÁM ĐỐC" — mâu thuẫn sẵn có của mẫu, hỏi chị trước khi sửa.

Bổ sung 22/09/2026 — LUẬT khi điền **Phụ lục thay đổi thông tin**:
- Cột "Thông tin cập nhật" luôn ghi **giá trị thật**. Dòng nào không thay đổi thì **chép lại
  giá trị cũ** sang cột cập nhật. **Tuyệt đối không ghi "Không thay đổi" hay "Không áp dụng"**
  ở bất kỳ ô nào — Ngọc Tú bắt lỗi ngày 22/09/2026 (bản Mai Thị Kim Ngân).
- Mục "3. Đơn vị tiếp nhận/cập nhật thông tin giao dịch": nếu khách vẫn là cá nhân (không lập
  hộ kinh doanh) thì điền chính thông tin cá nhân đó, không bỏ trống, không "không áp dụng".
- Mục "I. Thông tin các bên → Bên B" là thông tin **theo hợp đồng đã ký** (giá trị CŨ),
  không phải giá trị mới. Giá trị mới chỉ nằm ở cột cập nhật của Mục II và Mục 3.
- Mẫu chuẩn để đối chiếu: bản Nguyễn Đắc Khởi
  `D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Đại Lý\DIỆU VÂN\Nguyễn Đắc Khởi\02.2026.PLHĐ-NTC ...docx`.
- Hồ sơ khách xếp ở `D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Đại Lý\<NV kinh doanh>\<Tên khách>\`;
  bản chưa xong nằm ở `HỒ SƠ KHÁCH HÀNG\Hợp đồng tạm\<Tên khách>\`.

Bổ sung 01/10/2026 — NGUỒN MẪU CHÍNH THỨC (Tú chốt):
Mọi hợp đồng/phụ lục soạn cho Tú đều lấy form từ
`D:\Ngọc Tú\WORKING\CHỨNG TỪ\[MẪU] HỢP ĐỒNG\`. Tú gửi thông tin khách + nói cần lên loại gì →
chọn đúng form, điền, trả file .docx hoàn chỉnh (đúng chính tả, giữ nguyên định dạng).
10 file, chọn như sau:

| Cần lên | File mẫu | Khối Bên B |
|---|---|---|
| HĐ nguyên tắc — công ty/HKD | `[MẪU] HĐ NGUYÊN TẮC\[MẪU] HĐ NGUYÊN TẮC - Kí Doanh nghiệp.docx` | bảng 3, 6 dòng: Tên công ty·Địa chỉ·MST·Đại diện·SĐT·Email (đang trống) |
| HĐ nguyên tắc — cá nhân | `[MẪU] HĐ NGUYÊN TẮC\[MẪU] HĐ NGUYÊN TẮC 21.07.26.docx` | bảng 3, 9 dòng: Cửa hàng/Đại lý·Địa chỉ·Chủ cửa hàng·CCCD·Cấp ngày·Nơi cấp·SĐT·Email·MST |
| HĐ mua bán | `[MẪU] HĐ MUA BÁN.sử dung\[MẪU] - HĐ MUA BÁN.docx` | bảng 2 (6×6) là bảng hàng hoá, bảng 3 chữ ký |
| HĐ đại lý — cá nhân | `[MẪU] BỘ HỢP ĐỒNG ĐẠI LÝ-Chị Uyên (1)\[MẪU] Hợp đồng ĐẠI LÝ.docx` | |
| HĐ đại lý — doanh nghiệp | `…\[MẪU]HDDL-NTC 2026 Hợp đồng kí doanh nghiệp.docx` | bảng 3 là 8 dòng × **3 cột**, giá trị nằm ở **cột 3** |
| Phụ lục số 1 — cá nhân | `…\[MẪU] Phụ lục HD Đại lý.docx` | |
| Phụ lục số 1 — doanh nghiệp | `…\[MẪU]PLHD-NTC 2026 Phụ lục số 1 kí Doanh nghiệp.docx` | bảng 3, cột 3 |
| Phụ lục thay đổi thông tin | `…\[MẪU] PHU LUC THAY DOI THONG TIN HOP DONG - CO SO CA NHAN SANG HO KINH DOANH (1).docx` | bảng 3·4·5 (xem luật 22/09 ở trên) |
| Phụ lục chính sách NPP | `…\[MẪU] PHỤ LỤC NPP.docx` | không có bảng điền, chỗ trống nằm trong đoạn văn |
| Biên bản chiết khấu thanh toán | `[MẪU] BIÊN BẢN - VĂN BẢN\[MẪU] BB THOẢ THUẬN CHIẾT KHẤU TT.docx` | số dạng `…/2026-BBTT-NTC` |

**Lỗi sẵn có của mẫu — phải xử lý mỗi lần soạn, đừng chép nguyên:**
- **05/10/2026 Tú cho sửa 7 mẫu theo chuẩn skill KTT** (bản cũ ở `CHỨNG TỪ\_bỏ\[MẪU] HỢP ĐỒNG - bản trước 05.10.2026\`):
  2 HĐ đại lý (lãi 0,03%, bỏ "đơn phương chấm dứt" ở 5.2, thêm 5.5 hóa đơn, 13.2 Tòa án TP.HCM; bản cá nhân đổi
  địa danh sang Tây Ninh) · PL HĐ đại lý cá nhân (Tây Ninh) · PL NPP (lãi 0,03%, bỏ "đơn phương chấm dứt", nhãn MST) ·
  PL thay đổi TT (thêm III.6, nhãn MST) · HĐ mua bán (số HĐMB, Tòa án TP.HCM, thêm câu hóa đơn) · HĐNT cá nhân (số HĐNT).
  Chi tiết chuẩn ở `skill-checkhopdong-ra-soat-hd`. Dữ liệu khách mẫu (NGUYỄN THANH TÂM, ngày 14/07…) **vẫn còn**, vẫn phải thay mỗi lần soạn.
- `[MẪU] HĐ NGUYÊN TẮC 21.07.26.docx`: còn nguyên dữ liệu thật HKD TỦ NHỰA MẠNH HÙNG / LẠI THỊ DIỄM HƯƠNG
  (số HĐ đã sửa thành HĐNT ngày 05/10/2026).
- `[MẪU] - HĐ MUA BÁN.docx`: số HĐ đã thống nhất **HĐMB** (05/10/2026).
- `[MẪU] Hợp đồng ĐẠI LÝ.docx` + `[MẪU] Phụ lục HD Đại lý.docx`: còn số `019/2026/HĐĐL-NTC`,
  `01/2026/PLHĐ-NTC`, ngày **14/07/2026 Tp Hồ Chí Minh**, bên B **NGUYỄN THANH TÂM**.
  (Nơi ký luôn phải là **Tây Ninh** — luật 21/09/2026.)
- 2 file `…kí doanh nghiệp` / `…Phụ lục số 1 kí Doanh nghiệp`: còn `020/2026/HĐĐL-NTC`,
  **HỘ KINH DOANH ĐẠI LÝ NỆM THUẦN VIỆT / NGUYỄN HOÀNG THẢO MY** kèm CCCD, MST, SĐT, biển số.
- `[MẪU] - HĐ MUA BÁN.docx` và `[MẪU] PHU LUC THAY DOI THONG TIN…docx` mỗi file có **1 content
  control khoá** (`<w:lock w:val="contentLocked"/>`, tag `goog_rdk_*`). Word COM sẽ báo
  *"You are not allowed to edit this selection because it is protected"*. Gỡ thẻ lock trong
  `word/document.xml` rồi đóng gói lại trước khi sửa.

**Nếp làm:** điền xong thì bỏ tô vàng; ô không đổi thì chép lại giá trị cũ, không ghi
"không thay đổi"; thiếu dữ liệu thì hỏi Tú, không viết đại. Soát lại **từng ô** ngược với
thông tin khách Tú gửi rồi mới trả file. Đóng hết tiến trình WINWORD ẩn sau khi chạy COM.

Bổ sung 01/10/2026 — LUẬT: **mọi hợp đồng/phụ lục Tú nhờ soạn đều lưu về**
`D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Hợp đồng tạm\` (Tú chốt 01/10/2026).
Đặt tên phẳng trong thư mục đó: `<số>.2026.<mã loại>-NTC — <TÊN KHÁCH>.docx`
(vd `026.2026.HĐNT-NTC — HỘ KINH DOANH VIỆT NHẬT MATTRESS.docx`). Khách nào có thêm
phụ lục thì gom vào thư mục con tên khách ngay trong `Hợp đồng tạm`.
Không tự đẩy sang `HỒ SƠ KHÁCH HÀNG\Đại Lý\<NV>\<khách>\` — đó là chỗ hồ sơ đã hoàn tất.

Bổ sung 22/10/2026 (soạn HĐĐL 026/2026 + PL 01 cho Lại Trần Phương Thùy, Đà Nẵng):
- **Thời hạn HĐ đại lý: Tú chọn 2 năm** (ký 20/09/2026 → 19/09/2028), giống các HĐ 022–025.
  Mẫu vẫn ghi 1 năm → lần sau đề xuất 2 năm, khách nào khác thì hỏi.
- Đọc sổ cấp số: **đừng mở link `gviz/tq?tqx=out:csv`** trên thanh địa chỉ (Chrome tải file
  về Downloads). Mở trang `/edit` rồi chạy `fetch('.../gviz/tq?tqx=out:json&gid=0&range=A28:Q29')`
  trong trang. Dòng CSV ≠ số dòng sheet (tiêu đề gộp) → kiểm ô bằng `#t-name-box` trước khi ghi.
- Phụ lục số 1 có điều khoản riêng (trả nợ nhiều đợt, hỗ trợ bảng hiệu bằng chuyển khoản):
  sửa thẳng đoạn 1.1 / 1.2, thêm dòng "+ Hình thức · Điều kiện · Thời điểm" ngay dưới đoạn bảng hiệu;
  ngưỡng đơn đầu tiên ở Điều 2 để bằng ngưỡng điều kiện hỗ trợ.

Lưu ý mẫu `[MẪU] HĐ NGUYÊN TẮC - Kí Doanh nghiệp.docx`: khối Bên B chỉ có 6 dòng
(Tên công ty · Địa chỉ · Mã số thuế · Đại diện · Số điện thoại · Email) — **không có dòng
"Chức vụ"**. Thông tin chức vụ khách gửi (vd "Chủ hộ kinh doanh") không có ô để điền,
hỏi Tú nếu muốn ghép vào ô Đại diện.
