from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_researcher_client_helpers import build_researcher_client_helpers
from scripts.check_researcher_client_helpers import MANIFEST_PATH, _failures, _json
from scripts.researcher_client_helpers import (
    DOCUMENT_SAMPLE_PATH,
    RDF_SAMPLE_PATH,
    duckdb_document_summary,
    python_document_summary,
    rdf_sample_summary,
)


class ResearcherClientHelpersTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_researcher_client_helpers(
            manifest_path=None, generated_at="2026-06-11T00:00:00+10:00"
        )
        self.assertEqual(manifest["release_status"], "local-review-only")

    def test_examples_run_against_sample_artifacts(self) -> None:
        python_summary = python_document_summary(DOCUMENT_SAMPLE_PATH)
        duckdb_summary = duckdb_document_summary(DOCUMENT_SAMPLE_PATH)
        rdf_summary = rdf_sample_summary(RDF_SAMPLE_PATH)
        self.assertEqual(python_summary["row_count"], 3)
        self.assertEqual(duckdb_summary["row_count"], 3)
        self.assertEqual(rdf_summary["dataset_titles"], ["RDF linked-data sample package"])

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_was_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        self.assertEqual(manifest["helper_status"]["python_examples"], "implemented")
        self.assertEqual(manifest["validation_results"]["duckdb_example_runs"], True)


if __name__ == "__main__":
    unittest.main()
