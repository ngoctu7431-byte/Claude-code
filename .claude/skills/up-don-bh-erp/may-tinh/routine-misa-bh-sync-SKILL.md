---
name: misa-bh-sync
description: Mỗi 2 giờ (giờ lẻ: 1h, 3h … 23h) chạy máy quét BH: BH hôm nay/hôm qua trên MISA chưa có trên ERP → tạo Sales Order, kiểm rồi Submit; chuyện lạ thì báo
---

Bạn đang chạy tác vụ định kỳ mỗi 2 tiếng (giờ lẻ: 01h, 03h … 17h … 23h; Tú đổi từ 1 tiếng ngày 19/10/2026), KHÔNG có bộ nhớ của phiên trước. Người dùng: Ngọc Tú (đại lý B2B nệm), không phải dev. Báo cáo viết tiếng Việt, câu ngắn, ghi ngày tuyệt đối (dd/mm/yyyy). **Xưng hô: gọi Tú là "công chúa", xưng "em". Tú là nữ, KHÔNG gọi "anh"** (chốt 03/10/2026). Chữ "anh" trong các mẫu câu bên dưới là cách xưng cũ: khi viết thì thay bằng "công chúa".

Từ 29/09/2026 việc đọc MISA và tạo đơn ERP do **máy quét BH** (script Python) làm. Nó đọc MISA qua cửa dữ liệu, lấy chi tiết theo mã từng BH, không bấm màn hình. Bạn chỉ chạy lệnh, đọc kết quả, ghi sổ và báo. Bản cũ (tự bấm MISA bằng Claude in Chrome) đã bỏ vì gãy ngày 28/09/2026. Bản cũ cất ở `C:\Claude Code\routines\_bỏ\`.

## Luật cứng
- **KHÔNG** mở MISA, **KHÔNG** dùng Claude in Chrome, **KHÔNG** tự tạo, sửa, submit, huỷ hay xoá đơn ERP bằng tool MCP. Mọi đơn chỉ do máy quét tạo. Tool ERP chỉ được dùng để ĐỌC (Bước 5).
- **KHÔNG** sửa script hay file `.cmd` trong `C:\Claude Code\routines\quet-bh\`. Script lỗi thì báo nguyên văn.
- Không đụng `C:\Claude Code\.mcp.json` (máy quét tự đọc khoá ERP từ đó).
- Không hỏi xin phép gì thêm: các lệnh dưới đây đã được cho phép sẵn.
- **CHỈ chạy PowerShell đúng nguyên các dòng lệnh chép trong file này.** Không tự viết lệnh PowerShell/Bash nào khác, kể cả lệnh chỉ đọc (Get-Content, Get-Date, Test-Path, foreach…). Lệnh tự viết không có trong danh sách cho phép → phiên đứng chờ bấm "Allow" cả đêm, mọi lượt sau bị kẹt (sự cố 29/09/2026 17:08 → 30/09/2026 09:23, mất 15 lượt).
  - Đọc file (mốc ngày, sổ, nhật ký): dùng tool **Read**. File chưa có thì Read báo lỗi, coi như "chưa có".
  - Giờ hiện tại: lấy từ dòng đầu kết quả Bước 1 (`===== dd/mm/yyyy HH:MM:SS chay-routine`). Không gọi Get-Date.
  - Ghi file: tool **Write**/**Edit** (chỉ trong `C:\Claude Code\routines\`).

## Bước 1: chạy máy quét (mỗi lượt)
Dùng tool **PowerShell**, timeout 600000, đúng nguyên dòng này:
```
& "C:\Claude Code\routines\quet-bh\chay-routine.cmd"
```
Lệnh tự ghi nhật ký vào `C:\Claude Code\routines\quet-bh\log\`. Kết quả cần đọc nằm ở dòng cuối `TÓM TẮT: GHI THẬT · tạo N · đã có N · tắc N · tồn cũ N · lệch tiền N`.

**Telegram:** từ 29/09/2026, `chay-routine.cmd` và `cap-nhat-lech.cmd` TỰ gửi Telegram cho Tú khi có chuyện: up đơn, tắc, tồn cũ, lệch, nháp, bù ngày, MISA đăng xuất, lỗi. Tin trùng thì không gửi lại. Bạn KHÔNG cần gửi lại những tin đó. Dòng `⛔ Chưa cài Telegram` hoặc `⛔ gửi Telegram không được` thì ghi vào báo cáo.

## Bước 1b: sửa đơn ERP cho khớp BH kế toán đã sửa (mỗi lượt, ngay sau Bước 1)
Tú chốt 29/09/2026: "tự động rà soát các phiếu BH trên misa nếu có thay đổi và cập nhật lại trên ERP để khớp số liệu". Chạy (PowerShell, timeout 600000, đúng nguyên dòng):
```
& "C:\Claude Code\routines\quet-bh\cap-nhat-lech.cmd"
```
Bước 1 báo `PHIÊN MISA ĐÃ HẾT` hoặc `Lượt trước còn đang chạy` thì bỏ bước này. Máy tự sửa bằng "Cập nhật mặt hàng" (thêm dòng, tăng số lượng, đổi giá, bỏ dòng chưa giao), KHÔNG Cancel, KHÔNG đụng phiếu giao. Dòng cuối: `TÓM TẮT CẬP NHẬT: GHI THẬT · sửa N · không tự sửa được N · lỗi N`.
- `✅ ... ĐÃ SỬA` → báo Tú mỗi đơn một dòng, chép các dòng thay đổi máy in ra. Thêm câu: "phần hàng thêm hiện là chưa giao trên ERP, kho làm thêm phiếu giao nếu đã giao thật".
- `⛔ LỆCH MÀ KHÔNG TỰ SỬA ĐƯỢC` và `⚠️ LỖI` → như nhóm TẮC ở Bước 3: BH mới (chưa có trong sổ) thì ghi vào "Chờ Ngọc Tú quyết" và báo, chép nguyên văn lý do.

## Bước 1c: tự thử lại BH thiếu mã / thiếu khách (mỗi lượt, sau Bước 1b)
Tú chốt 03/10/2026: BH tắc vì thiếu mã hàng hoặc thiếu khách trên ERP, khi ERP đã bổ sung thì máy TỰ up, không chờ Tú nói "up". Bước 1 báo `PHIÊN MISA ĐÃ HẾT`, `TÀI KHOẢN MISA ĐANG MỞ Ở CHỖ KHÁC` hoặc `Lượt trước còn đang chạy` thì bỏ bước này.
Chạy PowerShell, timeout 600000, đúng nguyên dòng, **KHÔNG thêm tham số nào**:
```
& "C:\Claude Code\routines\quet-bh\thu-lai-thieu-ma.cmd"
```
Lệnh tự làm hết: đọc mục "## Chờ bổ sung mã (máy tự thử lại mỗi lượt)" trong sổ, xem ERP đã bổ sung mã/khách chưa, có rồi thì tự xoá dòng và up đúng BH đó (vẫn qua đủ luật kiểm trùng, kiểm tiền), vẫn tắc thì tự ghi BH vào "Chờ Ngọc Tú quyết". Bạn KHÔNG tự sửa mục này, KHÔNG tự chạy `chay-routine.cmd --chi …` (lệnh kèm tham số bị hỏi quyền, phiên treo — 03/10/2026 20:08).
Đọc kết quả: dòng `✅ THỬ LẠI ĐÃ UP: …` → báo Tú "ERP đã bổ sung mã/khách → đã up BHxxxxx → SAL-ORD-…". Dòng `⛔ THỬ LẠI VẪN TẮC: …` → báo Tú nguyên văn (máy đã tự ghi sổ). Dòng cuối `TÓM TẮT THỬ LẠI: up 0 · vẫn tắc 0 · …` → không báo gì.

## Bước 2: đối chiếu (MỘT lần mỗi ngày)
Dùng tool **Read** (không dùng PowerShell) đọc dòng đầu file `C:\Claude Code\routines\quet-bh\log\doi-chieu-lan-cuoi.txt`. File chưa có, hoặc dòng đầu không mang ngày hôm nay (dạng dd/mm/yyyy) thì chạy (PowerShell, timeout 600000):
```
& "C:\Claude Code\routines\quet-bh\doi-chieu.cmd"
```
Lệnh này CHỈ ĐỌC. Nó tìm (1) đơn ERP mà số BH không còn trên MISA, tức kế toán đã xoá hoặc lập lại BH và ERP đang trùng; (2) đơn ERP lệch tiền so với BH. Chỉ báo những dòng CHƯA có trong mục "Chờ Ngọc Tú quyết" của sổ. Lệch 1–2 đồng là làm tròn, bỏ qua.

## Bước 3: đọc kết quả, ghi sổ
Sổ: `C:\Claude Code\routines\misa-bh-sync-bo-qua.md`. Máy quét bỏ qua MỌI số BH có trong sổ. Sửa sổ bằng tool **Edit** (đã được cho phép), không dùng lệnh shell.
- `Lượt trước còn đang chạy` → kết thúc, không báo gì.
- `PHIÊN MISA ĐÃ HẾT` → (1) chạy (PowerShell, đúng nguyên dòng) `& "C:\Claude Code\routines\quet-bh\dang-nhap-misa.cmd"`. Lệnh này mở sẵn cửa sổ Chrome riêng ở trang đăng nhập MISA rồi thoát ngay, không bắt phiên phải chờ. (2) KHÔNG gọi PushNotification hay gui-tele: máy quét đã tự nhắc Telegram mỗi lượt khi MISA đăng xuất. (3) Kết thúc lượt. **KHÔNG** tự gõ tài khoản hay mật khẩu (luật cấm). Lượt sau tự chạy lại khi Tú đã đăng nhập.
  **Nhắc MỖI lượt** cho tới khi Tú đăng nhập, không chỉ lần đầu. Mỗi lần nhắc ghi rõ "chưa quét được từ <ngày trong `C:\Claude Code\routines\quet-bh\log\lan-quet-thanh-cong.txt`>". Không phải lo BH bị bỏ sót: đăng nhập xong, máy quét tự bù đủ các ngày lỡ.
- Dòng `BÙ NGÀY LỠ` → lượt này đã tự up BH của những ngày máy nghỉ hoặc MISA đăng xuất. Báo Tú một dòng: "Đã bù BH từ <ngày> tới nay: tạo N đơn".
- `Không bắt được cửa danh sách BH` → báo nguyên văn. Có thể MISA chậm hoặc đổi giao diện. Không tự làm cách khác.
- Có traceback hay lỗi lạ → chạy lại **một** lần. Vẫn lỗi thì báo 10 dòng cuối, nguyên văn.
- Nhóm **TẮC** mà lý do là `mã chưa có trên ERP: X`, `khách chưa có trên ERP: Y` hoặc ERP báo mặt hàng X "không được đánh dấu là mặt hàng sales": ghi vào mục "## Chờ bổ sung mã (máy tự thử lại mỗi lượt)" (KHÔNG vào "Chờ Ngọc Tú quyết"), đúng dạng `- BHxxxxx · ngày HT yyyy-mm-dd · thiếu mã: X` / `· thiếu khách: Y` / `· mã chưa bật bán: X`. Ngày HT lấy ở cuối dòng tắc (`· ngày HT yyyy-mm-dd`). Thiếu nhiều mã thì ghi đủ, cách nhau dấu phẩy (`thiếu mã: A, B`). Báo Tú: "BHxxxxx thiếu <mã/khách> trên ERP — bổ sung xong máy tự up".
- Nhóm **TẮC** mà lý do là `từng có đơn nhưng ĐÃ HUỶ: SAL-ORD-…`: xem người huỷ bằng `mcp__0f3084c7-eba9-42fd-b239-933fe4f344f1__list_documents` doctype "Sales Order", filters `{"name": "SAL-ORD-…", "docstatus": 2}`, fields `["modified_by"]`. Người huỷ là `nvtungjob@gmail.com` → Tú chốt 05/10/2026 "anh Tùng hủy thì thôi": ghi BH vào mục "## Bỏ vĩnh viễn: đơn ERP đã bị anh Tùng (nvtungjob) huỷ", KHÔNG up lại, KHÔNG báo Tú. Người khác huỷ → vào "Chờ Ngọc Tú quyết" như dưới.
- Nhóm **TẮC** (lý do khác), **TỒN CŨ**, **TIỀN LỆCH SO MISA**: mỗi BH MỚI (chưa có trong sổ) thêm một dòng vào mục "## Chờ Ngọc Tú quyết": `- BHxxxxx · <lý do máy in ra> (dd/mm/yyyy)`. Ghi vào sổ là để lượt sau không báo lại. Báo Tú đúng những BH mới này, chép nguyên văn lý do.
- Dòng `⛔ ... để NHÁP, không Submit` → đơn Nháp đó cũng ghi vào "Chờ Ngọc Tú quyết" kèm mã đơn. Không tự sửa, không tự Submit.
- **ĐỪNG** ghi BH đã up vào sổ: ghi vào là máy bỏ luôn bước so tiền. Máy đã tự ghi nhật ký.

## Bước 4: báo
- Chỉ có "tạo N", còn lại đều 0 (hoặc chỉ là BH đã ghi sổ từ trước) → một dòng: "dd/mm/yyyy HH:MM: đã tạo N đơn: BHxxxxx→SAL-ORD-…, …". N = 0 và không có gì mới → kết thúc một dòng "Không có BH mới".
- Có chuyện mới (tắc, tồn cũ, lệch, trùng, nháp, lỗi) → báo ngắn, mỗi BH một dòng, và nói Tú cần làm gì.

## Bước 5: báo cuối ngày (MỘT lần mỗi ngày, lượt đầu tiên từ 17:00 trở đi)
Nếu giờ hiện tại (lấy từ dòng đầu kết quả Bước 1) ≥ 17:00 thì chạy PowerShell, timeout 600000, đúng nguyên dòng, **KHÔNG thêm tham số nào**:
```
& "C:\Claude Code\routines\quet-bh\tong-ket-cuoi-ngay.cmd"
```
Lệnh tự đếm đơn ERP hôm nay, tự gửi Telegram, tự ghi mốc, và tự bỏ qua nếu hôm nay đã gửi. Bạn KHÔNG tự đếm, KHÔNG tự soạn tin, **KHÔNG gọi `gui-tele.cmd` kèm nội dung, KHÔNG gọi PushNotification** ở bước này: lệnh kèm nội dung bị hỏi quyền, phiên treo từ 19:16 ngày 05/10 tới 16:58 ngày 06/10/2026 (mất cả buổi sáng không up được đơn). Trước đó Write (01/10) và Edit (02/10) file mốc cũng treo y vậy.
Đây là "nhịp tim": hôm nào tới 18:00 mà Tú không nhận báo này, tức là máy tắt hoặc routine không chạy.

## Tú trả lời một BH đang chờ (khi phiên có Tú)
- "bỏ" → để nguyên trong sổ (sửa lý do thành "Tú bảo bỏ, dd/mm/yyyy").
- "up" / "đơn thật" → xoá dòng đó khỏi sổ, rồi chạy `& "C:\Claude Code\routines\quet-bh\chay-routine.cmd" --chi BHxxxxx`. BH cũ hơn hôm qua thì thêm `--tu <yyyy-mm-dd ngày hạch toán>`. Đang "NGHI TRÙNG" thì thêm `--cho-trung`.
- Mã hàng chưa có trên ERP → báo người phụ trách danh mục thêm. KHÔNG tự tạo mã hàng.
- Khách chưa có trên ERP: TỪ 15/10/2026 máy quét TỰ lấy thông tin khách ở MISA tạo sang ERP rồi up đơn (Tú chốt 15/10/2026), bạn KHÔNG tự tạo tay. Máy chỉ tạo khi không có khách nào na ná; có khách na ná thì máy tự dừng "NGHI TRÙNG khách" → báo Tú nguyên văn, đừng tạo.
- Huỷ đơn ERP (đơn trùng, đơn lệch tiền) → tool không huỷ được, và theo luật phải trình Tú. Chỉ nói Tú mở đơn nào để bấm Cancel.