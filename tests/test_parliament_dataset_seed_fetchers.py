from __future__ import annotations

import copy
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.check_parliament_dataset_seed_fetchers import (  # noqa: E402
    REQUIRED_DATASET_FAMILIES,
    _failures,
    _validate_manifest,
)
from scripts.fetch_parliament_dataset_seed_fetchers import (  # noqa: E402
    SeedTarget,
    fetch_seed_target,
    select_seed_targets,
)


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

    def json(self) -> dict[str, object]:
        raise NotImplementedError


class ParliamentDatasetSeedFetcherTests(unittest.TestCase):
    def test_target_selection_covers_required_families(self) -> None:
        targets = select_seed_targets()

        self.assertTrue(targets)
        self.assertEqual(
            {target.dataset_family for target in targets if target.approved},
            REQUIRED_DATASET_FAMILIES,
        )

    def test_fetch_seed_target_records_success_hashes_and_counts(self) -> None:
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
        sample_response = FakeResponse(
            sample_html,
            url="https://example.test/members/alpha",
        )

        with patch(
            "scripts.fetch_parliament_dataset_seed_fetchers.request_with_retries",
            side_effect=[index_response, sample_response],
        ):
            record = fetch_seed_target(target, output_dir=ROOT / "tmp-test-output")

        self.assertEqual(record["proof_status"], "fetched")
        self.assertEqual(record["index_record_count"], 2)
        self.assertEqual(record["sample_record_count"], 1)
        self.assertEqual(record["index_sha256"], hashlib.sha256(index_html.encode()).hexdigest())
        self.assertEqual(record["sample_sha256"], hashlib.sha256(sample_html.encode()).hexdigest())

    def test_fetch_seed_target_records_blocked_reason(self) -> None:
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

        def _raise(*_args, **_kwargs):
            response = requests.Response()
            response.status_code = 403
            response.url = target.index_url
            raise requests.HTTPError(response=response)

        with patch(
            "scripts.fetch_parliament_dataset_seed_fetchers.request_with_retries",
            side_effect=_raise,
        ):
            record = fetch_seed_target(target, output_dir=ROOT / "tmp-test-output")

        self.assertEqual(record["proof_status"], "blocked")
        self.assertIn("403", record["blocked_reason"])
        self.assertEqual(record["sample_record_count"], 0)

    def test_validate_manifest_rejects_unsupported_target(self) -> None:
        manifest = {
            "manifest_version": 1,
            "repository": "corpus-nz-hansard",
            "retrieved_at": "2026-07-03",
            "inventory_manifest": "manifests/parliament_dataset_inventory.json",
            "targets": [
                {
                    "approved": True,
                    "access_constraints": "public",
                    "dataset_family": "members_parties_seating_contacts",
                    "index_record_count": 2,
                    "index_sha256": "a" * 64,
                    "index_url": "https://example.test/members",
                    "proof_status": "fetched",
                    "sample_record_count": 1,
                    "sample_sha256": "b" * 64,
                    "sample_url": "https://example.test/members/alpha",
                    "source_id": "nz-parliament-members-current",
                    "source_posture": "official",
                    "fetched_at": "2026-07-03T00:00:00Z",
                    "request_urls": [
                        "https://example.test/members",
                        "https://example.test/members/alpha",
                    ],
                }
            ],
            "summary": {
                "approved_target_count": 1,
                "blocked_target_count": 0,
                "fetched_target_count": 1,
                "deferred_target_count": 0,
            },
            "policy": {
                "official_sources_first": True,
                "no_bulk_acquisition": True,
                "no_completion_claim": True,
            },
            "handoff": [
                {
                    "dataset_family": "members_parties_seating_contacts",
                    "next_track": "parliament_dataset_full_acquisition_20260703",
                    "proof_requirement": "Use this seed to prove retrieval feasibility only.",
                }
            ],
        }
        broken = copy.deepcopy(manifest)
        broken["targets"][0]["source_posture"] = "unsupported"

        failures = _validate_manifest(broken)

        self.assertTrue(failures)

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
