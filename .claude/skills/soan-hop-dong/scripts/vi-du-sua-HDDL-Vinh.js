const D = require("./lib2.js");
const R = "C00000", O = "BF8F00", G = "375623", K = "keep";
const LEG = [
  [["CHÚ GIẢI MÀU (bản đề xuất điều chỉnh của NTC, ngày 20/10/2026): ", null, true], ["Đỏ = nội dung bắt buộc sửa", R, false], [" · ", null, false], ["Vàng cam = nội dung nên sửa hoặc cần làm rõ", O, false], [" · ", null, false], ["Xanh lá = nội dung đề xuất thêm để bảo vệ quyền lợi các bên", G, false]],
  [["[Điền Nội dung]", R, true], [" = chỗ còn thiếu, phải điền trước khi ký · ", null, false], ["[Xác nhận lại]", R, true], [" = đã có thông tin nhưng cần đối chiếu, xác minh", null, false]],
];
const SOHD = "[Điền Nội dung — số HĐ do kế toán cấp theo sổ]/2026/HĐĐL-NTC";

// ===== HỢP ĐỒNG =====
const h = new D("hd");
h.legend(LEG);
h.replace("…/2026/HDDL-NTC", SOHD, R, true);
h.replaceParts("Tây Ninh, ngày 10 tháng 09 năm 2026", [["Tây Ninh, ngày 10 tháng 09 năm 2026 ", K], ["[Xác nhận lại — ngày ký thực tế]", R, true]]);
h.cloneAfter("- Mã số thuế: 2901217883", [["[Xác nhận lại — Giấy CN ĐKDN đang có trong hồ sơ là bản thay đổi lần 2 ngày 28/05/2012, chưa có ngành bán buôn/bán lẻ nệm; đề nghị Bên B cung cấp bản mới nhất]", R, true]]);
h.replace("0,05%/ngày", "0,03%/ngày", O);
h.cloneAfter("5.4. Các giao dịch phát sinh", [["5.5. Bên A xuất hóa đơn giá trị gia tăng cho Bên B theo đúng quy định pháp luật. Bên B có trách nhiệm cung cấp và cập nhật kịp thời thông tin xuất hóa đơn (tên, mã số thuế, địa chỉ, email nhận hóa đơn). Trường hợp Bên B cung cấp thông tin sai dẫn đến hóa đơn phải điều chỉnh, thay thế, Bên B chịu trách nhiệm về chi phí và hậu quả phát sinh.", G]]);
h.replaceParts("Tòa án có thẩm quyền để giải quyết.", [["Tòa án ", K], ["nhân dân ", R], ["có thẩm quyền ", K], ["tại Thành phố Hồ Chí Minh ", R], ["để giải quyết.", K], [" Phán quyết của Tòa án là chung thẩm và có hiệu lực bắt buộc đối với Các Bên. Bên thua kiện chịu toàn bộ án phí và chi phí hợp lý liên quan.", R]]);

// ===== PHỤ LỤC =====
const p = new D("pl");
p.legend(LEG);
p.replace("…/2026/PLHD-NTC", "[Điền Nội dung — số phụ lục, thường là 01]/2026/PLHĐ-NTC", R, true);
p.replace("…/2026/HDDL-NTC", SOHD, R, true, 3);
p.cloneAfter("- Đối với đơn hàng đầu tiên:", [["- Từ đơn hàng thứ hai trở đi, thời hạn thanh toán áp dụng theo Điều 5.1 Hợp Đồng.", O]]);
p.replaceParts("hai Bên sẽ thống nhất giá trị hoàn lại nếu có khi thanh lý Hợp Đồng.", [
  ["Bên B hoàn lại cho Bên A giá trị tài trợ tương ứng với thời gian còn lại của Hợp Đồng ", O], ["[Xác nhận lại — cách tính hoàn lại]", R, true],
  [", trừ trường hợp Hợp Đồng chấm dứt do lỗi của Bên A; khoản hoàn lại được đối trừ khi thanh lý Hợp Đồng.", O]]);
p.replaceParts("tối thiểu 200.000.000 đồng.", [["tối thiểu 200.000.000 đồng (Hai trăm triệu đồng).", K]]);

h.save(); p.save();
for (const [n, d] of [["HỢP ĐỒNG", h], ["PHỤ LỤC", p]]) { console.log("== " + n); d.log.forEach(l => console.log("   " + l.slice(0, 150))); }
