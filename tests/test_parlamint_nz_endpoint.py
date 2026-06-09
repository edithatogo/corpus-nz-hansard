import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parlamint_nz_endpoint import (
    MANIFEST_PATH,
    SAMPLE_XML_PATH,
    TEI_NS,
    _failures,
    _json,
)


class ParlaMintNzEndpointTest(unittest.TestCase):
    def test_sample_xml_is_tei(self):
        root = ET.parse(SAMPLE_XML_PATH).getroot()

        self.assertEqual(root.tag, f"{{{TEI_NS}}}TEI")

    def test_manifest_keeps_sample_not_release_boundary(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )

    def test_traceability_lists_neutral_components(self):
        manifest = _json(MANIFEST_PATH)

        self.assertTrue(manifest["traceability"][0]["neutral_component_ids"])

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
