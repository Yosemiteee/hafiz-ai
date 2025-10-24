"""Lightweight HTTP server for the Hafız AI web demo."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import unquote

from ..data import PASSAGES, PassageRepository
from ..evaluator import RecitationEvaluator


class HafizWebApp:
    """Core application logic for the demo web server."""

    def __init__(self) -> None:
        self.repository = PassageRepository(PASSAGES)
        self.evaluator = RecitationEvaluator()
        self.frontend_dir = Path(__file__).resolve().parent / "frontend"

    # Public API helpers -------------------------------------------------
    def list_passages(self) -> str:
        payload = [asdict(passage) for passage in self.repository.all()]
        return json.dumps(payload, ensure_ascii=False)

    def evaluate(self, passage_id: str, transcript: str, pronunciation: Optional[Dict[str, float]]) -> str:
        passage = self.repository.get(passage_id)
        feedback = self.evaluator.evaluate(
            expected_text=passage.arabic_text,
            actual_text=transcript,
            pronunciation_scores=pronunciation,
        )
        return json.dumps(asdict(feedback), ensure_ascii=False)

    # HTTP handling ------------------------------------------------------
    def resolve_asset(self, path: str) -> Optional[Path]:
        if not self.frontend_dir.exists():
            return None
        candidate = (self.frontend_dir / path).resolve()
        try:
            candidate.relative_to(self.frontend_dir.resolve())
        except ValueError:
            return None
        return candidate if candidate.exists() else None

    def serve_static(self, path: str) -> Tuple[HTTPStatus, Dict[str, str], bytes]:
        asset = self.resolve_asset(path)
        if not asset:
            return HTTPStatus.NOT_FOUND, {"Content-Type": "text/plain; charset=utf-8"}, b"Not Found"
        content_type = "text/plain; charset=utf-8"
        if asset.suffix == ".html":
            content_type = "text/html; charset=utf-8"
        elif asset.suffix == ".css":
            content_type = "text/css; charset=utf-8"
        elif asset.suffix == ".js":
            content_type = "application/javascript; charset=utf-8"
        body = asset.read_bytes()
        return HTTPStatus.OK, {"Content-Type": content_type}, body

    def dispatch(self, method: str, path: str, body: bytes) -> Tuple[HTTPStatus, Dict[str, str], bytes]:
        if method == "GET" and path == "/":
            return self.serve_static("index.html")
        if method == "GET" and path.startswith("/assets/"):
            asset_path = path.replace("/assets/", "", 1)
            return self.serve_static(asset_path)
        if method == "GET" and path == "/api/v1/passages":
            payload = self.list_passages().encode("utf-8")
            return HTTPStatus.OK, {"Content-Type": "application/json; charset=utf-8"}, payload
        if method == "POST" and path == "/api/v1/evaluate":
            try:
                data = json.loads(body.decode("utf-8")) if body else {}
            except json.JSONDecodeError:
                return HTTPStatus.BAD_REQUEST, {"Content-Type": "application/json; charset=utf-8"}, b"{}"
            passage_id = data.get("passage_id")
            transcript = data.get("transcript", "")
            pronunciation = data.get("pronunciation_scores")
            if not passage_id or transcript is None:
                return HTTPStatus.BAD_REQUEST, {"Content-Type": "application/json; charset=utf-8"}, b"{}"
            try:
                payload = self.evaluate(passage_id, transcript, pronunciation)
            except KeyError:
                return HTTPStatus.NOT_FOUND, {"Content-Type": "application/json; charset=utf-8"}, b"{}"
            return HTTPStatus.OK, {"Content-Type": "application/json; charset=utf-8"}, payload.encode("utf-8")
        return HTTPStatus.NOT_FOUND, {"Content-Type": "text/plain; charset=utf-8"}, b"Not Found"


class HafizRequestHandler(BaseHTTPRequestHandler):
    """HTTP handler bridging incoming requests to :class:`HafizWebApp`."""

    app = HafizWebApp()

    def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        status, headers, body = self.app.dispatch("GET", unquote(self.path), b"")
        self._write_response(status, headers, body)

    def do_POST(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length) if length else b""
        status, headers, body = self.app.dispatch("POST", unquote(self.path), data)
        self._write_response(status, headers, body)

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003 - keep quiet during tests
        return

    def _write_response(self, status: HTTPStatus, headers: Dict[str, str], body: bytes) -> None:
        self.send_response(status.value)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_dev_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start a blocking development server."""

    server = ThreadingHTTPServer((host, port), HafizRequestHandler)
    print(f"Hafız AI dev sunucusu {host}:{port} adresinde hazır. Tarayıcıdan açın.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu kapatılıyor...")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Hafız AI demo web sunucusu")
    parser.add_argument("--host", default="127.0.0.1", help="Sunucunun dinleyeceği adres")
    parser.add_argument("--port", type=int, default=8000, help="Sunucu portu")
    args = parser.parse_args()
    run_dev_server(args.host, args.port)


if __name__ == "__main__":
    main()
