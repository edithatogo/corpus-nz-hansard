from __future__ import annotations

import unittest

from scripts.build_nif_rdf_linguistic_views import build_nif_rdf_linguistic_views
from scripts.check_nif_rdf_linguistic_views import MANIFEST_PATH, _failures, _json


class NifRdfLinguisticViewsTests(unittest.TestCase):
    def test_builder_emits_sample_release_manifest(self) -> None:
        manifest = build_nif_rdf_linguistic_views(
            generated_at="2026-06-24T00:00:00+10:00", write=False
        )
        self.assertEqual(manifest["release_status"], "release-ready-sample-nif-rdf-view")
        self.assertTrue(manifest["public_claim"]["sample_only"])
        self.assertFalse(manifest["public_claim"]["full_corpus_release"])
        self.assertGreater(manifest["counts"]["token_views"], 0)

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["track_id"], "nif_rdf_linguistic_views_20260610")
        self.assertEqual(manifest["release_status"], "release-ready-sample-nif-rdf-view")


if __name__ == "__main__":
    unittest.main()
