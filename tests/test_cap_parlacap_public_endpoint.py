from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.build_cap_parlacap_public_endpoint import build_cap_parlacap_public_endpoint
from scripts.check_cap_parlacap_public_endpoint import MANIFEST_PATH, _failures, _json


class CapParlaCapPublicEndpointTests(unittest.TestCase):
    def test_builder_emits_blocked_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            manifest_path = tmp_path / "manifest.json"
            manifest = build_cap_parlacap_public_endpoint(
                manifest_path=manifest_path,
                generated_at="2026-06-11T00:00:00+10:00",
            )
            self.assertEqual(manifest["release_status"], "blocked-pending-validated-components")
            self.assertTrue(manifest_path.exists())

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "CAP / ParlaCAP public endpoint release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )


if __name__ == "__main__":
    unittest.main()
