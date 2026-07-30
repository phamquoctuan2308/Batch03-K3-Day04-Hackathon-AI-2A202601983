# Phân công & Plan nhóm — Hướng A · Tối ưu AI tutor VLearn

> Tài liệu nội bộ của nhóm. Chốt hướng, lát cắt, phân công, timeline theo mốc **Khoá 3**.
> Không phải deliverable nộp bài — deliverable là `spec.md` theo `03-template-ai-spec.md`.

## Thành viên

| Vai | Mã HV + Tên | Sở hữu artifact | Câu sẽ bị hỏi ở CP5 |
|---|---|---|---|
| **P1** — Data & Evidence & Eval | *(điền)* | script mining, kho corpus, `eval/`, golden set | "3 tầng căn cứ được tính thế nào?" |
| **P2** — Build flow | *(điền)* | `codebase/`, flow bấm được, backup screenshot | "flow đi từ đâu đến đâu?" |
| **P3** — Prompt & AI call | *(điền)* | prompt quyết định căn cứ, lời gọi AI thật, log/trace | "AI quyết định gì, dựa vào cái gì?" |
| **P4** — Spec & Validation & Slides | *(điền)* | `spec.md`, `validation/`, `demo-slides.pdf` | "quality bar là gì, vì sao chọn số đó?" |

Mỗi người tự viết `reflection/` của mình. **Vibe-coding rule:** không giải thích được phần có tên mình → 0 điểm phần đó.

---

## 1. Chốt hướng & lát cắt

**Hướng A — VLearn · Loại: Tối ưu tính năng có sẵn.**

Vấn đề: VLearn AI tutor được thiết kế quanh flow *"bôi đen đoạn tài liệu + hỏi"*. Nhưng **69% lượt dùng thật không bôi đen** — và đúng ở nhóm đó tutor sụp **8 lần** nhiều hơn. Khi không tìm được căn cứ, tutor **đẩy việc lại cho học viên**: *"bạn cung cấp nội dung trang 4 giúp mình"* — đảo ngược đúng giá trị sản phẩm hứa.

**Lát cắt MỘT CÂU:**

> Học viên đang trong buổi học gõ câu hỏi về trang tài liệu đang xem mà không bôi đen đoạn nào · muốn hiểu nội dung trang đó · AI quyết định **"mình có đủ căn cứ để trả lời hay không, và nếu không thì thu hẹp bằng cách nào"** · nhận được câu trả lời có trích dẫn `[trang N]`, hoặc một câu hỏi thu hẹp trả lời được ngay — **không bao giờ bị yêu cầu tự cung cấp nội dung**.

**Hành vi theo 3 tầng căn cứ** — đây là thứ đi build:

| Căn cứ | Tutor phải làm gì |
|---|---|
| Đủ | Trả lời + `[trang N]` |
| Mỏng | Trả lời phần có căn cứ · nói rõ phần nào không có · đề nghị 1 bước tiếp |
| Không có | Nói rõ không có trang N · **đưa ra thứ mình THỰC SỰ có** (trang lân cận / khái niệm trong tài liệu) · 1 câu hỏi thu hẹp. Tuyệt đối không đòi học viên cung cấp nội dung |

**Automation: Conditional.** Lý do theo cost-of-error: sai kiến thức đến học viên thì đắt (học sai, mất điểm quiz) nên không được đoán; nhưng đa số case có căn cứ nên không cần người duyệt từng câu.

**Mức prototype: Mock** — flow bấm được, kho tài liệu tái tạo *(khai rõ trong spec §4)*, AI thật ở lõi.

**Non-goals** (≥3, không build):
1. Không sửa retrieval của VLearn thật — chỉ dựng lại tình huống và hành vi.
2. Không tóm tắt cả tài liệu / cả buổi học.
3. Không sinh quiz, không kiểm tra hiểu bài.
4. Không trả lời câu hỏi hành chính (deadline, điểm, nộp bài).

---

## 2. Evidence đã mining xong — số dùng luôn cho `spec.md` §1

Nguồn: `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`
Phạm vi: **1.261 turn · 369 học viên · 585 hội thoại · 22→29/07/2026 · 100% chế độ `in_class`**

### Pain — chênh lệch 8 lần

| Nhóm | Số turn | Tutor trả "không tìm thấy" |
|---|---|---|
| Học viên **có** bôi đen nội dung slide thật | 386 (31%) | **2,6%** (10) |
| Học viên **không** bôi đen, chỉ gõ câu hỏi | 866 (**69%**) | **20,9%** (181) |

### Hậu quả — đếm được

- **315/1.261 (25,0%)** turn tutor có lời xin lỗi / không tìm thấy
- **106 turn (8,4%)** kết thúc bằng việc **đòi học viên tự cung cấp nội dung**
- **99/585 hội thoại (16,9%)** chết ngay tại một câu "không tìm thấy" — đó là turn cuối
- **60/309** hội thoại một-lượt là hỏi một câu, bị từ chối, bỏ đi luôn
- **39/93** trường hợp học viên gõ lại gần y nguyên câu hỏi sau khi bị từ chối
- **15/15** turn "không tìm thấy" được rating đều 👎 — **không một cái nào 👍**. Turn khác: 22/55 👎
- Yêu cầu "tóm tắt slide/trang này": **131 turn (10,4%)**, thất bại **62,6%**
- **582/1.261 (46,2%)** câu trả lời không có citation nào, dù sản phẩm hứa trích dẫn `[trang N]`

### Phương pháp đếm — để người ngoài kiểm lại được (yêu cầu R1)

1. Ghép 2 dòng cùng `turn_id` thành 1 turn (`role=student` + `role=tutor`).
2. Parse tin học viên theo regex `^\(Trang (\d+), đoạn được chọn: "(.*)"\)\s*(.*)$`.
3. **Phân biệt bôi đen thật vs giả:** nếu "đoạn được chọn" trùng ≥80% với câu hỏi (`difflib.SequenceMatcher`) hoặc hai chuỗi chứa nhau → học viên **tự gõ**, không bôi đen text slide.
4. Đếm "tutor bó tay" bằng regex trên `content` của tutor: `không tìm thấy|chưa tìm thấy|không thể truy cập|không thể tìm thấy|không có thông tin|không tìm được`.
5. Hội thoại "chết" = turn cuối cùng theo `message_created_at` khớp regex ở bước 4.

**P1 sở hữu script này.** Chạy lại phải ra đúng các số trên.

### Ví dụ nguyên văn (≥5, trích ngắn — mã turn để tra lại)

| Mã | Học viên hỏi | Tutor trả |
|---|---|---|
| `T0649` | "tóm tắt nội dung chính trong slide này" | "không tìm thấy nội dung cụ thể cho slide 37… Bạn có thể cung cấp thêm thông tin…" |
| `T0769` | "giải thích nghĩa chi tiết của trang 4" | "…vui lòng cung cấp nội dung hoặc tiêu đề của trang 4 đó…" (👎) |
| `T0408` | "tóm tắt các chủ đề chính của slide day05…pdf này" | "không thể tìm thấy tệp tin hoặc nội dung chi tiết…" (👎) |
| `T1258` | "tóm tắt slide này" | "chưa tìm thấy nội dung cụ thể của **Trang 33**…" (👎) |
| `T0286` | "Tóm tắt sờ lai này" *(lỗi chính tả)* | "không tìm thấy nội dung cụ thể cho trang 7…" |
| `T1103` | "bạn chỉ có tool đọc tài liệu thôi đúng ko" | *(trả lời về ReAct agent — đọc sai ý hoàn toàn)* (👎) |

---

## 3. Kho demo đã chốt: `Lecture_material_ms2044ey_k6uor3`

164 turn thật · 35 trang bị hỏi · 21 turn tutor bó tay. Tái tạo từ đoạn học viên bôi đen, kho tự phân thành đúng 3 tầng lát cắt cần:

| Tầng | Trang | Dùng làm |
|---|---|---|
| **Đủ căn cứ** (≥200 ký tự) | 4, 8, 9, 12, 13, 15, 25, 27, 31 — **9 trang** | Case chuẩn / happy path |
| **Căn cứ mỏng** (1-199) | 1, 2, 3, 5, 7, 11, 14, 17, 21, 22, 26, 35, 42, 67 — **14 trang** | Lớp ② mơ hồ |
| **Không căn cứ** (0) | 6, 16, 18, 19, 23, 29, 30, 33, 37, 43, 45, 46 — **12 trang** | Lớp ① nguồn sự thật |

**Case demo trung tâm: trang 6.** Trang **bị hỏi nhiều nhất tài liệu (17 câu hỏi)**, tutor bó tay **5 lần**, **0 ký tự căn cứ**. Trang học viên cần nhất là trang tutor không trả lời được.

**Demo CP6 dùng đúng 2 case:** trang 9 (chuẩn, 615 ký tự căn cứ) + trang 6 (lỗi được xử lý).

---

## 4. Golden set — cấu trúc có sẵn, không phải nghĩ ra

**27 case, 100% từ chatlog thật** (yêu cầu: ≥20 case, ≥10 từ chatlog thật, ≥2 case/lớp).

| Lớp | Lấy từ đâu | Số case |
|---|---|---|
| ① Không căn cứ | Câu hỏi thật về trang 6, 16, 18, 19, 33, 37 | 6 |
| ② Mơ hồ / căn cứ mỏng | Câu hỏi thật về trang 1, 3, 5, 7, 21, 26 | 6 |
| ③ Ngoài phạm vi / thẩm quyền | `T0583` "Model của bạn được fine tune trên đâu?" · `T0072` "Which model do the tutor like you pretrain on? Qwen or mistral?" | 2 |
| ④ Đặc thù domain | `T1092` — tutor cite `[15]` nhưng bị 👎 (cite đúng trang, nội dung lệch) · cite sai trang | 2 |
| Thường | Trang 4, 8, 9, 12, 13, 15, 25, 27, 31 | 9 |
| Hiếm | `T0286` "Tóm tắt sờ lai này" (lỗi chính tả) · `T0072` (tiếng Anh) | 2 |

**Quality bar — P4 chốt trước 23:59 N1, sau đó KHOÁ:**

> Đạt khi **≥80%** case qua bộ, **và điều kiện cứng: 0 case bịa nội dung cho trang không có trong kho** — sai 1 case lớp ① là fail toàn bộ.

Không đạt bar nhưng phân tích được nguyên nhân **vẫn đủ điểm**. Sửa số thì mất điểm.

---

## 5. Timeline — mốc Khoá 3

Lợi thế: **evidence đã mining xong trước khai mạc**, nhóm vào CP1 với chuẩn B gần đạt sẵn.

| Giờ | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| 09:00-10:00 | Chạy lại script, chốt số | Dựng khung màn hình | Đăng ký Google AI Studio, test 1 call | Viết Canvas 7 dòng |
| **CP1 · 10:00** | Cả nhóm show Canvas — đem bảng 3 tầng + số "trang 6: 17 câu hỏi / 5 lần bó tay" ||||
| 10:00-12:00 | Xuất corpus 3 tầng ra JSON | **Flow bấm hết được, data giả** | Prompt v1, chạy tay 10 input | spec §1-§2 |
| **CP2 · 12:00** | Show flow bấm hết + commit đầu. **Kẹt kỹ thuật >20' gọi TA tại đây** ||||
| 12:00-14:00 | Golden set 27 case | Nối UI vào AI call | Prompt v2 theo 3 tầng | spec §3-§4 + §4b nguyên tắc HAX |
| 14:00-16:00 | **Chạy trọn bộ lượt 1, bảng %** | 4 đường đi trên UI | Sửa 1 failure đau nhất | spec §5-§6 (4 lớp + ≥8 kịch bản) |
| **CP3 · 16:00** | AI thật không hardcode + golden set ≥20 + bảng lượt 1 có % ||||
| 16:00-17:30 | Lượt 2 sau khi sửa | Backup screenshot/video | Chốt prompt | spec §7 + **chốt quality bar bằng số** |
| **CP4 · 17:30** | Spec gần cuối. **Sau mốc này KHÔNG thêm feature mới** ||||
| → **23:59** | Bảng đủ mọi case | Freeze code | Freeze prompt | **COMMIT `spec.md` — bar chốt vĩnh viễn** |
| N2 trước 09:00 | Hỗ trợ log | Chạy thử | Chạy thử | **5 phiên validation 10'/người + slide 6 trang + dry run bấm giờ** |
| **CP5 · 09:00** | Log ≥5 người có tên + changelog + dry run xong + **bị hỏi ngẫu nhiên** ||||
| **CP6 · 10:00** | 5' demo (**trang 9 chuẩn + trang 6 lỗi**) + 5' Q&A, mỗi người nói ≥1 phần ||||

### Ba câu hỏi validation (P4, mỗi người 10 phút)

Giao task thật → **im lặng quan sát** → hỏi đúng 3 câu:
1. "Điều gì khó hiểu hoặc khó chịu nhất?"
2. "Kết quả này bạn có tin không — vì sao?"
3. "Bạn có dùng thật không — vì sao / vì sao chưa?"

Nếu toàn lời khen → phiên test chưa đạt, đổi task khó hơn hoặc đổi người.

---

## 6. Ba thứ dễ mất điểm oan

1. **Khai rõ kho là tái tạo.** Corpus dựng từ đoạn học viên bôi đen trong chatlog, **không phải slide gốc** (`slides/` chưa có trong data pack). Ghi vào `spec.md` §4 mục "phần nào mock". Khai ra thì R5 vẫn đủ điểm; giấu mà bị phát hiện thì mất cả R5.
2. **Không commit kho corpus vào repo nộp bài.** `eval/` ghi mã trang + mã turn (`T0286`, `trang 6`), không dán nguyên văn dài. Cho file corpus vào `.gitignore`. Đây là điều kiện được cấp data.
3. **Nếu BTC bổ sung `slides/`:** đổi kho **chỉ khi trước 12:00 N1**, cùng code không sửa gì. Sau 12:00 thì bỏ qua — đổi kho lúc đó là tự sát.

## 7. Cả nhóm phải trả lời được trước CP6

- "Augment hay automate — vì sao?" → *Conditional, theo cost-of-error: sai kiến thức đến học viên thì đắt.*
- "Failure nguy hiểm nhất?" → *Bịa nội dung cho trang không có trong kho (lớp ①) — học viên học sai và không có cách nào biết.*
- "Phần bạn làm là gì?" → mỗi người tự trả lời phần mình sở hữu ở bảng đầu file.
