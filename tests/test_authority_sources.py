import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_authority_sources import MANIFEST_PATH, REQUIRED_DOMAINS, _failures, _json


class AuthoritySourcesTest(unittest.TestCase):
    def test_manifest_covers_all_authority_domains(self):
        manifest = _json(MANIFEST_PATH)

        self.assertEqual(set(manifest["domains"]), REQUIRED_DOMAINS)
        self.assertEqual(set(manifest["domain_coverage"]), REQUIRED_DOMAINS)

    def test_official_sources_cover_each_domain(self):
        manifest = _json(MANIFEST_PATH)
        for domain in REQUIRED_DOMAINS:
            sources = [source for source in manifest["sources"] if domain in source["domains"]]
            self.assertTrue(
                any(source["publisher"] == "New Zealand Parliament" for source in sources),
                domain,
            )

    def test_policy_blocks_text_inference_as_authority(self):
        manifest = _json(MANIFEST_PATH)

        self.assertTrue(manifest["policy"]["text_derived_inference_not_authority"])
        self.assertTrue(manifest["policy"]["publish_authoritative_fields_requires_declared_inputs"])
        self.assertTrue(manifest["policy"]["official_sources_first"])

    def test_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
