from __future__ import annotations

import unittest

from scripts.build_web_annotation_selector_contract import build_web_annotation_selector_contract
from scripts.check_web_annotation_selector_contract import MANIFEST_PATH, _failures, _json


class WebAnnotationSelectorContractTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_web_annotation_selector_contract(
            manifest_path=None,
            generated_at="2026-06-11T00:00:00+10:00",
        )
        self.assertEqual(manifest["contract_id"], "web_annotation_selector_contract_20260610")

    def test_contract_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["selector_schema"], "schemas/web_annotation_selector.schema.json")
        self.assertEqual(manifest["validation_results"]["blocking_errors"], 0)


if __name__ == "__main__":
    unittest.main()
