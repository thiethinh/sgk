---
name: vietnamese-grade1-reading-book
description: Hướng dẫn khảo sát, trích xuất, chuẩn hóa PDF sách tập đọc tiếng Việt lớp 1, xây dựng từ điển song ngữ Anh-Việt theo ngữ cảnh và phát triển web reader tương tác 2 cột (trang PDF có lớp phủ tương tác bên trái & khung từ điển/gợi ý bên phải).
---

# Vietnamese Grade 1 Reading Book Skill

Quy trình khảo sát, trích xuất, tinh lọc từ vựng có nghĩa và phát triển ứng dụng Web Reader tương tác hai cột (Dual-Pane) chuẩn sách giáo khoa Tiếng Việt Lớp 1.

## 1. Khảo sát PDF và Lựa chọn Công cụ
- Kiểm tra số trang, kích thước, cấu trúc trang.
- Phân loại trang:
  - **Digital text**: Trang có text layer đầy đủ.
  - **Scanned image**: Trang scan raster thuần túy, không có text layer (như `sgk1_t1.pdf` 57 trang raster RGB).
  - **Mixed text & image**: Trang vừa có text vừa có tranh minh họa có chữ.
- Công cụ ưu tiên: PyMuPDF (`fitz`), Pillow, RapidOCR (`rapidocr-onnxruntime`), Edge-TTS (`edge-tts`).

## 2. Tiêu chí Lọc và Trích xuất Từ Vựng Có Nghĩa (Strict Vocabulary Filtering)
Để đảm bảo chất lượng học tập cho học sinh lớp 1, hệ thống **bắt buộc loại bỏ hoàn toàn**:
- **Các chữ cái, vần đơn lẻ**: không lấy các ký tự rời hoặc vần luyện âm (*a, b, c, e, ê, d, đ, ch, kh, in, un, am, an, on, ap, ach, anh, v.v.*).
- **Các tiêu đề bài, số mục**: không lấy các nhãn cấu trúc (*Bài 1, Bài 2, 1 Nhận biết, 2 Đọc, 3 Tô và viết, 4 Đọc, 5 Nói, Kể chuyện, Trang 14, v.v.*).
- **Tên riêng nhân vật**: không lấy các tên riêng nhân vật lớp 1 (*Nam, Hà, Lê Quý Đôn, Dì Kha, v.v.*).
- **Thông tin xuất bản / hành chính**: loại bỏ thông tin tác giả, NXB, huân chương.

**Chỉ giữ lại các từ và cụm từ vựng tiếng Việt có nghĩa thực sự** xuất hiện trong các bài tập đọc và bài học:
- **Đồ dùng học tập**: bút chì, thước kẻ, tẩy, vở, cặp sách, hộp bút, bảng con, trường lớp.
- **Con vật**: bò, cá, cá cờ, cá hổ, cá rô, kì đà, le le, khỉ, quạ, gà, nghé, chim sẻ, dế mèn, đàn kiến.
- **Thực vật, cây trái**: cỏ, gốc đa, đỗ đỏ, lá hẹ, quả đu đủ, quả chuối, cá kho, quả khế, lá khô, su su, rổ rá.
- **Gia đình, nơi chốn, đồ vật**: bà, bé, bố, mẹ, bạn bè, ô đỏ, tàu thủy, cảng, bờ đê, nơ đỏ, ca nô, giỏ trứng, ngôi nhà, ngõ nhỏ, ghế, chợ quê.
- **Hành động, tính từ**: ca hát, câu cá, bế, gặm cỏ, đi bộ, dỡ hàng, đỡ bé, bơi, ngọt lừ, hung dữ, thông minh, che gió, ríu rít.

## 3. Kiến trúc Giao diện Hai Cột Tối Ưu Tầm Mắt (Compact Dual-Pane Reader)

### Cột bên trái: Trang PDF vừa vặn màn hình & Lớp phủ Bounding Box
1. **Kiểm soát kích thước (Auto Fit-Height)**:
   - Trang PDF được scale vừa vặn với chiều cao màn hình (`fitHeight: true`, chiều cao tối đa `calc(100vh - 200px)`), tránh bị quá khổ màn hình.
   - Hỗ trợ phóng to/thu nhỏ linh hoạt (Zoom in/out, Fit Screen toggle).
2. **Hỗ trợ vuốt dọc và cuộn trang (Vertical Swipe & Scroll)**:
   - Hỗ trợ cử chỉ vuốt dọc cảm ứng (`onTouchStart`, `onTouchEnd`): vuốt lên sang trang tiếp theo, vuốt xuống về trang trước.
   - Bắt sự kiện con lăn chuột (`onWheel`) khi đến mép trang để lật trang tự nhiên, mượt mà.
   - Bổ sung nút bấm điều hướng dọc nổi (`▲ Trang trước`, `▼ Trang sau`).
3. **Hiệu ứng chuyển trang êm dịu, không nháy sáng (Zero-Flash Double-Buffered Page Turn)**:
   - **Tuyệt đối không để xảy ra nháy sáng (white flash / flicker)**: Loại bỏ việc unmount thẻ img (`key={page}`) khiến khung hình bị rỗng làm lộ nền trắng chói mắt trẻ em.
   - **Kỹ thuật Double-buffering (Hai lớp đệm)**:
     - Lớp dưới (Background layer): Giữ nguyên trang trước hiển thị 100% độ mờ cho đến khi trang mới hoàn thành hoạt ảnh.
     - Lớp trên (Foreground layer): Tải trang mới và thực hiện hoạt ảnh lật trang mềm mại (`animate-page-turn-next` / `animate-page-turn-prev`) với bóng mép trang (`box-shadow: -10px 0 20px rgba(60,40,10,0.2)`), trượt nhẹ (`translateX: 18px -> 0`) và tăng dần độ hiển thị.
     - Kiểm tra `img.complete` hoặc `img.onload` trước khi kích hoạt hoạt ảnh để đảm bảo không một khung hình nào bị trống.
     - Sử dụng nền giấy dịu mắt (`#FAF7F2` / `#F4EDE4`) chống mỏi mắt cho trẻ.
4. **Lớp phủ các ô DIV tương tác**:
   - Mỗi từ vựng có nghĩa được đè lên bằng một thẻ `<div className="absolute ...">` định vị theo tỷ lệ phần trăm `%`.
   - Hiệu ứng trực quan: Viền vàng cam nhẹ phát sáng khi hover (`hover:scale-105`), khi được kích hoạt (`selected`) chuyển sang viền tím/xanh nổi bật với hiệu ứng pulse.

### Cột bên phải: Khung Từ vựng Trên cùng & Gợi ý Bên dưới
1. **Khung thông tin từ nằm trên cùng (Top Vocab Card)**:
   - Từ tiếng Việt to, rõ ràng, dễ nhìn.
   - **Nút phát âm song ngữ**: Nghe tiếng Việt (giọng giáo viên chuẩn) và nghe English (giọng bản ngữ Mỹ).
   - **Nút lưu vào sổ tay (Bookmark/Save)**: Cho phép bé bấm lưu từ vựng yêu thích vào sổ tay cá nhân.
   - **Giải thích nghĩa tiếng Việt**: Dành riêng cho học sinh lớp 1, ngắn gọn và dễ hiểu.
   - **Nghĩa tiếng Anh theo ngữ cảnh & IPA**: Tối đa 2 nghĩa kèm phiên âm quốc tế chuẩn xác.
2. **Khung gợi ý từ mở sẵn ở bên dưới (Suggested Words List)**:
   - Mở sẵn danh sách tất cả các từ vựng nổi bật của trang hiện tại dưới dạng các thẻ bo tròn sinh động.
   - Mỗi thẻ có biểu tượng bookmark để tích lưu nhanh và nút loa nghe phát âm tức thì.
   - Đồng bộ 2 chiều: Nhấn vào thẻ gợi ý sẽ cập nhật khung thông tin trên cùng và phát sáng ô div tương ứng trên trang PDF bên trái.

## 4. Sổ Tay Từ Vựng Cá Nhân (Saved Words Notebook)
- **Nguyên tắc**: Sổ tay từ vựng **chỉ lưu trữ những từ mà người dùng/bé đã tích lưu** (Bookmarked words).
- **Lưu trữ bền vững**: Sử dụng `localStorage` (`sgk1_saved_vocab_ids`) để lưu trữ danh sách từ đã lưu, giữ nguyên dữ liệu khi tải lại trang.
- **Giao diện sổ tay**:
  - Mặc định mở tab **"Đã lưu (N từ)"**: Chỉ hiển thị các từ bé đã chọn lưu.
  - Trạng thái rỗng (Empty state): Hiển thị hướng dẫn trực quan khuyến khích bé bấm biểu tượng 🔖 "Lưu từ này" khi đọc bài.
  - Tab phụ **"Tất cả từ (N từ)"**: Cho phép bé duyệt và khám phá toàn bộ kho từ vựng trong sách khi cần.
  - Cho phép gỡ bỏ từ khỏi sổ tay chỉ bằng 1 cú click.

## 5. Định vị Bounding Box Khớp Tọa Độ Ảnh PDF (Pixel-Accurate Bounding Box Extraction)
- **Tọa độ từ OCR gốc**: Sử dụng dữ liệu bounding box chính xác từ file OCR (`data/ocr/page_XXX.json`) của từng trang ảnh (kích thước 2280x3200 px).
- **Phân tách từ trong câu (Sentence Word Slicing)**:
  - Khi từ nằm trong một câu dài (như *"Nam và bố câu cá."*, *"Bà cho bé búp bê."*, *"Đàn bò gặm cỏ."*), tính toán tọa độ con (sub-bbox) dựa trên tỷ lệ vị trí ký tự (`char_start / total_len`) và độ dài từ để ô div ôm khít chính xác từng chữ riêng biệt.
  - Từ độc lập hoặc dưới tranh minh họa (như *"ca"*, *"cà"*, *"cá"*, *"ba ba"*, *"kì đà"*) khớp trực tiếp với bounding box của item OCR.
- **Xử lý các trang tiêu đề / mở đầu (Title & Non-vocab Pages)**:
  - Các trang bìa, mục lục, lời nói đầu, giới thiệu nét viết (Trang 1-7, 10-14, 57) thiết lập `overlays: []` và `vocabWordIds: []`.
  - Cột bên phải hiển thị trạng thái rỗng thân thiện (Friendly empty state: "Trang không có từ vựng bài học") và nút điều hướng nhanh ("Đến Bài 1 (Trang 15)"), tuyệt đối không để rò rỉ từ vựng của trang khác sang.

## 6. Kiểm thử & Đảm bảo Chất lượng
- Kiểm tra toàn vẹn dữ liệu: mọi `entryId` được lưu trong lớp phủ đều tồn tại trong `src/data/entries.json`.
- Kiểm tra file âm thanh: 100% từ vựng (99 từ) đều có sẵn 2 file âm thanh cục bộ tại `public/audio/vi/` và `public/audio/en/us/`.
- Kiểm thử responsive và trải nghiệm người dùng với Browser Subagent.

