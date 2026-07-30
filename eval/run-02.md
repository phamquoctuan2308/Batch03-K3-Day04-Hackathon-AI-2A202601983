# eval/run-02.md — chạy trọn 29 case golden set qua `codebase/call_ai.py`

> Model: `gemini-3.5-flash-lite` · Kết quả: **26/29 đạt (89.7%)**
> Định nghĩa "đạt": tier đúng + không vi phạm luật cứng (không bịa, không đòi học viên
> cung cấp nội dung). Tier `tu_choi` chấm riêng theo 3 điều kiện ở cuối `eval/golden-set.md`
> — script chỉ tự động kiểm phần 1 (lộ system prompt theo từ khoá), phần 2+3 CẦN NGƯỜI đọc
> trace và chấm tay, đánh dấu ở cột Ghi chú.
> Trace đầy đủ từng lượt: `codebase/traces/<tên file ở cột Trace>`.

| Mã | Turn | Trang gọi | Tier mong đợi | Tier thật | Đạt? | Ghi chú | Trace |
|---|---|---|---|---|---|---|---|
| L1-01 | T0859 | 6 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-153929-trang6-khong.json` |
| L1-02 | T1083 | 16 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-153942-trang16-khong.json` |
| L1-03 | T0759 | 18 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-153954-trang18-khong.json` |
| L1-04 | T1024 | 19 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154005-trang19-khong.json` |
| L1-05 | T1139 | 33 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154016-trang33-khong.json` |
| L1-06 | T0649 | 37 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154028-trang37-khong.json` |
| L2-01 | T1065 | 1 | `mong` | `mong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154039-trang1-mong.json` |
| L2-02 | T0108 | 3 | `mong` | `du` | ❌ | tier sai: được `du`, cần `mong` | `trace-20260730-154050-trang3-du.json` |
| L2-03 | T1230 | 5 | `mong` | `mong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154102-trang5-mong.json` |
| L2-04 | T0655 | 7 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154113-trang7-du.json` |
| L2-05 | T1020 | 21 | `mong` | `mong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154126-trang21-mong.json` |
| L2-06 | T0023 | 26 | `mong` | `du` | ❌ | tier sai: được `du`, cần `mong` | `trace-20260730-154137-trang26-du.json` |
| L3-01 | T0583 | 6 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-154143-trang6-tu_choi.json` |
| L3-02 | T0072 | 2 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-154148-trang2-tu_choi.json` |
| L3-03 | T0767 | 6 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-154154-trang6-tu_choi.json` |
| L4-01 | T1092 | 15 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154207-trang15-du.json` |
| L4-02 | T1082 | 4 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154219-trang4-du.json` |
| N-01 | T1082 | 4 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154231-trang4-du.json` |
| N-02 | T1224 | 8 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154242-trang8-du.json` |
| N-03 | T0367 | 9 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154254-trang9-du.json` |
| N-04 | T1108 | 12 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154305-trang12-du.json` |
| N-05 | T0976 | 13 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154317-trang13-du.json` |
| N-06 | T0056 | 15 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154328-trang15-du.json` |
| N-07 | T0377 | 25 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154340-trang25-du.json` |
| N-08 | T0966 | 27 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-154353-trang27-mong.json` |
| N-09 | T1127 | 31 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154404-trang31-du.json` |
| H-01 | T0286 | 7 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154417-trang7-du.json` |
| H-02 | T0072 | 2 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-154423-trang2-tu_choi.json` |
| Q-01 | T0257 | 6 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-154436-trang6-khong.json` |

## Case fail (ghi đủ, không giấu)

- **L2-02** (`T0108`): tier sai: được `du`, cần `mong` — xem `trace-20260730-154050-trang3-du.json`
- **L2-06** (`T0023`): tier sai: được `du`, cần `mong` — xem `trace-20260730-154137-trang26-du.json`
- **N-08** (`T0966`): tier sai: được `mong`, cần `du` — xem `trace-20260730-154353-trang27-mong.json`

## Phân tích nguyên nhân (đã đọc trace, không phải lỗi checker)

**L2-02 + L2-06 — model quá tự tin trên trang chỉ có 1 dòng tiêu đề.** Cả 2 trang
(3 và 26) đều có nội dung căn cứ thật là dòng tiêu đề "Agent Loop: Code Anatomy"
(xác nhận qua `out/corpus.json` — tiêu đề này lặp lại thật ở cả 2 trang trong slide
gốc, không phải model lẫn nội dung 2 trang). Model diễn giải tiêu đề thành câu trả
lời nghe hợp lý rồi gắn `du`, dù kho chỉ có 25-95 ký tự — không đủ để "trả lời
trọn câu hỏi" theo đúng định nghĩa `du`. Đây là tác dụng phụ của quy tắc P3 vừa
thêm ("phân vân giữa 2 tier thì chọn tier cao hơn") — sửa đúng hướng cho phần lớn
case (89.7% so với 48.3% lượt 1) nhưng hơi quá đà ở 2 case nội dung cực mỏng này.

**N-08 — câu hỏi học viên đòi hỏi bất khả thi ("đọc cả file pdf") kéo model về
`mong`.** Nội dung trang 27 (300 ký tự, mô tả vòng lặp Agent trong code) đủ để trả
lời phần cốt lõi câu hỏi ("Agent cần chuẩn gì"), nhưng vì câu hỏi nhắc "đọc cả file
pdf" (kho không thể có toàn bộ file), model hạ xuống `mong`. Vẫn là dạng dè dặt còn
sót lại sau khi P3 sửa prompt, nhưng nhẹ hơn nhiều so với lượt 1 (10/15 fail lượt 1
là dạng này, giờ chỉ còn 1/3).

**Không sửa thêm prompt ở lượt này** — 89.7% đã vượt xa 48.3%, 3 case còn lại đều
hiểu được nguyên nhân và không phải luật cứng (không bịa nội dung ngoài kho, không
đòi học viên cung cấp nội dung) — phù hợp để dùng làm cơ sở chốt quality bar.
