> Chép từ bộ nhớ Claude trên máy tính của Ngọc Tú ngày 31/10/2026. Đường dẫn `C:\…`, `D:\…` là của
> máy tính đó; trên iPad/iPhone thì dữ liệu do Tú gửi kèm. Chữ "anh Tú"/"chị" = công chúa (Tú).

Tú đưa ngày 01/10/2026, bảo "đọc và học". Bộ skill `checkhopdong` (bản 24/09/2026, của Kế toán trưởng Uyên):
`D:\CLAUDE\Check hợp đồng\checkhopdong\` — `SKILL.md` + `references\01…09`. Có thêm `Checkhopdong.zip` và
`HUONG_DAN_CAI_DAT_CHECKHOPDONG.docx`. **Đã cài 17/10/2026** (Tú bảo "cài đi") vào
`C:\Users\admin\.claude\skills\checkhopdong\` — chép nguyên 11 file, không sửa. Bản ở ổ D: là bản gốc;
KTT gửi bản mới thì chép đè cả hai chỗ.

Dùng khi: Tú nhờ "check / rà soát hợp đồng", hoặc soát lại HĐ/phụ lục mình vừa soạn trước khi gửi khách.
Đọc thẳng SKILL.md và references, đừng làm theo trí nhớ. Ý chính:
- Nhận diện công ty bằng **MST**: NTC 1102015078 · TVG 0318692955 · TVD 0318733601. Hai bên đều trong hệ thống → dừng, trình KTT.
- Mặc định chế độ B → 3 file: báo cáo soát 9 cột (SP1) · bản HĐ đã sửa tô màu (SP2) · so sánh trước–sau (SP3).
- 4 mức: BẮT BUỘC SỬA · NÊN SỬA · CÓ THỂ GIỮ · CHỈ HÌNH THỨC. Hỏi tối đa 3 câu, gộp một lần ở đầu.
- Chuẩn bán ra (NTC): TK **MB 3192384679321** (gia công thì 0000711892658) · lãi chậm trả **0,03%/ngày** ·
  phạt ≤ 8% · tranh chấp **Tòa án nhân dân có thẩm quyền tại TP.HCM** (kể cả NTC) · có điều xuất hóa đơn GTGT
  "theo đúng quy định pháp luật" (Điều 5.5 mẫu mới) · không tự động gia hạn · phụ lục phải dẫn số + ngày HĐ gốc.
- Anh Lê Văn Quang ký hợp lệ theo UQ 01/2026/UQ-NTC; HĐ > 500 triệu chỉ là "cần trình duyệt nội bộ", không phải sai thẩm quyền.
- Skill bảo ghi chỗ thiếu là `[Điền Nội dung]` / `[Xác nhận lại]` chữ đỏ đậm — chỉ áp dụng khi **rà soát**;
  khi **soạn** HĐ cho Tú thì vẫn theo luật của Tú: thiếu dữ liệu thì hỏi (xem `quy-trinh-cap-so-hop-dong-va-soan-hd`).
- **LUẬT LƯU (Tú chốt 17/10/2026): check xong thì lưu vào
  `D:\Ngọc Tú\WORKING\HỒ SƠ KHÁCH HÀNG\Hợp đồng tạm\Hợp đồng đã check\`** — thay cho `PROMTAI`/`01_Draft`
  của skill (máy Tú không có PROMTAI). Đừng hỏi lại nơi lưu. Mỗi khách một thư mục con tên khách, trong đó để
  cả 3 file (báo cáo soát · bản đã sửa · so sánh trước–sau). Không ghi đè file gốc, không lưu vào `Đại Lý\<NV>\`.
- **LUẬT ĐẶT TÊN (Tú chốt 17/10/2026)** — thay cho quy tắc tên file trong `07-luu-tru-dat-ten.md` của skill.
  Loại file đứng ĐẦU, có số thứ tự, viết có dấu, tên ngắn:
  `1. Báo cáo rà soát - <loại HĐ viết tắt> <số HĐ> <tên đối tác ngắn>.docx` ·
  `2. Hợp đồng đã sửa - …docx` · `3. So sánh trước sau - …docx`
  (vd `1. Báo cáo rà soát - HĐVC 04-2026 Nam Trung Bắc.docx`). Số HĐ thay `/` bằng `-`.
  **Why:** tên kiểu skill (`04-2026-NTB-NTC 2026 HDMV NTC_… - Bao cao…`) dài, Explorer cắt mất đuôi → Tú tưởng 3 bản trùng.
  Bộ nhiều văn bản (HĐ + phụ lục) thì bản đã sửa đánh `2a.` `2b.` (vd 20/10/2026 bộ Viễn Đông Vinh).
- **Công cụ** ở `C:\Claude Code\routines\checkhopdong\`: `sua-docx-to-mau.js` (Node — sửa thẳng document.xml của
  file gốc, giữ định dạng, tô màu ĐÚNG cụm đổi bằng `replaceParts` với phần "keep"; chèn khối chú giải màu),
  `vi-du-sua-HDDL-Vinh.js` (cách gọi), `mau-bao-cao-ra-soat.html` (khung báo cáo 9 cột → Word COM → docx).
  Đừng tô cả câu khi chỉ đổi vài chữ (lỗi đã gặp 20/10/2026). Thư mục nháp scratchpad có thể bị dọn giữa phiên.
- Soát luôn: **khối chữ ký** (mẫu HĐ đại lý ghi "GIÁM ĐỐC", thiếu tên — người ký thật là PGĐ Lê Văn Quang),
  **số tiền bằng chữ**, và **điều kiện hỗ trợ trong phụ lục so với đơn thực tế trên ERP** (Sales Order theo
  customer). Chèn tên người ký: xem `vi-du-sua-HDDL-PhuongThuy-chen-ten-ky.js` — điền vào dòng trống sẵn trong ô,
  không thêm dòng mới (thêm dòng làm dài ô → đẩy sang trang trống). Kiểm số trang bản sửa = bản gốc (22/10/2026).
- HĐ mua bán từng lần: tra **Sales Order theo po_no (ĐH…/BH…)** trên ERP để đối chiếu **pháp nhân + MST + ngày giao**
  với Bên B trong HĐ. Ca Manto 22/10/2026: HĐ 08 ghi "TNHH THƯƠNG MẠI MANTO HOTEL 0319575877" nhưng ĐH02930 là
  "TNHH MANTO HOTEL 0319541324" — hai pháp nhân khác nhau. HĐ mua lại hàng mình vừa bán → hỏi KTT mua lại hay trả hàng.
  Bảng hàng bị cắt ngang trang sau khi chèn chú giải → thêm `<w:cantSplit/>` cho các dòng bảng.
- HĐ vận chuyển **mẫu của hãng lớn** (Viettel Post 26/10/2026): soi kỹ cụm bồi thường — "giá vốn chứng minh bằng
  hóa đơn mua vào" (NTC tự sản xuất → không có), "rủi ro không chuyển cho bên vận chuyển", "chỉ đền phần bảo hiểm
  không trả" + buộc NTC mua bảo hiểm; quyền cầm giữ hàng; tòa án ở Hà Nội. File `.doc` → mở bằng Word COM, SaveAs2
  docx vào nháp rồi sửa; bản đã sửa lưu .docx.
- NTC đã có HĐ **bưu chính/COD** với Viettel Post số 842648/04/24/VTPost-HĐCOD (25/04/2024, Tổng GĐ ký, không thời
  hạn) — phạm vi là bưu gửi, bồi thường theo mức giới hạn bưu chính của VTP. Bao xe nguyên chuyến từng được "căn cứ"
  vào HĐ này (BBNT 01/VTPost-HHMXT17712, T03/2026, Tây Ninh–Khánh Hòa 25tr) nhưng HĐ không có điều khoản bao xe →
  bao xe nên đi theo HĐ nguyên tắc vận chuyển hàng hóa riêng (bản VTP CN Tây Ninh đã soát 26/10/2026).
  PDF scan: máy có **PyMuPDF** (`import pymupdf`) → đổi trang sang PNG rồi đọc ảnh (Word không mở được PDF).
- Skill viết cho nhân viên kế toán; "trình chị Uyên" trong skill = việc Tú không tự chốt được.

HĐ **vận chuyển** (NTC thuê chành = mua vào dịch vụ): skill không có mẫu duyệt → luôn "cần trình KTT". Dùng
`VẬN CHUYỂN\Chành xe Anh Tèo-Bảo An Phát\09072026 2026 HDVC NTC_Bao An Phat Final.docx` (+ file "Bao cao noi dung
dieu chinh…gui NCC") làm chuẩn tham khảo câu chữ (đơn giá theo báo giá, phát sinh phải xác nhận trước, hồ sơ thanh
toán, bồi thường + cấn trừ, vận chuyển phụ, bất khả kháng). Riêng tranh chấp: bản đó ghi "Tòa án nơi Bên A đặt trụ
sở" — lệch chuẩn hiện hành, phải theo TP.HCM. Đã check lần đầu: HĐVC 04/2026/NTB-NTC Chành Bồ Đề (17/10/2026).
Cách làm file: viết HTML → Word COM mở, chỉnh khổ/lề/số trang → SaveAs2 docx (máy không có python-docx). Soát
bố cục bằng `Pages.Item(n).EnhMetaFileBits` → PNG; chữ trên nền trắng trong ảnh trông như in đậm là ẢO, kiểm
`Font.Bold` mới chắc.

Phát hiện 01/10/2026: 2 mẫu HĐ đại lý của Tú trong `D:\Ngọc Tú\WORKING\CHỨNG TỪ\[MẪU] HỢP ĐỒNG\[MẪU] BỘ HỢP ĐỒNG ĐẠI LÝ-Chị Uyên (1)\`
(`[MẪU] Hợp đồng ĐẠI LÝ.docx`, `[MẪU]HDDL-NTC 2026 Hợp đồng kí doanh nghiệp.docx`, sửa lần cuối 10/09/2026) là **bản trước
24/09/2026**: Điều 5.2 còn 0,05%/ngày, Điều 13.2 "Tòa án có thẩm quyền" chung chung, chưa có Điều 5.5 hóa đơn.
→ **05/10/2026 Tú bảo sửa các mẫu theo skill — đã sửa 7 file**, xem `quy-trinh-cap-so-hop-dong-va-soan-hd`.
Còn lệch chuẩn, chờ Tú quyết (đụng điều khoản thanh toán/thời hạn → skill bắt trình KTT): HĐ mua bán đặt cọc 30%
(chuẩn bán từng lần ≥ 50%) · 2 HĐ nguyên tắc có "tự động gia hạn từng năm" (chuẩn: không, ký phụ lục gia hạn) và
cho "thanh toán tiền mặt", không ghi TK MB của Bên A.
Câu III.6 của PL thay đổi TT là em tự viết theo ý skill tả (skill không chép nguyên văn) — nếu KTT có câu chuẩn thì thay.
