"""Build Zenodo metadata for the canonical Hansard corpus release."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = Path(".zenodo.json")

DESCRIPTION = (
    "Document-level corpus pipeline for New Zealand Hansard records from a supplied "
    "DocumentsDB extract. The source ZIP is not redistributed. Public artifacts contain "
    "derived normalized Parquet output, code, documentation, schemas, manifests, and "
    "release evidence needed to audit and reproduce the dataset. The underlying source "
    "text is New Zealand Parliamentary Debates/Hansard material; project documentation "
    "records the Parliament provenance statement that no copyright exists in New Zealand "
    "Parliamentary Debates/Hansard. Original repository code, documentation, manifests, "
    "and release tooling are MIT licensed. This dataset is not an official New Zealand "
    "Parliament publication channel and is not endorsed by New Zealand Parliament."
)

RELATED_IDENTIFIERS = [
    {
        "identifier": "https://doi.org/10.5281/zenodo.20595194",
        "relation": "isVersionOf",
        "scheme": "doi",
    },
    {
        "identifier": "https://doi.org/10.5281/zenodo.20591996",
        "relation": "isVersionOf",
        "scheme": "doi",
    },
    {
        "identifier": "https://github.com/edithatogo/corpus-nz-hansard",
        "relation": "isSupplementedBy",
        "scheme": "url",
    },
    {
        "identifier": "https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0",
        "relation": "isSupplementedBy",
        "scheme": "url",
    },
    {
        "identifier": "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
        "relation": "isIdenticalTo",
        "scheme": "url",
    },
]


def build_zenodo_metadata(output: Path | str | None = DEFAULT_OUTPUT) -> dict[str, Any]:
    """Build and optionally write Zenodo-compatible metadata."""
    metadata: dict[str, Any] = {
        "title": "NZ Hansard Corpus",
        "upload_type": "dataset",
        "description": DESCRIPTION,
        "creators": [{"name": "Dylan Mordaunt"}],
        "version": "0.1.0",
        "license": "other-open",
        "publication_date": "2026-06-08",
        "keywords": [
            "New Zealand",
            "Hansard",
            "Parliament",
            "corpus",
            "open data",
            "legislative data",
        ],
        "related_identifiers": RELATED_IDENTIFIERS,
    }
    if output is not None:
        output_path = Path(output)
        output_path.write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build .zenodo.json metadata.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    build_zenodo_metadata(args.output)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
