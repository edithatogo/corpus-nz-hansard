from __future__ import annotations

import json
import unittest

from scripts.fetch_bills_api import _json_artifact_text


class FetchBillsApiTests(unittest.TestCase):
    def test_json_artifact_text_preserves_complete_payload(self) -> None:
        payload = [{"id": str(i), "text": "x" * 1000} for i in range(800)]
        text = _json_artifact_text(payload)

        self.assertFalse(text.rstrip().endswith("... (truncated)"))
        self.assertEqual(json.loads(text), payload)
        self.assertGreater(len(text), 500_000)


if __name__ == "__main__":
    unittest.main()
