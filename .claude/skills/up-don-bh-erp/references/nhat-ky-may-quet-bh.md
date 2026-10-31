> Chép từ bộ nhớ Claude trên máy tính của Ngọc Tú ngày 31/10/2026. Đường dẫn `C:\…`, `D:\…` là của
> máy tính đó; trên iPad/iPhone thì dữ liệu do Tú gửi kèm. Chữ "anh Tú"/"chị" = công chúa (Tú).

**TỪ 29/09/2026 ROUTINE DÙNG MÁY QUÉT BH (script), KHÔNG BẤM MISA BẰNG CHROME NỮA.** Gói do anh Công viết
(`C:\Claude Code\routines\goi-quet-bh\`), cài ở `C:\Claude Code\routines\quet-bh\`: Python 3.12 (winget, user) +
venv + Playwright. Script đọc MISA qua cửa dữ liệu nội bộ (`sa_voucher_get/paging_filter_v2`,
`get_paging_detail`), chi tiết theo mã từng BH, dùng hồ sơ Chrome riêng chạy ẩn
(`~\.ntv-secrets\chrome-misa`). Khoá ERP: script tự đọc `C:\Claude Code\.mcp.json` (khoá của
ngoctu.7431@gmail.com, đã kiểm). **30/09/2026 đã cập nhật lên bản gộp của anh Công** (gói ở
`D:\CLAUDE\goi-quet-bh\`, 19:26 29/09): chỉ thay 5 file `.py`, giữ nguyên `.cmd` (nội dung giống, giữ để quyền
"Always allow" khớp). Bản cũ cất ở `routines\_bỏ\quet-bh-truoc-cap-nhat-30-09-2026\`. Lần sau có gói mới: so
hash, cất bản cũ vào `_bỏ`, chép, chạy `xem-thu.cmd` rồi mới báo. Routine chỉ chạy `chay-routine.cmd` mỗi giờ, và `doi-chieu.cmd` (chỉ đọc)
mỗi ngày một lần. Lệnh ở `quet-bh\LENH.txt`, nhật ký ở `quet-bh\log\`. MISA đăng xuất thì chạy lệnh
"Đăng nhập MISA" trong LENH.txt: Tú tự đăng nhập, rồi đóng cửa sổ. Nếu Tú quên đóng, đóng bằng
`CloseMainWindow` để cookie được lưu, đừng kill tiến trình.
Why: đọc bằng Chrome gãy 28/09/2026 (đọc nhầm chi tiết, chạy chồng, Chrome tắt). How: đừng quay lại
Claude in Chrome cho việc này. Script lỗi thì báo nguyên văn, không tự làm tay.
**MISA đăng xuất (Tú muốn "tự động đăng nhập", 29/09/2026):** Claude KHÔNG được gõ hay cất mật khẩu, luật
cấm kể cả khi Tú cho phép. Cách thay: routine chạy `quet-bh\dang-nhap-misa.cmd` để mở sẵn cửa sổ đăng
nhập (chạy tách, không treo), rồi PushNotification cho Tú. Tú đăng nhập, đóng cửa sổ, lượt sau tự chạy.
Đừng đề xuất lưu mật khẩu vào script hay file.
**Lệch ERP↔MISA: tự đào dữ liệu trước, đừng đẩy Tú đi hỏi kế toán (Tú nhắc "em tự xử lý được mà", 29/09/2026).**
Why: máy quét đọc được chi tiết dòng hàng MISA theo mã BH, và MCP ERP đọc được đơn, phiếu giao. Bảo Tú "xin kế
toán chi tiết" là đẩy việc mình làm được. How: tự viết script CHỈ ĐỌC ở scratchpad, import
`quet-bh-misa-len-erp.py` rồi gọi `headers_misa()`, `quet_bh()`, `quet_dong_bh(H, refid)` (không sửa script gốc).
So từng dòng với SO, rồi trình Tú đúng từng thay đổi (đơn nào, dòng nào, SL/giá cũ → mới) để gật một lần.
Chỉ hỏi kế toán khi dữ liệu MISA tự nó mâu thuẫn, hoặc việc chạm kho (huỷ phiếu giao).
**Kế toán sửa BH sau khi up → máy TỰ SỬA SO cho khớp (Tú chốt 29/09/2026: "tự động rà soát các phiếu BH trên misa
nếu có thay đổi và cập nhật lại trên ERP để khớp số liệu").** Script `quet-bh\cap-nhat-lech-bh.py` (Claude viết
29/09/2026) + `cap-nhat-lech.cmd`, routine gọi mỗi lượt (Bước 1b SKILL.md), quyền đã thêm vào settings.json. Sửa bằng
"Cập nhật mặt hàng" (`update_child_qty_rate`), KHÔNG Cancel. Chỉ tự sửa khi chưa xuất hoá đơn, không dòng nào xuống
dưới số đã giao, mã hàng có sẵn, thuế khớp, và tính trước tổng khớp MISA ±2đ. Sai mã hàng đã giao (vd BH04854) thì báo,
việc của kho. Why: Tú muốn ERP luôn khớp MISA mà không phải trình từng đơn. How: đã được phép sẵn, đừng hỏi lại cho
từng đơn. Số BH nhắc trong sổ phải viết không kèm "BH" nếu muốn máy vẫn so tiền BH đó.
**NGOẠI LỆ: đơn đã có phiếu giao mà bị sửa mặt hàng ngay trên ERP thì KỆ (Tú chốt 15/10/2026, sau khi thấy máy đảo
SAL-ORD-2026-00429 1000→840→1000 mỗi giờ: anh Tùng trả hàng 160 tấm GNCSAL, máy "sửa lại cho khớp MISA").**
Nguyên tắc: **thay đổi từ MISA thì cập nhật về ERP; thay đổi phát sinh từ ERP thì KHÔNG đồng bộ lại cho giống MISA.**
Cách làm (sửa 15/10/2026, bản cũ ở `routines\_bỏ\cap-nhat-lech-bh (truoc luat ERP sua thi ke, 15-10-2026).py`): `cap-nhat-lech-bh.py`
ghi mốc `quet-bh\log\cap-nhat-lech-trang-thai.json` = {số BH: {ver = `edit_version` BH trên MISA, so = tên SO}} mỗi lượt
mà ERP đang khớp MISA (tổng ±2đ); gieo mốc lần đầu bằng `cap-nhat-lech-bh.py --gieo` (15/10/2026 11:01, 261 BH, không sửa gì).
Khi ERP lệch MISA: nếu `edit_version` MISA **y như mốc** (MISA không đổi → lệch do sửa bên ERP) VÀ đơn có Delivery Note chưa huỷ
(kể cả phiếu trả hàng, người nào tạo cũng được) → BỎ QUA, in mục "BỎ QUA vì đơn đã có phiếu giao và sửa ngay trên ERP"
(không vào "không tự sửa được", không báo Tú). MISA đổi (`edit_version` khác mốc) → sửa về ERP như cũ rồi cập nhật mốc.
`quet-bh-misa-len-erp.py` (`erp_sua_da_giao`) dùng cùng mốc để KHÔNG báo "TIỀN LỆCH" cho các đơn đó. BH chưa có mốc (đang lệch
từ trước khi gieo) → giữ cách cũ. Tra phiếu giao/mốc lỗi → giữ cách cũ. Không đọc được bảng Version của ERP (403) nên không dùng
lịch sử sửa. Giới hạn: kế toán đụng BH trên MISA mà `edit_version` đổi dù nội dung không đổi → máy coi là MISA đổi, đồng bộ lại
(có thể đè bản anh Tùng sửa); đơn CHƯA có phiếu giao thì vẫn đồng bộ về MISA như cũ.
Đổi `po_no` trên SO đã Submit: MCP `update_document` làm được (đã làm 00245, 00244 ngày 29/09/2026).
**Máy nghỉ / MISA đăng xuất nhiều ngày (Tú: "xử lý triệt để rủi ro", 29/09/2026):** máy quét ghi mốc
`quet-bh\log\lan-quet-thanh-cong.txt` sau mỗi lượt GHI THẬT quét trọn. Lượt sau tự up BH từ ngày của mốc,
dòng in ra là "BÙ NGÀY LỠ". Nên BH của những ngày lỡ KHÔNG rơi vào "tồn cũ". Tồn cũ chỉ còn nghĩa: đã có
lượt thấy mà vẫn chưa lên ERP. Sàn là **01/10/2026** (Tú chốt 01/10/2026: "up đơn BH bắt đầu từ ngày hạch toán 01/10/2026"; trước là
24/09/2026). Sàn nằm ở `SAN_MOC` trong `quet-bh-misa-len-erp.py`. BH trước 01/10 không tự up nữa, kể cả bù
ngày lỡ. Phần rà BH đã sửa (`cap-nhat-lech-bh.py`, `SAN`) vẫn giữ 24/09 để đơn cũ vẫn khớp MISA.
**MISA mở ở chỗ khác (từ 30/09/2026):** máy quét dừng với dòng "TÀI KHOẢN MISA ĐANG MỞ Ở CHỖ KHÁC", vì cùng tài
khoản đang mở trên Chrome hoặc ô web trong app Claude (việc tạo ĐH MISA, xem `misa-tao-don-dat-hang`). Máy
không tự bấm "Tiếp tục đăng nhập". Xử lý: đóng MISA ở chỗ kia, lượt sau tự chạy và bù. Routine nhắc Tú MỖI lượt khi MISA đăng xuất, và gửi
"nhịp tim" cuối ngày từ 17:00 (bao-cuoi-ngay.txt): tới 18:00 chưa nhận là máy hoặc routine chết. Máy Tú
(kiểm 29/09/2026, `powercfg /a`) KHÔNG có chế độ ngủ nào, chỉ có ngủ đông, và ngủ đông = "Không bao giờ".
Nên máy không tự ngủ. Số 15 phút `STANDBYIDLE` trong powercfg là số chết, không có tác dụng: đừng báo
nhầm là "máy ngủ sau 15 phút". Claude đã bật tự mở khi khởi động (ClaudeStartup). Claude không sửa cài
đặt hệ thống: việc đó để Tú bấm.
**Thông báo Telegram (dựng 29/09/2026):** bot riêng của Tú. Mã bot và chat_id nằm ở
`~\.ntv-secrets\telegram.env`, do Tú tự dán qua `quet-bh\cai-tele.cmd`. Claude KHÔNG đọc, KHÔNG in mã bot.
`chay-routine.cmd` và `cap-nhat-lech.cmd` tự gọi `tele.py --tu-log` sau mỗi lượt: có chuyện mới báo, tin
trùng trong ngày không gửi lại (`log\tele-da-gui.json`), MISA đăng xuất thì nhắc mỗi lượt. Gửi tay:
`gui-tele.cmd "nội dung"`. Tin nhắn không tới thì kiểm file cài còn không, rồi chạy lại cai-tele.cmd.
**Sổ bỏ qua KHÔNG chứa BH đã up nữa** (tách ra `routines\misa-bh-da-up.md`), vì máy quét bỏ qua mọi số BH
trong sổ, tức bỏ luôn bước so tiền. Đối chiếu 29/09/2026 tìm ra: BH04879/04880/04850 bị kế toán xoá trên
MISA → đơn 00245/00244/00225 thừa (00245, 00244 trùng BH04903, BH04901). 11 đơn BH ngày 24/09
(00208–00218) bị `nvtungjob` huỷ lúc 18:50 ngày 24/09/2026 mà sổ cũ không biết. Máy quét dừng hỏi khi
cùng khách + cùng tiền trong ±7 ngày (thay luật 24/09 "khác số BH vẫn up").
**NGHI TRÙNG phải so cả SẢN PHẨM (Tú sửa lưng 07/10/2026: "sản phẩm của 2 đơn có giống nhau đâu").** Máy quét
(`nghi_trung` trong quet-bh-misa-len-erp.py, sửa 07/10/2026) chỉ chặn khi cùng khách + cùng tổng tiền ±7 ngày
VÀ cùng {(mã hàng, kích thước hạ size): số lượng}. **Tấm nguyên ≠ tấm cắt hạ size** dù cùng mã (BH04986 NA10-6
hạ size 150×190 vs BH05092 NA10-6 tấm nguyên, cùng 4.778.000). Kích thước lấy từ ghi chú dòng ("Hạ size 150cm x
190cm x 10cm"), ERP lưu ở cột Mô tả. Khác hàng thì up bình thường. Why: chặn oan làm Tú phải đi gỡ. How: khi Tú bảo up một
BH nghi trùng, em phải so dòng hàng hai đơn trước rồi báo rõ giống/khác, đừng up mà không nhìn hàng.
**Nhịp routine: 2 TIẾNG/LẦN từ 19/10/2026 (Tú: "mỗi 2 tiếng cập nhật 1 lần, không cần 1 tiếng"; trước đó 1 tiếng).** Tác vụ `misa-bh-sync`,
cron `0 1-23/2 * * *` (giờ lẻ 01h…23h, lệch vài phút do jitter) để vẫn có một lượt rơi vào 17:xx cho "nhịp tim" cuối ngày (Bước 5, lượt đầu từ 17:00).
BH mới lên ERP và lệch ERP↔MISA được sửa chậm tối đa ~2 giờ.
**KHÔNG CỘNG GỘP MÃ HÀNG + MÔ TẢ PHẢI CÓ, VIẾT NGẮN (Tú chốt 19/10/2026: "không được cộng gộp mã hàng"; "BH có mô tả/ghi chú thì ERP cũng
phải có, đừng thiếu, nhưng viết ngắn").** Mỗi dòng MISA = một dòng ERP (vd PVH10-6 ×6 và PVH10-6 ×1 "Cắt dán" là HAI dòng). Code ở
`routines\quet-bh\dong_bh.py` (`lap_plan` ghép 1-1 theo mã + kích thước cắt trong ghi chú, lượt 3 ghép dòng ERP mất mô tả; `rut_gon`: "Cắt dán:
250cm x 200cm x 10cm" → "Cắt dán 250x200x10cm"; `chuan`/`cac_ghi_chu` bỏ trùng). `cap-nhat-lech-bh.py` dùng `lap_plan` thay cho gộp theo mã;
`quet-don-misa-len-erp.py` `dung_don` ghi mô tả đã rút gọn (bỏ diễn giải mặc định "Bán hàng <khách>"). ⚠️ `update_child_qty_rate` GHI ĐÈ Mô tả của MỌI dòng
(đọc mã nguồn ERPNext 19/10/2026) nên LUÔN truyền `description` — lần sửa BH05237/SO 00609 (15/10/2026) quên truyền nên mất sạch ghi chú. Sau mỗi lần sửa
máy kiểm lại Mô tả còn không, mất thì báo ⚠️. Tổng khớp mà MISA vừa sửa (`edit_version` đổi) cũng soi lại dòng+mô tả. Bản cũ ở
`routines\_bỏ\cap-nhat-lech-bh (truoc luat khong gop ma, 19-10-2026).py`. CHƯA khôi phục ghi chú đã mất trên đơn cũ (00609, BH04981, 05040, 05064, 05088,
05119, 05124, 05146, 05156, 05189) — chờ Tú gật.
**Đơn anh Tùng đã Xuất phiếu giao hàng → KHÔNG up BH của đơn đó (Tú chốt 14/10/2026: "những đơn nào anh Tùng đã bấm
Xuất phiếu giao hàng trên ERP rồi thì đừng up đơn BH đó nữa"; làm sống lại, có thu hẹp, luật 24/09 đã huỷ).** Máy quét
(`phieu_giao_cua_tung` + `DA_GIAO` trong quet-bh-misa-len-erp.py, sửa 14/10/2026, bản cũ ở `routines\_bỏ\quet-bh-misa-len-erp
(truoc luat phieu giao anh Tung, 14-10-2026).py`): BH nghi trùng (cùng khách + cùng tổng ±1đ + cùng {mã hàng, hạ size: SL}
trong ±7 ngày) mà MỌI đơn ERP trùng đó đều có Delivery Note chưa huỷ do `nvtungjob@gmail.com` tạo → BỎ, in mục "BỎ QUA vì
đơn trùng đã có phiếu giao của anh Tùng", KHÔNG vào "TẮC" nên không báo Tú. Đơn trùng chưa giao, hoặc phiếu giao do người
khác tạo → vẫn dừng hỏi như cũ. Chưa phủ: đơn anh Tùng tự nhập + xuất phiếu mà tổng tiền/hàng KHÁC BH (không coi là trùng, máy
vẫn up) — muốn phủ thì hỏi Tú nới điều kiện. Đã thử mô phỏng BH05203 (trùng 00473/BH05109, phiếu MAT-DN-2026-00349): ra bỏ đúng.
Lưu ý: anh Tùng cũng tự lập SO mang po_no = số BH rồi giao luôn (BH05203→00586, BH05019→00587, 13/10/2026 23:02) — máy thấy po_no
đã có nên bỏ qua, không trùng. Tra phiếu giao lỗi thì giữ cách cũ (dừng hỏi), không bỏ oan.
**Đơn ERP bị anh Tùng (nvtungjob) huỷ → bỏ luôn BH đó (Tú chốt 05/10/2026: "anh Tùng hủy thì thôi").** Không up lại
(`--tao-lai`), không hỏi Tú. Sổ có mục "## Bỏ vĩnh viễn: đơn ERP đã bị anh Tùng (nvtungjob) huỷ" (BH04948, BH04974,
11 BH ngày 24/09). SKILL.md Bước 3 tự xếp vào đó. Người khác huỷ thì vẫn hỏi Tú.
**Bảng đổi mã MISA → ERP (từ 05/10/2026):** `quet-bh\doi-ma-misa-erp.json` (vd `"TPET169": "TPET169*8"`, Tú chốt
05/10/2026). `quet_dong_bh` tự đổi mã trước khi kiểm, áp cho cả máy quét lẫn máy sửa lệch. Chỉ thêm cặp mã khi Tú
chốt là cùng một hàng. Mã MISA gần giống mã ERP thì hỏi Tú, đừng tự đoán.
**BH thiếu KHÁCH trên ERP → máy TỰ lấy thông tin khách ở MISA tạo sang ERP rồi up đơn (Tú chốt 15/10/2026: "không có mã khách
hàng thì lấy thông tin khách hàng ở MISA đồng bộ qua rồi tạo luôn").** Máy quét (`tao_khach_tu_misa`, `khach_nghi_trung`, `KHACH_MOI`
trong quet-bh-misa-len-erp.py; bản cũ ở `routines\_bỏ\quet-bh-misa-len-erp (truoc tu tao khach tu MISA, 15-10-2026).py`): khi
`tim_customer` ra "(0 ứng viên)" thì tạo Customer (customer_name = tên MISA, customer_type Company, group "Khách lẻ B2C", tax_id nếu mã
MISA là MST 10/13 số hoặc 12 số, mobile_no/email nếu có, `customer_details` = "mã MISA: <mã> · Tạo tự động từ BH…" để lần sau
tim_customer khớp) + Address Billing (địa chỉ, phường, tỉnh từ BH) + Contact (nếu có SĐT/email). CHỐNG TRÙNG trước khi tạo: so tên bỏ dấu/
bỏ tiền tố (Hộ kinh doanh, Công ty TNHH…) và số 9+ chữ số (SĐT trong tên/mobile_no) với MỌI khách ERP; có ứng viên na ná → KHÔNG tạo, dừng
"khách chưa có trên ERP nhưng NGHI TRÙNG khách đã có: …" cho Tú (vụ trùng Lã Thị Kiều Oanh 21/09/2026). Chạy thử (không --that) chỉ in "SẼ TẠO".
In mục "KHÁCH LẤY TỪ MISA TẠO SANG ERP". `thu-lai-thieu-ma.py`: dòng "thiếu khách" luôn coi là sẵn sàng để thử lại. SKILL.md misa-bh-sync đã sửa
dòng "KHÔNG tự tạo" (chỉ còn cấm tự tạo MÃ HÀNG). Chưa thử tạo thật vì lúc kiểm không còn BH nào thiếu khách (BH05230 đã có khách);
payload đã kiểm hợp lệ bằng validate_only. Khách tạo tự động chưa có sales team/bảng giá riêng — Tú bổ sung nếu cần.
**BH thiếu mã hàng / thiếu khách → máy TỰ up lại khi ERP đã bổ sung (Tú chốt 03/10/2026).** Sổ có mục riêng
"## Chờ bổ sung mã (máy tự thử lại mỗi lượt)", dòng dạng `- BHxxxxx · ngày HT yyyy-mm-dd · thiếu mã: X` /
`thiếu khách: Y` / `mã chưa bật bán: X`. SKILL.md Bước 1c: routine chỉ chạy `quet-bh\thu-lai-thieu-ma.cmd` (KHÔNG tham số); script
`thu-lai-thieu-ma.py` tự đọc ERP, xoá dòng, gọi `chay-routine.cmd --chi BHxxxxx --tu <ngày HT>`, vẫn tắc thì tự ghi
"Chờ Ngọc Tú quyết", đã có sẵn trên ERP thì bỏ qua. **Lệnh PowerShell kèm tham số (`--chi …`) KHÔNG khớp allow
`… *` → phiên nền treo (03/10/2026 20:08).** Lần 4: `gui-tele.cmd "<tin tổng kết>"` cũng treo, từ 19:16 ngày
05/10 tới 16:58 ngày 06/10/2026 (mất cả buổi sáng). Nay Bước 5 chỉ chạy `quet-bh\tong-ket-cuoi-ngay.cmd` (không
tham số, tự đếm + gửi + ghi mốc, mỗi ngày một lần). Đã chạy được 17:04 ngày 06/10/2026. SKILL.md bỏ hết
PushNotification/gui-tele kèm nội dung. Phiên nền chỉ được gọi lệnh cố định, mọi tham số để script tự lo. Script đã sửa 03/10/2026 cho `--tu` có tác dụng khi
`--tu-dong --chi` (trước đó bị bỏ qua, BH cũ hơn hôm qua không up được bằng chay-routine.cmd), vẫn giữ sàn
SAN_MOC; dòng TẮC in thêm `· ngày HT yyyy-mm-dd`. Why: Tú không muốn phải nhắc "up" sau khi đã thêm mã. How: các
lý do khác (trùng, thuế, huỷ) vẫn vào "Chờ Ngọc Tú quyết".
**Routine "bị pause" sáng 30/09/2026 (Tú phải bấm Play):** lượt 17:07 ngày 29/09 tự viết một lệnh PowerShell
chỉ đọc (Get-Content 3 file mốc + Get-Date) không có trong danh sách cho phép → đứng chờ bấm Allow lúc 17:08,
cả đêm không lượt nào chạy (18:07 → 09:07 ngày 30/09, mất 15 lượt, lỡ luôn "nhịp tim" 17:00). Why: SKILL.md ghi
"Đọc file…" mà không nói dùng tool nào, phiên tự chế lệnh. How: SKILL.md đã thêm luật cứng "CHỈ chạy PowerShell
đúng nguyên dòng chép sẵn; đọc file bằng Read; giờ lấy từ dòng đầu kết quả chay-routine". Viết bước mới cho
routine thì phải chỉ rõ tool + lệnh nguyên văn, đừng để phiên tự nghĩ lệnh.
Lần 2, 01/10/2026 17:08: bước "nhịp tim" dùng tool **Write** tạo mới `quet-bh\log\bao-cuoi-ngay.txt` → bị hỏi
quyền dù đã có allow `Write(//c/Claude Code/routines/**)`, kẹt tới 22:18 (mất 5 lượt). Lần 3, 02/10/2026 17:08:
đổi sang **Edit** cũng kẹt y hệt (tới 19:23 ngày 03/10, mất cả ngày 03/10). Cách đã chạy được 03/10/2026: script
`quet-bh\danh-dau-cuoi-ngay.cmd` tự ghi mốc, có allow PowerShell trong settings.json (2 dạng). How: **phiên nền
KHÔNG ghi file bằng Write/Edit ở `quet-bh\log\`**. Cần ghi thì làm một .cmd nhỏ + thêm allow, rồi Run now kiểm.
(Sửa sổ `routines\misa-bh-sync-bo-qua.md` bằng Edit thì vẫn chạy được, đã kiểm 01/10/2026.) Thấy lượt
"running" mà im >30 phút thì xem lệnh cuối trong bản ghi phiên, stop_session lượt đó rồi Run now.
**Quyền cho routine (Tú dặn 29/09/2026: "tắt hỏi đi, không để ý bấm là nó dừng mãi"):** routine chạy chế
độ Manual. Quyền PowerShell phải viết ĐÚNG dạng app lưu khi bấm Always allow, tức nguyên lệnh
`& "C:\\Claude Code\\routines\\quet-bh\\chay-routine.cmd"`. Dạng `*...*` tự viết KHÔNG ăn. Đã thêm vào
`~/.claude/settings.json`, cả dạng có tham số ` *`. Why: mỗi hộp hỏi là một lượt treo. How: thêm lệnh
mới cho routine thì phải thêm quyền cùng lúc, rồi bấm "Run now" thử cho tới khi chạy hết mà không hỏi,
xong mới báo.

**THAY BẰNG CHỨNG TỪ BÁN HÀNG (BH) — chốt 24/09/2026:** Ngọc Tú yêu cầu từ 24/09/2026 quét MISA
**Bán hàng → tab "Bán hàng"** (`https://actapp.misa.vn/app/SA/SAVoucher`, cột Số chứng từ `BHxxxxx`),
mỗi BH mới → một **Đơn bán hàng (Sales Order) trên ERP, Submit ngay (trạng thái Duyệt), không để
nháp**. Chi tiết BH mở bằng click vào số BH → popup `/app/popup/SAVoucherDetail/<uuid>`; bảng hàng
có cột Mã hàng · Số lượng · Đơn giá (trước thuế) · Thành tiền · % Thuế GTGT. `po_no` lưu mã BH
(vd "BH04842") để kiểm trùng.
(Luật "BH đã có phiếu giao hàng thì bỏ qua" chị nói lúc đầu ngày 24/09/2026 đã **huỷ** cùng ngày.
Xem đoạn "TRÙNG = TRÙNG SỐ BH" bên dưới. **14/10/2026 Tú làm sống lại bản thu hẹp: đơn anh Tùng đã xuất phiếu giao
thì không up BH của đơn đó — xem đoạn "Đơn anh Tùng đã Xuất phiếu giao hàng" ở trên.**)
**Ngày của BH = cột "Ngày hạch toán" (chốt 29/09/2026):** chị nói "up BH ngày 28/09" thì up đúng
các BH có Ngày hạch toán 28/09. `transaction_date` của SO cũng lấy ngày này. Why: chị lọc và đối
chiếu theo cột này trên MISA. How: SKILL.md phần NHIỆM VỤ đã ghi rõ. Việc lỗi ngày 28/09/2026 (up
nhầm BH ngày 26) là do up trước khi thấy lời dặn "26 khỏi", không phải do đọc sai cột.
**Kiểm kĩ sản phẩm + số tiền (chị dặn 29/09/2026):** MISA hiện chi tiết chậm, bảng có thể còn giữ
chi tiết của BH trước. Why: lượt 29/09/2026 suýt đọc nhầm 6 BH (lấy chi tiết của BH khác). How: chỉ
dùng chi tiết khi Σ(Thành tiền − CK + Thuế) = Tổng tiền của đúng BH đó. Sau khi tạo đơn, đối chiếu cả
grand_total lẫn total_qty (SKILL.md Bước 4 và 8).
**TRÙNG = TRÙNG SỐ BH (chốt lần cuối 24/09/2026, thay hết các luật "trùng" trước đó):** chỉ bỏ qua
BH khi trên ERP **đã có Sales Order mang `po_no` = đúng số BH đó** (trùng mã BH, khách, sản phẩm,
giá). BH **khác số** thì VẪN UP, dù cùng khách, cùng hàng, cùng tiền với đơn ĐH cũ, hay đã có phiếu
giao hàng (DN). Luật cũ "đã có phiếu giao thì bỏ qua" và "cùng khách cùng tiền thì bỏ qua" đều
**BỎ** (24/09/2026; riêng phiếu giao do anh Tùng bấm thì Tú làm sống lại 14/10/2026, bản thu hẹp ở đoạn trên). Why: mỗi BH là một chứng từ bán hàng riêng, chị muốn ERP có đủ từng BH, và chị đã tự nhận
phần chồng doanh số với đơn ĐH cũ. How: kiểm trùng chỉ bằng `po_no`, không dò theo số tiền.
**BH chỉ có dòng Phí** (vd phí bảo hành `Phi1`) thì vẫn bỏ qua, luật này giữ nguyên. Khách trùng số
điện thoại thì chọn khách đã có đơn trên ERP (Trần Quang Quyết → "Anh Quyết 0703955146").
**Tác vụ tự động BH (tạo 24/09/2026):** `misa-bh-sync`, lịch `0 * * * *` (1 tiếng/lần, chạy ở phút
~07), SKILL.md ở `C:\Users\admin\.claude\scheduled-tasks\misa-bh-sync\`. Chỉ xét BH từ 24/09/2026.
Sổ `C:\Claude Code\routines\misa-bh-sync-bo-qua.md` (dời từ `.claude\scheduled-tasks\` ngày 29/09/2026; bản cũ cất ở `routines\_bỏ\`) ghi BH đã bỏ qua / chờ chị quyết
/ đã up. Khi chị trả lời về một BH "chờ quyết" thì sửa sổ này (xoá dòng để cho up lại). Tác vụ
KHÔNG tự tạo khách hay mã hàng, gặp trùng SO hoặc DN thì để chờ, không up.
**"Tự động up đầy đủ" (Ngọc Tú dặn 25/09/2026):** ngày 25/09/2026 có 15 BH, nhưng một lượt chỉ
thấy 9 vì 6 BH sinh ra sau khi quét, và BH04854 bị kế toán sửa tiền SAU khi đã up (38,6tr → 9,47tr).
Why: chị muốn ERP luôn đủ và đúng từng BH, không phải tự đi soát. How: SKILL.md có Bước 3b: mỗi lượt
so lại tổng tiền BH hôm nay/hôm qua với SO đã up (lệch → "Chờ Ngọc Tú quyết"), và quét lại danh sách
trước khi kết thúc. Tool ERP (MCP) **không cancel được** SO đã submit (update docstatus bị chặn,
`frappe.client.cancel` qua call_method mất tham số), nên sửa SO sai phải huỷ tay trên ERP.
**Thuế trống thì hỏi trước (chốt 28/09/2026):** dòng hàng MISA để trống ô "% Thuế GTGT" (vd SORA20-1
trong BH04917) thì coi như thuế khác 8%: không up, hỏi chị trước. Why: trống thuế thì không biết là
0% hay kế toán quên nhập. Up sai, tổng tiền ERP sẽ lệch MISA. How: ghi "Chờ Ngọc Tú quyết". Chị gật thì tax
dùng "Actual" = đúng tiền thuế MISA (như BH04917→SAL-ORD-2026-00272). Đã ghi vào SKILL.md Bước 5 và 7.
**Sự cố 28–29/09/2026 và luật rút ra (Ngọc Tú bảo "vá lỗi, rút kinh nghiệm", 29/09/2026):**
1. *Phiên nền treo vì chờ bấm cho phép sửa sổ.* Lượt 09:38 ngày 29/09 tạo xong 7 SO (00288–00294) lúc
   14:16 rồi đứng im chờ quyền Edit. Nó chiếm chỗ nên mọi lượt 10:07–14:07 đều bị bỏ. Why: sửa file
   trong `~/.claude` luôn phải hỏi (thư mục được bảo vệ), rule allow không có tác dụng, và rule cũ viết
   kiểu `C:\\...` là sai cú pháp. Trên Windows phải viết `//c/...`. How: sổ đã dời ra
   `C:\Claude Code\routines\`, và `~/.claude/settings.json` đã có allow `Edit/Write(//c/Claude Code/routines/**)`.
   **Mọi file mà phiên nền phải GHI thì để ngoài `.claude`.**
2. *Bước chống chạy chồng để một phiên treo chặn cả ngày.* How: phiên kia im quá 30 phút thì coi là
   treo, cứ chạy lượt mới và báo chị. Kiểm `po_no` lại NGAY trước mỗi lần tạo đơn để không tạo trùng.
3. *Up dồn BH tồn cũ.* Ngày 26–28/09 hai ngày không có lượt nào chạy, rồi một lượt up luôn BH ngày 26
   mà chị không muốn. How: tự up chỉ BH có Ngày hạch toán hôm nay và hôm qua. Cũ hơn thì hỏi chị.
4. *Bộ lọc kỳ MISA đang bật "Hôm qua"*, suýt sót 9 BH hôm nay. How: kiểm bộ lọc trước khi tin danh sách.
Tất cả đã ghi vào SKILL.md. Routine chỉ chạy khi máy và app Claude đang mở. Tắt máy thì lỡ lượt,
không báo lỗi gì. Chrome rớt kết nối nhiều lần (22/09, 28/09 17:07, 29/09 sáng và ~14:35): chưa rõ
nguyên nhân, cách trị tận gốc là chuyển sang API MISA (chị đang cân nhắc).
**Rewind làm mất file đã sửa:** ngày 29/09/2026 chị bấm quay lại, các file vá bị trả về bản cũ.
Sau khi rewind, kiểm lại file trên đĩa trước khi báo "đã vá".

**Ngọc Tú là người chốt việc up BH lên ERP** (chốt 24/09/2026). Đồng nghiệp (vd tài khoản
`nvtungjob@gmail.com`) có tự nhập đơn tay trên ERP, nhưng đừng khuyên "thống nhất ai up", cũng đừng
chờ đồng nghiệp. Chị nói "kệ ổng". Why: chị là người chủ chốt mảng này. How: cứ làm theo lệnh của
chị. Đơn nháp của đồng nghiệp thì không đụng vào.

**ĐÃ HUỶ phần Đơn đặt hàng 24/09/2026** (Ngọc Tú chốt): từ nay **không đưa Đơn đặt hàng MISA lên ERP nữa**, tác vụ
`misa-order-sync` đã tắt (enabled=false) và SKILL.md có dòng chặn ở đầu. Đừng bật lại, đừng tự
nhập đơn MISA vào ERP khi chưa được Ngọc Tú yêu cầu lại rõ ràng. Phần dưới chỉ còn để tham khảo.

Tác vụ nền `misa-order-sync` (`C:\Users\admin\.claude\scheduled-tasks\misa-order-sync\SKILL.md`),
lịch `*/30 * * * *`, chốt giữ 30 phút (23/09/2026). Khi Ngọc Tú hỏi "sao đơn chưa lên ERP",
kiểm đúng 3 chỗ này trước khi đoán:

1. **Phiên treo vì chờ bấm Allow.** Đây là nguyên nhân hay bị nhìn nhầm thành "phiên chạy
   hàng giờ". Phiên nền đứng im chờ người bấm, `last_activity_at` không nhúc nhích.
   Đã sửa 23/09/2026: chuyển danh sách cho phép từ `C:\Claude Code\.claude\settings.local.json`
   (chỉ áp cho phiên mở đúng thư mục đó) lên `C:\Users\admin\.claude\settings.json` (áp mọi
   phiên, kể cả phiên nền). Mỗi tool là một mục riêng — allow `create_document` KHÔNG áp cho
   `submit_document`.
2. **Tiện ích Claude in Chrome mất kết nối.** Phiên kết thúc sau 7–10 lượt với ghi chú
   "extension not connected". Ngày 22/09/2026 có 3 lượt liên tiếp chết vì lỗi này. Không phải
   do MISA đăng xuất — cần Chrome đang mở và extension sống.
3. **Bộ lọc MISA không được chỉ lấy "Chưa thực hiện"** (chốt 23/09/2026, Ngọc Tú yêu cầu sau
   khi ĐH03046 bị bỏ sót). Đơn ở trạng thái **"Chưa ghi doanh số"** (chi tiết đơn hiện Tình
   trạng = "Đang thực hiện") cũng phải mở ra, kiểm hai cột **"Số lượng"** và **"Số lượng đã
   xuất"** trong bảng Hàng tiền: còn hàng chưa xuất hết → **mặc định coi là CHƯA THỰC HIỆN**,
   tức đơn cần nhập lên ERP. Xuất đủ 100% mới bỏ qua.
   Ví dụ ĐH03046 (HỘ KINH DOANH NỆM THUẦN VIỆT 1, 14 dòng hàng, tổng 39 tấm, mới xuất 3).

**Dọn tab Chrome** (thêm vào SKILL.md 24/09/2026): mỗi lượt chạy mở 1 tab MISA mới, trước không có
bước đóng lại nên tab dồn cả ngày (~48 tab/ngày) làm Ngọc Tú rối, phải tự tắt tay. Đã thêm bước
đóng tab (`tabs_close_mcp`) vào cuối SKILL.md — Kết thúc phiên.

**Chống chạy chồng phiên** (thêm vào SKILL.md 23/09/2026, Bước 0): phiên mới gọi
`list_task_runs`, nếu có run khác `status: "running"` với `started_at` sớm hơn thì thoát ngay,
không đụng MISA lẫn ERP. Hai phiên cùng chạy sẽ cùng đọc một danh sách và tạo trùng đơn.

4. **Kết nối lại được thì tự chạy tiếp, đừng hỏi lại xin phép** (chốt 23/09/2026). Tác vụ này
   đã được phép tự nhập + submit đơn theo đúng SKILL.md — khi Chrome/extension mất kết nối rồi
   nối lại (dù là giữa chừng phiên hay ở lượt kế tiếp), cứ tiếp tục quét MISA → tạo → submit
   như bình thường, không cần dừng lại hỏi "chạy luôn hay đợi". Ngọc Tú đã nói rõ: tác vụ nền
   phải tự giác, hỏi lại nhiều lần cho việc đã được cho phép sẵn làm bực mình.

**Đơn nhiều dòng hàng (đã giải được, 23/09/2026):** bảng "Hàng tiền" trong popup chi tiết đơn có
phân trang RIÊNG (khác phân trang của danh sách đơn ngoài cùng) — mặc định 20 dòng/trang. Đừng
bấm số trang, mà bấm vào ô **"Số dòng/trang"** ngay dưới bảng Hàng tiền (không phải ô cùng tên ở
danh sách ngoài) và chọn **50** — bảng sẽ tải đủ hết dòng trong 1 lần, không cần lật trang. Đã
áp dụng thành công cho ĐH03043 (Hoàng Thị Hường, 39 dòng giá + vài dòng ghi chú, 287.982.000 ₫)
— trước đây tưởng phải nhập tay, thực ra không cần.
Mẹo đọc nhanh bảng Hàng tiền bằng JS thay vì get_page_text (đỡ tốn context vì get_page_text kéo
theo toàn bộ danh sách đơn phía sau):
`Array.from(document.querySelectorAll('table')).filter(t=>t.innerText.includes('Mã hàng'))` lấy
bảng cuối cùng khớp, đọc `header = rows[0]`, dùng `header.indexOf('Mã hàng')` v.v. để lấy đúng cột
— chỉ số cột lệch 1 tuỳ đơn có cột "Tỷ lệ CK/Tiền chiết khấu" hay không, nên luôn tra theo tên cột,
đừng hard-code index.
Click vào "Số đơn hàng" bằng `ref` từ `find`/`read_page` đôi khi bị stale sau khi bảng re-render
(vd sau khi đổi Số dòng/trang) — dùng querySelectorAll tìm phần tử có `textContent.trim() === 'ĐH0xxxx'`
rồi `.click()` bằng JS cho chắc, thay vì cứ theo `ref` cũ.

**Why**: Ngày 23/09/2026 Ngọc Tú phát hiện hàng loạt đơn ĐH03042–ĐH03048 chưa lên ERP dù tác
vụ vẫn bật. Chẩn đoán ban đầu "mỗi phiên chạy 6 tiếng" là SAI — thực chất phiên đứng chờ
bấm Allow, và nhiều lượt chết vì Chrome.

**How to apply**: Xem `erp-sales-order-entry-rules` cho quy tắc nhập đơn. Việc xoá bản ghi ERP
vẫn phải trình trước theo luật cứng, kể cả khi phiên nền muốn xoá đơn Draft nhập sai.
**TẠM NGƯNG routine auto up BH từ 23/10/2026 (Tú: "tạm ngưng routine auto up đơn BH nha").** Tác vụ `misa-bh-sync` đã tắt (`enabled: false`), không xoá; lượt cuối chạy lúc 13:07 ngày 23/10/2026. Bật lại khi Tú bảo: `update_scheduled_task misa-bh-sync enabled=true`. Máy quét và các script vẫn nguyên, chạy tay được (`xem-thu.cmd`, `chay-routine.cmd`).
**BẬT LẠI routine auto up BH ngày 24/10/2026 (Tú: "play lại routine up đơn nha").** Tác vụ `misa-bh-sync` `enabled: true`, nhịp 2 tiếng/lần như cũ. Mốc tạm ngưng 23/10/2026 ở trên không còn hiệu lực.
**TẠM NGƯNG routine auto up BH lần 2 từ 26/10/2026 (Tú: "ngưng routine tự động up đơn BH lên ERP, khi nào t vô t kêu m up thì m up 1 lượt luôn").** Tác vụ `misa-bh-sync` `enabled: false`, không xoá. Từ nay KHÔNG tự chạy: khi Tú kêu "up đơn" thì em chạy ĐÚNG MỘT LƯỢT máy quét ghi thật (`C:\Claude Code\routines\quet-bh\chay-routine.cmd`, xem trước bằng `xem-thu.cmd`) rồi báo kết quả; không bật lại tác vụ nếu Tú chưa bảo. Mốc bật lại 24/10/2026 không còn hiệu lực.
