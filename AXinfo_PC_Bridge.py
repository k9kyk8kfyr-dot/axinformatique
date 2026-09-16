# -*- coding: utf-8 -*-
"""AXinfo PC Bridge - compatible with Python 3.4+ (no third-party packages)."""
import os
import json
import socket
import random
import string
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
PORT = 8765
TOKEN_FILE = os.path.join(ROOT, "axinfo_pc_token.txt")
DATA_FILE = os.path.join(ROOT, "AXinfo_PC_Data.json")
LAST_SEEN_FILE = os.path.join(ROOT, "AXinfo_PC_LastSeen.txt")
REVISION_FILE = os.path.join(ROOT, "AXinfo_PC_Revision.txt")


def make_token():
    chars = string.ascii_letters + string.digits
    rng = random.SystemRandom()
    return "".join(rng.choice(chars) for _ in range(32))


def load_or_create_token():
    try:
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, "r", encoding="utf-8") as fh:
                value = fh.read().strip()
            if value:
                return value
    except Exception:
        pass
    value = make_token()
    with open(TOKEN_FILE, "w", encoding="utf-8") as fh:
        fh.write(value)
    return value


TOKEN = load_or_create_token()


def current_revision():
    try:
        with open(REVISION_FILE, "r", encoding="utf-8") as fh:
            return int(fh.read().strip() or "0")
    except Exception:
        return 0

def bump_revision():
    value = current_revision() + 1
    try:
        with open(REVISION_FILE, "w", encoding="utf-8") as fh:
            fh.write(str(value))
    except Exception:
        pass
    return value



class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        super(Handler, self).end_headers()

    def _json(self, code, obj):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _token(self):
        try:
            q = parse_qs(urlparse(self.path).query)
            return q.get("token", [""])[0]
        except Exception:
            return ""

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/status":
            # Status endpoint is intentionally token-protected for the app's persistent heartbeat.
            if self._token() != TOKEN:
                self._json(403, {"ok": False, "error": "invalid token"})
                return
            try:
                with open(LAST_SEEN_FILE, "w", encoding="utf-8") as fh:
                    fh.write(str(__import__("time").time()))
            except Exception:
                pass
            self._json(200, {"ok": True, "hasData": os.path.exists(DATA_FILE), "revision": current_revision(), "updatedAt": os.path.getmtime(DATA_FILE) if os.path.exists(DATA_FILE) else 0})
            return

        if path == "/api/info":
            if self._token() != TOKEN:
                self._json(403, {"ok": False, "error": "invalid token"})
                return
            self._json(200, {"ok": True, "name": "AXinfo PC Bridge", "version": "v20", "sync": "local"})
            return

        if path == "/api/load":
            if self._token() != TOKEN:
                self._json(403, {"ok": False, "error": "invalid token"})
                return
            if not os.path.exists(DATA_FILE):
                self._json(200, {"ok": True, "data": None})
                return
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                self._json(200, {"ok": True, "data": data, "revision": current_revision(), "updatedAt": os.path.getmtime(DATA_FILE) if os.path.exists(DATA_FILE) else 0})
            except Exception as exc:
                self._json(500, {"ok": False, "error": str(exc)})
            return

        return super(Handler, self).do_GET()

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/api/save":
            self._json(404, {"ok": False, "error": "not found"})
            return
        if self._token() != TOKEN:
            self._json(403, {"ok": False, "error": "invalid token"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("data must be an object")
            tmp = DATA_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
            os.replace(tmp, DATA_FILE)
            revision = bump_revision()
            self._json(200, {"ok": True, "revision": revision, "updatedAt": os.path.getmtime(DATA_FILE)})
        except Exception as exc:
            self._json(400, {"ok": False, "error": str(exc)})


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def local_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not send data; it asks Windows which local interface would be used.
        sock.connect(("8.8.8.8", 80))
        return sock.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"
    finally:
        sock.close()


def main():
    os.chdir(ROOT)
    ip = local_ip()
    print("=" * 58)
    print("AXinfo PC Bridge v21 - AUTO SYNC / OFFLINE")
    print("=" * 58)
    print("PC address: http://" + ip + ":" + str(PORT))
    print("Pairing token: " + TOKEN)
    print("")
    print("Test on this PC: http://127.0.0.1:" + str(PORT) + "/bridge.html")
    print("Keep this window open while syncing.")
    print("Phone and PC can work offline; Wi-Fi is only needed for live sync.")
    print("")
    print("If Windows Firewall asks, allow Private networks.")
    print("=" * 58)
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nAXinfo PC Bridge stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
