# Ghi chú cho Claude

## Quy tắc giá nghiệp vụ (ERP Người Thuần Việt)

### Báo giá cho người dùng luôn là giá ĐÃ GỒM VAT

- Người dùng (xưng "công chúa", gọi Claude là "nô tì") hỏi giá thì **luôn báo giá đã gồm VAT 8%**.
- Quy đổi: `giá có VAT = price_list_rate × 1,08`, làm tròn đến đồng (ví dụ 529.629,63 → 572.000đ).
- Chỉ báo thêm giá chưa VAT khi được hỏi hoặc khi sắp ghi giá vào ERP.

### Cách khách gọi tên hàng

- **"Cstn"** (cao su thiên nhiên) = dòng **Natural**, tên đầy đủ "Nệm Cao Su Thiên Nhiên Việt Nhật Natural", mã `NAxx-y` (ví dụ `NA10-6`).
  Không nhầm với Nano gấp (`NA2xx`, `NA3xx`).
- Cách ghi kích thước: "1m6 x 15p sl 2t" = rộng 160cm × dày 15cm, số lượng 2 tấm (dài mặc định 200cm).

### Nệm gấp 2 / gấp 3 = giá nệm thường cùng loại + 150.000đ

- Giá nệm gấp 2, gấp 3 **luôn bằng giá nệm thường cùng dòng, cùng độ dày, cùng kích thước + 150.000đ (đã gồm VAT)**.
- Áp dụng cho **mọi bảng giá** (đại lý Miền Nam/Trung/Bắc, bán sỉ, Standard Selling…), trừ khi người dùng nói khác.
- Ví dụ: Nệm Sora 10cm 100x200 (`SORA10-1`) = 572.000đ → Nệm Sora 100x200x10 Gấp 3 (`SR310`) = 722.000đ.
- Các dòng đã xác nhận áp dụng:
  - **Sora**: mã gấp 3 là `SR3xx`.
  - **Nano**: mã gấp 2 là `NA2xx`, mã gấp 3 là `NA3xx` (ví dụ `NA310-3` = Nano 160x200x10 Gấp 3).
    Nano gấp ghép với nệm **Nano thường**, không ghép với **Nano Plus** (`NANP…`) vì đó là dòng khác.
    Nano thường có nhiều mã trùng cùng kích thước (`NAN10`, `NANO10`, `NAN10-1` đều là 100x200x10).
    Nếu giá các mã trùng này khác nhau, hỏi lại người dùng nên lấy giá của mã nào.

**Lưu ý VAT:** `price_list_rate` trong ERP lưu giá **chưa VAT 8%** (572.000đ được lưu là 529.629,63).
Khi nhập vào ERP, phần cộng thêm phải quy về chưa VAT: 150.000 / 1,08 = **138.888,89đ**.
Công thức: `giá_gấp (ERP) = (giá_thường_có_VAT + 150.000) / 1,08`.
Đã đối chiếu: Standard Selling của `SR310` = 668.518,52 = 722.000 / 1,08.

**Ghép mã nệm gấp với nệm thường theo tên sản phẩm** (dòng, độ dày, kích thước), không suy theo hậu tố mã:
hậu tố của mã gấp không trùng với mã thường (`SORA10-1` là 100x200 nhưng `SR310-1` là 120x200).

### Đưa đơn từ Misa lên ERP

- Chỉ đưa lên **chứng từ bán hàng** của Misa, tức các số chứng từ bắt đầu bằng **`BH`** (ví dụ `BH00123`).
- Mỗi chứng từ `BH` tạo thành một **Đơn bán hàng (Sales Order)** trên ERP, không tạo Hóa đơn bán hàng (Sales Invoice).
- **Không** đưa lên đơn đặt hàng, tức các số chứng từ bắt đầu bằng **`ĐH`** (hoặc `DH`), dù chúng có trong file xuất từ Misa.
- Lọc theo tiền tố số chứng từ trước khi ghép khách hàng hoặc mã hàng. Báo lại cho người dùng số đơn `ĐH` đã bỏ qua.
- Số chứng từ Misa ghi vào ô **`po_no`** (số PO của khách) trên Sales Order, ví dụ `SAL-ORD-2026-00495` có `po_no` = `BH05132`.
- Trước khi tạo đơn, kiểm tra trên ERP xem số `BH` đó đã có Sales Order có `po_no` trùng chưa (tính cả đơn nháp). Đã có thì bỏ qua, không tạo trùng.
