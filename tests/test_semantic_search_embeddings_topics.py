from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_semantic_search_embeddings_topics import build_semantic_search_embeddings_topics  # noqa: I001
from scripts.check_semantic_search_embeddings_topics import (
    MANIFEST_PATH,
    _failures,
    _json,
    _jsonl_rows,
)  # noqa: I001


class SemanticSearchEmbeddingsTopicsTests(unittest.TestCase):
    def test_builder_emits_manifest(self) -> None:
        manifest = build_semantic_search_embeddings_topics(
            manifest_path=MANIFEST_PATH, generated_at="2026-06-11T00:00:00+10:00"
        )
        self.assertEqual(manifest["release_status"], "sample-not-release")
        self.assertGreaterEqual(manifest["validation_counts"]["topic_count"], 2)

    def test_manifest_configuration_is_consistent(self) -> None:
        self.assertEqual(_failures(), [])

    def test_manifest_and_rows_were_written(self) -> None:
        manifest = _json(MANIFEST_PATH)
        rows = _jsonl_rows(
            ROOT / "samples/semantic-search-embeddings/semantic_search_embeddings_topics.jsonl"
        )
        self.assertEqual(manifest["validation_counts"]["record_count"], 10)
        self.assertEqual(len(rows), 10)
        self.assertEqual(
            len(rows[0]["embedding_vector"]), manifest["validation_counts"]["embedding_dimension"]
        )
        self.assertGreaterEqual(len({row["topic_id"] for row in rows}), 2)


if __name__ == "__main__":
    unittest.main()
