# -*- coding: utf-8 -*-
import unittest
from wcsstp_core import OwnerSovereignGate

class TestWcsstpCore(unittest.TestCase):
    def setUp(self):
        self.gate = OwnerSovereignGate(registry_file=":memory:")

    def test_class_a_human_qualia(self):
        res = self.gate.verify_human_qualia(cadence_ms=120.0)
        self.assertEqual(res["verdict"], "HUMAN_QUALIA_VERIFIED")
        self.assertEqual(res["class"], "A")
        self.assertTrue(res["v_score"] >= 85.0)
        self.assertTrue(res["latency_us"] < 500.0)

    def test_class_c_synthetic_bot_intercept(self):
        res = self.gate.verify_human_qualia(cadence_ms=4.2)
        self.assertEqual(res["verdict"], "SYNTHETIC_BOT_INTERCEPTED")
        self.assertEqual(res["class"], "C")
        self.assertEqual(res["v_score"], 0.0)

    def test_class_b_partner_token_lifecycle(self):
        token, payload = self.gate.issue_partner_token(
            partner_name="Test_Researcher",
            organization="EU DeepTech Lab",
            daily_quota=5,
            valid_days=7,
            allowed_scopes=["api_docs", "telemetry"]
        )
        self.assertTrue(token.startswith("wcp_b_"))
        
        # Valid scope
        ok, reason, _ = self.gate.verify_partner_request(token, "api_docs")
        self.assertTrue(ok)
        self.assertEqual(reason, "AUTHORIZED_CLASS_B_ACCESS")

        # Invalid scope
        ok, reason, _ = self.gate.verify_partner_request(token, "admin_core")
        self.assertFalse(ok)
        self.assertIn("SCOPE_UNAUTHORIZED", reason)

        # Quota exhaustion
        for _ in range(4):
            self.gate.verify_partner_request(token, "api_docs")
        
        ok_quota, reason_quota, _ = self.gate.verify_partner_request(token, "api_docs")
        self.assertFalse(ok_quota)
        self.assertIn("DAILY_QUOTA_EXCEEDED", reason_quota)

        # Revocation
        tid = payload["tid"]
        self.gate.revoke_token(tid, "Security test audit")
        ok_rev, reason_rev, _ = self.gate.verify_partner_request(token, "api_docs")
        self.assertFalse(ok_rev)
        self.assertIn("TOKEN_REVOKED", reason_rev)

if __name__ == "__main__":
    unittest.main()
