# AXinfo PC Bridge — Windows / Python 3
# Run: python AXinfo_PC_Server.py
# Then open the displayed PC URL in the browser.
import json, os, socket, secrets
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT=os.path.dirname(os.path.abspath(__file__))
DATA_FILE=os.path.join(ROOT,"AXinfo_PC_Data.json")
PORT=8765
TOKEN_FILE=os.path.join(ROOT,"AXinfo_PC_TOKEN.txt")

if os.path.exists(TOKEN_FILE):
    TOKEN=open(TOKEN_FILE,"r",encoding="utf-8").read().strip()
else:
    TOKEN=secrets.token_urlsafe(12)
    open(TOKEN_FILE,"w",encoding="utf-8").write(TOKEN)

def local_ip():
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8",80)); return s.getsockname()[0]
    except Exception: return "127.0.0.1"
    finally: s.close()

class Handler(SimpleHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type,X-AXinfo-Token")
        self.send_header("Access-Control-Allow-Methods","GET,PUT,OPTIONS")
    def _auth(self):
        return self.headers.get("X-AXinfo-Token","")==TOKEN
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if self.path=="/api/ping":
            if not self._auth(): return self.send_error(401,"Invalid token")
            self.send_response(200); self._cors(); self.send_header("Content-Type","application/json; charset=utf-8"); self.end_headers()
            self.wfile.write(json.dumps({"ok":True,"name":"AXinfo PC Server"}).encode())
            return
        if self.path=="/api/data":
            if not self._auth(): return self.send_error(401,"Invalid token")
            db={}
            if os.path.exists(DATA_FILE):
                try: db=json.load(open(DATA_FILE,"r",encoding="utf-8"))
                except Exception: db={}
            self.send_response(200); self._cors(); self.send_header("Content-Type","application/json; charset=utf-8"); self.end_headers()
            self.wfile.write(json.dumps(db,ensure_ascii=False).encode())
            return
        super().do_GET()
    def do_PUT(self):
        if self.path!="/api/data":
            return self.send_error(404)
        if not self._auth(): return self.send_error(401,"Invalid token")
        try:
            n=int(self.headers.get("Content-Length","0"))
            payload=json.loads(self.rfile.read(n).decode("utf-8"))
            db=payload.get("db")
            if not isinstance(db,dict): raise ValueError("Invalid db")
            json.dump({"db":db,"updatedAt":payload.get("updatedAt")},open(DATA_FILE,"w",encoding="utf-8"),ensure_ascii=False,indent=2)
            self.send_response(200); self._cors(); self.send_header("Content-Type","application/json; charset=utf-8"); self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_error(400,str(e))

if __name__=="__main__":
    os.chdir(ROOT)
    ip=local_ip()
    print("\n=== AXinfo PC Bridge ===")
    print("PC address:", f"http://{ip}:{PORT}")
    print("Pairing token:", TOKEN)
    print("Keep this window open while syncing.")
    print("Phone and PC must be on the same Wi-Fi.")
    print("Press Ctrl+C to stop.\n")
    ThreadingHTTPServer(("0.0.0.0",PORT),Handler).serve_forever()
