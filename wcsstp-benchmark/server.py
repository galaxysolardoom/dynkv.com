# -*- coding: utf-8 -*-
"""
WCSSTP™ Microservice Test Server (Interactive Control Cockpit)
DYNKV Studio · Helsinki · 2026
"""

import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from wcsstp_core import OwnerSovereignGate

gate = OwnerSovereignGate(registry_file="/data/wcsstp_registry.json")

class WcsstpHandler(BaseHTTPRequestHandler):
    def _send_json(self, status: int, data: dict):
        body = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self):
        if self.path == "/health":
            self._send_json(200, {
                "status": "HEALTHY",
                "service": "WCSSTP™ Protocol Test Suite",
                "studio": "DYNKV Studio · Helsinki",
                "shield": "ACTIVE",
                "timestamp": int(time.time())
            })
        elif self.path == "/metrics":
            self._send_json(200, {
                "shield_status": gate.registry.get("shield_status"),
                "intercepted_bots": gate.registry.get("intercepted_bots", 0),
                "human_qualia_verifications": gate.registry.get("human_qualia_verifications", 0),
                "active_class_b_partners": len([p for p in gate.registry.get("partners", {}).values() if p.get("status") == "ACTIVE"]),
                "revoked_tokens": len(gate.registry.get("revoked", {}))
            })
        else:
            # Interactive HTML Cockpit
            html = """<!DOCTYPE html>
<html lang="bg">
<head>
    <meta charset="utf-8">
    <title>WCSSTP™ Sovereign Shield Interactive Cockpit · DYNKV Studio</title>
    <style>
        :root {
            --bg: #07090e;
            --card: rgba(15, 23, 42, 0.9);
            --cyan: #00e5ff;
            --purple: #c084fc;
            --gold: #fbbf24;
            --green: #34d399;
            --red: #f87171;
            --border: rgba(0, 229, 255, 0.25);
        }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: #fff; margin: 0; padding: 25px; line-height: 1.5; }
        .container { max-width: 860px; margin: 0 auto; }
        .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }
        .logo-title { font-size: 22px; font-weight: 800; color: #fff; display: flex; align-items: center; gap: 10px; }
        .badge { background: rgba(0, 229, 255, 0.12); border: 1px solid var(--cyan); color: var(--cyan); padding: 4px 12px; border-radius: 999px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 24px; }
        .card { background: var(--card); border: 1px solid var(--border); border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .card h3 { margin-top: 0; font-size: 16px; color: var(--cyan); display: flex; align-items: center; gap: 8px; }
        .btn { border: none; padding: 10px 18px; border-radius: 10px; font-weight: 700; font-size: 13px; cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px; margin: 4px; }
        .btn-green { background: #059669; color: #fff; }
        .btn-green:hover { background: #10b981; box-shadow: 0 0 15px rgba(16, 185, 129, 0.4); }
        .btn-red { background: #dc2626; color: #fff; }
        .btn-red:hover { background: #ef4444; box-shadow: 0 0 15px rgba(239, 68, 68, 0.4); }
        .btn-gold { background: #d97706; color: #fff; }
        .btn-gold:hover { background: #fbbf24; color: #000; box-shadow: 0 0 15px rgba(251, 191, 36, 0.4); }
        .btn-cyan { background: #0891b2; color: #fff; }
        .btn-cyan:hover { background: #06b6d4; box-shadow: 0 0 15px rgba(6, 182, 212, 0.4); }
        .console { background: #05070d; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 16px; font-family: monospace; font-size: 12.5px; color: #38bdf8; min-height: 180px; max-height: 320px; overflow-y: auto; white-space: pre-wrap; }
        .stat-strip { display: flex; justify-content: space-between; gap: 12px; margin-bottom: 20px; }
        .stat-box { flex: 1; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 14px; text-align: center; }
        .stat-val { font-size: 24px; font-weight: 800; color: #fff; }
        .stat-lbl { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo-title">
                <span>🛡️</span>
                <span>WCSSTP™ Sovereign Shield Cockpit</span>
            </div>
            <div>
                <span class="badge">DYNKV STUDIO · DOCKER PORT 8081</span>
            </div>
        </div>

        <div class="stat-strip">
            <div class="stat-box">
                <div class="stat-val" id="stat-shield" style="color: var(--green);">ACTIVE</div>
                <div class="stat-lbl">Статус на щита</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-human" style="color: var(--cyan);">0</div>
                <div class="stat-lbl">Човешки Qualia валидации</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-bots" style="color: var(--red);">0</div>
                <div class="stat-lbl">Неутрализирани ботове</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-partners" style="color: var(--gold);">0</div>
                <div class="stat-lbl">Активни партньори</div>
            </div>
        </div>

        <div class="grid">
            <!-- Test Controls -->
            <div class="card">
                <h3>⚡ Симулационен панел за тестове</h3>
                <p style="font-size: 13px; color: #94a3b8;">Щракни бутон, за да симулираш заявки към протокола:</p>
                <div style="display: flex; flex-direction: column; gap: 8px;">
                    <button class="btn btn-green" onclick="testHuman()">
                        🟢 Тест: Жив Човек (Клас A, каденс 120ms)
                    </button>
                    <button class="btn btn-red" onclick="testBot()">
                        🔴 Тест: AI Ботнет Атака (Клас C, спам 4ms)
                    </button>
                    <button class="btn btn-gold" onclick="testIssueToken()">
                        🔑 Тест: Издай Клас B Партньорски Токен
                    </button>
                    <button class="btn btn-cyan" onclick="testVerifyToken()">
                        🔍 Тест: Провери Токен и Дневна Квота
                    </button>
                </div>
            </div>

            <!-- Terminal Output -->
            <div class="card">
                <h3>📟 Жив телеметричен терминал</h3>
                <div class="console" id="output">Готов за тест. Щракни бутон вляво...</div>
            </div>
        </div>
    </div>

    <script>
        let lastToken = "";

        async function updateMetrics() {
            try {
                const res = await fetch('/metrics');
                const data = await res.json();
                document.getElementById('stat-shield').textContent = data.shield_status || "ACTIVE";
                document.getElementById('stat-human').textContent = data.human_qualia_verifications || 0;
                document.getElementById('stat-bots').textContent = data.intercepted_bots || 0;
                document.getElementById('stat-partners').textContent = data.active_class_b_partners || 0;
            } catch (e) {
                console.error(e);
            }
        }

        function log(msg, obj) {
            const out = document.getElementById('output');
            const ts = new Date().toLocaleTimeString();
            let text = `[${ts}] ${msg}`;
            if (obj) text += `\\n` + JSON.stringify(obj, null, 2);
            out.textContent = text + `\\n\\n----------------------------------------\\n` + out.textContent;
            updateMetrics();
        }

        async function testHuman() {
            try {
                const res = await fetch('/verify/human', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({cadence_ms: 125.4})
                });
                const data = await res.json();
                log("🟢 УСПЕШНА ВАЛИДАЦИЯ НА ЖИВ ЧОВЕК (Клас A)", data);
            } catch (e) { log("Грешка при заявка: " + e); }
        }

        async function testBot() {
            try {
                const res = await fetch('/verify/human', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({cadence_ms: 3.8})
                });
                const data = await res.json();
                log("🔴 ПРИХВАНАТ И БЛОКИРАН СИНТЕТИЧЕН БОТ (Клас C)", data);
            } catch (e) { log("Грешка при заявка: " + e); }
        }

        async function testIssueToken() {
            try {
                const res = await fetch('/tokens/issue', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        partner_name: "Didol_Direct_Test_Suite",
                        organization: "DYNKV Studio Research Hub",
                        daily_quota: 100,
                        valid_days: 14,
                        allowed_scopes: ["public_press", "api_docs"]
                    })
                });
                const data = await res.json();
                lastToken = data.token;
                log("🔑 ИЗДАДЕН WCSSTP КЛАС B ПАРТНЬОРСКИ ТОКЕН", data);
            } catch (e) { log("Грешка при заявка: " + e); }
        }

        async function testVerifyToken() {
            if (!lastToken) {
                log("⚠️ Първо щракни 'Издай Клас B Токен', за да има активен токен за проверка!");
                return;
            }
            try {
                const res = await fetch('/tokens/verify', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        token: lastToken,
                        scope: "api_docs"
                    })
                });
                const data = await res.json();
                log("🔍 ВЕРИФИКАЦИЯ НА ТОКЕН И ОТЧИТАНЕ НА КВОТА", data);
            } catch (e) { log("Грешка при заявка: " + e); }
        }

        updateMetrics();
        setInterval(updateMetrics, 5000);
    </script>
</body>
</html>"""
            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        if self.path == "/verify/human":
            cadence = float(payload.get("cadence_ms", 120.0))
            res = gate.verify_human_qualia(cadence_ms=cadence)
            self._send_json(200, res)

        elif self.path == "/tokens/issue":
            name = payload.get("partner_name", "Anonymous_Lab")
            org = payload.get("organization", "External_Partner")
            quota = int(payload.get("daily_quota", 500))
            days = int(payload.get("valid_days", 14))
            scopes = payload.get("allowed_scopes", ["public_press", "api_docs"])
            token, pld = gate.issue_partner_token(name, org, quota, days, scopes)
            self._send_json(201, {"token": token, "payload": pld})

        elif self.path == "/tokens/verify":
            token = payload.get("token", "")
            scope = payload.get("scope", "public_press")
            ok, reason, pld = gate.verify_partner_request(token, scope)
            self._send_json(200 if ok else 403, {"authorized": ok, "reason": reason, "payload": pld})

        else:
            self._send_json(404, {"error": "Endpoint not found"})

def run_server(port: int = 8081):
    server = HTTPServer(("0.0.0.0", port), WcsstpHandler)
    print(f">>> WCSSTP Test Suite listening on http://0.0.0.0:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run_server(8081)
