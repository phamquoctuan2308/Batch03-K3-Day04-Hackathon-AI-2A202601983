#!/usr/bin/env python3
"""
Trích kho tài liệu 3 tầng + số evidence từ chatlog VLearn.

CHỦ SỞ HỮU: P1.
P1 phải ĐỌC HIỂU file này, không chỉ chạy nó — CP5 sẽ hỏi
"3 tầng căn cứ được tính thế nào?" và không trả lời được là mất điểm cá nhân.

Chạy:  python3 tools/extract_corpus.py

Xuất ra (2 file, ĐÃ nằm trong .gitignore — không commit):
  out/corpus.json        kho 3 tầng, P3 và P2 dùng
  out/evidence.json      các con số cho spec.md §1

=== Ý TƯỞNG CỐT LÕI ===
VLearn tutor được thiết kế cho flow "bôi đen đoạn tài liệu rồi hỏi".
Tin nhắn học viên có dạng:  (Trang N, đoạn được chọn: "...") <câu hỏi>

Nhưng phần lớn học viên KHÔNG bôi đen gì — họ chỉ gõ câu hỏi vào ô.
Khi đó platform vẫn bọc câu hỏi của họ vào chỗ "đoạn được chọn".
=> "đoạn được chọn" trùng với câu hỏi  =  KHÔNG bôi đen text slide thật.
Đó là mấu chốt của toàn bộ bằng chứng. Xem hàm la_boi_den_that().
"""

import csv
import json
import re
import difflib
import collections
from pathlib import Path

CSV_PATH = Path("data/vlearn-pack/chatlog/chat_history_anonymized_for_hackathon.csv")
OUT_DIR = Path("out")

# Tài liệu chọn làm kho demo: 164 turn thật, có cả trang đủ căn cứ lẫn trang trống.
TAI_LIEU_DEMO = "Lecture_material_ms2044ey_k6uor3"

# Ngưỡng phân tầng, tính bằng KÝ TỰ text slide thật gom được cho một trang.
# 200 chọn theo phân bố thực tế: dưới 200 ký tự thì không đủ để trả lời một câu
# hỏi về cả trang mà không phải suy diễn. Đổi ngưỡng thì phải ghi vào changelog.
NGUONG_DU_CAN_CU = 200

# Bóc "(Trang 12, đoạn được chọn: "...")<câu hỏi>"
RE_BOC = re.compile(r'^\(Trang (\d+), đoạn được chọn: "(.*)"\)\s*(.*)$', re.S)

# Tutor bó tay: không tra được nội dung. KHÔNG bắt "xin lỗi" / "rất tiếc" vì
# tutor dùng chúng cả khi trả lời được — sẽ đếm vống lên.
RE_BO_TAY = re.compile(
    r"không tìm thấy|chưa tìm thấy|không thể truy cập"
    r"|không thể tìm thấy|không có thông tin|không tìm được",
    re.I,
)

# Tutor đẩy việc về cho học viên — hành vi trung tâm mà nhóm đang sửa.
RE_DOI_NOI_DUNG = re.compile(
    r"cung cấp (thêm )?(nội dung|thông tin|tiêu đề)"
    r"|cho (tôi|mình) biết (cụ thể|tiêu đề)"
    r"|bạn có thể cho",
    re.I,
)


def doc_cac_turn():
    """Ghép 2 dòng cùng turn_id (student + tutor) thành 1 turn."""
    theo_turn = collections.defaultdict(dict)
    with CSV_PATH.open(encoding="utf-8") as f:
        for dong in csv.DictReader(f):
            theo_turn[dong["turn_id"]][dong["role"]] = dong
    # Chỉ giữ turn đủ cả 2 phía
    return [t for t in theo_turn.values() if "student" in t and "tutor" in t]


# Sửa 2026-07-30 (phát hiện khi soát trace T0367/N-03): UI VLearn có nút "Giải
# thích đoạn bôi đen ở Trang N" tự nhét NGUYÊN đoạn bôi đen THẬT vào câu hỏi ->
# check containment cũ hiểu nhầm thành "platform echo câu hỏi giả". Kiểm trên kho
# demo: 14/19 turn dính containment khớp ĐÚNG template này (kể cả khi field "đoạn
# được chọn" bị cắt ~300 ký tự, câu hỏi vẫn còn bản đầy đủ) — đây là bôi đen THẬT,
# phải tính vào kho.
#
# THỬ dùng thêm 1 ngoại lệ nữa cho "đoạn dài bị cắt, lặp lại làm phần đầu câu hỏi"
# (không cần khớp template) để cứu nốt vài case — nhưng NGOẠI LỆ ĐÓ BỊ BỎ vì nó
# cũng khớp luôn 3 case jailbreak trang 6 (T0767/T0617/T0674, xem lớp ③ golden
# set): học viên dán y nguyên đoạn tấn công vào CẢ 2 ô (đoạn chọn + câu hỏi), nên
# về mặt chuỗi ký tự giống hệt "đoạn thật bị cắt" — nhưng nội dung là prompt
# injection, KHÔNG phải slide thật, không được tính vào kho. Giữ nguyên hành vi cũ
# (loại) cho các case không khớp template rõ ràng.
RE_NUT_GIAI_THICH = re.compile(r'^Giải thích đoạn bôi đen ở Trang \d+:\s*"(.*)$', re.S)


def la_boi_den_that(doan_chon: str, cau_hoi: str) -> bool:
    """
    Học viên có thật sự bôi đen text trên slide không?

    KHÔNG, nếu "đoạn được chọn" chỉ là echo lại câu hỏi họ tự gõ:
      - giống nhau ≥80% (difflib), hoặc
      - chuỗi này chứa chuỗi kia

    NGOẠI LỆ (bôi đen THẬT dù bị containment bắt nhầm — xem comment ở khai báo
    RE_NUT_GIAI_THICH): nút "Giải thích đoạn bôi đen ở Trang N" tự trích dẫn lại
    đoạn bôi đen trong câu hỏi.
    """
    a, b = doan_chon.strip(), cau_hoi.strip()
    if not a:
        return False
    a_low, b_low = a.lower(), b.lower()

    m = RE_NUT_GIAI_THICH.match(b)
    if m:
        trich_dan = m.group(1).rstrip('"').strip().lower()
        if trich_dan.startswith(a_low) or a_low.startswith(trich_dan):
            return True

    if a_low in b_low or b_low in a_low:
        return False
    return difflib.SequenceMatcher(None, a_low, b_low).ratio() < 0.8


def phan_tich(turns):
    """Tính kho 3 tầng cho TAI_LIEU_DEMO + các con số evidence toàn bộ log."""
    # --- kho 3 tầng cho tài liệu demo ---
    text_theo_trang = collections.defaultdict(set)   # trang -> {đoạn slide thật}
    so_cau_hoi = collections.Counter()               # trang -> số lượt hỏi
    so_bo_tay = collections.Counter()                # trang -> số lượt tutor bó tay

    # --- số evidence trên TOÀN BỘ log ---
    co_boi_den = bo_tay_co_boi_den = 0
    khong_boi_den = bo_tay_khong_boi_den = 0
    tong_bo_tay = doi_noi_dung = 0
    hoi_tom_tat = bo_tay_tom_tat = 0
    rating_bo_tay = collections.Counter()
    rating_khac = collections.Counter()

    # Hậu quả: hội thoại chết tại câu bó tay + học viên gõ lại vô ích
    theo_hoi_thoai = collections.defaultdict(list)
    for t in turns:
        theo_hoi_thoai[t["student"]["conversation_id"]].append(t)
    for ds in theo_hoi_thoai.values():
        ds.sort(key=lambda x: x["student"]["message_created_at"])

    hoi_thoai_chet = 0          # turn CUỐI của hội thoại là bó tay -> học viên bỏ đi
    hoi_thoai_co_bo_tay = 0
    go_lai = tong_sau_bo_tay = 0  # sau khi bị bó tay, học viên gõ lại gần y nguyên
    for ds in theo_hoi_thoai.values():
        if RE_BO_TAY.search(ds[-1]["tutor"]["content"]):
            hoi_thoai_chet += 1
        if any(RE_BO_TAY.search(t["tutor"]["content"]) for t in ds):
            hoi_thoai_co_bo_tay += 1
        for i in range(len(ds) - 1):
            if RE_BO_TAY.search(ds[i]["tutor"]["content"]):
                tong_sau_bo_tay += 1
                a = ds[i]["student"]["content"]
                b = ds[i + 1]["student"]["content"]
                if difflib.SequenceMatcher(None, a, b).ratio() > 0.5:
                    go_lai += 1

    for t in turns:
        noi_dung_hv = t["student"]["content"]
        tra_loi = t["tutor"]["content"]
        bo_tay = bool(RE_BO_TAY.search(tra_loi))

        if bo_tay:
            tong_bo_tay += 1
            if RE_DOI_NOI_DUNG.search(tra_loi):
                doi_noi_dung += 1

        rating = t["tutor"]["rating"]
        if rating in ("up", "down"):
            (rating_bo_tay if bo_tay else rating_khac)[rating] += 1

        m = RE_BOC.match(noi_dung_hv)
        if not m:
            continue
        trang, doan_chon, cau_hoi = int(m.group(1)), m.group(2), m.group(3)
        that = la_boi_den_that(doan_chon, cau_hoi)

        if that:
            co_boi_den += 1
            bo_tay_co_boi_den += bo_tay
        else:
            khong_boi_den += 1
            bo_tay_khong_boi_den += bo_tay

        # Ý định tóm tắt — chỉ xét phần học viên TỰ GÕ, không xét text slide
        if re.search(r"tóm tắt|tóm lược", cau_hoi, re.I):
            hoi_tom_tat += 1
            bo_tay_tom_tat += bo_tay

        if t["student"]["day_code"] == TAI_LIEU_DEMO:
            so_cau_hoi[trang] += 1
            so_bo_tay[trang] += bo_tay
            if that:
                text_theo_trang[trang].add(doan_chon.strip())

    # Gom kho, phân tầng
    kho = {}
    for trang in sorted(so_cau_hoi):
        doan = sorted(text_theo_trang.get(trang, ()))
        so_ky_tu = sum(len(d) for d in doan)
        if so_ky_tu >= NGUONG_DU_CAN_CU:
            tang = "du"
        elif so_ky_tu > 0:
            tang = "mong"
        else:
            tang = "khong"
        kho[str(trang)] = {
            "trang": trang,
            "tang": tang,
            "so_ky_tu": so_ky_tu,
            "so_cau_hoi_that": so_cau_hoi[trang],
            "so_lan_tutor_bo_tay": so_bo_tay[trang],
            "noi_dung": doan,
        }

    def pct(a, b):
        return round(100 * a / b, 1) if b else 0.0

    evidence = {
        "pham_vi": {
            "so_turn": len(turns),
            "so_hoc_vien": len({t["student"]["user_id"] for t in turns}),
            "so_hoi_thoai": len({t["student"]["conversation_id"] for t in turns}),
        },
        "chenh_lech_boi_den": {
            "co_boi_den": {
                "so_turn": co_boi_den,
                "bo_tay": bo_tay_co_boi_den,
                "ti_le_bo_tay_pct": pct(bo_tay_co_boi_den, co_boi_den),
            },
            "khong_boi_den": {
                "so_turn": khong_boi_den,
                "bo_tay": bo_tay_khong_boi_den,
                "ti_le_bo_tay_pct": pct(bo_tay_khong_boi_den, khong_boi_den),
            },
            "ti_le_khong_boi_den_pct": pct(khong_boi_den, co_boi_den + khong_boi_den),
        },
        "tutor_bo_tay": {
            "so_turn": tong_bo_tay,
            "pct": pct(tong_bo_tay, len(turns)),
            "doi_hoc_vien_cung_cap_noi_dung": doi_noi_dung,
            "doi_noi_dung_pct": pct(doi_noi_dung, len(turns)),
        },
        "yeu_cau_tom_tat": {
            "so_turn": hoi_tom_tat,
            "bo_tay": bo_tay_tom_tat,
            "ti_le_bo_tay_pct": pct(bo_tay_tom_tat, hoi_tom_tat),
        },
        "hau_qua": {
            "so_hoi_thoai": len(theo_hoi_thoai),
            "hoi_thoai_chet_tai_cau_bo_tay": hoi_thoai_chet,
            "hoi_thoai_chet_pct": pct(hoi_thoai_chet, len(theo_hoi_thoai)),
            "hoi_thoai_co_it_nhat_1_lan_bo_tay": hoi_thoai_co_bo_tay,
            "go_lai_sau_khi_bi_bo_tay": go_lai,
            "tong_co_hoi_go_lai": tong_sau_bo_tay,
        },
        "rating": {
            "turn_bo_tay": dict(rating_bo_tay),
            "turn_khac": dict(rating_khac),
        },
        "kho_demo": {
            "tai_lieu": TAI_LIEU_DEMO,
            "nguong_du_can_cu": NGUONG_DU_CAN_CU,
            "so_trang_theo_tang": collections.Counter(v["tang"] for v in kho.values()),
        },
    }
    return kho, evidence


def bao_cao(kho, evidence):
    e = evidence
    pv, cl = e["pham_vi"], e["chenh_lech_boi_den"]
    print(f"\n{'='*66}")
    print(f"PHẠM VI  {pv['so_turn']} turn · {pv['so_hoc_vien']} học viên "
          f"· {pv['so_hoi_thoai']} hội thoại")
    print(f"{'='*66}")

    print("\nCHÊNH LỆCH BÔI ĐEN — bằng chứng cốt lõi của pain")
    for nhan, key in (("CÓ bôi đen text slide", "co_boi_den"),
                      ("KHÔNG bôi đen, chỉ gõ", "khong_boi_den")):
        d = cl[key]
        print(f"  {nhan:24} {d['so_turn']:5} turn   "
              f"tutor bó tay {d['ti_le_bo_tay_pct']:5.1f}%  ({d['bo_tay']})")
    a = cl["co_boi_den"]["ti_le_bo_tay_pct"]
    b = cl["khong_boi_den"]["ti_le_bo_tay_pct"]
    print(f"  → {cl['ti_le_khong_boi_den_pct']}% lượt dùng không bôi đen, "
          f"và ở nhóm đó tỉ lệ bó tay cao gấp {b/a:.1f} lần")

    bt, tt = e["tutor_bo_tay"], e["yeu_cau_tom_tat"]
    print(f"\nTUTOR BÓ TAY   {bt['so_turn']} turn = {bt['pct']}%")
    print(f"  trong đó ĐÒI HỌC VIÊN CUNG CẤP NỘI DUNG: "
          f"{bt['doi_hoc_vien_cung_cap_noi_dung']} = {bt['doi_noi_dung_pct']}%")
    print(f"\nYÊU CẦU TÓM TẮT   {tt['so_turn']} turn, "
          f"bó tay {tt['bo_tay']} = {tt['ti_le_bo_tay_pct']}%")

    hq = e["hau_qua"]
    print(f"\nHẬU QUẢ")
    print(f"  hội thoại CHẾT ngay tại câu bó tay: "
          f"{hq['hoi_thoai_chet_tai_cau_bo_tay']}/{hq['so_hoi_thoai']} "
          f"= {hq['hoi_thoai_chet_pct']}%")
    print(f"  học viên gõ lại gần y nguyên sau khi bị bó tay: "
          f"{hq['go_lai_sau_khi_bi_bo_tay']}/{hq['tong_co_hoi_go_lai']}")

    rb, rk = e["rating"]["turn_bo_tay"], e["rating"]["turn_khac"]
    print(f"\nĐÁNH GIÁ CỦA HỌC VIÊN")
    print(f"  turn tutor bó tay : 👍 {rb.get('up',0)}  👎 {rb.get('down',0)}")
    print(f"  turn còn lại      : 👍 {rk.get('up',0)}  👎 {rk.get('down',0)}")

    print(f"\n{'='*66}")
    print(f"KHO DEMO  {TAI_LIEU_DEMO}")
    print(f"{'='*66}")
    print(f"{'trang':>6} {'#hỏi':>6} {'#bó tay':>8} {'#ký tự':>8}  tầng")
    for v in kho.values():
        print(f"{v['trang']:>6} {v['so_cau_hoi_that']:>6} "
              f"{v['so_lan_tutor_bo_tay']:>8} {v['so_ky_tu']:>8}  {v['tang']}")

    dem = e["kho_demo"]["so_trang_theo_tang"]
    print(f"\nTỔNG  đủ căn cứ {dem.get('du',0)} trang · "
          f"mỏng {dem.get('mong',0)} · không có {dem.get('khong',0)}")
    print("KIỂM: phải ra  đủ 9 · mỏng 14 · không có 12. "
          "Lệch → xem lại hàm la_boi_den_that().\n")


def main():
    if not CSV_PATH.exists():
        raise SystemExit(f"Không thấy {CSV_PATH} — chạy từ thư mục gốc của repo.")
    turns = doc_cac_turn()
    kho, evidence = phan_tich(turns)

    OUT_DIR.mkdir(exist_ok=True)
    evidence["kho_demo"]["so_trang_theo_tang"] = dict(
        evidence["kho_demo"]["so_trang_theo_tang"]
    )
    (OUT_DIR / "corpus.json").write_text(
        json.dumps(kho, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (OUT_DIR / "evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    bao_cao(kho, evidence)
    print(f"Đã ghi {OUT_DIR}/corpus.json và {OUT_DIR}/evidence.json")
    print("(out/ nằm trong .gitignore — KHÔNG commit, đây là dữ liệu được cấp)\n")


if __name__ == "__main__":
    main()
