from __future__ import annotations

import unittest

from scripts.build_akoma_ntoso_public_endpoint import build_akoma_ntoso_public_endpoint
from scripts.check_akoma_ntoso_public_endpoint import MANIFEST_PATH, _failures, _json


class AkomaNtosoPublicEndpointTests(unittest.TestCase):
    def test_builder_emits_sample_public_endpoint_manifest(self) -> None:
        manifest = build_akoma_ntoso_public_endpoint(
            manifest_path=None,
            generated_at="2026-06-11T00:00:00+10:00",
        )
        self.assertEqual(manifest["release_status"], "release-ready-sample-public-endpoint")
        self.assertEqual(
            manifest["release_notes"]["status"],
            "sample-public-release-notes-published",
        )

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "Akoma Ntoso public endpoint release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "release-ready-sample-public-endpoint",
        )
        self.assertEqual(
            manifest["release_notes"]["examples"],
            [
                "samples/akoma-ntoso/Akoma-Ntoso.sample.xml",
                "samples/akoma-ntoso/Akoma-Ntoso.metadata.xml",
            ],
        )


if __name__ == "__main__":
    unittest.main()
