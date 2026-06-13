"""Build exploratory semantic-search embeddings and topic-model outputs."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.semantic_search_embeddings_topics import (  # noqa: E402, I001
    DOC_PATH,
    JSONL_PATH,
    MANIFEST_PATH,
    README_PATH,
    RECORD_SCHEMA_PATH,
    REVIEW_PATH,
    SCHEMA_PATH,
    build_semantic_search_embeddings_topics as build_semantic_search_seed_outputs,
    _manifest_schema,
    _record_schema,
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_semantic_search_embeddings_topics(
    *, manifest_path: Path | None = None, generated_at: str | None = None
) -> dict[str, Any]:
    manifest_path = manifest_path or MANIFEST_PATH
    generated_at = generated_at or datetime.now(UTC).isoformat()
    manifest = build_semantic_search_seed_outputs(generated_at=generated_at, write=True)
    _write_json(manifest_path, manifest)
    _write_json(SCHEMA_PATH, _manifest_schema())
    _write_json(
        RECORD_SCHEMA_PATH, _record_schema(manifest["validation_counts"]["embedding_dimension"])
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build exploratory semantic-search embeddings and topic-model outputs."
    )
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_semantic_search_embeddings_topics(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Wrote {JSONL_PATH}")
    print(f"Wrote {REVIEW_PATH}")
    print(f"Wrote {README_PATH}")
    print(f"Wrote {DOC_PATH}")
    print(f"Records rendered: {manifest['validation_counts']['record_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
