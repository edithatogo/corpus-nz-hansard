import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_osf_optional_mirror_policy import _failures


class OsfOptionalMirrorPolicyTest(unittest.TestCase):
    def test_manifest_keeps_osf_non_canonical_until_activation_controls_exist(self):
        manifest = json.loads(
            (ROOT / "manifests/osf_optional_mirror_policy.json").read_text(encoding="utf-8")
        )

        self.assertEqual(manifest["repository"], "corpus-nz-hansard")
        self.assertEqual(manifest["corpus_family_sibling"], "corpus-nz-legislation")
        self.assertEqual(manifest["osf"]["decision"], "optional_future_mirror")
        self.assertEqual(manifest["osf"]["status"], "inactive")
        self.assertFalse(manifest["osf"]["claims_allowed"])
        self.assertIsNone(manifest["osf"]["project_url"])
        self.assertEqual(manifest["citation"]["authoritative_target"], "zenodo")
        self.assertIn("10.5281/zenodo.20595194", manifest["citation"]["required_text"])
        self.assertEqual(manifest["mirror_controls"]["checksum_algorithm"], "sha256")

    def test_osf_optional_mirror_policy_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
