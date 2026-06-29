import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_monthly_dynamic_archive_publication import (
    _contract_failures,
    _evidence_failures,
    _failures,
    _workflow_failures,
)
from scripts.build_monthly_dynamic_archive_evidence import _count_manifest_files


class MonthlyDynamicArchivePublicationTest(unittest.TestCase):
    def test_committed_monthly_publication_configuration_is_consistent(self):
        self.assertEqual(_failures(), [])

    def test_workflow_rejects_direct_zenodo_publication(self):
        failures = _workflow_failures(
            'cron: "17 3 1 * *"\n'
            "workflow_dispatch:\n"
            "publication_mode:\n"
            "- dry-run\n"
            "- huggingface\n"
            "- zenodo-draft\n"
            "- full\n"
            "Resolve publication mode\n"
            "Build monthly release evidence\n"
            "Upload monthly publication result artifacts\n"
            "attestations: write\n"
            "contents: read\n"
            "id-token: write\n"
            "SOURCE_ARCHIVE_URL\n"
            "HF_TOKEN\n"
            "ZENODO_TOKEN\n"
            "ARCHIVE_CREATORS_JSON\n"
            "zenodo-production-publish environment\n"
            "python scripts/publish_zenodo_deposition.py\n"
        )

        self.assertIn(
            "Monthly workflow must not directly publish Zenodo depositions.",
            failures,
        )

    def test_contract_requires_exact_evidence_fields(self):
        failures = _contract_failures(
            {
                "workflow": ".github/workflows/monthly_dynamic_archive_publication.yml",
                "cadence": "monthly",
                "evidence_required_fields": ["manifest_version"],
                "zenodo": {
                    "publish_requires_protected_environment": True,
                    "zenodraft_required_or_formally_evaluated": True,
                },
            }
        )

        self.assertIn(
            "Monthly contract evidence_required_fields do not match checker policy.",
            failures,
        )

    def test_evidence_requires_rights_boundary_and_consistent_track(self):
        contract = {
            "track_id": "monthly_dynamic_archive_publication_20260629",
        }
        evidence = {
            "manifest_version": 1,
            "track_id": "other",
            "generated_at": "2026-06-29T00:00:00+00:00",
            "run": {"commit_sha": "abc"},
            "source": {},
            "archive": {
                "tarball": {"path": "a", "exists": False, "size_bytes": None, "sha256": None},
                "manifest": {"path": "b", "exists": False, "size_bytes": None, "sha256": None},
            },
            "huggingface": {"repo_id": "edithatogo/nz-hansard-corpus"},
            "zenodo": {
                "protected_publish_environment": "zenodo-production-publish",
                "publish_handoff_only": True,
            },
            "validation": {
                "record_validation": {
                    "path": "manifests/record_schema_validation.json",
                    "exists": True,
                    "size_bytes": 1,
                    "sha256": "abc",
                },
                "record_count": 193922,
            },
            "rights_boundary": {
                "source_zip_committed": True,
                "source_zip_publicly_published": False,
                "no_official_endorsement_claim": True,
            },
        }

        failures = _evidence_failures(contract, evidence)

        self.assertIn(
            "Evidence manifest track_id does not match the publication contract.",
            failures,
        )
        self.assertIn(
            "Evidence manifest must state that the source zip is not committed.",
            failures,
        )

    def test_archive_manifest_files_are_counted(self):
        self.assertEqual(_count_manifest_files({"files": [{"path": "a"}, {"path": "b"}]}), 2)
        self.assertEqual(_count_manifest_files({"file_count": 3, "files": []}), 3)


if __name__ == "__main__":
    unittest.main()
