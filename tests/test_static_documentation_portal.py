from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_static_documentation_portal import render_static_documentation_portal
from scripts.check_static_documentation_portal import HTML_PATH, MANIFEST_PATH, _failures, _json


class StaticDocumentationPortalTests(unittest.TestCase):
    def test_renderer_emits_manifest(self) -> None:
        manifest, html_text = render_static_documentation_portal(
            generated_at="2026-06-11T00:00:00+10:00"
        )
        self.assertEqual(manifest["current_public_release"]["version"], "0.1.0")
        self.assertIn("Static Documentation Portal", html_text)

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_validation_is_read_only(self) -> None:
        manifest_before = MANIFEST_PATH.read_text(encoding="utf-8")
        html_before = HTML_PATH.read_text(encoding="utf-8")
        self.assertEqual(_failures(), [])
        self.assertEqual(MANIFEST_PATH.read_text(encoding="utf-8"), manifest_before)
        self.assertEqual(HTML_PATH.read_text(encoding="utf-8"), html_before)

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["validation_results"]["public_release_urls_recorded"], True)
        self.assertGreaterEqual(manifest["validation_results"]["track_rows"], 1)


if __name__ == "__main__":
    unittest.main()
