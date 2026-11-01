import urllib.request
import ssl
import socket
import json
import time
import datetime
import os

LOG_FILE = r'C:\Users\didar\Desktop\AsteropeAI DYNKVStudio\00_DYNKV_STUDIO_MANAGEMENT_AND_BUSINESS_HUB\DYNKV-Studio-Web\DYNKV_SECURITY_MONITOR_LOG.jsonl'

TARGET_ENDPOINTS = [
    'https://dynkv.com/',
    'https://dynkv.com/demos/01_WCSSTP_Cognitive_Turing_Demo.html',
    'https://dynkv.com/demos/02_VeryFix_V8_Biometric_Consensus_Demo.html',
    'https://dynkv.com/legal/05_DYNKV_STUDIO_STANDARD_MUTUAL_NDA_2026_BG.html',
    'https://dynkv.com/legal/07_PERIFERIS_HARDWARE_IP_AND_INDIEGOGO_PROTECTION_NOTICE_2026.html'
]

EXPECTED_IPS = {
    '185.199.108.153',
    '185.199.109.153',
    '185.199.110.153',
    '185.199.111.153'
}

def run_security_audit():
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    report = {
        'timestamp': timestamp,
        'dns_status': 'UNKNOWN',
        'resolved_ips': [],
        'ssl_status': 'UNKNOWN',
        'endpoints': {},
        'integrity_verified': False,
        'overall_health': 'FAIL'
    }

    # 1. DNS Resolution & Anti-Spoofing Check
    try:
        addrinfo = socket.getaddrinfo('dynkv.com', 443, proto=socket.IPPROTO_TCP)
        resolved_ips = list(set([item[4][0] for item in addrinfo if item[0] == socket.AF_INET]))
        report['resolved_ips'] = resolved_ips
        
        # Check against expected GitHub Pages IP block
        if all(ip in EXPECTED_IPS for ip in resolved_ips) and len(resolved_ips) > 0:
            report['dns_status'] = 'SECURE_GITHUB_PAGES'
        else:
            report['dns_status'] = f'WARNING_UNEXPECTED_IPS: {resolved_ips}'
    except Exception as e:
        report['dns_status'] = f'DNS_ERROR: {str(e)}'

    # 2. SSL Handshake Check
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection(('dynkv.com', 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname='dynkv.com') as ssock:
                cert = ssock.getpeercert()
                expiry = cert.get('notAfter')
                report['ssl_status'] = f'VALID_EXPIRY_{expiry}'
    except Exception as e:
        report['ssl_status'] = f'SSL_ERROR: {str(e)}'

    # 3. Endpoints Status & Latency
    all_ok = True
    for ep in TARGET_ENDPOINTS:
        t0 = time.time()
        try:
            req = urllib.request.Request(ep, headers={'User-Agent': 'DYNKV-Security-Watchdog/2.0'})
            with urllib.request.urlopen(req, timeout=8) as resp:
                elapsed_ms = round((time.time() - t0) * 1000, 1)
                code = resp.getcode()
                content = resp.read()
                report['endpoints'][ep] = {
                    'status': code,
                    'latency_ms': elapsed_ms,
                    'bytes': len(content)
                }
                if code != 200:
                    all_ok = False
                
                # Check integrity on home page
                if ep == 'https://dynkv.com/':
                    text = content.decode('utf-8', errors='ignore')
                    if 'DYNKV Studio' in text and 'contact@dynkv.com' in text:
                        report['integrity_verified'] = True
                    else:
                        all_ok = False
        except Exception as e:
            report['endpoints'][ep] = {'status': 'ERROR', 'error': str(e)}
            all_ok = False

    if all_ok and report['dns_status'] == 'SECURE_GITHUB_PAGES' and 'VALID' in report['ssl_status'] and report['integrity_verified']:
        report['overall_health'] = '100% SECURE & OPERATIONAL'
    else:
        report['overall_health'] = 'DEGRADED OR ALERT'

    # Append to log
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as lf:
            lf.write(json.dumps(report) + '\n')
    except Exception as e:
        print("Log write error:", e)

    return report

if __name__ == '__main__':
    res = run_security_audit()
    print("=== DYNKV STUDIO SECURITY WATCHDOG REPORT ===")
    print(f"Timestamp: {res['timestamp']}")
    print(f"Overall Health: {res['overall_health']}")
    print(f"DNS Status: {res['dns_status']} (IPs: {res['resolved_ips']})")
    print(f"SSL Status: {res['ssl_status']}")
    print(f"Content Integrity Verified: {res['integrity_verified']}")
    print("Endpoints Checked:")
    for ep, d in res['endpoints'].items():
        print(f"  [{d.get('status')}] {ep} ({d.get('latency_ms', '?')} ms)")
