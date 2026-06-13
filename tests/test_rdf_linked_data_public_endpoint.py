from __future__ import annotations

import unittest

from scripts.build_rdf_linked_data_public_endpoint import build_rdf_linked_data_public_endpoint
from scripts.check_rdf_linked_data_public_endpoint import MANIFEST_PATH, _failures, _json


class RdfLinkedDataPublicEndpointTests(unittest.TestCase):
    def test_builder_emits_blocked_manifest(self) -> None:
        manifest = build_rdf_linked_data_public_endpoint(generated_at="2026-06-11T00:00:00+10:00")
        self.assertEqual(manifest["release_status"], "blocked-pending-validated-components")

    def test_repo_manifest_shape_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_repo_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["artifact_name"], "RDF / Linked Data public endpoint release")
        self.assertEqual(
            manifest["validation_results"]["readiness_status"],
            "blocked-pending-validated-components",
        )


if __name__ == "__main__":
    unittest.main()
