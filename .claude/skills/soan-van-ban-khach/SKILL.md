---
name: soan-van-ban-khach
description: Soạn văn bản gửi khách hàng của Nệm Thành Công (thông báo, báo giá, thư ngỏ, chính sách, xác nhận đơn…) theo đúng định dạng & giao diện mẫu chuẩn của công ty (header logo TC + địa chỉ, thanh kẻ navy/xanh, tiêu đề lớn, mục đánh số tròn, khối nhạt, chân ký + thanh footer navy). Dùng khi công chúa nhờ soạn thông báo, báo giá, văn bản, công văn hay bất cứ thứ gì để gửi cho khách.
---

# Soạn văn bản gửi khách – mẫu chuẩn Nệm Thành Công

Mọi văn bản gửi khách (thông báo, báo giá, thư ngỏ, chính sách, xác nhận…) **phải dùng đúng giao diện này**.

- Ảnh mẫu gốc: `assets/mau-goc-thong-bao-03-2026.jpg` (Thông báo số 03/2026/TB-KD) — xem để đối chiếu giao diện.
- Khung HTML khổ A4: `assets/mau-van-ban.html` — copy ra rồi thay các `{{...}}`.
- Logo: `assets/logo-tc.png` (để cùng thư mục với file HTML khi xuất).

## Cấu trúc bắt buộc (theo thứ tự)

1. **Header**: logo TC bên trái + "CÔNG TY CỔ PHẦN SẢN XUẤT & THƯƠNG MẠI / NỆM THÀNH CÔNG" (navy, đậm);
   bên phải: "Đường số 8, CCN Hoàng Gia, ấp Mới 2, Xã Mỹ Hạnh, Tỉnh Tây Ninh / Hotline: 1800 646 836 / nemthanhcong.com".
2. **Thanh kẻ** 2 màu: navy ~3/4 bên trái, xanh da trời ~1/4 bên phải.
3. Dòng **Số: xx/2026/TB-KD** (trái) — **Tây Ninh, ngày … tháng … năm …** (phải, in nghiêng).
   Ký hiệu số: `TB-KD` thông báo, `BG-KD` báo giá (hỏi công chúa nếu chưa rõ số).
4. **Tiêu đề lớn in hoa đậm** (THÔNG BÁO / BÁO GIÁ / THƯ NGỎ…) + dòng **V/v: …** màu navy.
5. **Kính gửi: …** (đậm) + đoạn mở đầu cảm ơn khách; ý chính **in đậm**.
6. **Băng nổi bật** (tùy chọn): khối navy bên trái (tiêu đề in hoa + dòng phụ) + ô xanh da trời bên phải chứa con số lớn
   (giờ chốt, % chiết khấu, ngày hiệu lực, tổng tiền…).
7. **Các mục đánh số** trong vòng tròn navy (hoặc xanh cho mục phụ), tiêu đề mục màu navy. Nội dung mục dùng 1 trong:
   - khối nền nhạt viền trái navy, 2 cột (nhãn đậm | nội dung, ví dụ in nghiêng xám);
   - 2 thẻ nền xanh nhạt với số lớn màu xanh;
   - **bảng giá** `table.tb` (đầu bảng navy, dòng xen kẽ, dòng tổng nền xanh nhạt) — dùng cho báo giá;
   - gạch đầu dòng chấm navy.
8. Đoạn kết (cụm cần nhấn mạnh tô **xanh đậm**) + "*Trân trọng cảm ơn sự đồng hành của Quý khách hàng!*".
9. **Chân**: "Nơi nhận" bên trái (Như trên; Ban Giám đốc (để b/c); bộ phận liên quan (để t/h); Lưu: P.KD B2B)
   — bên phải "TM. CÔNG TY / GIÁM ĐỐC", chỗ trống ký + đóng mộc, tên **Phạm Văn Bình** (hỏi nếu người ký khác).
10. **Thanh footer navy** sát đáy: "NỆM THÀNH CÔNG · Thương hiệu: NỆM VIỆT NHẬT – NỆM THUẦN VIỆT".

## Quy tắc

- Văn phong lịch sự, xưng "Công ty" – "Quý khách hàng". Gọn trong **1 trang A4** nếu được.
- Báo giá: giá luôn **đã gồm VAT 8%** (theo CLAUDE.md), ghi rõ "(đã gồm VAT 8%)" ở đầu cột/dòng tổng; định dạng số `572.000`.
- **Không tự chèn chữ ký / mộc đỏ** — để trống ô ký cho công chúa tự ký, đóng mộc.
- Xuất bản: render HTML → PDF/PNG khổ A4 bằng Playwright (Chromium có sẵn), `printBackground: true`,
  rồi gửi file cho công chúa; nếu cần sửa thì sửa HTML và xuất lại.
