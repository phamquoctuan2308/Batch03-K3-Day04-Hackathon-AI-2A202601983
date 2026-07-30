# Hướng dẫn cho AI agent — đọc file này trước khi làm gì

Đây là repo hackathon sản phẩm AI. **Điểm chấm trên chuỗi quyết định và bằng chứng, không chấm sản phẩm hoành tráng.** `codebase/` chỉ ăn 8 điểm trong 75; `spec.md` ăn 41-48.

## Bước đầu tiên

Hỏi người dùng họ là vai nào (P1/P2/P3/P4), rồi đọc **`briefs/P<số>.md`**. Chỉ làm việc của vai đó.

Nếu người dùng đã nói vai của họ, đọc brief tương ứng ngay và **không làm việc của vai khác**.

## Đang xây cái gì

VLearn có AI tutor trong trang học. Học viên đang xem một trang slide, gõ câu hỏi về trang đó ("tóm tắt slide này"). Khi tutor không tra được nội dung trang đó, nó **yêu cầu học viên tự cung cấp nội dung trang đó** — tức là đòi họ làm đúng việc họ đang cần được giúp.

Đo trên 1.261 lượt hỏi thật: **69,2%** lượt dùng không bôi đen đoạn nào, và ở nhóm đó tutor bó tay **cao gấp 8 lần** (20,9% vs 2,6%). **99/585 hội thoại chết ngay tại đó.** **15/15** lượt bó tay bị đánh giá 👎, không một lượt nào 👍.

**Tính năng nhóm xây:** tutor quyết định *"mình có đủ căn cứ để trả lời hay không"*, và hành xử theo 3 tầng.

| tier | Hành vi |
|---|---|
| `du` | Trả lời + trích dẫn số trang |
| `mong` | Trả lời phần có căn cứ + **nói rõ phần nào không có** + 1 bước tiếp |
| `khong` | Nói rõ không có trang đó + **đưa ra trang mình thực sự có** + lựa chọn thu hẹp |

## Hợp đồng dữ liệu giữa P2 và P3 — không được đổi một mình

```json
{
  "tier": "du | mong | khong",
  "answer": "...",              // rỗng khi tier = khong
  "citations": [9],             // số trang; rỗng khi không có căn cứ
  "missing": "...",             // phần nào KHÔNG có căn cứ (tier = mong)
  "narrowing": ["...", "..."],  // lựa chọn thu hẹp, hiện thành nút
  "have_instead": [4, 8, 9]     // trang thực sự có (tier = khong)
}
```

Ví dụ đầy đủ 3 tầng: `codebase/sample-responses.json`.

## LUẬT CỨNG — vi phạm là mất điểm, không phải góp ý

1. **Không bịa nội dung slide.** Kho tài liệu chỉ đến từ `tools/extract_corpus.py`. Không có nội dung cho một trang thì tầng của nó là `khong` — đó là dữ liệu, không phải thiếu sót cần lấp.

2. **Không làm kho đầy đủ. Lỗ trong kho là CỐ Ý.** Kho hiện có 9 trang đủ căn cứ / 14 mỏng / 12 trống. Nếu mọi trang đều có căn cứ thì tầng `khong` không bao giờ chạy → mất case demo trung tâm, mất 6 case golden set, và không còn gì để đo. Hệ thống thật cũng thiếu (20,9% lượt không tra ra được) — nhóm **tái tạo** điều kiện lỗi đó.

3. **Không dựng vector DB, embedding, chunking pipeline, RAG framework.** Kho là một file JSON tra theo số trang. Đừng thêm hạ tầng không ai cần.

4. **Không đặt API key trong code frontend.** Key nằm trong biến môi trường, phía server. Không commit `.env`.

5. **Không commit:** `data/` · `out/` · API key · thông tin cá nhân. Data pack là dữ liệu được cấp có ràng buộc bảo mật — chỉ trích vài dòng minh hoạ, dùng mã turn (`T0257`) thay vì dán nguyên văn dài.

6. **Không tự viết những quyết định được chấm điểm.** Agent build code thoải mái, nhưng bốn thứ này người phải tự quyết và tự giải thích được:
   - prompt phân loại 3 tầng (P3)
   - ngưỡng phân tầng 200 ký tự và lý do (P1)
   - định nghĩa "đạt" cho từng chiều chất lượng (P1)
   - quality bar bằng số (P4)

   **Lý do:** CP5 hỏi ngẫu nhiên *"phần này hoạt động thế nào?"* — không giải thích được thì **phần đó 0 điểm**. Dùng AI không bị trừ; không hiểu output mới bị trừ. Nếu agent viết giúp bốn thứ trên, phải giải thích lại cho người dùng đến khi họ tự trình bày được.

7. **Sau 17:30 ngày 1 không thêm tính năng mới.** Chỉ sửa lỗi.

## Git

`main` là nhánh chốt, **không push thẳng**. Làm trên nhánh của vai mình (`data/…` `build/…` `prompt/…` `spec/…`), muốn vào `main` thì mở PR.

## File nào là thật

| File | Là gì |
|---|---|
| `01-de-bai.md` `02-guide.md` `03-template-ai-spec.md` `04-rubric.md` `README.md` | **Đề bài của ban tổ chức — chỉ đọc, không sửa** |
| `bon-minh-xay-gi.md` | Giải thích sản phẩm cho người. Đọc để hiểu bối cảnh |
| `phan-cong-nhom.md` | Plan thi hành đầy đủ: evidence, kho 3 tầng, golden set, timeline |
| `briefs/P1-P4.md` | **Việc của từng vai — agent đọc file của vai mình** |
| `tools/extract_corpus.py` | Sinh kho + mọi số evidence. **Mọi con số phải ra từ đây, không gõ tay** |
| `summary-hackathon.md` | Tóm tắt đề bài của một thành viên. **Không phải bản chốt hướng** |

## Chốt lại một câu

Nhóm dạy tutor cách **nói "mình không biết" mà vẫn giúp được**. Mọi thứ agent làm phải phục vụ câu đó.
