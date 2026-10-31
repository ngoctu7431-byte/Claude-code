# Cài máy quét BH MISA → ERP lên máy Tú (Windows)

Dựng 29/09/2026. Thay cách routine của Tú đang đọc MISA bằng Claude in Chrome (bấm từng dòng, đọc chữ trên màn). Cách đó đã gãy ngày 28/09.

**Đổi gì:** đọc BH qua đúng cửa dữ liệu mà trang MISA dùng. Chi tiết lấy theo mã từng BH nên không lẫn sang BH khác. Không bấm màn hình, không đụng Chrome hằng ngày của Tú.

**Không đổi gì:** vẫn là routine Claude của Tú chạy mỗi tiếng. Nó chỉ đổi từ "tự đi bấm MISA" sang "chạy một lệnh rồi báo kết quả".

Thử trên dữ liệu thật ngày 28/09 (chỉ xem): bắt đúng 2 cặp trùng (BH04901, BH04903). 15 BH đã có trên ERP đều khớp tiền. 5 BH còn lại tắc đúng lý do: mã phí `Phi1`/`Phi2` chưa có, khách bán lẻ chưa có hồ sơ.

> **Cách nhanh nhất:** đưa tờ này cho **Claude trên máy Tú**, bảo nó làm từ bước 1 tới bước 4. Chỉ riêng lúc bộ cài hỏi **API Key / Secret** thì **Tú tự gõ**. Khoá không đi qua chat.

---

## Cần có trước

| Thứ | Ghi chú |
|---|---|
| **Python 3.9 trở lên** | Mở PowerShell, gõ `py --version`. Chưa có thì cài từ python.org, lúc cài **tích ô "Add python.exe to PATH"**. Hoặc gõ `winget install Python.Python.3.12`. |
| **Google Chrome** | Chrome đang dùng hằng ngày là được. Script mở một hồ sơ Chrome **riêng**, không đụng tab hay tài khoản của Tú. |
| **Khoá API ERP của Tú** | Tú đã có. Bộ cài in ra khoá thuộc tài khoản nào: phải ra `ngoctu.7431@gmail.com`. Ra `nvtungjob@gmail.com` là khoá của Tùng (ngày 28/09 đơn bị tạo và huỷ bằng khoá này), khi đó Tú lấy khoá của chính mình. |
| **Tài khoản MISA của Tú** | Phải xem được *Bán hàng → Bán hàng* (danh sách BH). |
| **Đường dẫn sổ bỏ qua** `misa-bh-sync-bo-qua.md` | Hỏi Claude trên máy Tú: *"sổ bỏ qua BH nằm ở đâu"*. Script đọc mọi chữ `BHxxxxx` trong file đó rồi không đụng tới. |

## Bước 1: chép gói

Tú lưu `goi-quet-bh-may-tu.zip` **ở đâu cũng được**, rồi giải nén (chuột phải → *Extract All*). Trong đó có 4 file:

```
quet-don-misa-len-erp.py    ← phần tạo đơn ERP (tìm khách, thuế, kho, submit)
quet-bh-misa-len-erp.py     ← phần đọc BH
cai-quet-bh.py              ← bộ cài
HUONG-DAN-CAI-QUET-BH.md    ← tờ này
```

## Bước 2: chạy bộ cài

**Nháy đúp `cai-quet-bh.py`.** Nếu Windows hỏi mở bằng gì thì chọn *Python*.

Không nháy đúp được thì mở **PowerShell**, gõ `py` và **một dấu cách**, **kéo file `cai-quet-bh.py` thả vào cửa sổ**, rồi Enter.

Bộ cài làm 4 việc:
1. Kiểm Python và Chrome.
2. Chép script vào **`C:\Claude Code\routines\quet-bh\`**, đúng thư mục làm việc của Claude trên máy Tú.
3. Cài Playwright.
4. Hỏi **API Key** và **API Secret**, rồi cất vào `C:\Users\<tên>\.ntv-secrets\frappe-prod.env`. File khoá nằm ngoài thư mục script, để Claude không vô tình đọc hay chép khoá đi đâu.

**Đạt khi** có dòng `Khoá ERP chạy được — tài khoản: ngoctu.7431@gmail.com`. Bộ cài cũng ghi sẵn các lệnh dùng tiếp vào **`C:\Claude Code\routines\quet-bh\LENH.txt`**, cứ mở file đó ra mà chép.

Script **không ghi file dữ liệu nào**. Nó đọc MISA, tạo đơn ERP, rồi in kết quả ra màn hình. Chứng từ ở `D:\Ngọc Tú\WORKING\CHỨNG TỪ\` không liên quan, không cần dời.

## Bước 3: đăng nhập MISA một lần

Chạy lệnh *"Đăng nhập MISA"* trong `LENH.txt`. Lệnh đó có dạng:

```
"C:\Claude Code\routines\quet-bh\.venv\Scripts\python.exe" "C:\Claude Code\routines\quet-bh\quet-bh-misa-len-erp.py" --dang-nhap
```

Một cửa sổ Chrome **riêng** hiện ra. Tú đăng nhập MISA như bình thường, vào được trang chủ thì **đóng cửa sổ đó**. Phiên được lưu ở `C:\Users\<tên>\.ntv-secrets\chrome-misa`. Script không giữ mật khẩu.

Script in ra `PHIÊN MISA ĐÃ HẾT` nghĩa là MISA tự đăng xuất. Lúc đó chạy lại đúng lệnh này.

## Bước 4: chạy thử CHỈ XEM

Chạy lệnh *"Chạy thử CHỈ XEM"* trong `LENH.txt`, thay `<đường dẫn sổ bỏ qua>` bằng đường dẫn thật. Lệnh này **không ghi gì**, chỉ in ra 5 nhóm:

| Nhóm | Nghĩa | Ai làm gì |
|---|---|---|
| **ĐÃ CÓ TRÊN ERP** | BH đã up, tiền khớp | Không cần làm gì |
| **TIỀN LỆCH SO MISA** | Kế toán đã sửa BH sau khi up | Người quyết sửa đơn ERP. Máy **không tự sửa** |
| **TỒN CŨ** | BH 2–7 ngày trước chưa lên ERP | Máy **không tự up**. Cố ý bỏ thì ghi số BH vào sổ bỏ qua. Cần up thì chạy lệnh một BH ở bước 5 |
| **TẮC** | Nghi trùng · thuế trống · mã hàng/khách chưa có trên ERP · cộng dòng không khớp | Người xử nguyên nhân rồi chạy lại |
| **SẼ TẠO** | BH hôm nay/hôm qua, đã qua hết các bước kiểm | Lượt `--that` sẽ tạo |

Lần đầu nhóm **TỒN CŨ** sẽ dài. Đo 29/09: 66 BH ngày 22–26/09, trong đó có ngày 26 anh đã bảo bỏ. Ghi hết những BH cố ý không up vào sổ bỏ qua để các lượt sau sạch.

**Tới đây thì dừng, chụp kết quả gửi anh Công xem**, rồi mới sang bước 5.

## Bước 5: ghi thật MỘT BH trước

Chọn một BH trong nhóm **SẼ TẠO**. Dùng lệnh chạy thử, thêm `--chi BHxxxxx --that`:

```
"C:\Claude Code\routines\quet-bh\.venv\Scripts\python.exe" "C:\Claude Code\routines\quet-bh\quet-bh-misa-len-erp.py" --tu-dong --chi BHxxxxx --that --bo-qua "<sổ>"
```

**Đạt khi** in ra `✅ BHxxxxx → SAL-ORD-… · tổng … khớp · SL … khớp · đã Submit`. Mở đơn đó trên ERP xem kho, người bán, ngày giao.

Hai lệnh xử ca tắc (thay phần sau `.py`):

```
--tu 2026-09-28 --chi BH04901 --cho-trung --that     ← người đã xác nhận "nghi trùng" là đơn thật
--tu 2026-09-25 --chi BH04852 --that                 ← up một BH tồn cũ đã được duyệt
```

## Bước 6: sửa routine của Tú

Trong app Claude trên máy Tú, mở routine đang chạy mỗi tiếng. **Thay toàn bộ lời dặn cũ** bằng đoạn dưới. Lệnh chép từ dòng *"Routine gọi"* trong `LENH.txt`.

```
Mỗi lượt chỉ làm đúng một việc: chạy lệnh "Routine gọi" trong
C:\Claude Code\routines\quet-bh\LENH.txt (có --tu-dong --that --bo-qua "<sổ bỏ qua>").

KHÔNG mở MISA, KHÔNG dùng Claude in Chrome, KHÔNG tự tạo, sửa hay huỷ đơn ERP bằng cách khác.

Đọc kết quả:
- Có "Lượt trước còn đang chạy" → dừng, không báo.
- Có "PHIÊN MISA ĐÃ HẾT" → báo Tú chạy lệnh "Đăng nhập MISA" trong LENH.txt.
- Dòng TÓM TẮT có tắc, tồn cũ hoặc lệch tiền lớn hơn 0 → báo Tú, chép NGUYÊN VĂN các nhóm đó, kèm số đơn đã tạo.
- Chỉ có "tạo N" (còn lại đều 0) → báo gọn một dòng: đã tạo N đơn, kèm số BH → số đơn.

Tú trả lời một BH tắc thì:
- "bỏ" → thêm số BH vào sổ bỏ qua.
- "up" / "đơn thật" → chạy lệnh với --chi BHxxxxx --that (thêm --cho-trung nếu đang nghi trùng; thêm --tu <ngày hạch toán> nếu là BH cũ).
- Mã hàng hoặc khách chưa có trên ERP → báo người phụ trách danh mục thêm, KHÔNG tự tạo.
```

## Máy tự kiểm những gì mỗi lượt

- **Chạy chồng:** khoá theo tiến trình. Lượt trước chưa xong thì lượt sau thoát ngay. Script không ngồi chờ người, nên không còn kiểu "đang chờ anh thì không tính là đang chạy".
- **Trùng:** kiểm số BH ở ô `po_no`, tính cả đơn nháp. Cùng khách, cùng tổng tiền với đơn khác trong ±7 ngày thì tắc.
- **Đọc đúng hàng:** cộng dòng hàng phải bằng tiền hàng BH, cộng VAT dòng phải bằng VAT BH. Dòng để trống thuế thì tắc.
- **Tạo xong:** đọc lại đơn thật. Kho, tổng tiền và tổng số lượng phải khớp MISA thì mới Submit. Lệch thì để **Nháp** và báo.
- **Ngày:** ngày đơn = Ngày hạch toán. Ngày giao = +7, trừ khi Diễn giải ghi GẤP **kèm ngày cụ thể** (vd `giao gấp 3/10`). Chữ "gấp" trần như "Gấp gọn đóng bao" không tính.

## Vẫn còn hở (không giấu)

- **Chưa chạy trên Windows lần nào.** Mọi lượt thử đều trên máy Mac của anh Công. Bước 2–5 trên máy Tú là lần chạy Windows đầu tiên. Lỗi thì chụp nguyên màn hình gửi anh.
- **Máy Tú phải bật.** Máy ngủ thì lượt đó không chạy. BH quá 1 ngày rơi vào TỒN CŨ, phải người duyệt.
- **Phiên MISA hết hạn** thì phải đăng nhập lại tay. Chưa đo được phiên sống bao lâu.
- **Cửa dữ liệu này là cửa nội bộ của web MISA,** không phải API công khai. MISA đổi giao diện thì script báo `Không bắt được cửa danh sách BH` và **không tạo bừa**.
- Đường bền hơn là xin MISA mở quyền Open API `get_list_sa_voucher` cho khoá công ty. Cần người có quyền **Quản trị** vào *Thiết lập → Kết nối ứng dụng*.
