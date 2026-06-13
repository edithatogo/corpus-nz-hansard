from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_entity_linking_exploratory_outputs import (
    build_entity_linking_exploratory_outputs,
)
from scripts.check_entity_linking_exploratory_outputs import (
    MANIFEST_PATH,
    _failures,
    _json,
    _jsonl_rows,
)


class EntityLinkingExploratoryOutputsTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_entity_linking_exploratory_outputs(
            manifest_path=MANIFEST_PATH, generated_at="2026-06-11T00:00:00+10:00"
        )
        self.assertEqual(manifest["release_status"], "sample-not-release")

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_and_rows_were_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        rows = _jsonl_rows(
            ROOT / "samples/entity-linking-exploratory/entity_linking_exploratory.jsonl"
        )
        self.assertEqual(manifest["validation_counts"]["record_count"], 7)
        self.assertEqual(len(rows), 7)
        self.assertEqual(rows[1]["linking_status"], "linked")


if __name__ == "__main__":
    unittest.main()
