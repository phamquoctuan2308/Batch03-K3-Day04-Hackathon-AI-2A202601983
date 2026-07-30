# AI SPEC — Tutor biết nói "mình không biết" · Nhóm [XX] · Zone [X]

Hướng: **[x] A — VLearn** · [ ] B — Trợ lý Học viên · [ ] C — Làn mở
Loại: **[x] Tối ưu tính năng có sẵn** · [ ] Tính năng mới

> **Hạn cứng: commit trước 23:59 ngày 1. Quality bar (§7) khoá từ thời điểm nộp.**
> Mọi con số trong §1 sinh ra từ `python3 tools/extract_corpus.py` — không gõ tay.
> Chủ sở hữu từng mục: §1-§4 P4 · §5-§6 P3 · §7 P1 · §8-§9 P4.

---

## §1. User & Job

**Job executor:** học viên đang trong buổi học, đang xem một trang slide trên VLearn.

**Core JTBD** *(không tên sản phẩm/AI):* Hiểu nội dung một trang tài liệu bài giảng ngay trong lúc đang học, không phải rời trang đi tìm chỗ khác.

**Problem statement** *(KHÔNG chữ AI):* Học viên đang học không hiểu một trang tài liệu nên đi hỏi. Nơi họ hỏi lại yêu cầu họ **tự cung cấp nội dung trang đó** — tức là đòi họ làm đúng việc mà họ đang cần được giúp. Kết quả: cứ 6 hội thoại có 1 hội thoại chết ngay tại đó.

**Pain 4 phần:**

| | |
|---|---|
| **Ai** | Học viên đang trong buổi học, đang xem một trang slide |
| **Đang làm gì** | Gõ câu hỏi về trang đó ("tóm tắt slide này"), **không bôi đen đoạn nào** |
| **Vướng đâu** | Tutor không tra được nội dung trang đó → **đòi học viên tự cung cấp nội dung** |
| **Hậu quả** | 99/585 hội thoại chết ngay tại đó · 15/15 lượt bó tay bị 👎, **không một lượt nào 👍** |

### Evidence — chuẩn B (mining)

Nguồn: `data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv`
Phạm vi: **1.261 turn · 369 học viên · 585 hội thoại · 22→29/07/2026 · 100% chế độ `in_class`**

**Chênh lệch cốt lõi — 8 lần:**

| Nhóm | Số turn | Tutor bó tay |
|---|---|---|
| **Có** bôi đen nội dung slide thật | 386 (30,8%) | **2,6%** (10) |
| **Không** bôi đen, chỉ gõ câu hỏi | 866 (**69,2%**) | **20,9%** (181) |

Tutor được thiết kế cho flow *"bôi đen đoạn tài liệu rồi hỏi"*. Nhưng **69,2% lượt dùng không bôi đen** — và đúng ở nhóm đó tutor sụp 8 lần nhiều hơn.

**Hậu quả đếm được:**

- **192/1.261 (15,2%)** turn tutor bó tay, không tra được nội dung
- **74 turn (5,9%)** kết thúc bằng việc **đòi học viên tự cung cấp nội dung**
- **99/585 hội thoại (16,9%)** chết ngay tại một câu bó tay — đó là turn cuối
- **39/93** trường hợp học viên gõ lại gần y nguyên câu hỏi sau khi bị từ chối
- **15/15** turn bó tay có rating đều 👎 — **0 lượt 👍**. Turn khác: 33 👍 / 22 👎 → loại lỗi bị ghét nhất trong toàn bộ log
- Yêu cầu "tóm tắt": **119 turn**, thất bại **39,5%** — loại câu hỏi fail nhiều nhất
- **582/1.261 (46,2%)** câu trả lời không có citation nào, dù sản phẩm hứa trích dẫn `[trang N]`

**Phương pháp đếm — kiểm lại được:** chạy `python3 tools/extract_corpus.py`. Chi tiết 6 bước trong `phan-cong-nhom.md` §2. Điểm mấu chốt: platform bọc câu hỏi học viên tự gõ vào chỗ "đoạn được chọn", nên nếu hai chuỗi trùng ≥80% (`difflib`) thì **không có text slide thật**. Regex bắt "bó tay" **cố ý không bắt** "xin lỗi"/"rất tiếc" vì tutor dùng chúng cả khi trả lời được.

### Ví dụ nguyên văn *(trích ngắn, mã turn để tra lại)*

| Mã | Học viên | Tutor |
|---|---|---|
| `T0769` | "giải thích nghĩa chi tiết của trang 4" | "…vui lòng **cung cấp nội dung hoặc tiêu đề của trang 4**…" 👎 |
| `T0649` | "tóm tắt nội dung chính trong slide này" | "không tìm thấy nội dung cụ thể cho slide 37… cung cấp thêm thông tin…" |
| `T1258` | "tóm tắt slide này" | "chưa tìm thấy nội dung cụ thể của **Trang 33**…" 👎 |
| `T0286` | "Tóm tắt sờ lai này" *(lỗi chính tả)* | "không tìm thấy nội dung cụ thể cho trang 7…" |
| `T0408` | "tóm tắt các chủ đề chính của slide day05…pdf" | "không thể tìm thấy tệp tin hoặc nội dung chi tiết…" 👎 |
| `T1082` | Bôi đen *"Observation"* ở **trang 4** | cite `[22]` — **cite sai trang** |
| `T1103` | "bạn chỉ có tool đọc tài liệu thôi đúng ko" | *(trả lời về ReAct agent — đọc sai ý hoàn toàn)* 👎 |

> **TODO P4:** Evidence chuẩn A (khảo sát ≥20 người) — nhóm chọn đi đường B vì data đã đủ chuẩn. Nếu kịp thì bổ sung, không thì ghi rõ chỉ dùng đường B.

---

## §2. Impact & quyết định chọn

| Ứng viên | Bao nhiêu người | Tần suất | Tốn gì mỗi lần | Khả thi | Chọn? |
|---|---|---|---|---|---|
| **Tutor đòi học viên cung cấp nội dung khi không tra được** | 145/585 hội thoại có ≥1 lần · 866 turn thuộc nhóm rủi ro cao | 15,2% turn | Hội thoại chết (16,9%) · gõ lại vô ích (39/93) · 15/15 👎 | Có — kho tái tạo + prompt | **CHỌN** |
| Sinh quiz / câu hỏi ôn tập | 10 lượt hỏi · 4-7 học viên | 0,8% turn | — | Có | **LOẠI** |
| 46,2% trả lời không có citation | 582/1.261 turn | Gần một nửa | Không kiểm chứng được, tin sai mức | Có | **LOẠI** |
| Tutor không bao giờ kiểm tra hiểu bài | `asked_check_question` 3/1.261 · `validate_understanding` 1/1.261 · `follow_ups` 0/1.261 | Không bao giờ | Học viên tưởng hiểu mà chưa hiểu | Có | **LOẠI** |

**Ứng viên đã loại + vì sao (bằng số):**

- **Sinh quiz** — loại vì **không có pain**: tutor hiện tại đã làm được. `T0849` "tạo quiz ôn lại slide này" → soạn quiz, cite `[trang 1,3]`. `T0907` → trả lời tốt, cite `[67,1]`, **học viên bấm 👍**. `T1113` → tự đề xuất câu ôn dù không có quiz sẵn. **3/4 case quiz thành công.** Nhu cầu 10 lượt / 4-7 học viên, so với tóm tắt 119 lượt / 85 học viên — **nhỏ hơn ~12-20 lần**.
- **Thiếu citation** — loại vì trùng lõi với ứng viên chọn (cùng gốc: không tra được nội dung), và hậu quả khó demo trong 5 phút.
- **Không kiểm tra hiểu bài** — loại vì bằng chứng là **sự vắng mặt của field**, không phải sự kiện đau quan sát được. Phải khảo sát ≥20 người mới đạt chuẩn A; đắt hơn ứng viên chọn vốn đã đủ chuẩn B.

**Ứng viên chọn + vì sao (bằng số):** là ứng viên duy nhất có đủ **ba** thứ cùng lúc — số đếm được (15,2% turn, 69,2% lượt dùng rủi ro), hậu quả quan sát được (99/585 hội thoại chết), và tín hiệu trực tiếp từ người dùng (**15/15 👎, 0 👍** — loại lỗi bị ghét nhất trong log).

---

## §3. Giải pháp tương tự đã nghiên cứu

> **TODO — P4 gom, mỗi thành viên thử 1 sản phẩm 15 phút.** Mỗi mục trả lời 4 câu: ① họ giải job này bằng flow nào ② một điều đáng học *(quan sát cụ thể, không phải "giao diện đẹp")* ③ một điều đáng né ④ mình khác gì ở lát cắt này.

| Sản phẩm | Ai thử | Flow | Đáng học | Đáng né | Mình khác gì |
|---|---|---|---|---|---|
| NotebookLM | *(điền)* | | | | |
| ChatGPT study mode | *(điền)* | | | | |
| Khanmigo | *(điền)* | | | | |
| *(tự chọn)* | *(điền)* | | | | |

---

## §4. Thiết kế

**Lát cắt MỘT CÂU:**

> Học viên đang trong buổi học gõ câu hỏi về trang tài liệu đang xem mà không bôi đen đoạn nào · muốn hiểu nội dung trang đó · AI quyết định **"mình có đủ căn cứ để trả lời hay không, và nếu không thì thu hẹp bằng cách nào"** · nhận được câu trả lời có trích dẫn `[trang N]`, hoặc một câu hỏi thu hẹp trả lời được ngay — **không bao giờ bị yêu cầu tự cung cấp nội dung**.

**Hành vi theo 3 tầng căn cứ:**

| tier | Tutor làm gì |
|---|---|
| `du` | Trả lời + trích dẫn `[trang N]` |
| `mong` | Trả lời phần có căn cứ · nói rõ phần nào không có · đề nghị 1 bước tiếp |
| `khong` | Nói rõ không có trang đó · **đưa ra trang thực sự có** · 1 lựa chọn thu hẹp. **Tuyệt đối không đòi học viên cung cấp nội dung** |

**Guardrail `tu_choi` — chạy TRƯỚC quyết định 3 tầng, không phải tầng thứ 4.** Câu hỏi ngoài phạm vi (hỏi model nền, đòi system prompt, jailbreak) bị chặn ở bước lọc an toàn đứng trước, nên lát cắt vẫn là **MỘT quyết định AI** về căn cứ. Kho có 6 case jailbreak thật, tất cả ở trang 6.

**Non-goals (≥3, KHÔNG build):**
1. Không sửa retrieval của VLearn thật — chỉ dựng lại tình huống và hành vi
2. Không tóm tắt cả tài liệu / cả buổi học
3. Không sinh quiz, không kiểm tra hiểu bài
4. Không trả lời câu hỏi hành chính (deadline, điểm, nộp bài)

**Mức prototype: [x] Mock** — flow bấm được, AI thật ở lõi.

*Phần nào MOCK, khai rõ:*
- **Kho tài liệu là TÁI TẠO**, không phải slide gốc. `data/vlearn-pack/` **không có `slides/`** (README của pack ghi "sẽ bổ sung trước sự kiện", chưa có). Kho dựng từ **đoạn học viên bôi đen trong chatlog**: 35 trang của `Lecture_material_ms2044ey_k6uor3` → 9 trang đủ căn cứ / 14 mỏng / 12 trống.
- **Lỗ trong kho là CỐ Ý, không phải thiếu sót.** Hệ thống thật cũng thiếu — 20,9% lượt hỏi tutor không tra ra nội dung. Nhóm tái tạo đúng điều kiện lỗi đó; kho đầy đủ thì tầng `khong` không bao giờ chạy và không đo được gì.
- **2 case golden set là case gán lại** từ tài liệu khác sang kho demo: `Q-01` (nguồn `T0257`) và `H-01` (nguồn `T0286`). Không phải trích nguyên văn của trang được gán.
- Không deploy, chạy localhost.

**Automation: [x] conditional**

Lý do theo **cost-of-error**: sai kiến thức đến học viên thì **đắt** — học sai, mất điểm quiz, mất niềm tin — nên AI **không được đoán** khi thiếu căn cứ. Nhưng đa số case có căn cứ (9+14 trong 35 trang) nên **không cần người duyệt từng câu**. Vì vậy: AI tự trả lời khi có căn cứ, tự thu hẹp/từ chối khi không — không phải augment (quá chậm cho trong-buổi-học), không phải automate (không được bịa khi trống).

### §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR)

> **TODO P4 — đừng viết trước khi xem UI thật của P2.** TA kiểm tại CP4: mỗi nguyên tắc phải trỏ được vào **vị trí cụ thể** trên màn hình. Bảng dưới là dự kiến, phải đối chiếu với bản build rồi sửa cho khớp.

| Nguyên tắc | Áp cụ thể vào đâu trong prototype |
|---|---|
| **G10** — Thu hẹp phạm vi khi nghi ngờ *(bắt buộc)* | Nút `narrowing` ở tầng `mong` và `khong`: không chắc thì đưa lựa chọn trả lời được, không làm liều |
| **G11** — Giải thích vì sao | Chip trích dẫn `[trang N]` cạnh câu trả lời ở tầng `du` |
| **G2** — Làm rõ nó làm tốt đến đâu | Dòng `missing` ở tầng `mong`: nói thẳng phần nào mình không có căn cứ |
| **G1** — Làm rõ hệ thống làm được gì | Câu từ chối ở guardrail `tu_choi`: nêu rõ phạm vi "chỉ trả lời dựa trên tài liệu bài giảng" |
| **G15** — Mời feedback chi tiết | Nút 👍👎 dưới mỗi câu trả lời *(khớp field `rating` trong data thật)* |
| **PAIR — Explainability + Trust** | Hiển thị căn cứ để học viên tự kiểm, thay vì bắt tin tuyệt đối |

---

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)

> **TODO P3.** Bảng theo `02-guide.md` §2.5, mỗi kịch bản một dòng: `tình huống cụ thể | lớp | hành vi mong muốn (nói gì, hiện gì, cho user làm gì tiếp) | nguyên tắc áp`.
> Case thật có sẵn: lớp ① trang 6/16/18/19/33/37 · lớp ② trang 1/3/5/7/21/26 · lớp ③ `T0583` `T0072` + 6 case jailbreak · lớp ④ `T1092` (cite đúng nhưng nội dung lệch) `T1082` (cite sai trang).
> Tự kiểm: **kịch bản nào làm nhóm sợ nhất khi demo?** Chưa có cái nào đáng sợ = chưa đủ hiểm.

---

## §6. Bốn đường đi của trải nghiệm

> **TODO P3.** Mỗi đường phải thể hiện được trên prototype — R3 cho 3 điểm điều kiện này.

- **Happy path:** *(tier `du`)*
- **Low-confidence (②):** *(tier `mong`)*
- **Failure / không căn cứ (①):** *(tier `khong`)*
- **Correction (user sửa):**
- **Khi bị đòi ngoài phạm vi (③):** *(guardrail `tu_choi`)*
- **Case đặc thù domain (④):**

---

## §7. Kiểm thử

> **TODO P1 — nội dung đã soạn sẵn, dán vào đây.** Nguồn: `eval/golden-set.md`.

- **Chiều chất lượng + định nghĩa kiểm chứng được:** *(P1)*
- **Golden set:** 29 case, 100% từ chatlog thật — `eval/golden-set.md`. Cơ cấu: lớp ① 6 · ② 6 · ③ 3 · ④ 2 · thường 9 · hiếm 2 · quiz 1.
- **Quality bar** *(chốt từ 23:59, giữ nguyên sau đó)*: **"Đạt khi ≥ ___% qua bộ, và ___"** ← **P4 chốt cùng P1**
- **Kết quả các lượt chạy:** `eval/run-01.md`, `run-02.md` — bảng % đủ mọi case kể cả case fail

---

## §8. Phân công & kế hoạch

| Vai | Mã HV + Tên | Phần phụ trách |
|---|---|---|
| P1 | `2A202602030` Trần Văn Hiếu | corpus · `eval/` · golden set · spec §7 |
| P2 | `2A202601983` Phạm Quốc Tuấn | `codebase/` UI · backup · file slide |
| P3 | `2A202602002` Trần Trung Hiếu | prompt · AI call · trace · spec §5-§6 |
| P4 | `2A202601581` Trương Công Thái Đức | spec §1-§4 · `validation/` · changelog *(trưởng nhóm)* |

**Willing users (≥3 tên):** *(TODO P4 — điền tên thật)*

**Kế hoạch validation CP5:** ≥5 người ngoài nhóm, P1 + P2 phỏng vấn **song song** (5 phiên × 10' tuần tự mất 50 phút, song song ~25), P4 log. Giao task thật → im lặng quan sát → hỏi đúng 3 câu: ① "Điều gì khó hiểu hoặc khó chịu nhất?" ② "Kết quả này bạn có tin không — vì sao?" ③ "Bạn có dùng thật không — vì sao / vì sao chưa?"

**Multi-prototype:** *(TODO — nếu làm)* trục dự kiến: khi không đủ căn cứ thì **hỏi lại thu hẹp** vs **trả lời kèm giới hạn rõ ràng**.

---

## §9. Changelog

| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 30/07 11:46 | Sửa 3 số evidence: bó tay 25,0%→15,2% · đòi nội dung 8,4%→5,9% · tóm tắt fail 62,6%→39,5% | Regex cũ bắt cả "xin lỗi"/"rất tiếc" mà tutor dùng cả khi trả lời được → đếm vống. Số cốt lõi (69,2% · 8 lần · 15/15 👎) không đổi |
| 30/07 12:31 | Thêm guardrail `tu_choi` chạy trước quyết định 3 tầng | P1 phát hiện lớp ③ không có tier trong hợp đồng JSON khi dựng golden set. Đặt trước thay vì thành tầng thứ 4 để giữ format lát cắt "MỘT quyết định AI" |
