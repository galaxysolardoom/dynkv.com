# -*- coding: utf-8 -*-
"""
WCSSTP™ Microservice Test Server (Interactive Evaluation Cockpit)
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
            # Interactive HTML Cockpit (100% English)
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WCSSTP™ Sovereign Shield Interactive Cockpit · DYNKV Studio</title>
    <style>
        :root {
            --bg: #07090e;
            --card: rgba(15, 23, 42, 0.95);
            --cyan: #00e5ff;
            --purple: #c084fc;
            --gold: #fbbf24;
            --green: #34d399;
            --red: #f87171;
            --border: rgba(0, 229, 255, 0.25);
        }
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            background: var(--bg); 
            color: #f1f5f9; 
            margin: 0; 
            padding: 24px; 
            line-height: 1.5; 
        }
        .container { max-width: 960px; margin: 0 auto; }
        
        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 24px; 
            border-bottom: 1px solid var(--border); 
            padding-bottom: 18px; 
        }
        .logo-title { 
            font-size: 22px; 
            font-weight: 800; 
            color: #fff; 
            display: flex; 
            align-items: center; 
            gap: 12px; 
            letter-spacing: 0.5px;
        }
        .badge { 
            background: rgba(0, 229, 255, 0.12); 
            border: 1px solid var(--cyan); 
            color: var(--cyan); 
            padding: 5px 14px; 
            border-radius: 999px; 
            font-size: 11px; 
            font-weight: 700; 
            text-transform: uppercase; 
            letter-spacing: 0.5px;
        }

        .stat-strip { 
            display: grid; 
            grid-template-columns: repeat(4, 1fr); 
            gap: 14px; 
            margin-bottom: 24px; 
        }
        .stat-box { 
            background: rgba(255,255,255,0.03); 
            border: 1px solid rgba(255,255,255,0.1); 
            border-radius: 14px; 
            padding: 16px; 
            text-align: center; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .stat-val { font-size: 26px; font-weight: 800; color: #fff; margin-bottom: 4px; }
        .stat-lbl { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 700; }

        .grid { 
            display: grid; 
            grid-template-columns: 1fr 1.15fr; 
            gap: 20px; 
            margin-bottom: 24px; 
        }
        .card { 
            background: var(--card); 
            border: 1px solid var(--border); 
            border-radius: 16px; 
            padding: 22px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5); 
        }
        .card h3 { 
            margin-top: 0; 
            font-size: 17px; 
            color: var(--cyan); 
            display: flex; 
            align-items: center; 
            gap: 10px; 
            margin-bottom: 12px;
        }
        
        .btn { 
            width: 100%;
            border: none; 
            padding: 12px 18px; 
            border-radius: 10px; 
            font-weight: 700; 
            font-size: 13.5px; 
            cursor: pointer; 
            transition: all 0.2s; 
            display: flex; 
            align-items: center; 
            justify-content: flex-start;
            gap: 10px; 
            margin-bottom: 10px; 
        }
        .btn-green { background: #059669; color: #fff; }
        .btn-green:hover { background: #10b981; box-shadow: 0 0 18px rgba(16, 185, 129, 0.45); transform: translateY(-1px); }
        .btn-red { background: #b91c1c; color: #fff; }
        .btn-red:hover { background: #ef4444; box-shadow: 0 0 18px rgba(239, 68, 68, 0.45); transform: translateY(-1px); }
        .btn-gold { background: #b45309; color: #fff; }
        .btn-gold:hover { background: #f59e0b; color: #000; box-shadow: 0 0 18px rgba(245, 158, 11, 0.45); transform: translateY(-1px); }
        .btn-cyan { background: #0e7490; color: #fff; }
        .btn-cyan:hover { background: #06b6d4; box-shadow: 0 0 18px rgba(6, 182, 212, 0.45); transform: translateY(-1px); }

        .console-box {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        .console { 
            background: #04060a; 
            border: 1px solid rgba(0, 229, 255, 0.2); 
            border-radius: 12px; 
            padding: 16px; 
            font-family: 'Consolas', 'Courier New', monospace; 
            font-size: 12px; 
            color: #38bdf8; 
            flex-grow: 1;
            min-height: 280px; 
            max-height: 380px; 
            overflow-y: auto; 
            white-space: pre-wrap; 
            box-shadow: inset 0 2px 8px rgba(0,0,0,0.8);
        }
        .security-banner {
            background: rgba(192, 132, 252, 0.08);
            border: 1px solid var(--purple);
            border-radius: 12px;
            padding: 14px 18px;
            font-size: 13px;
            color: #e2e8f0;
            margin-top: 10px;
        }
        .security-banner strong { color: var(--purple); }
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
                <div class="stat-lbl">Shield Status</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-human" style="color: var(--cyan);">0</div>
                <div class="stat-lbl">Human Qualia Verifications</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-bots" style="color: var(--red);">0</div>
                <div class="stat-lbl">Intercepted Bots</div>
            </div>
            <div class="stat-box">
                <div class="stat-val" id="stat-partners" style="color: var(--gold);">0</div>
                <div class="stat-lbl">Active B2B Partners</div>
            </div>
        </div>

        <div class="grid">
            <!-- Test Controls -->
            <div class="card">
                <h3>⚡ Protocol Simulation & Verification Panel</h3>
                <p style="font-size: 13px; color: #94a3b8; margin-bottom: 16px;">
                    Click a test button to dispatch live simulation requests to the protocol:
                </p>
                
                <button class="btn btn-green" onclick="testHuman()">
                    <span>🟢</span> 
                    <span>Test 1: Biological Human (Class A · Cadence 125ms)</span>
                </button>
                
                <button class="btn btn-red" onclick="testBot()">
                    <span>🔴</span> 
                    <span>Test 2: AI Botnet Attack (Class C · Burst Cadence 3.8ms)</span>
                </button>
                
                <button class="btn btn-gold" onclick="testIssueToken()">
                    <span>🔑</span> 
                    <span>Test 3: Issue Class B Partner Token (EU AI Act Art. 14)</span>
                </button>
                
                <button class="btn btn-cyan" onclick="testVerifyToken()">
                    <span>🔍</span> 
                    <span>Test 4: Verify Token & Check Daily Quota</span>
                </button>

                <div class="security-banner">
                    <strong>🛡️ Zero-PII Defense:</strong> All evaluations are computed deterministically via sensory entropy and cryptographic signatures without tracking cookies, IP logging, or biometrics.
                </div>
            </div>

            <!-- Terminal Output -->
            <div class="card console-box">
                <h3>📟 Live Telemetry Terminal (Real-Time JSON Stream)</h3>
                <div class="console" id="output">Ready for evaluation. Click any test button on the left...</div>
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
            out.textContent = text + `\\n\\n----------------------------------------\\n\\n` + out.textContent;
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
                log("🟢 HUMAN QUALIA VERIFIED (Class A)", data);
            } catch (e) { log("Request Error: " + e); }
        }

        async function testBot() {
            try {
                const res = await fetch('/verify/human', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({cadence_ms: 3.8})
                });
                const data = await res.json();
                log("🔴 SYNTHETIC BOTNET INTERCEPTED (Class C)", data);
            } catch (e) { log("Request Error: " + e); }
        }

        async function testIssueToken() {
            try {
                const res = await fetch('/tokens/issue', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        partner_name: "Global_Security_Audit_Partner",
                        organization: "Enterprise AI Security Audit Lab",
                        daily_quota: 500,
                        valid_days: 14,
                        allowed_scopes: ["public_press", "api_docs", "telemetry"]
                    })
                });
                const data = await res.json();
                lastToken = data.token;
                log("🔑 WCSSTP CLASS B PARTNER TOKEN ISSUED (EU AI Act Art. 14)", data);
            } catch (e) { log("Request Error: " + e); }
        }

        async function testVerifyToken() {
            if (!lastToken) {
                log("⚠️ WARNING: Please click 'Test 3: Issue Class B Partner Token' first to create an active token!");
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
                log("🔍 TOKEN VERIFICATION & QUOTA METERING (200 OK)", data);
            } catch (e) { log("Request Error: " + e); }
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
