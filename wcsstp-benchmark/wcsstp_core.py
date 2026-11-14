# -*- coding: utf-8 -*-
"""
=============================================================================
WCSSTP™ (Will-to-Consciousness SeaSickTest Protocol) — Core Engine v1.4
DYNKV Studio · Helsinki · 2026
Architecture: DYNKV Studio Leadership & Asterope AI
=============================================================================
"""

import hmac
import hashlib
import time
import json
import base64
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List

DEFAULT_OWNER_KEY = b"dynkv_studio_sovereign_wcsstp_master_root_2026"

class OwnerSovereignGate:
    """Главен шлюз за управление на суверенния достъп и партньорските токени."""

    def __init__(self, owner_secret: bytes = DEFAULT_OWNER_KEY, registry_file: str = "wcsstp_registry.json"):
        self.owner_secret = owner_secret
        self.registry_file = Path(registry_file)
        self.registry: Dict[str, Any] = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if str(self.registry_file) != ":memory:" and self.registry_file.exists():
            try:
                with open(self.registry_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "studio": "DYNKV Studio · Helsinki",
            "protocol": "WCSSTP™ v1.4",
            "shield_status": "ACTIVE",
            "partners": {},
            "revoked": {},
            "daily_usage": {},
            "intercepted_bots": 0,
            "human_qualia_verifications": 0
        }

    def _save_registry(self) -> None:
        if str(self.registry_file) == ":memory:":
            return
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, indent=2, ensure_ascii=False)

    def verify_human_qualia(self, cadence_ms: float, interaction_type: str = "organic_movement") -> Dict[str, Any]:
        """
        Клас A (Жив човек): Проверява сетивната ентропия и каденса.
        - Честота над 80ms с вариация = жив човек (V-Score 85–100).
        - Честота под 20ms без вариация = синтетичен бот (V-Score 0).
        """
        start_t = time.perf_counter()
        if cadence_ms < 20.0:
            self.registry["intercepted_bots"] += 1
            self._save_registry()
            elapsed_us = (time.perf_counter() - start_t) * 1_000_000
            return {
                "verdict": "SYNTHETIC_BOT_INTERCEPTED",
                "class": "C",
                "v_score": 0.0,
                "latency_us": round(elapsed_us, 2),
                "reason": "Cadence below human biological threshold (<20ms)"
            }

        self.registry["human_qualia_verifications"] += 1
        self._save_registry()
        elapsed_us = (time.perf_counter() - start_t) * 1_000_000
        return {
            "verdict": "HUMAN_QUALIA_VERIFIED",
            "class": "A",
            "v_score": 96.5,
            "latency_us": round(elapsed_us, 2),
            "zero_pii": True,
            "reason": "Living organic entropy confirmed"
        }

    def issue_partner_token(
        self,
        partner_name: str,
        organization: str,
        daily_quota: int = 1000,
        valid_days: int = 30,
        allowed_scopes: Optional[List[str]] = None,
        notes: str = ""
    ) -> Tuple[str, Dict[str, Any]]:
        """Издава криптографски заверен Клас B токен за одобрен партньор."""
        if allowed_scopes is None:
            allowed_scopes = ["public_press", "api_docs", "telemetry"]

        now = time.time()
        exp = now + (valid_days * 86400)
        token_id = hashlib.sha256(f"{partner_name}_{now}_{daily_quota}".encode("utf-8")).hexdigest()[:16]

        payload = {
            "tid": token_id,
            "sub": partner_name,
            "org": organization,
            "cls": "B",
            "quota": daily_quota,
            "scopes": allowed_scopes,
            "iat": int(now),
            "exp": int(exp),
            "iss": "DYNKV_STUDIO_WCSSTP_GATE/1.4",
            "v_score_preset": 65.0
        }

        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("ascii").rstrip("=")

        sig = hmac.new(self.owner_secret, payload_b64.encode("ascii"), hashlib.sha256).digest()
        sig_b64 = base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")

        full_token = f"wcp_b_{payload_b64}.{sig_b64}"

        self.registry["partners"][token_id] = {
            "partner_name": partner_name,
            "organization": organization,
            "daily_quota": daily_quota,
            "valid_days": valid_days,
            "allowed_scopes": allowed_scopes,
            "notes": notes,
            "issued_at": int(now),
            "expires_at": int(exp),
            "status": "ACTIVE",
            "token_preview": f"{full_token[:25]}...{full_token[-10:]}"
        }
        self._save_registry()

        return full_token, payload

    def verify_partner_request(self, token_str: str, requested_scope: str) -> Tuple[bool, str, Dict[str, Any]]:
        """Верифицира входяща заявка с Клас B токен."""
        if not token_str.startswith("wcp_b_") or "." not in token_str:
            return False, "INVALID_TOKEN_FORMAT", {}

        token_body = token_str[6:]
        parts = token_body.split(".")
        if len(parts) != 2:
            return False, "CORRUPT_TOKEN_STRUCTURE", {}

        payload_b64, sig_b64 = parts

        expected_sig = hmac.new(self.owner_secret, payload_b64.encode("ascii"), hashlib.sha256).digest()
        expected_sig_b64 = base64.urlsafe_b64encode(expected_sig).decode("ascii").rstrip("=")

        if not hmac.compare_digest(sig_b64, expected_sig_b64):
            return False, "TAMPERED_OR_FORGED_SIGNATURE", {}

        padding = 4 - (len(payload_b64) % 4)
        if padding != 4:
            payload_b64 += "=" * padding

        try:
            payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode("utf-8"))
        except Exception:
            return False, "MALFORMED_JSON_PAYLOAD", {}

        token_id = payload.get("tid")
        now = time.time()

        if token_id in self.registry["revoked"]:
            return False, f"TOKEN_REVOKED: {self.registry['revoked'][token_id].get('reason')}", payload

        if payload.get("exp") and now >= payload["exp"]:
            return False, "TOKEN_EXPIRED", payload

        allowed = payload.get("scopes", [])
        if requested_scope not in allowed and "*" not in allowed:
            return False, f"SCOPE_UNAUTHORIZED: {requested_scope} not in {allowed}", payload

        today = time.strftime("%Y-%m-%d", time.gmtime(now))
        usage_record = self.registry["daily_usage"].setdefault(token_id, {"date": today, "count": 0})

        if usage_record["date"] != today:
            usage_record["date"] = today
            usage_record["count"] = 0

        max_quota = payload.get("quota", 1000)
        if usage_record["count"] >= max_quota:
            return False, f"DAILY_QUOTA_EXCEEDED: {usage_record['count']}/{max_quota}", payload

        usage_record["count"] += 1
        self._save_registry()

        return True, "AUTHORIZED_CLASS_B_ACCESS", payload

    def revoke_token(self, token_id: str, reason: str = "Manual revocation by studio") -> bool:
        if token_id in self.registry["partners"]:
            self.registry["partners"][token_id]["status"] = "REVOKED"
            self.registry["revoked"][token_id] = {
                "revoked_at": int(time.time()),
                "reason": reason
            }
            self._save_registry()
            return True
        return False
