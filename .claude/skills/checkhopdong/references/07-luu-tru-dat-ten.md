# 07 · Đặt tên file, lưu trữ và xử lý bản nháp

## Đường dẫn thư mục hồ sơ

### THƯ MỤC GỐC — skill tự tìm, không phải điền tay

```
<THƯ_MỤC_GỐC> = %USERPROFILE%\OneDrive\KẾ TOÁN CHUẨN\UNGDUNGAI2026\PROMTAI
```

`%USERPROFILE%` là thư mục người dùng Windows đang đăng nhập, ví dụ `C:\Users\Ke toan`. Skill tự thay giá trị này theo máy đang chạy, **không ai phải sửa file khi cài đặt**.

**Cách xác định, theo thứ tự:**

1. Thay `%USERPROFILE%` bằng thư mục người dùng thật của máy đang chạy, rồi kiểm tra đường dẫn có mở được không.
2. Không mở được → thử các biến thể tên OneDrive công ty, ví dụ `OneDrive - <tên công ty>` thay cho `OneDrive`.
3. Vẫn không thấy → tìm thư mục tên `PROMTAI` có chứa đủ ba thư mục con `01_Draft`, `02_Mau_da_phe_duyet`, `03_Ho_so_final`.
4. Vẫn không thấy → **hỏi người dùng**, gộp vào nhóm tối đa 3 câu hỏi ở đầu phiên. **Không tự đoán, không tự tạo thư mục mới.**

### Các thư mục con — tính từ thư mục gốc

```
<THƯ_MỤC_GỐC>\01_Draft                        bản nháp
<THƯ_MỤC_GỐC>\02_Mau_da_phe_duyet             mẫu đã phê duyệt
<THƯ_MỤC_GỐC>\03_Ho_so_final                  hồ sơ final
<THƯ_MỤC_GỐC>\NHAT_KY_RA_SOAT_HOP_DONG.xlsx   nhật ký rà soát
```

### Khi không xác định được thư mục gốc

Vẫn rà soát và xuất báo cáo bình thường, chỉ dừng ở bước lưu trữ. Ghi rõ ở cuối báo cáo:
> "Chưa xác định được thư mục hồ sơ trên máy này. File tạm để ở [nơi đang lưu], cần chuyển vào đúng thư mục sau khi xác nhận đường dẫn."

---

## Viết tắt loại văn bản

| Loại văn bản | Viết tắt |
|---|---|
| Hợp đồng mua vào | `HDMV` |
| Hợp đồng bán ra | `HDRA` |
| Hợp đồng đại lý | `HDDL` |
| Phụ lục hợp đồng | `PLHD` |
| Phụ lục chuyển giao | `PLCG` |
| Biên bản thanh lý hợp đồng | `BBTLHD` |
| Biên bản nghiệm thu | `BBNT` |
| Biên bản đối chiếu công nợ | `BBDCCN` |

## Viết tắt công ty

| Công ty | Trong số hợp đồng | Tên folder |
|---|---|---|
| Nệm Thành Công | `NTC` | `Nem Thanh Cong` |
| Thuần Việt Global | `TVG` | `Global` |
| Thuần Việt Digital | `TVD` | `Digital` |

---

## Cấu trúc tên file

```
[Số HĐ] [Năm ký] [Loại VB viết tắt] [Cty viết tắt]_[Tên đối tác].docx
```

Các thành phần **cách nhau bằng dấu cách**. Riêng công ty và đối tác nối bằng dấu gạch dưới `_`.

> ⚠️ Không dùng dấu `/` trong tên file — Windows không cho phép.

**Ví dụ thật đang có trong hồ sơ:**
```
012026 2026 HDMV NTC_Phuc Vinh.docx
01-2025-HDDL-TVG 2025 BBTLHD Global_HKD Nem Thuan Viet.docx
092-26-HD-HT 2026 HDMV Digital_Xe Nang HT.docx
```

Thiếu số hợp đồng hoặc năm ký → **hỏi trước khi đặt tên final**, không tự đặt.

---

## Cấu trúc thư mục hồ sơ final

```
03_Ho_so_final\
  <Tên folder công ty>\
    Mua_vao  |  Ban_ra\
      Nha_cung_cap  |  Khach_hang\
        <Tên đối tác>\
          01_Trao_doi_Phe_duyet\
          02_Ho_so_phe_duyet\
              Chung_tu_phap_ly\
              Cong_no_Thanh_toan\
              <Số hợp đồng>_<Tên đối tác>\
```

- Mua vào → `Nha_cung_cap` · Bán ra → `Khach_hang`
- Mỗi đối tác có đúng **hai** folder cấp một: `01_Trao_doi_Phe_duyet` và `02_Ho_so_phe_duyet`.

### Lưu gì vào đâu

| Vị trí | Nội dung |
|---|---|
| **`01_Trao_doi_Phe_duyet\`** | Tài liệu **nội bộ** của quá trình duyệt: báo cáo rà soát (SP1) · bản báo cáo đã có phản hồi của Kế toán trưởng Uyên · báo cáo so sánh trước–sau (SP3) · phiếu trình ký (SP5) · email và nội dung thảo luận |
| **`02_Ho_so_phe_duyet\`** | Hồ sơ **đã chốt**. Gồm 2 folder con và các file gửi ra ngoài |
| `02_Ho_so_phe_duyet\Chung_tu_phap_ly\` | Giấy chứng nhận đăng ký doanh nghiệp / hộ kinh doanh, CCCD, giấy ủy quyền của đối tác. **Dùng chung cho mọi hợp đồng** của đối tác đó |
| `02_Ho_so_phe_duyet\Cong_no_Thanh_toan\` | Biên bản đối chiếu công nợ, ủy nhiệm chi, chứng từ thanh toán. Gom theo đối tác, không tách theo từng hợp đồng |
| `02_Ho_so_phe_duyet\` *(đặt trực tiếp, không trong folder con)* | Bảng đề nghị điều chỉnh gửi khách hàng / nhà cung cấp / nhân viên (SP4) · **Hợp đồng / phụ lục chưa ký nhưng Kế toán trưởng đã duyệt lưu** (bản gửi khách), tên file thêm hậu tố ` ban gui khach chua ky` |
| **`02_Ho_so_phe_duyet\<Số hợp đồng>_<Tên đối tác>\`** | **Một folder cho mỗi hợp đồng**, chứa toàn bộ văn bản đã ký của hợp đồng đó: hợp đồng · phụ lục · phụ lục chuyển giao · biên bản thanh lý · biên bản nghiệm thu |

### Nguyên tắc phân biệt hai folder cấp một

| | `01_Trao_doi_Phe_duyet` | `02_Ho_so_phe_duyet` |
|---|---|---|
| Tính chất | Đang bàn, đang duyệt | Đã chốt |
| Người xem | Nội bộ công ty | Có thể đưa ra ngoài |
| Ví dụ | Báo cáo rà soát, phản hồi của Kế toán trưởng Uyên | Hợp đồng đã ký, hợp đồng chưa ký đã duyệt lưu, bảng đề nghị đã gửi đối tác |

### Văn bản chưa ký xong (Kế toán trưởng chốt 24/09/2026)

| Tình trạng | Lưu ở đâu |
|---|---|
| Đang soạn, đang chỉnh, Kế toán trưởng **chưa duyệt** | `01_Draft` |
| **Chưa ký xong nhưng Kế toán trưởng đã duyệt lưu** | **Đưa vào hồ sơ final**: `02_Ho_so_phe_duyet\` đặt trực tiếp, tên file thêm hậu tố ` ban gui khach chua ky`. VD: `022-2026-HDDL-NTC 2026 HDDL NTC_HKD Hoc Dung_v2 ban gui khach chua ky.docx` |
| Đã ký đủ chữ ký và đóng dấu | `02_Ho_so_phe_duyet\<Số hợp đồng>_<Tên đối tác>\`, tên file chuẩn, không hậu tố |

Khi có bản đã ký: lưu bản ký vào folder hợp đồng. Bản ` ban gui khach chua ky` **giữ nguyên, không tự xóa**. Muốn dọn thì liệt kê và xin phép Kế toán trưởng như quy trình xóa bên dưới.

### Tên folder theo hợp đồng

```
<Số hợp đồng>_<Tên đối tác>
```

- **Số hợp đồng** giữ đúng như ghi trên hợp đồng, chỉ thay dấu `/` thành `-` vì Windows không cho dùng `/` trong tên thư mục.
- **Tên đối tác** viết **không dấu**, có tiền tố loại hình, giống tên folder đối tác ở cấp trên.

Ví dụ với hợp đồng số `022/2026/HĐĐL-NTC` ký với HKD Học Dung:

```
022-2026-HĐĐL-NTC_HKD Hoc Dung\
     022-2026-HĐĐL-NTC 2026 HDDL   NTC_HKD Hoc Dung.docx
     022-2026-HĐĐL-NTC 2026 PLHD   NTC_HKD Hoc Dung.docx
     022-2026-HĐĐL-NTC 2026 BBTLHD NTC_HKD Hoc Dung.docx
```

**Vì sao mỗi hợp đồng một folder:** một đối tác có thể ký nhiều hợp đồng qua các năm. Tách theo số hợp đồng thì hợp đồng nào đi với phụ lục và biên bản nào luôn rõ ràng, không lẫn giữa các năm. Còn chứng từ pháp lý và công nợ thì để ngoài vì dùng chung cho cả đối tác.

## Quy tắc đặt tên folder đối tác

Có **tiền tố loại hình** + tên **không dấu**.

```
HKD Tran Vu Phi
CTY CP Quoc Khanh
```

---

## ✅ Kho hồ sơ đã chuẩn hóa xong — 23/09/2026

Ba folder lệch chuẩn đã được đổi tên theo phê duyệt của Kế toán trưởng:

| Tên cũ | Tên mới |
|---|---|
| `03_Ho_so_final\Nệm Thành Công` | `Nem Thanh Cong` |
| `Global\...\HKD Huynh The Hau 1992\04_Phu_luc` | `02_Phu_luc` |
| `Global\...\Tran Vu Phi` | `HKD Tran Vu Phi` |

Chỉ đổi tên, không xóa và không ghi đè file nào — 57 file trước và sau đều nguyên vẹn. Bản sao lưu đầy đủ tại `CLAUDE\Uyen-ERP\_BACKUP\2026-09-23\03_Ho_so_final_TRUOC_KHI_DOI_TEN\`.

**Quy tắc khi lưu file mới:** tuyệt đối **không tạo folder mới trùng nội dung** với folder đã có của cùng một đối tác. Trước khi tạo folder đối tác mới, phải liệt kê folder hiện có để kiểm tra trùng — kể cả trùng do khác dấu hoặc khác tiền tố.

---

## ⚠️ Kho hồ sơ hiện tại còn theo cấu trúc CŨ 6 folder

Cấu trúc hai tầng ở trên là chuẩn **mới** Kế toán trưởng chốt ngày 23/09/2026. Các thư mục đối tác đang có trong `03_Ho_so_final` vẫn theo cấu trúc **cũ 6 folder** và **chưa được phép chuyển**.

| Folder cũ | Chuyển về |
|---|---|
| `01_Hop_dong` · `02_Phu_luc` · `05_Thanh_ly` | → `02_Ho_so_phe_duyet\<Số hợp đồng>_<Tên đối tác>\` — tách theo số hợp đồng ghi ở đầu tên file |
| `03_Chung_tu_phap_ly` | → `02_Ho_so_phe_duyet\Chung_tu_phap_ly\` |
| `04_Cong_no_Thanh_toan` | → `02_Ho_so_phe_duyet\Cong_no_Thanh_toan\` |
| `06_Trao_doi_Phe_duyet` | → `01_Trao_doi_Phe_duyet\` — riêng bảng đề nghị gửi đối tác (SP4) chuyển sang `02_Ho_so_phe_duyet\` |

**Quy tắc trong lúc chờ chuyển đổi:**

- Đối tác **đã có** thư mục theo cấu trúc cũ → **lưu tiếp theo cấu trúc cũ** của đối tác đó. Không tạo song song folder mới trong cùng một thư mục đối tác, vì sẽ làm hồ sơ nằm hai chỗ.
- Đối tác **chưa có** thư mục → tạo mới theo **cấu trúc hai tầng** ở trên.
- Ghi một dòng vào báo cáo cho biết đã lưu theo cấu trúc nào.

*Ghi chú: thư mục `HKD Huynh The Hau 1992` hiện chỉ có `02_Phu_luc` và `05_Thanh_ly`. Tạo bổ sung folder khi thực sự có hồ sơ cần lưu, không tạo folder rỗng.*

---

## Quy trình lưu bản cuối

1. Mọi bản demo, bản đang chỉnh, bản Kế toán trưởng chưa duyệt → lưu vào `01_Draft`.
2. Trước khi lưu vào hồ sơ final, **bắt buộc hỏi**: *"File này đã là bản cuối cùng chưa?"* — hoặc với bản chưa ký: *"Chị duyệt lưu bản chưa ký này vào hồ sơ final chưa?"*
3. Chỉ khi Kế toán trưởng xác nhận → mới lưu vào `03_Ho_so_final` theo cấu trúc trên (bản chưa ký theo bảng "Văn bản chưa ký xong").
4. Lưu xong, ghi 1 dòng nhật ký (SP6).

---

## Xử lý bản nháp sau khi có bản final

Kế toán trưởng đã chốt: sau khi lưu vào hồ sơ final thì **dọn bản nháp**. Nhưng quy tắc cứng của Kế toán trưởng là **mỗi lần xóa đều phải xin phép riêng**. Vì vậy quy trình bắt buộc là:

1. **Liệt kê** đầy đủ danh sách file draft liên quan đến hợp đồng đó: tên file, đường dẫn, số lượng, dung lượng.
2. **Xin phép Kế toán trưởng** cho lần xóa này. Lần trước được đồng ý **không** có nghĩa lần này được phép.
3. Chị đồng ý → **sao lưu toàn bộ** sang `CLAUDE\Uyen-ERP\_BACKUP\<yyyy-mm-dd>\` kèm file `_GHICHU.txt`.
4. Sao lưu xong mới được xóa.
5. Báo lại vị trí bản sao lưu để hoàn tác được khi cần.

> Không có bản sao lưu thì **không được xóa**.

---

## Dọn `01_Trao_doi_Phe_duyet` sau khi hồ sơ phê duyệt đã chốt

Mục tiêu: giảm số file, cho nhẹ máy và nhẹ đồng bộ OneDrive.

**Điều kiện được phép dọn — phải đủ CẢ BA:**

1. Hồ sơ trong `02_Ho_so_phe_duyet` đã đầy đủ và **Kế toán trưởng xác nhận là bản chốt**.
2. Hợp đồng **không đang tranh chấp**, không có khiếu nại đang xử lý.
3. Hợp đồng đã **thanh lý xong và hết công nợ**, hoặc Kế toán trưởng xác nhận không cần giữ hồ sơ trao đổi.

**Quy trình bắt buộc — 6 bước, không được rút gọn:**

1. **Kiểm tra ba điều kiện** trên. Thiếu bất kỳ điều kiện nào → **không đề xuất dọn**, giữ nguyên.
2. **Liệt kê** đầy đủ: tên từng file, đường dẫn, số lượng, tổng dung lượng.
3. **Xin phép Kế toán trưởng cho đúng lần này.** Lần trước được đồng ý **không** có nghĩa lần này được phép — mỗi hợp đồng phải hỏi riêng.
4. Chị đồng ý → **nén toàn bộ folder thành một file zip**, đặt tên `<Số hợp đồng>_<Tên đối tác>_Trao_doi.zip`, lưu vào `CLAUDE\Uyen-ERP\_BACKUP\<yyyy-mm-dd>\` kèm `_GHICHU.txt`.
5. **Kiểm tra zip mở được và đủ số file** rồi mới xóa folder gốc.
6. **Báo lại vị trí file zip** để hoàn tác được khi cần.

> ❗ Không có bản zip kiểm tra được thì **không được xóa**.

**Vì sao vẫn phải giữ bản nén:** báo cáo rà soát và nội dung trao đổi là **bằng chứng nội bộ** cho thấy công ty đã thẩm định hợp đồng trước khi ký. Khi có tranh chấp với đối tác hoặc thanh tra thuế, đây là tài liệu chứng minh sự cẩn trọng. Xóa sạch không giữ bản nào là rủi ro lớn hơn nhiều so với vài trăm KB tiết kiệm được.

**Nếu Kế toán trưởng yêu cầu xóa mà chưa đủ ba điều kiện:** vẫn làm theo yêu cầu của Kế toán trưởng, nhưng phải nêu rõ một dòng cảnh báo trước khi xóa, ví dụ *"Hợp đồng chưa thanh lý, vẫn còn công nợ — hồ sơ trao đổi có thể cần dùng lại."*

---

## Hai thư mục cấm

| Thư mục | Quy định |
|---|---|
| `02_Mau_da_phe_duyet` | **Không xóa, không ghi đè** bất kỳ file nào khi Kế toán trưởng chưa cho phép |
| `02_Ho_so_phe_duyet` trong `03_Ho_so_final` | **Không xóa, không ghi đè** bất kỳ file nào khi Kế toán trưởng chưa cho phép |

Cần sửa file trong hai thư mục này → lưu **bản mới** với tên khác, giữ nguyên bản cũ. Ghi đè chỉ khi Kế toán trưởng phê duyệt đúng file đó, và vẫn phải sao lưu trước.

`01_Trao_doi_Phe_duyet` là folder **duy nhất** trong `03_Ho_so_final` được phép dọn, và chỉ theo đúng quy trình 6 bước ở trên.
