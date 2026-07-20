import http.server
import json
import random
import string
import threading
import socket
import sys
import time

HOST = "127.0.0.1"
PORT = 80

fake_hwid = "".join(random.choices(string.hexdigits, k=32))

def json_response(body, status=200):
    body_bytes = json.dumps(body).encode("utf-8")
    resp = f"HTTP/1.1 {status} OK\r\nContent-Type: application/json\r\nContent-Length: {len(body_bytes)}\r\nAccess-Control-Allow-Origin: *\r\nConnection: close\r\n\r\n".encode("utf-8")
    return resp + body_bytes

def handle_request(method, path, body):
    # launcher-auth endpoint
    if path == "/api/license/launcher-auth":
        return json_response({
            "success": True,
            "active": True,
            "username": "cracked by grave",
            "plan": "Lifetime",
            "expiresAt": "2099-12-31T23:59:59Z",
            "hardware_id": fake_hwid,
            "message": "License active"
        })

    if path == "/api/license/discord-check":
        return json_response({
            "success": True,
            "active": True,
            "username": "cracked by grave",
            "message": "Discord user verified"
        })

    if path == "/forgot-password":
        return json_response({"success": True})

    if path == "/dashboard":
        return json_response({"success": True, "username": "cracked by grave", "plan": "Lifetime"})

    # fallback
    return json_response({"success": True, "message": "ok"})

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        resp = handle_request("GET", self.path, None)
        self.wfile.write(resp)

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b""
        resp = handle_request("POST", self.path, body)
        self.wfile.write(resp)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[EMULATOR] {args[0]} {args[1]} {args[2]}")

def run():
    server = http.server.HTTPServer((HOST, PORT), Handler)
    print(f"[EMULATOR] mogdive.xyz emulator running on http://{HOST}:{PORT}")
    print(f"[EMULATOR] HWID: {fake_hwid}")
    print(f"[EMULATOR] Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[EMULATOR] Shutting down...")
        server.server_close()

if __name__ == "__main__":
    run()
