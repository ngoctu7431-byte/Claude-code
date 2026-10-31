# 04 · Thể thức trình bày và quy cách sản phẩm đầu ra

Có **hai bộ thể thức khác nhau**, không được lẫn lộn:

- **Nhóm A — Báo cáo nội bộ** (SP1, SP3, SP5): trình bày gọn, tối giản, theo lựa chọn của Kế toán trưởng.
- **Nhóm B — File hợp đồng để ký** (SP2): theo thể thức văn bản hợp đồng đầy đủ.

---

# PHẦN A — Báo cáo nội bộ (SP1, SP3, SP5)

## Thiết lập trang

| Mục | Quy định |
|---|---|
| Khổ giấy | **A4 ngang** cho SP1 và SP3. A4 dọc cho SP5. |
| Lề | Trên 20mm · Dưới 20mm · Trái 30mm · Phải 15mm |
| Font thân | Times New Roman 13 |
| Font trong bảng | Times New Roman 11 |
| Tiêu đề báo cáo | Times New Roman 14, IN HOA, ĐẬM, căn giữa |
| **Header trang** | ❌ Không dùng |
| **Footer trang** | ❌ Không dùng |
| **Số trang** | ❌ Không dùng |
| **Trang bìa** | ❌ Không dùng |
| **Logo** | ❌ Không dùng |
| **Mục lục tự động** | ❌ Không dùng |
| **Đánh số mục 1. / 1.1. / 1.1.1.** | ❌ Không dùng — dùng tiêu đề chữ, không đánh số |

## Bảng

- Hàng tiêu đề: nền **xanh navy `1F3864`**, chữ trắng đậm, căn giữa, **lặp lại ở mỗi trang**.
- Thân bảng: viền mảnh xám `BFBFBF`, hàng lẻ nền xám rất nhạt (zebra), chữ căn trên.

## Bộ màu mức độ — Phương án 2

| Mức độ | Màu chữ | Màu nền |
|---|---|---|
| BẮT BUỘC SỬA | `C00000` đỏ đô | `FCE4E4` |
| NÊN SỬA | `BF8F00` cam hổ phách | `FFF2CC` |
| CÓ THỂ GIỮ | `375623` xanh lá đậm | `E2EFDA` |
| CHỈ HÌNH THỨC | `7F7F7F` xám | `F2F2F2` |

Nhãn mức độ viết dạng chip chữ hoa: `[BẮT BUỘC SỬA]` `[NÊN SỬA]` `[CÓ THỂ GIỮ]` `[CHỈ HÌNH THỨC]`

## Cách ghi số liệu

| Mục | Chuẩn |
|---|---|
| Số tiền | Phân cách nghìn bằng dấu chấm, kèm chữ trong ngoặc. VD: `150.000.000 đồng (Một trăm năm mươi triệu đồng)` |
| Ngày tháng | Có số 0 đứng trước. VD: `ngày 02 tháng 01 năm 2026` |

---

## SP1 — Báo cáo rà soát nội bộ

### Khối 1 — Thông tin chung (bảng 2 cột, đặt đầu báo cáo)

Công ty đại diện · Đối tác (tên + MST) · Loại văn bản · Chiều giao dịch · Số hợp đồng và ngày ký · Giá trị hợp đồng (chưa VAT / đã VAT) · Mẫu đã phê duyệt dùng đối chiếu · Người rà soát và ngày rà soát.

Trên cùng đặt một dòng **KẾT LUẬN NHANH** in đậm, tô nền theo mức độ:
`CÓ THỂ KÝ` / `KÝ SAU KHI SỬA` / `CHƯA THỂ KÝ`

Nếu văn bản thuộc diện phải trình — xem `08-phan-quyen-nhan-vien.md` — thêm ngay dưới một dòng nền cam:
`⚠️ CẦN TRÌNH KẾ TOÁN TRƯỞNG TRƯỚC KHI PHẢN HỒI ĐỐI TÁC — lý do: …`

### Khối 1B — Điều khoản cần Kế toán trưởng đọc kỹ (bảng riêng, ngay sau Thông tin chung)

Bốn nhóm điều khoản không có ngưỡng cứng, công ty quyết theo từng hợp đồng. **Không đánh lỗi**, nhưng bắt buộc trích ra để Kế toán trưởng đọc và tự quyết.

| Điều khoản | Vị trí | Hợp đồng đang ghi |
|---|---|---|
| Thời hạn thanh toán | Điều …, tr… | *trích nguyên văn* |
| Đặt cọc / tạm ứng | | |
| Bảo hành *(khi ta mua vào)* | | |
| Đơn phương chấm dứt *(khi ta bán ra)* | | |

- Trích **nguyên văn**, không diễn giải lại. Số tiền và phần trăm ghi rõ.
- Hợp đồng không có nội dung nào → ghi `Không quy định` vào ô đó, đồng thời đưa một dòng tương ứng vào bảng rà soát ở mức **NÊN SỬA**.
- Bảng này **luôn có**, kể cả khi hợp đồng hoàn toàn không có lỗi.

Chi tiết nhóm nào thuộc diện này xem `03-chuan-dieu-khoan.md`.

### Khối 2 — Bảng rà soát chi tiết, đúng 9 cột

| # | Cột | Yêu cầu |
|---|---|---|
| 1 | STT | |
| 2 | Vị trí | Ghi rõ Điều/Khoản/trang. VD: `Điều 4.2, trang 3` |
| 3 | Nội dung theo mẫu | Trích **nguyên văn** điều khoản tương ứng trong mẫu đã phê duyệt (`09-mau-da-phe-duyet.md`), tối đa 2 dòng. Xem quy tắc điền bên dưới |
| 4 | Hiện trạng hợp đồng | Trích **nguyên văn** đoạn có vấn đề trong hợp đồng đang rà, tối đa 2 dòng |
| 5 | Rủi ro / nhận xét | Nêu rủi ro **quy ra tiền hoặc thuế**, không nói chung chung |
| 6 | Mức độ | Chip màu 4 mức |
| 7 | Đề xuất | Sửa / Bổ sung / Bỏ / Hỏi đối tác / Hỏi nội bộ |
| 8 | Nội dung đề xuất điều chỉnh | **Viết sẵn câu thay thế** để dán thẳng vào hợp đồng |
| 9 | Phản hồi / xác nhận của Kế toán trưởng | **Để trống** |

**Quy tắc điền cột 3 "Nội dung theo mẫu"** — để nhìn ngang một dòng là thấy mẫu ghi gì, hợp đồng ghi gì:

| Trường hợp | Ghi vào cột 3 |
|---|---|
| Mẫu có điều khoản tương ứng | Trích nguyên văn đoạn trong mẫu, kèm vị trí trong mẫu. VD: `Mẫu Điều 5.2: "…lãi suất 0,03%/ngày…"` |
| Mẫu có điều khoản, hợp đồng bỏ mất | Trích đoạn trong mẫu; cột 4 ghi `Không có` |
| Hợp đồng thêm điều khoản mẫu không có | `Mẫu không quy định` |
| Lỗi đối chiếu thông tin (tên, MST, địa chỉ, tài khoản, người đại diện, ngưỡng điều khoản) | Ghi chuẩn công ty, có tiền tố `[Chuẩn công ty]`. VD: `[Chuẩn công ty] TK MB Bank 3192384679321` — lấy từ `01-cong-ty.md`, `02-tai-khoan.md`, `03-chuan-dieu-khoan.md` |
| Chưa có mẫu đã phê duyệt cùng loại | `Chưa có mẫu đã phê duyệt` — riêng lỗi đối chiếu thông tin/ngưỡng vẫn ghi `[Chuẩn công ty]` như trên |
| Dòng cuối gom lỗi hình thức | Để trống |

Khổ A4 ngang; độ rộng cột gợi ý (tổng ≈ 100%): STT 4 · Vị trí 8 · Nội dung theo mẫu 15 · Hiện trạng hợp đồng 15 · Rủi ro 16 · Mức độ 8 · Đề xuất 7 · Nội dung đề xuất 17 · Phản hồi 10.

Sắp xếp **BẮT BUỘC SỬA lên đầu**.

**Dòng cuối bảng** gom toàn bộ lỗi hình thức thành một dòng duy nhất:
> "Đã chỉnh N lỗi trình bày (chính tả, dấu câu, viết hoa, căn lề, khoảng cách), không ảnh hưởng nội dung." — mức độ `CHỈ HÌNH THỨC`

### Khối 3 — Kết luận

Đủ 9 mục theo SKILL.md phần 7, trong đó mục 7 là **ba rủi ro lớn nhất xếp theo số tiền ảnh hưởng**.

### Sau khi Kế toán trưởng phản hồi

Nội dung Kế toán trưởng ghi `không điều chỉnh` hoặc `theo thông tin hợp đồng` ở cột 9 → **xem là không điều chỉnh**, loại khỏi phạm vi chỉnh sửa, không hỏi lại.

---

## SP3 — Báo cáo so sánh trước – sau

Luôn tạo kèm mỗi khi đã xuất file hợp đồng đã chỉnh (SP2).

Bảng 5 cột:

| STT | Vị trí / Điều khoản | Nội dung trước khi chỉnh | Nội dung sau khi chỉnh | Ghi chú / Lý do chỉnh |

**Chỉ ghi thay đổi có ý nghĩa** về nội dung, quyền, nghĩa vụ, thông tin pháp lý, số liệu tài chính:

- Thông tin các bên, người đại diện, MST/CCCD, giấy phép kinh doanh, địa chỉ, số điện thoại, tài khoản ngân hàng
- Căn cứ ký kết, số hợp đồng/phụ lục, ngày ký, ngày hiệu lực, thời hạn, ngày thanh lý
- Nghĩa vụ thanh toán, công nợ, phí phạt, chi phí phát sinh, giá trị còn lại, thời hạn thanh toán, hồ sơ chứng từ, hóa đơn, thuế
- Quyền/nghĩa vụ các bên, điều kiện chấm dứt, thanh lý, chuyển giao, bảo mật, tranh chấp
- Nội dung mới bổ sung hoặc nội dung cũ bị bỏ

**Không đưa vào** SP3: lỗi chính tả, khoảng cách chữ, chữ hoa/thường, dấu câu, font, cỡ chữ, căn lề, thụt đầu dòng, giãn dòng, màu chữ, thể thức — trừ khi thay đổi đó làm đổi ý nghĩa pháp lý hoặc tài chính.

---

## SP4 — Bảng đề nghị điều chỉnh gửi đối tác

**Chỉ làm khi được yêu cầu.**

Chỉ tổng hợp các nội dung thay đổi thực tế về nội dung hợp đồng. **Tuyệt đối không** đưa lỗi chính tả, khoảng cách chữ, chữ hoa/thường, dấu câu, căn lề vào bản gửi đối tác.

Giọng văn lịch sự, trung tính, hướng tới thống nhất — không dùng từ mang tính quy kết.

---

## SP5 — Phiếu trình ký 1 trang

**Chỉ làm khi được yêu cầu.** A4 dọc, gói gọn trong 1 trang.

Gồm: bảng tóm tắt (hợp đồng, đối tác, giá trị, người ký, tài khoản thanh toán, kết quả rà soát, trạng thái) · **ba rủi ro lớn nhất kèm số tiền ảnh hưởng** · ô ký 3 cấp: Người rà soát — Kế toán trưởng — Giám đốc.

---

## Nơi lưu các sản phẩm

| Sản phẩm | Lưu vào |
|---|---|
| SP1 báo cáo rà soát · SP3 báo cáo so sánh · SP5 phiếu trình ký | `01_Trao_doi_Phe_duyet` |
| SP4 bảng đề nghị điều chỉnh gửi đối tác | `02_Ho_so_phe_duyet` (đặt trực tiếp) |
| SP2 file hợp đồng đã chỉnh | Chưa duyệt → `01_Draft`. **Chưa ký xong nhưng Kế toán trưởng đã duyệt lưu → đưa vào hồ sơ final** tại `02_Ho_so_phe_duyet` (đặt trực tiếp, hậu tố ` ban gui khach chua ky`). Ký đủ chữ ký và đóng dấu → `02_Ho_so_phe_duyet\<Số hợp đồng>_<Tên đối tác>` |

Nguyên tắc: `01_Trao_doi_Phe_duyet` là tài liệu nội bộ của quá trình duyệt; `02_Ho_so_phe_duyet` là hồ sơ đã chốt, có thể đưa ra ngoài. Chi tiết xem `07-luu-tru-dat-ten.md`.

---

## SP6 — Dòng nhật ký theo dõi hợp đồng

Ghi 1 dòng vào file Excel theo dõi, các cột:

`Ngày rà soát | Công ty | Chiều | Loại VB | Số HĐ | Đối tác | Giá trị | Số lỗi bắt buộc sửa | Số lỗi nên sửa | Kết luận | Người rà soát | Đường dẫn file final`

Chưa có file theo dõi thì tạo mới tại `PROMTAI\NHAT_KY_RA_SOAT_HOP_DONG.xlsx`, **không ghi đè** nếu đã có — chỉ thêm dòng.

---

# PHẦN B — File hợp đồng đã chỉnh (SP2)

Đây là văn bản **để ký**, phải theo thể thức hợp đồng đầy đủ. Không áp dụng quy tắc "không header/footer/số trang" của Phần A.

## Thiết lập trang

| Mục | Quy định |
|---|---|
| Khổ giấy | **A4 dọc** — giữ đúng khổ bản gốc. Chỉ dùng ngang cho phụ lục/bảng nhiều cột thực sự cần |
| Lề | Trái **30mm** · Phải 20mm · Trên 20mm · Dưới 20mm |
| Font | Times New Roman, Unicode, **màu đen**, nội dung cỡ **13** |
| Tiêu đề và thành phần thể thức | Cỡ 12–14 theo vai trò, phải đồng bộ toàn văn bản |
| Căn lề nội dung | Đều hai lề |
| Thụt đầu dòng đoạn thường | 10mm |
| Khoảng cách sau đoạn | Tối thiểu 6pt |
| Giãn dòng | 1,15 — không vượt quá 1,5 |
| **Số trang** | Số Ả Rập, cỡ 13, kiểu đứng, **căn giữa tại lề trên**, **không hiện ở trang 1**. Phụ lục độc lập đánh số riêng |

Chuẩn tham chiếu: Phụ lục I ban hành kèm **Nghị định 187/2025/NĐ-CP** (hiệu lực 01/07/2025). Đây là chuẩn cho văn bản quy phạm pháp luật — với hợp đồng thì **vận dụng các quy tắc kỹ thuật phù hợp**, không máy móc bổ sung thành phần chỉ dành cho văn bản quy phạm pháp luật.

## Bố cục đầu văn bản

- Tên công ty đặt **bên trái**.
- Quốc hiệu – tiêu ngữ đặt **bên phải**.
- Dưới dòng "Độc lập - Tự do - Hạnh phúc" phải có dấu phân cách cân đối với dòng tiêu ngữ. Theo thể thức pháp luật thì dùng đường kẻ ngang nét liền; theo mẫu hợp đồng doanh nghiệp thì được dùng `----------o0o----------` căn giữa, và khi đó **không** đồng thời giữ đường viền Word bên dưới.
- Số hợp đồng đặt góc **trái**, ngay dưới tên công ty, **cách tên công ty 1 dòng**.
- Dòng địa danh – thời gian đặt ngay dưới tiêu ngữ, **căn phải**, **luôn in nghiêng**.
- Tiêu đề hợp đồng cách dòng ngày tháng 1 dòng và cách phần căn cứ 1 dòng.
- Các căn cứ hợp đồng/phụ lục nên **in nghiêng**, căn chỉnh gọn.

## Địa danh trong dòng ngày tháng

Lấy theo **địa danh của bên công ty ta đại diện**, không lấy theo địa chỉ đối tác.

| Công ty | Ghi |
|---|---|
| NTC | `Tây Ninh, ngày ... tháng ... năm ...` |
| Global | `Tp Hồ Chí Minh, ngày ... tháng ... năm ...` |
| Digital | `Tp Hồ Chí Minh, ngày ... tháng ... năm ...` |

Không tự đổi `Tp Hồ Chí Minh` thành `Thành phố Hồ Chí Minh` nếu mẫu đã thống nhất dùng `Tp`.

## Bố cục thân văn bản

- Không thụt đầu dòng cho: tiêu đề văn bản, tên bên, tiêu đề điều/mục, dòng căn cứ, dòng địa danh – ngày tháng, tiêu đề bảng, phần chữ ký.
- Các khoản cùng cấp (1.1, 1.2, 2.1, 2.2) phải **cùng mức lề, cùng kiểu căn chỉnh** trong toàn văn bản.
- **Không** dùng dấu cách, tab thủ công hay khoảng trắng để giả lập thụt đầu dòng. Phải chỉnh bằng định dạng đoạn trong Word: left indent, first line indent, alignment, spacing.
- Thông tin Bên A / Bên B tách khối rõ ràng, có khoảng cách đoạn phù hợp trước khi sang bên kia.
- Dòng dài như số tài khoản, địa chỉ, CCCD phải tự xuống dòng hợp lý.
- Tiêu đề điều in đậm; nội dung thường không in đậm. **Bỏ** các chỗ in đậm không cần thiết.
- Không để lẫn nhiều font, nhiều cỡ chữ, hoặc font lỗi mã. Thấy chữ lỗi dấu tiếng Việt phải sửa font/mã trước khi báo hoàn thành.

## Không được tự bỏ thông tin của đối tác

Với thông tin liên hệ/thông báo của khách hàng, nhà cung cấp, đối tác trong file gốc: chỉ được **bổ sung thêm** thông tin mới hoặc thông tin theo hồ sơ pháp lý. **Không tự ý bỏ** địa chỉ thường trú, địa chỉ liên hệ, địa chỉ cửa hàng, số điện thoại, email, người liên hệ đã có — trừ khi người dùng yêu cầu bỏ rõ ràng.

## Đánh dấu chỉnh sửa trong SP2

Dùng **tô màu**, không dùng Track Changes.

Đánh dấu **chính xác đúng cụm từ cần thay đổi**. Không tô màu, gạch bỏ hay đánh dấu lan man cả câu, cả đoạn nếu chỉ cần sửa một cụm từ. Không tô màu những nội dung không thay đổi.

| Màu | Ý nghĩa |
|---|---|
| Đỏ `C00000` | Nội dung bắt buộc sửa |
| Vàng/cam `BF8F00` | Nội dung nên sửa hoặc cần làm rõ |
| Xanh lá `375623` | Nội dung đề xuất thêm để bảo vệ công ty |

Chèn **một khối chú giải màu ở đầu file SP2** để đối tác mở ra hiểu ngay màu nào nghĩa gì.

Khi trao đổi bằng văn bản thuần (không phải file Word):
- Nội dung cần bỏ: `~~gạch bỏ~~`
- Nội dung thêm/thay thế: `**[SỬA: nội dung đề xuất]**`
- Nội dung bắt buộc sửa: `**[BẮT BUỘC SỬA: nội dung đề xuất]**`
- Nội dung cần kiểm tra thêm: `**[CẦN KIỂM TRA: nội dung cần xác minh]**`

---

## ⭐ Chỗ trống cần điền và nội dung cần xác nhận — LUÔN TÔ CHỮ ĐỎ

Áp dụng cho **mọi sản phẩm**: file hợp đồng đã chỉnh (SP2), báo cáo rà soát (SP1), báo cáo so sánh (SP3), bảng gửi đối tác (SP4), phiếu trình ký (SP5).

| Nhãn | Dùng khi nào | Định dạng |
|---|---|---|
| **`[Điền Nội dung]`** | Có một chỗ **bắt buộc phải điền** mà hiện đang trống hoặc chưa có dữ liệu: số hợp đồng, ngày ký, số tiền, hạn mức công nợ, thời hạn, tên người đại diện, số giấy phép… | Chữ **ĐỎ `C00000`**, **in đậm**, trong ngoặc vuông |
| **`[Xác nhận lại]`** | Thông tin **đã có sẵn** nhưng cần đối chiếu, xác minh hoặc Kế toán trưởng quyết: địa chỉ lệch CCCD, số giấy ủy quyền, mức lãi khác chuẩn, tài khoản chưa khớp bảng tra… | Chữ **ĐỎ `C00000`**, **in đậm**, trong ngoặc vuông |

### Bốn quy tắc bắt buộc

1. **Đặt ngay tại vị trí** trong văn bản, không gom xuống cuối, không chỉ ghi ở phần ghi chú.
2. **Không dùng dấu chấm lửng** `…`, `……….`, `___` hay để trống trắng. Mọi chỗ trống đều phải là `[Điền Nội dung]` màu đỏ để mắt nhìn ra ngay.
3. **Nêu rõ cần điền gì** ngay sau nhãn khi chưa hiển nhiên. Ví dụ: `[Điền Nội dung — hạn mức công nợ]`.
4. Ở **cột "Nội dung đề xuất điều chỉnh"** của báo cáo rà soát: câu chữ viết sẵn mà còn chỗ trống thì chỗ đó cũng phải là `[Điền Nội dung]` màu đỏ, để Kế toán trưởng dán vào hợp đồng là thấy ngay còn thiếu gì.

### Ví dụ

❌ **Sai:**
> "Hạn mức công nợ tối đa của Bên B tại mọi thời điểm là ……… đồng."

✅ **Đúng:** *(phần trong ngoặc vuông tô đỏ đậm)*
> "Hạn mức công nợ tối đa của Bên B tại mọi thời điểm là **[Điền Nội dung — hạn mức công nợ]** đồng."

❌ **Sai:**
> "Địa chỉ thường trú: Thôn 3, Xã Bình Giang, Tỉnh Ninh Bình (cần kiểm tra lại với CCCD)"

✅ **Đúng:**
> "Địa chỉ thường trú: Thôn 3, Xã Bình Giang, Tỉnh Ninh Bình **[Xác nhận lại — CCCD ghi Vũ Bản, Bình Lục, Hà Nam]**"

### Chú giải

Khi trong văn bản có dùng hai nhãn này, chèn thêm một dòng vào khối chú giải màu ở đầu file:

> **[Điền Nội dung]** = chỗ còn thiếu, phải điền trước khi ký · **[Xác nhận lại]** = đã có thông tin nhưng cần đối chiếu, xác minh

## Rà soát thể thức trước khi xuất bản final

Tự kiểm lại: khổ A4 · font Times New Roman Unicode màu đen · nội dung cỡ 13 · lề trái 30mm, các lề còn lại 20mm · căn đều hai lề · thụt đầu dòng 10mm · khoảng cách sau đoạn ≥ 6pt · giãn dòng 1,15 · số trang · khoảng cách giữa thông tin các bên · bảng biểu · phần chữ ký · tên file.

Nếu người dùng phản ánh lỗi thể thức qua ảnh chụp → kiểm tra và sửa **theo hiển thị thực tế trong Word**, không chỉ dựa vào thông số kỹ thuật nếu mắt thường vẫn thấy lệch.
