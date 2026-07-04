from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parliament_dataset_full_acquisition import (  # noqa: E402
    REQUIRED_DATASET_FAMILIES,
    _failures,
    _validate_manifest,
)
from scripts.fetch_parliament_dataset_full_acquisition import (  # noqa: E402
    acquire_full_target,
    select_full_acquisition_targets,
)
from scripts.fetch_parliament_dataset_seed_fetchers import SeedTarget  # noqa: E402
from test_support import repo_tmp_dir

TEST_TMP = repo_tmp_dir()


class FakeResponse:
    def __init__(
        self,
        text: str,
        *,
        url: str,
        status_code: int = 200,
        content_type: str = "text/html; charset=utf-8",
    ) -> None:
        self.text = text
        self.url = url
        self.status_code = status_code
        self.headers = {"Content-Type": content_type}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            response = requests.Response()
            response.status_code = self.status_code
            response.url = self.url
            raise requests.HTTPError(response=response)


class ParliamentDatasetFullAcquisitionTests(unittest.TestCase):
    def test_target_selection_covers_required_families(self) -> None:
        targets = select_full_acquisition_targets()

        self.assertTrue(targets)
        self.assertEqual(
            {target.dataset_family for target in targets if target.approved},
            REQUIRED_DATASET_FAMILIES,
        )
        selected_ids = {target.source_id for target in targets}
        self.assertIn("nz-parliament-hansard-current", selected_ids)
        self.assertIn("nz-parliament-daily-progress", selected_ids)
        self.assertIn("nz-parliament-parliamentary-rules", selected_ids)
        self.assertIn("nz-parliament-standing-orders", selected_ids)
        self.assertIn("nz-parliament-speakers-rulings", selected_ids)

    def test_acquire_full_target_writes_cache_and_reconciles(self) -> None:
        target = SeedTarget(
            dataset_family="members_parties_seating_contacts",
            source_id="nz-parliament-members-current",
            source_posture="official",
            index_url="https://example.test/members",
            sample_patterns=("member",),
            access_constraints="public",
            fallback_for=(),
            approved=True,
        )
        index_html = """
            <html>
              <body>
                <a href="/members/alpha">Alpha</a>
                <a href="/members/beta">Beta</a>
              </body>
            </html>
        """
        sample_html = "<html><body><h1>Alpha</h1></body></html>"
        index_response = FakeResponse(index_html, url=target.index_url)
        sample_response = FakeResponse(sample_html, url="https://example.test/members/alpha")
        case_dir = TEST_TMP / "parliament_full_acquisition"

        with patch(
            "scripts.fetch_parliament_dataset_full_acquisition.request_with_retries",
            side_effect=[index_response, sample_response],
        ):
            record = acquire_full_target(target, cache_dir=case_dir)

        self.assertEqual(record["proof_status"], "fetched")
        self.assertEqual(record["index_record_count"], 2)
        self.assertEqual(record["detail_artifact_count"], 1)
        self.assertEqual(record["detail_record_count"], 1)
        self.assertEqual(record["index_sha256"], hashlib.sha256(index_html.encode()).hexdigest())
        self.assertEqual(
            record["detail_sha256s"], [hashlib.sha256(sample_html.encode()).hexdigest()]
        )
        self.assertTrue(
            (
                case_dir
                / "members_parties_seating_contacts"
                / "nz-parliament-members-current"
                / "target.json"
            ).exists()
        )

    def test_acquire_full_target_resumes_from_cache(self) -> None:
        target = SeedTarget(
            dataset_family="petitions",
            source_id="nz-parliament-petitions",
            source_posture="official",
            index_url="https://example.test/petitions",
            sample_patterns=("petition",),
            access_constraints="public",
            fallback_for=(),
            approved=True,
        )
        case_dir = TEST_TMP / "parliament_full_acquisition_resume"
        target_dir = case_dir / "petitions" / "nz-parliament-petitions"
        target_dir.mkdir(parents=True, exist_ok=True)
        cached_record = {
            "access_constraints": "public",
            "approved": True,
            "blocked_reason": None,
            "cache_dir": str(target_dir),
            "cache_hit": True,
            "coverage_window": "current",
            "dataset_family": "petitions",
            "detail_artifact_count": 0,
            "detail_paths": [],
            "detail_record_count": 0,
            "detail_sha256s": [],
            "detail_urls": [],
            "fetched_at": "2026-07-03T00:00:00Z",
            "index_cache_path": str(target_dir / "index.html"),
            "index_fetched_at": "2026-07-03T00:00:00Z",
            "index_record_count": 0,
            "index_sha256": "a" * 64,
            "index_url": target.index_url,
            "proof_status": "index-only",
            "refresh_cadence": "daily",
            "request_urls": [target.index_url],
            "resume_used": True,
            "rights_boundary": "not-public-release-ready",
            "source_id": target.source_id,
            "source_posture": target.source_posture,
        }
        target_json = target_dir / "target.json"
        target_json.write_text(json.dumps(cached_record, indent=2) + "\n", encoding="utf-8")
        (target_dir / "index.html").write_text("<html></html>", encoding="utf-8")

        with patch(
            "scripts.fetch_parliament_dataset_full_acquisition.request_with_retries",
            side_effect=AssertionError("should not refetch cached target"),
        ):
            record = acquire_full_target(target, cache_dir=case_dir)

        self.assertTrue(record["cache_hit"])
        self.assertEqual(record["proof_status"], "index-only")
        self.assertEqual(record["index_sha256"], "a" * 64)

    def test_acquire_full_target_records_blocked_reason(self) -> None:
        target = SeedTarget(
            dataset_family="journals",
            source_id="nz-parliament-weekly-journals-archive",
            source_posture="official",
            index_url="https://example.test/journals",
            sample_patterns=("journals",),
            access_constraints="public",
            fallback_for=(),
            approved=True,
        )

        def _raise(*_args, **_kwargs):
            response = requests.Response()
            response.status_code = 403
            response.url = target.index_url
            raise requests.HTTPError(response=response)

        with patch(
            "scripts.fetch_parliament_dataset_full_acquisition.request_with_retries",
            side_effect=_raise,
        ):
            record = acquire_full_target(
                target, cache_dir=TEST_TMP / "parliament_full_acquisition_blocked"
            )

        self.assertEqual(record["proof_status"], "blocked")
        self.assertIn("403", record["blocked_reason"])

    def test_validate_manifest_rejects_public_release_boundary(self) -> None:
        manifest = {
            "manifest_version": 1,
            "repository": "corpus-nz-hansard",
            "retrieved_at": "2026-07-03T00:00:00Z",
            "inventory_manifest": "manifests/parliament_dataset_inventory.json",
            "seed_manifest": "manifests/parliament_dataset_seed_fetchers.json",
            "publication_boundary": "not-public-release-ready",
            "policy": {
                "official_sources_first": True,
                "rights_safe": True,
                "no_bulk_acquisition": True,
                "no_public_release": True,
            },
            "summary": {
                "approved_target_count": 1,
                "blocked_target_count": 0,
                "cache_hit_count": 0,
                "detail_artifact_count": 1,
                "family_count": 1,
                "fetched_target_count": 1,
                "reconciled_family_count": 1,
                "resume_hit_count": 0,
                "total_target_count": 1,
            },
            "targets": [
                {
                    "access_constraints": "public",
                    "approved": True,
                    "blocked_reason": None,
                    "cache_dir": "derived/full/journals/nz-parliament-weekly-journals-archive",
                    "cache_hit": False,
                    "coverage_window": "current",
                    "dataset_family": "journals",
                    "detail_artifact_count": 1,
                    "detail_paths": [
                        "derived/full/journals/nz-parliament-weekly-journals-archive/detail-01.html"
                    ],
                    "detail_record_count": 1,
                    "detail_sha256s": ["b" * 64],
                    "detail_urls": ["https://example.test/journals/1"],
                    "fetched_at": "2026-07-03T00:00:00Z",
                    "index_cache_path": "derived/full/journals/nz-parliament-weekly-journals-archive/index.html",
                    "index_fetched_at": "2026-07-03T00:00:00Z",
                    "index_record_count": 2,
                    "index_sha256": "a" * 64,
                    "index_url": "https://example.test/journals",
                    "proof_status": "fetched",
                    "refresh_cadence": "weekly",
                    "request_urls": [
                        "https://example.test/journals",
                        "https://example.test/journals/1",
                    ],
                    "resume_used": False,
                    "rights_boundary": "not-public-release-ready",
                    "source_id": "nz-parliament-weekly-journals-archive",
                    "source_posture": "official",
                }
            ],
            "reconciliation": [
                {
                    "dataset_family": "journals",
                    "reconciliation_status": "pass",
                    "source_ids": ["nz-parliament-weekly-journals-archive"],
                    "shared_hostname": "www3.parliament.nz",
                    "notes": "index and detail counts are bounded",
                }
            ],
        }
        broken = copy.deepcopy(manifest)
        broken["publication_boundary"] = "public-release-ready"

        failures = _validate_manifest(broken)

        self.assertTrue(any("publication_boundary" in failure for failure in failures))

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
