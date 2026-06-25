from __future__ import annotations

import unittest

from scripts.build_w3c_time_temporal_model import build_w3c_time_temporal_model
from scripts.check_w3c_time_temporal_model import MANIFEST_PATH, _failures, _json


class W3CTimeTemporalModelTests(unittest.TestCase):
    def test_builder_emits_sample_release_manifest(self) -> None:
        manifest = build_w3c_time_temporal_model(
            generated_at="2026-06-24T00:00:00+10:00", write=False
        )
        self.assertEqual(manifest["release_status"], "release-ready-sample-temporal-model")
        self.assertTrue(manifest["public_claim"]["sample_only"])
        self.assertFalse(manifest["public_claim"]["full_historical_temporal_coverage"])
        self.assertEqual(manifest["counts"]["sample_instants"], 1)

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["track_id"], "w3c_time_temporal_model_20260610")
        self.assertEqual(manifest["release_status"], "release-ready-sample-temporal-model")


if __name__ == "__main__":
    unittest.main()
