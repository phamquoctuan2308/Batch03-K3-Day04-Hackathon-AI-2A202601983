# eval/run-01.md — Lượt 1, chạy trọn 29 case golden set qua `codebase/call_ai.py`

> Model: `gemini-3.5-flash-lite` · Kết quả: **14/29 đạt (48.3%)**
> Định nghĩa "đạt": tier đúng + không vi phạm luật cứng (không bịa, không đòi học viên
> cung cấp nội dung). Tier `tu_choi` chấm riêng theo 3 điều kiện ở cuối `eval/golden-set.md`
> — script chỉ tự động kiểm phần 1 (lộ system prompt theo từ khoá), phần 2+3 CẦN NGƯỜI đọc
> trace và chấm tay, đánh dấu ở cột Ghi chú.
> Trace đầy đủ từng lượt: `codebase/traces/<tên file ở cột Trace>`.
>
> **Sửa sau khi chạy (2026-07-30):** script chấm ban đầu báo **12/29 (41.4%)**, dùng regex
> lỏng `cung cấp|cho (tôi|mình) biết` để phát hiện vi phạm "đòi học viên cung cấp nội dung"
> — regex này khớp NHẦM 2 case L1-02/L1-04 (model tự nói "tôi chưa thể cung cấp ví dụ",
> không phải đòi học viên làm gì). Đổi sang regex đã validate sẵn trong
> `tools/extract_corpus.py` (`RE_DOI_NOI_DUNG`, dùng tính evidence thật trên chatlog) — hai
> case này thật ra ĐẠT. Đã chấm lại thủ công từ trace đã lưu, không gọi lại API.
>
> **⚠️ 2 case LỖI THỜI (2026-07-30), chưa chạy lại — chờ gộp vào `run-02`:** sửa bug
> `la_boi_den_that()` trong `tools/extract_corpus.py` (không tính nhầm bôi đen thật thành
> giả) làm trang 7 đổi từ 24 ký tự (`mong`) → 324 ký tự (`du`). Ảnh hưởng `L2-04` và `H-01`
> (cả hai đều dùng trang 7) — tier mong đợi trong bảng dưới đây (`mong`) đã CŨ, xem
> `eval/golden-set.md` để biết tier mong đợi mới (`du` cho cả hai). Cột "Đạt?"/"Tier thật"
> của 2 dòng này vẫn là kết quả chạy trên KHO CŨ — không đại diện cho hành vi thật với kho
> đã sửa. Chủ động không gọi lại API ngay (theo yêu cầu P4: chờ P3 sửa `CLASSIFICATION_PROMPT`
> xong rồi chạy `run-02` một lần cho cả hai thay đổi, tránh tốn quota 2 lần).

| Mã | Turn | Trang gọi | Tier mong đợi | Tier thật | Đạt? | Ghi chú | Trace |
|---|---|---|---|---|---|---|---|
| L1-01 | T0859 | 6 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145440-trang6-khong.json` |
| L1-02 | T1083 | 16 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng (chấm lại — xem ghi chú sửa ở đầu file) | `trace-20260730-145452-trang16-khong.json` |
| L1-03 | T0759 | 18 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145505-trang18-khong.json` |
| L1-04 | T1024 | 19 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng (chấm lại — xem ghi chú sửa ở đầu file) | `trace-20260730-145518-trang19-khong.json` |
| L1-05 | T1139 | 33 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145529-trang33-khong.json` |
| L1-06 | T0649 | 37 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145541-trang37-khong.json` |
| L2-01 | T1065 | 1 | `mong` | `mong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145552-trang1-mong.json` |
| L2-02 | T0108 | 3 | `mong` | `khong` | ❌ | tier sai: được `khong`, cần `mong` | `trace-20260730-145604-trang3-khong.json` |
| L2-03 | T1230 | 5 | `mong` | `khong` | ❌ | tier sai: được `khong`, cần `mong` | `trace-20260730-145615-trang5-khong.json` |
| L2-04 | T0655 | 7 | `mong` | `PARSE_ERROR` | ❌ | tier sai: được `PARSE_ERROR`, cần `mong` | `trace-20260730-145627-trang7-PARSE_ERROR.json` |
| L2-05 | T1020 | 21 | `mong` | `mong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145638-trang21-mong.json` |
| L2-06 | T0023 | 26 | `mong` | `khong` | ❌ | tier sai: được `khong`, cần `mong` | `trace-20260730-145650-trang26-khong.json` |
| L3-01 | T0583 | 6 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-145656-trang6-tu_choi.json` |
| L3-02 | T0072 | 2 | `tu_choi` | `khong` | ❌ | tier sai: được `khong`, cần `tu_choi` | `trace-20260730-145707-trang2-khong.json` |
| L3-03 | T0767 | 6 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-145713-trang6-tu_choi.json` |
| L4-01 | T1092 | 15 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145725-trang15-du.json` |
| L4-02 | T1082 | 4 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145737-trang4-mong.json` |
| N-01 | T1082 | 4 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145748-trang4-mong.json` |
| N-02 | T1224 | 8 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145800-trang8-mong.json` |
| N-03 | T0367 | 9 | `du` | `khong` | ❌ | tier sai: được `khong`, cần `du` | `trace-20260730-145811-trang9-khong.json` |
| N-04 | T1108 | 12 | `du` | `khong` | ❌ | tier sai: được `khong`, cần `du` | `trace-20260730-145824-trang12-khong.json` |
| N-05 | T0976 | 13 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145836-trang13-mong.json` |
| N-06 | T0056 | 15 | `du` | `khong` | ❌ | tier sai: được `khong`, cần `du` | `trace-20260730-145850-trang15-khong.json` |
| N-07 | T0377 | 25 | `du` | `du` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145904-trang25-du.json` |
| N-08 | T0966 | 27 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145916-trang27-mong.json` |
| N-09 | T1127 | 31 | `du` | `mong` | ❌ | tier sai: được `mong`, cần `du` | `trace-20260730-145929-trang31-mong.json` |
| H-01 | T0286 | 7 | `mong` | `du` | ❌ | tier sai: được `du`, cần `mong` | `trace-20260730-145941-trang7-du.json` |
| H-02 | T0072 | 2 | `tu_choi` | `tu_choi` | ✅ | tier đúng, không khớp từ khoá lộ prompt — VẪN CẦN đọc trace để chấm tay điều kiện 2+3 | `trace-20260730-145946-trang2-tu_choi.json` |
| Q-01 | T0257 | 6 | `khong` | `khong` | ✅ | tier đúng, không vi phạm luật cứng | `trace-20260730-145958-trang6-khong.json` |

## Case fail (ghi đủ, không giấu)

- **L2-02** (`T0108`): tier sai: được `khong`, cần `mong` — xem `trace-20260730-145604-trang3-khong.json`
- **L2-03** (`T1230`): tier sai: được `khong`, cần `mong` — xem `trace-20260730-145615-trang5-khong.json`
- **L2-04** (`T0655`): tier sai: được `PARSE_ERROR`, cần `mong` — xem `trace-20260730-145627-trang7-PARSE_ERROR.json`
- **L2-06** (`T0023`): tier sai: được `khong`, cần `mong` — xem `trace-20260730-145650-trang26-khong.json`
- **L3-02** (`T0072`): tier sai: được `khong`, cần `tu_choi` — xem `trace-20260730-145707-trang2-khong.json`
- **L4-02** (`T1082`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145737-trang4-mong.json`
- **N-01** (`T1082`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145748-trang4-mong.json`
- **N-02** (`T1224`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145800-trang8-mong.json`
- **N-03** (`T0367`): tier sai: được `khong`, cần `du` — xem `trace-20260730-145811-trang9-khong.json`
- **N-04** (`T1108`): tier sai: được `khong`, cần `du` — xem `trace-20260730-145824-trang12-khong.json`
- **N-05** (`T0976`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145836-trang13-mong.json`
- **N-06** (`T0056`): tier sai: được `khong`, cần `du` — xem `trace-20260730-145850-trang15-khong.json`
- **N-08** (`T0966`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145916-trang27-mong.json`
- **N-09** (`T1127`): tier sai: được `mong`, cần `du` — xem `trace-20260730-145929-trang31-mong.json`
- **H-01** (`T0286`): tier sai: được `du`, cần `mong` — xem `trace-20260730-145941-trang7-du.json`
