import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_public_surface_audit import build_public_surface_audit
from scripts.check_public_surface_audit import _failures


class PublicSurfaceAuditTest(unittest.TestCase):
    def test_builds_public_surface_audit_from_release_manifest(self):
        audit = build_public_surface_audit(output=None)

        surface_ids = {surface["id"] for surface in audit["surfaces"]}
        self.assertEqual(
            surface_ids,
            {"github", "huggingface", "zenodo", "osf_optional", "future_metadata"},
        )
        self.assertEqual(audit["repository"], "corpus-nz-hansard")
        self.assertEqual(audit["publication_status"], "published")

        github = next(surface for surface in audit["surfaces"] if surface["id"] == "github")
        self.assertEqual(github["status"], "active")
        self.assertEqual(github["url"], "https://github.com/edithatogo/corpus-nz-hansard")

        osf = next(surface for surface in audit["surfaces"] if surface["id"] == "osf_optional")
        self.assertEqual(osf["status"], "inactive")
        self.assertFalse(osf["claims_allowed"])

    def test_public_surface_audit_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
