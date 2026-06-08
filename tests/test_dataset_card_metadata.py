import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class DatasetCardMetadataTest(unittest.TestCase):
    def test_dataset_card_has_huggingface_yaml_metadata(self):
        card = (ROOT / "DATASET_CARD.md").read_text(encoding="utf-8")
        self.assertTrue(card.startswith("---\n"))
        _, metadata, body = card.split("---", 2)

        self.assertIn('pretty_name: "NZ Hansard Corpus"', metadata)
        self.assertIn("license: mit", metadata)
        self.assertIn("license_link:", metadata)
        self.assertNotIn("license_name:", metadata)
        self.assertIn("size_categories:", metadata)
        self.assertIn("task_categories:", metadata)
        self.assertIn("tags:", metadata)
        self.assertIn("new-zealand", metadata)
        self.assertIn("hansard", metadata)
        self.assertIn("parquet", metadata)

        self.assertIn("# NZ Hansard Corpus Dataset Card", body)
        self.assertIn("https://doi.org/10.5281/zenodo.20595194", body)


if __name__ == "__main__":
    unittest.main()
