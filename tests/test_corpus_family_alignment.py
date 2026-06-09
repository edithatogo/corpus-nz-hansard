import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_corpus_family_alignment import ALIGNMENT_PATH, _failures, _json


class CorpusFamilyAlignmentTest(unittest.TestCase):
    def test_alignment_manifest_records_family_labels_and_public_surfaces(self):
        alignment = _json(ALIGNMENT_PATH)

        self.assertEqual(alignment["repository"], "corpus-nz-hansard")
        self.assertIn("corpus-nz-hansard", alignment["family"]["preferred_labels"])
        self.assertIn("corpus-nz-legislation", alignment["family"]["preferred_labels"])
        self.assertEqual(
            alignment["family"]["sibling_corpus"]["known_current_public_name"],
            "nz-legislation-corpus-pipeline",
        )

        gates = {gate["id"]: gate for gate in alignment["environment_gates"]}
        self.assertEqual(
            set(gates),
            {"github", "huggingface", "zenodo", "osf_optional", "future_metadata"},
        )
        self.assertEqual(
            gates["github"]["public_url"],
            "https://github.com/edithatogo/corpus-nz-hansard",
        )
        self.assertEqual(
            gates["huggingface"]["public_url"],
            "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
        )
        self.assertEqual(
            gates["zenodo"]["public_url"],
            "https://zenodo.org/records/20595194",
        )
        self.assertEqual(gates["github"]["non_migration_decision"], "keep-existing-url")
        self.assertEqual(gates["osf_optional"]["non_migration_decision"], "not-yet-published")

    def test_corpus_family_alignment_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
