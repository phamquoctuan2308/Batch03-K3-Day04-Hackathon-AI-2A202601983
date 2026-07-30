# validation/log.md — Feedback log vòng validation CP5

> Nhóm Vin Brothers · Zone D305 · phiên thử ngày 31/07/2026
> Cách làm theo `02-guide.md` §4.2. Mỗi người **10 phút**. P1 và P2 phỏng vấn song song, P4 ghi.

---

## Trước khi bắt đầu — kiểm 3 thứ

- [ ] `python3 codebase/server.py` chạy được trên máy dùng để thử, `.env` đã có `GEMINI_API_KEY`
- [ ] Mở sẵn `http://localhost:8765`, để dropdown ở **Trang 6**, công tắc **"Hỏi AI thật" BẬT**
- [ ] Mở sẵn file này để gõ trực tiếp trong lúc quan sát

## Cách chạy một phiên

**1. Giao task — đọc đúng một câu, không giải thích thêm:**

> *"Bạn đang học bài này và không hiểu trang đang xem. Dùng cái này để hiểu nó."*

**2. Rồi IM LẶNG.** Không hướng dẫn, không nói "bấm nút kia đi", không đỡ lời khi họ lúng túng.
Chỗ họ lúng túng **chính là dữ liệu** — ghi lại họ bấm gì, dừng ở đâu, hỏi lại gì.

**3. Sau khi họ dùng xong, hỏi đúng 3 câu:**

| # | Câu hỏi |
|---|---|
| ① | Điều gì khó hiểu hoặc khó chịu nhất? |
| ② | Kết quả này bạn có tin không — vì sao? |
| ③ | Bạn có dùng thật không — vì sao / vì sao chưa? |

**4. Ghi NGUYÊN VĂN lời họ nói.** Không tóm tắt, không sửa cho hay hơn.
Quote nguyên văn mới tính điểm; lời tóm tắt thì không.

> ⚠️ **Nếu mọi phản hồi đều là lời khen thì phiên test chưa đạt** (guide §4.2).
> Giao task khó hơn, hoặc đổi người thử.

---

## Bảng log

*(Mức nghiêm trọng: **cao** = chặn không dùng được · **vừa** = dùng được nhưng khó chịu · **thấp** = góp ý thẩm mỹ)*

| # | Người thử (tên · vai · willing user?) | Task giao | Quan sát *(họ bấm gì, kẹt đâu)* | Quote nguyên văn | Mức |
|---|---|---|---|---|---|
| 1 | Phan Hoàng Long · học viên cùng khoá · willing user | *(điền sau phiên)* |  |  |  |
| 2 | Phạm Nguyên Việt · học viên cùng khoá · willing user | *(điền sau phiên)* |  |  |  |
| 3 | Lục Minh Đức · học viên cùng khoá · willing user | *(điền sau phiên)* |  |  |  |
| 4 | *(chưa mời được)* |  |  |  |  |
| 5 | *(chưa mời được)* |  |  |  |  |

---

## Tổng hợp — điền sau khi xong cả 5 phiên

**Chủ đề lặp nhiều nhất:**
*(điều gì ≥2 người cùng nói? đó mới là tín hiệu, một người nói có thể là cá biệt)*

**1-2 thay đổi làm TRƯỚC demo:**
*(việc gì · vì sao · đã ghi vào `spec.md` §9 Changelog chưa)*

**Giữ nguyên có lý do:**
*(feedback nào nghe nhưng cố ý không sửa — và căn cứ để không sửa. Rubric tính cả trường hợp này, miễn có lý do)*

**Đưa vào backlog (lên slide 6):**

---

## Kiểm trước khi coi là xong

- [ ] Đủ **≥5 người ngoài nhóm**
- [ ] Mỗi dòng có **quote nguyên văn**, không phải lời tóm tắt
- [ ] Có **tên/vai** từng người
- [ ] Có **≥1 thay đổi từ feedback ghi trong `spec.md` §9**, hoặc giữ nguyên kèm lý do có căn cứ
- [ ] Không phải toàn lời khen

> **Rubric R6 — 8 điểm:** log ≥5 mẩu có quote + tên (4đ) · ≥1 thay đổi từ feedback hoặc giữ nguyên có lý do (4đ)
