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

from scripts.check_parliament_video_seed_fetchers import (  # noqa: E402
    _failures,
    _validate_manifest,
)
from scripts.fetch_parliament_video_seed_fetchers import (  # noqa: E402
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


class ParliamentVideoSeedFetcherTests(unittest.TestCase):
    def test_target_selection_is_bounded_and_prioritized(self) -> None:
        targets = select_seed_targets()

        self.assertTrue(targets)
        self.assertEqual(len({target.source_id for target in targets}), len(targets))
        self.assertIn("official-youtube-nz-parliament", {target.source_id for target in targets})
        self.assertIn("select-committee-vimeo-pages", {target.source_id for target in targets})
        self.assertTrue(all(target.max_requests <= 2 for target in targets))

    def test_fetch_seed_target_records_hashes_and_sample_links(self) -> None:
        target = SeedTarget(
            source_id="official-youtube-nz-parliament",
            title="Official NZ Parliament YouTube channel",
            source_family="social_video_platform",
            source_role="official",
            source_classification="official",
            index_url="https://example.test/channel/videos",
            sample_url="https://example.test/channel/videos/alpha",
            access_constraints="public",
            proof_role="channel",
            max_requests=2,
        )
        index_html = """
            <html>
              <head><title>NZ Parliament</title></head>
              <body>
                <a href="/channel/videos/alpha">Alpha</a>
                <a href="/channel/videos/beta">Beta</a>
              </body>
            </html>
        """
        sample_html = "<html><body><h1>Alpha</h1></body></html>"
        index_response = FakeResponse(index_html, url=target.index_url)
        sample_response = FakeResponse(sample_html, url=target.sample_url)

        with patch(
            "scripts.fetch_parliament_video_seed_fetchers.request_with_retries",
            side_effect=[index_response, sample_response],
        ):
            record = fetch_seed_target(target, output_dir=ROOT / "tmp-test-output")

        self.assertEqual(record["proof_status"], "fetched")
        self.assertEqual(record["index_record_count"], 2)
        self.assertEqual(record["sample_record_count"], 1)
        self.assertEqual(record["index_sha256"], hashlib.sha256(index_html.encode()).hexdigest())
        self.assertEqual(record["sample_sha256"], hashlib.sha256(sample_html.encode()).hexdigest())
        self.assertEqual(record["request_urls"], [target.index_url, target.sample_url])

    def test_fetch_seed_target_records_blocked_reason(self) -> None:
        target = SeedTarget(
            source_id="tvnz-archive-looking-back",
            title="TVNZ Archive / Looking Back historical footage references",
            source_family="broadcast_archive",
            source_role="fallback",
            source_classification="fallback-validation",
            index_url="https://example.test/tvnz",
            sample_url="https://example.test/tvnz/detail",
            access_constraints="rights_review_required",
            proof_role="historical_broadcast_validation",
            max_requests=2,
        )

        def _raise(*_args, **_kwargs):
            response = requests.Response()
            response.status_code = 403
            response.url = target.index_url
            raise requests.HTTPError(response=response)

        with patch(
            "scripts.fetch_parliament_video_seed_fetchers.request_with_retries",
            side_effect=_raise,
        ):
            record = fetch_seed_target(target, output_dir=ROOT / "tmp-test-output")

        self.assertEqual(record["proof_status"], "blocked")
        self.assertIn("403", record["blocked_reason"])
        self.assertEqual(record["sample_record_count"], 0)

    def test_validate_manifest_rejects_missing_required_fields(self) -> None:
        manifest = {
            "manifest_version": 1,
            "track_id": "parliament_video_seed_fetchers_20260705",
            "repository": "corpus-nz-hansard",
            "generated_at": "2026-07-05",
            "policy": {
                "metadata_first": True,
                "no_media_download": True,
                "no_video_file_download": True,
                "no_audio_file_download": True,
                "no_public_media_release": True,
                "no_completeness_claim": True,
            },
            "summary": {
                "target_count": 0,
                "fetched_target_count": 0,
                "blocked_target_count": 0,
                "deferred_target_count": 0,
            },
            "targets": [],
            "handoff": [],
        }
        broken = copy.deepcopy(manifest)
        broken["policy"].pop("no_audio_file_download")

        failures = _validate_manifest(broken)

        self.assertTrue(any("no_audio_file_download" in failure for failure in failures))

    def test_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])


if __name__ == "__main__":
    unittest.main()
