const D = require("./lib2.js");
const R = "C00000", O = "BF8F00", G = "375623", K = "keep";
const LEG = [
  [["CHÚ GIẢI MÀU (bản đề xuất điều chỉnh của NTC, ngày 22/10/2026): ", null, true], ["Đỏ = nội dung bắt buộc sửa", R, false], [" · ", null, false], ["Vàng cam = nội dung nên sửa hoặc cần làm rõ", O, false], [" · ", null, false], ["Xanh lá = nội dung đề xuất thêm để bảo vệ quyền lợi các bên", G, false]],
  [["[Điền Nội dung]", R, true], [" = chỗ còn thiếu, phải điền trước khi ký · ", null, false], ["[Xác nhận lại]", R, true], [" = đã có thông tin nhưng cần đối chiếu, xác minh", null, false]],
];
// chèn tên người ký vào ô chữ ký Bên A: thêm 1 đoạn sau đoạn trống kế đoạn chức danh
function addSignerName(d, titleText, name) {
  const t = d.paras().filter(p => D.text(p.xml) === titleText || D.text(p.xml) === "PHÓ GIÁM ĐỐC");
  if (t.length !== 1) throw new Error("chức danh gặp " + t.length);
  const all = d.paras(); const k = all.findIndex(p => p.s === t[0].s); const blank = all[k + 1], next = all[k + 2];
  if (D.text(blank.xml) !== "") throw new Error("đoạn sau chức danh không trống");
  const rs = D.runs(t[0].xml); const rpr = (rs[rs.length - 1].rpr || "<w:rPr></w:rPr>").replace(/<w:color [^>]*\/>/, "").replace("</w:rPr>", `<w:color w:val="${R}"/></w:rPr>`);
  const run = `<w:r>${rpr}<w:t xml:space="preserve">${name}</w:t></w:r>`;
  const sameCell = next && !d.x.slice(blank.e, next.s).includes("</w:tc>");
  if (sameCell && D.text(next.xml) === "") {           // còn dòng trống sẵn trong ô → điền tên vào đó
    const nx = next.xml.replace(/<\/w:p>$/, run + "</w:p>");
    d.x = d.x.slice(0, next.s) + nx + d.x.slice(next.e);
  } else {                                               // hết dòng → giãn dòng trống rồi thêm đoạn tên
    let bx = blank.xml;
    bx = /<w:spacing [^>]*w:after=/.test(bx) ? bx.replace(/(<w:spacing [^>]*)w:after="\d+"/, '$1w:after="960"') : bx.replace("<w:spacing ", '<w:spacing w:after="960" ');
    let ppr = (t[0].xml.match(/<w:pPr>[\s\S]*?<\/w:pPr>/) || [""])[0].replace(/w:after="\d+"/, 'w:after="0"');
    const np = `<w:p>${ppr}${run}</w:p>`;
    d.x = d.x.slice(0, blank.s) + bx + np + d.x.slice(blank.e);
  }
  d.log.push("thêm tên người ký Bên A: " + name + (sameCell ? " (điền vào dòng trống sẵn)" : " (thêm dòng)"));
}

// ===== HỢP ĐỒNG =====
const h = new D("hd");
h.legend(LEG);
h.replaceParts("GIÁM ĐỐC", [["PHÓ ", R], ["GIÁM ĐỐC", K]]);
addSignerName(h, "PHÓ GIÁM ĐỐC", "LÊ VĂN QUANG");
h.replaceParts("vòng (30) ngày", [["vòng ba mươi (30) ngày", K]]);

// ===== PHỤ LỤC =====
const p = new D("pl");
p.legend(LEG);
p.replace("Tám mươi ba triệu, chín trăm lẻ tám nghìn, ba trăm lẻ năm nghìn đồng", "Tám mươi ba triệu chín trăm lẻ tám nghìn ba trăm lẻ năm đồng", R);
p.replace("trong tháng 10/2026", "chậm nhất ngày 31/10/2026", O);
p.replace("trong tháng 11/2026", "chậm nhất ngày 30/11/2026", O);
p.cloneAfter("- Đối với đơn hàng đầu tiên:", [["- Từ đơn hàng thứ hai trở đi, thời hạn thanh toán áp dụng theo Điều 5.1 Hợp Đồng.", O]]);
p.replaceParts("Giá trị đơn hàng đầu tiên của Bên B tối thiểu 500.000.000 đồng (bằng chữ: Năm trăm triệu đồng).", [
  ["Giá trị đơn hàng đầu tiên của Bên B tối thiểu 500.000.000 đồng (bằng chữ: Năm trăm triệu đồng). ", K],
  ["[Xác nhận lại — đơn đầu BH05069 ngày 07/10/2026 trị giá 436.419.154 đồng, chưa đạt 500.000.000 đồng. Nếu tính cộng dồn thì ghi rõ: tổng giá trị các đơn hàng Bên B đặt từ ngày 20/09/2026 đến hết ngày [Điền Nội dung] tối thiểu 500.000.000 đồng]", R, true]]);
p.replaceParts("hai Bên sẽ thống nhất giá trị hoàn lại nếu có khi thanh lý Hợp Đồng.", [
  ["Bên B hoàn lại cho Bên A giá trị tài trợ tương ứng với thời gian còn lại của Hợp Đồng ", O], ["[Xác nhận lại — cách tính hoàn lại]", R, true],
  [", trừ trường hợp Hợp Đồng chấm dứt do lỗi của Bên A; khoản hoàn lại được đối trừ khi thanh lý Hợp Đồng.", O]]);
p.cloneAfter("+ Thời điểm thanh toán:", [["+ Hồ sơ hỗ trợ: Bên B cung cấp cho Bên A hình ảnh bảng hiệu đã hoàn thiện và biên bản nghiệm thu bảng hiệu có xác nhận của nhân viên kinh doanh Bên A trước khi nhận khoản hỗ trợ. ", G], ["[Xác nhận lại — kế toán xác định chứng từ cần có để hạch toán khoản hỗ trợ]", R, true]]);
p.replaceParts("tối thiểu 500.000.000 đồng.", [["tối thiểu 500.000.000 đồng (Năm trăm triệu đồng).", K]]);
p.replaceParts("ngày 20  tháng 09  năm 2026", [["ngày 20 tháng 09 năm 2026", K]]);
p.replaceParts("Nơi Cấp", [["Nơi cấp", K]]);
addSignerName(p, "PHÓ GIÁM ĐỐC", "LÊ VĂN QUANG");

h.save(); p.save();
for (const [n, d] of [["HỢP ĐỒNG", h], ["PHỤ LỤC", p]]) { console.log("== " + n); d.log.forEach(l => console.log("   " + l.slice(0, 150))); }
