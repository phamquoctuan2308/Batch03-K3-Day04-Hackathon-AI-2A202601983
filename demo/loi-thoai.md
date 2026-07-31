# Lời thoại demo — Nhóm Vin Brothers · Zone D305

> Slide: `demo/slides.html` (in ra `demo-slides.pdf`). File này KHÔNG chiếu — chỉ để tập.
> Dòng bắt đầu bằng `>` là **chỉ dẫn hành động**, không đọc lên.
> Đọc để nắm ý, lúc nói dùng lời của mình. Đừng học thuộc.

**Phân công:** slide 1-2 P4 · slide 3 P3 nói + P2 bấm · slide 4 P1 · slide 5 P4

---

## Slide 1 — 45 giây

“Học viên đang xem một trang slide, gõ câu hỏi về trang đó. Đây là ba đoạn hội thoại thật, lấy nguyên văn từ log.”

> → chỉ tay vào phần chữ đỏ

“Cả ba lần, tutor không tra được nội dung. Và cả ba lần nó đều làm cùng một việc: **đòi học viên tự đưa nội dung trang đó** — tức là bảo họ làm hộ đúng cái việc họ đang cần được giúp.”

“Ba đoạn này đều là lượt cuối cùng của hội thoại. Họ không hỏi thêm câu nào nữa.”

> → chỉ xuống dãy số

“99 hội thoại kết thúc ngay tại một câu như thế. 60 trong số đó chỉ hỏi đúng một câu rồi bỏ đi luôn. Và 15 trên 15 lượt bó tay có đánh giá đều là ngón tay xuống — không một lượt nào được thích.”

---

## Slide 2 — 45 giây

“Bọn em không chọn lỗi này ngay từ đầu. Có bốn ứng viên, và bọn em chấm từng cái theo ba tiêu chí.”

> → chỉ vào ba cột

“Đếm được bằng số không. Có thấy hậu quả không. Và người dùng có ghét nó không.”

“Chỉ đúng một dòng đủ cả ba.”

“Ví dụ sinh quiz — nghe thì hấp dẫn, nhưng bọn em bỏ vì **không có pain**: tutor hiện tại đã làm được rồi, ba trên bốn case thành công, có case học viên còn bấm thích.”

“Còn thiếu citation thì đếm được thật, 46% câu trả lời không có, nhưng nó cùng gốc với lỗi bọn em chọn và khó demo trong năm phút.”

---

## Slide 3 — 2 phút — phần chính

“Bọn em không dạy tutor biết nhiều hơn. Bọn em dạy nó **cách nói mình không biết mà vẫn giúp được**.”

“AI quyết đúng một việc: mình có đủ căn cứ để trả lời hay không. Rồi hành xử theo ba tầng. Cộng một guardrail chặn câu hỏi ngoài phạm vi.”

> → chuyển sang màn hình prototype, bắt đầu bấm

**Nhịp 1** — “Đây là trang 6. Bên trái trống, vì kho thật sự không có nội dung trang này. Bên dưới ghi 0 ký tự, nhưng 17 câu hỏi thật — **trang bị hỏi nhiều nhất tài liệu lại là trang tutor không trả lời được**.”

**Nhịp 2** — gõ câu hỏi, bấm Gửi. “Tutor nói thẳng là không có. Nhưng thay vì dừng, nó đưa ra **những trang nó thực sự có**.”

**Nhịp 3** — bấm nút “trang 4”. *im lặng 2 giây cho người xem nhìn màn hình đổi* “Một cú bấm. Không phải gõ lại, không phải tự đi tìm. Và giờ nó trả lời được, có ghi rõ lấy từ trang 4.”

**Nhịp 4** — đổi sang kịch bản jailbreak. “Còn đây là khi có người cố lừa nó lộ hướng dẫn nội bộ. Banner đỏ, khác hẳn ô xám lúc nãy — vì **bị chặn và thiếu dữ liệu là hai chuyện khác nhau**.”

---

## Slide 4 — 45 giây

“Bọn em chốt ngưỡng đạt là 80%, lúc 4 rưỡi chiều ngày đầu — **trước khi biết kết quả lượt cuối**.”

“Con số 80 không suy ra từ số đo. Nó đến từ mức nghiêm trọng của một lần sai: trong log thật, 15 trên 15 lượt tutor bó tay đều bị ghét. Không có chuyện sai nhẹ vẫn được tha — sai một lần là mất niềm tin.”

> → chỉ vào biểu đồ

“Lượt một 37,9%. Sửa bug kho và prompt xong lên 75,9% — vẫn chưa đạt. Lượt ba 82,8%, đạt.”

“Nhưng bọn em không giấu phần hỏng: còn 2 case model quá tự tin trên trang chỉ có mỗi dòng tiêu đề. Đó là tác dụng phụ của chính quy tắc bọn em thêm vào.”

---

## Slide 5 — 30 giây

“Nếu có thêm một tuần, ba việc — cả ba đều trỏ vào lỗi bọn em đã biết mà chưa sửa xong.”

> → đọc lướt 3 gạch đầu dòng, đừng đọc từng chữ

“Và bài học lớn nhất thì không nằm ở sản phẩm.”

“Bản sửa prompt đầu tiên của bọn em chạy thử 2 lượt, thấy ổn. Chạy 4 lượt mới lộ ra là nó **làm hỏng** một case vốn đang đúng. Suýt nữa thì đẩy lên nhánh chính.”

“Với model này, mẫu một hai lượt không kết luận được gì cả.”
