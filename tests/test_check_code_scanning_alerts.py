from __future__ import annotations

import unittest

from scripts.check_code_scanning_alerts import (
    AlertHit,
    alert_severity,
    blocking_alerts,
    _format_hit,
)


class CheckCodeScanningAlertsTest(unittest.TestCase):
    def test_alert_severity_prefers_security_severity_level(self) -> None:
        alert = {"rule": {"security_severity_level": "HIGH", "severity": "note"}}
        self.assertEqual(alert_severity(alert), "high")

    def test_alert_severity_falls_back_to_rule_severity(self) -> None:
        alert = {"rule": {"severity": "critical"}}
        self.assertEqual(alert_severity(alert), "critical")

    def test_blocking_alerts_filters_by_commit_and_severity(self) -> None:
        alerts = [
            {
                "number": 7,
                "html_url": "https://example.invalid/7",
                "rule": {"id": "py/bad-tag-filter", "security_severity_level": "high"},
                "most_recent_instance": {
                    "commit_sha": "abc123",
                    "message": {"text": "bad regex"},
                },
            },
            {
                "number": 8,
                "html_url": "https://example.invalid/8",
                "rule": {"id": "py/low-severity", "security_severity_level": "low"},
                "most_recent_instance": {
                    "commit_sha": "abc123",
                    "message": {"text": "ignore"},
                },
            },
            {
                "number": 9,
                "html_url": "https://example.invalid/9",
                "rule": {"id": "py/high-other-commit", "security_severity_level": "high"},
                "most_recent_instance": {
                    "commit_sha": "def456",
                    "message": {"text": "wrong commit"},
                },
            },
        ]

        hits = blocking_alerts(alerts, commit_sha="abc123")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].number, 7)
        self.assertEqual(hits[0].rule_id, "py/bad-tag-filter")
        self.assertEqual(hits[0].severity, "high")
        self.assertEqual(hits[0].message, "bad regex")

    def test_format_hit(self) -> None:
        hit = AlertHit(7, "py/bad-tag-filter", "high", "bad regex", "https://example.invalid/7")
        self.assertEqual(
            _format_hit(hit),
            "#7 py/bad-tag-filter [high] bad regex (https://example.invalid/7)",
        )


if __name__ == "__main__":
    unittest.main()
