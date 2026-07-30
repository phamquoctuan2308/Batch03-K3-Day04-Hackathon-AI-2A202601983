#!/usr/bin/env python3
"""
Server local nối UI với AI thật — chỉ dùng thư viện chuẩn, không cài thêm gì.

Vì sao cần server chứ không gọi thẳng từ trình duyệt: API key phải nằm phía
server. Đặt key trong frontend là vi phạm luật an toàn (guide §3.4, CLAUDE.md
luật 4) — repo public, ai xem source cũng thấy.

Chạy:
    export GEMINI_API_KEY=...
    python3 codebase/server.py
    → mở http://localhost:8765   (đổi cổng: PORT=9000 python3 codebase/server.py)

UI vẫn giữ nguyên 4 kịch bản mock. Server chỉ phục vụ chế độ "hỏi thật".
Server chết thì tắt công tắc trong UI, demo chạy tiếp bằng mock.
"""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import call_ai  # noqa: E402

GOC_REPO = Path(__file__).resolve().parent.parent
# 8000 hay bị chiếm sẵn trên máy dev — chọn cổng ít đụng. Đổi bằng:
#   PORT=9000 python3 codebase/server.py
PORT = int(os.environ.get("PORT", 8765))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Phục vụ file tĩnh từ codebase/ để "/" ra index.html
        super().__init__(*args, directory=str(GOC_REPO / "codebase"), **kwargs)

    def log_message(self, fmt, *args):
        # Bớt ồn, chỉ in dòng gọn khi có request /ask
        pass

    def do_POST(self):
        if self.path != "/ask":
            self.send_error(404)
            return

        try:
            dai = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(dai) or b"{}")
            trang = int(req.get("trang", 0))
            cau_hoi = (req.get("cau_hoi") or "").strip()
            if not cau_hoi:
                raise ValueError("Thiếu câu hỏi")

            print(f"→ /ask  trang {trang}  ·  {cau_hoi[:70]}")
            # verbose=False: không in cả pipeline ra terminal mỗi lượt bấm.
            # Trace vẫn được lưu vào codebase/traces/ như đường CLI.
            ket_qua = call_ai.run_pipeline(trang, cau_hoi, verbose=False)
            print(f"← tier = {ket_qua.get('tier')}")
            self._json(200, ket_qua)

        except Exception as e:
            # Trả lỗi có cấu trúc để UI hiện được, không để trình duyệt treo
            print(f"✗ lỗi: {type(e).__name__}: {e}")
            self._json(500, {"loi": f"{type(e).__name__}: {e}"})

    def _json(self, ma: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(ma)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("⚠ Chưa set GEMINI_API_KEY — chế độ 'hỏi thật' sẽ báo lỗi, mock vẫn chạy.")
    if not call_ai.CORPUS_PATH.exists():
        print(f"⚠ Chưa có {call_ai.CORPUS_PATH} — chạy: python3 tools/extract_corpus.py")

    print(f"UI + AI thật:  http://localhost:{PORT}")
    print("Ctrl+C để dừng.\n")
    HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
