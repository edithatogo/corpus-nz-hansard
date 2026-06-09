import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_zenodo_metadata import build_zenodo_metadata
from scripts.check_zenodo_rights_metadata import _failures


class ZenodoRightsMetadataTest(unittest.TestCase):
    def test_builds_zenodo_metadata_with_rights_and_public_links(self):
        metadata = build_zenodo_metadata(output=None)

        self.assertEqual(metadata["title"], "NZ Hansard Corpus")
        self.assertEqual(metadata["upload_type"], "dataset")
        self.assertEqual(metadata["version"], "0.1.0")
        self.assertEqual(metadata["license"], "other-open")
        self.assertIn("source ZIP is not redistributed", metadata["description"])
        self.assertIn("New Zealand Parliamentary Debates/Hansard", metadata["description"])

        identifiers = {item["identifier"] for item in metadata["related_identifiers"]}
        self.assertIn("https://github.com/edithatogo/corpus-nz-hansard", identifiers)
        self.assertIn("https://huggingface.co/datasets/edithatogo/nz-hansard-corpus", identifiers)
        self.assertIn("https://doi.org/10.5281/zenodo.20595194", identifiers)

    def test_zenodo_rights_metadata_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
