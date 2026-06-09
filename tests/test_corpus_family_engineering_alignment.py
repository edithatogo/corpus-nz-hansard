import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_corpus_family_engineering_alignment import MANIFEST_PATH, _failures, _json


class CorpusFamilyEngineeringAlignmentTest(unittest.TestCase):
    def test_manifest_records_sibling_baseline_and_future_migration(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["repository"], "corpus-nz-hansard")
        self.assertEqual(
            manifest["sibling_repository"]["preferred_label"],
            "corpus-nz-legislation",
        )
        self.assertEqual(manifest["sibling_repository"]["observed_cli"], "nzlc")
        self.assertEqual(manifest["migration"]["target_package"], "nz_hansard_corpus")
        self.assertEqual(manifest["migration"]["target_cli"], "nzhc")

    def test_statuses_separate_adopted_quality_from_future_refactor(self):
        manifest = _json(MANIFEST_PATH)
        statuses = {item["id"]: item["status"] for item in manifest["standards"]}

        self.assertEqual(statuses["uv-lock"], "adopted")
        self.assertEqual(statuses["ruff"], "adopted")
        self.assertEqual(statuses["zenodo-protection"], "adopted")
        self.assertEqual(statuses["src-layout"], "future")
        self.assertEqual(statuses["typer-cli"], "future")
        self.assertEqual(statuses["pytest"], "future")

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
