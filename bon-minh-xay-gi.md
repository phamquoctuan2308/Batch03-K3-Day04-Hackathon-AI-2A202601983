# Bọn mình đang xây cái gì

> Đọc file này trước. Nó giải thích **sản phẩm**.
> Còn `phan-cong-nhom.md` là chi tiết thi hành — ai làm gì, mấy giờ, chấm điểm ra sao.

**Hướng A — Tối ưu AI tutor VLearn.**

---

## Chuyện đã xảy ra thật

Hội thoại `T0769` trong chatlog:

> **Học viên** *(đang xem trang 4)*
> "giải thích nghĩa chi tiết của trang 4"
>
> **AI tutor**
> "Rất xin lỗi, hiện tại hệ thống tìm kiếm không tìm thấy nội dung cụ thể cho trang 4. Bạn có thể vui lòng **cung cấp nội dung hoặc tiêu đề của trang 4** đó để mình hỗ trợ giải thích rõ hơn cho bạn không?"
>
> → học viên bấm 👎

Đọc lại lần nữa cho kỹ:

**Học viên hỏi *vì* họ không hiểu trang 4 — và tutor nhờ họ tóm tắt trang 4 cho nó.**

Đây không phải lỗi lẻ.

---

## Nó xảy ra ở đa số lượt dùng

Đo trên **1.261 lượt hỏi thật · 369 học viên · 585 hội thoại**.

VLearn tutor được thiết kế cho flow *"bôi đen đoạn tài liệu rồi hỏi"*. Nhưng phần lớn học viên không bôi đen gì — họ chỉ gõ câu hỏi.

| Số | Nghĩa là gì |
|---|---|
| **62,7%** | lượt dùng **không** bôi đen đoạn nào |
| **9,5×** | tỉ lệ tutor bó tay cao hơn ở nhóm đó — 22,9% so với 2,4% |
| **99 / 585** | hội thoại **chết ngay** tại câu "không tìm thấy", không có lượt sau |
| **15 / 15** | lượt "không tìm thấy" có đánh giá đều là 👎 — **không một lượt nào 👍** |

Số cuối là thứ đáng chú ý nhất: trong toàn bộ chatlog, đây là loại lỗi bị học viên ghét nhất. Các lượt khác tỉ lệ 👎 là 22/55.

---

## Cái bọn mình xây

**Một quyết định duy nhất của AI: "mình có đủ căn cứ để trả lời hay không?"**

Trả lời xong câu đó thì có ba cách hành xử. Toàn bộ prototype là làm cho **ba cách này khác nhau rõ rệt trên màn hình**.

### 1. Đủ căn cứ → trả lời, kèm trích dẫn

Có nội dung trang đó trong kho. Trả lời bình thường, nhưng phải chỉ ra căn cứ ở đâu để học viên tự kiểm.

> Đoạn này nói về … `[trang 9]`

### 2. Căn cứ mỏng → trả lời phần chắc, nói rõ phần không chắc

Chỉ có một mẩu nội dung. Trả lời phần có căn cứ, và **nói thẳng phần nào mình đang không có** — thay vì lấp đầy bằng phỏng đoán.

> Phần đầu trang 1 nói về … `[trang 1]`
> *Phần còn lại của trang này mình chưa có nội dung, nên mình không suy diễn.*

### 3. Không có căn cứ → nói thật, rồi đưa ra thứ mình thực sự có

**Đây là chỗ tutor hiện tại hỏng.** Nó đẩy việc về cho học viên. Bọn mình không bao giờ làm thế — nói rõ mình không có, rồi mở đúng một đường đi tiếp.

> Mình chưa có nội dung trang 6. Những trang mình có quanh đó là 4, 5 và 7.
> `[ Giải thích trang 4 ]` `[ Giải thích trang 5 ]` `[ Giải thích trang 7 ]`

*(Ba ví dụ trên là hành vi bọn mình **thiết kế**, không phải output thật — đây chính là thứ P2 phải dựng và P3 phải làm cho AI sinh ra.)*

---

## Phạm vi

| Có làm | Không làm |
|---|---|
| Một màn hình: chọn trang, gõ câu hỏi, nhận trả lời | Không sửa VLearn thật — dựng lại tình huống thôi |
| Ba cách hành xử ở trên, nhìn là thấy khác nhau | Không tóm tắt cả tài liệu, cả buổi học |
| Một lời gọi AI thật ở đúng quyết định "có căn cứ hay không" | Không sinh quiz, không kiểm tra hiểu bài |
| Bộ 27 câu hỏi thật lấy từ chatlog, để đo đúng bao nhiêu % | Không trả lời deadline, điểm, nộp bài |

---

## Ai làm gì — bản một dòng

| | |
|---|---|
| **P1** | **Kho tài liệu + đo.** Dựng kho 3 tầng từ chatlog, xây bộ 27 câu hỏi, chạy và ra bảng phần trăm |
| **P2** | **Màn hình.** Làm cho bấm đi hết được, và ba cách hành xử hiện ra khác nhau rõ ràng |
| **P3** | **Quyết định của AI.** Viết prompt phân loại ba tầng, gọi AI thật, lưu lại vết chạy |
| **P4** | **Spec + người dùng thử.** Viết tài liệu thiết kế, chốt ngưỡng đạt, đưa cho 5 người ngoài nhóm dùng thử |

Chi tiết giờ giấc, mốc bàn giao, cắt gì khi chậm: xem `phan-cong-nhom.md`.

---

## Nếu chỉ nhớ một câu

**Bọn mình dạy tutor cách nói "mình không biết" mà vẫn giúp được.**

Điểm không nằm ở sản phẩm hoành tráng — nằm ở chuỗi quyết định và bằng chứng.
