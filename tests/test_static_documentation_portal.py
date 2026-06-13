from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_static_documentation_portal import build_static_documentation_portal
from scripts.check_static_documentation_portal import MANIFEST_PATH, _failures, _json


class StaticDocumentationPortalTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_static_documentation_portal(
            manifest_path=MANIFEST_PATH, generated_at="2026-06-11T00:00:00+10:00"
        )
        self.assertEqual(manifest["current_public_release"]["version"], "0.1.0")

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["validation_results"]["public_release_urls_recorded"], True)
        self.assertGreaterEqual(manifest["validation_results"]["track_rows"], 1)


if __name__ == "__main__":
    unittest.main()
