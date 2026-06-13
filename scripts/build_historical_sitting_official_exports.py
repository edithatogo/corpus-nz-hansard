"""Build a derived index for the official historical sitting PDF export surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/historical_sitting_official_exports.json"
DEFAULT_OUTPUT_DIR = ROOT / "derived/historical_sitting_official_exports"
DEFAULT_INDEX_PATH = DEFAULT_OUTPUT_DIR / "historical_sitting_official_export_index.json"
DEFAULT_CACHE_DIR = DEFAULT_OUTPUT_DIR / "pdf"


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _relativize(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def _download_pdf(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; corpus-nz-hansard/1.0)",
            "Accept": "application/pdf,*/*;q=0.8",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:  # nosec: B310
        return response.read()


def _first_text_snippet(reader: PdfReader, max_chars: int = 800) -> str:
    snippets: list[str] = []
    for page in reader.pages[:3]:
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text:
            snippets.append(text)
        if sum(len(item) for item in snippets) >= max_chars:
            break
    snippet = "\n".join(snippets)
    return snippet[:max_chars]


def build_historical_sitting_official_exports(
    *,
    manifest_path: Path = MANIFEST_PATH,
    output_path: Path = DEFAULT_INDEX_PATH,
    cache_dir: Path = DEFAULT_CACHE_DIR,
    generated_at: str | None = None,
) -> dict[str, Any]:
    manifest = _json(manifest_path)
    generated_at = generated_at or datetime.now(UTC).isoformat()
    cache_dir.mkdir(parents=True, exist_ok=True)

    sources: list[dict[str, Any]] = []
    for source in manifest["sources"]:
        pdf_bytes = _download_pdf(source["url"])
        digest = hashlib.sha256(pdf_bytes).hexdigest()
        pdf_path = cache_dir / f'{source["id"]}.pdf'
        pdf_path.write_bytes(pdf_bytes)

        reader = PdfReader(BytesIO(pdf_bytes))
        snippet = _first_text_snippet(reader)
        sources.append(
            {
                "id": source["id"],
                "title": source["title"],
                "url": source["url"],
                "publication_stage": source["publication_stage"],
                "coverage_note": source["coverage_note"],
                "page_count": len(reader.pages),
                "has_text": bool(snippet.strip()),
                "text_excerpt": snippet,
                "sha256": digest,
                "byte_size": len(pdf_bytes),
                "cached_pdf": _relativize(pdf_path),
            }
        )

    payload = {
        "artifact_name": "historical_sitting_official_exports_index",
        "artifact_version": "0.1.0",
        "generated_at": generated_at,
        "source_manifest": _relativize(manifest_path),
        "sources": sources,
        "notes": [
            "This derived index records the confirmed official PDF export surfaces.",
            "It is a machine-readable starting point for PDF-backed reconciliation.",
        ],
    }
    _write_json(payload, output_path)
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a derived index for the official historical sitting PDF exports."
    )
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_INDEX_PATH)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE_DIR)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_historical_sitting_official_exports(
        manifest_path=args.manifest,
        output_path=args.output,
        cache_dir=args.cache_dir,
    )
    print(f"Wrote {args.output}")
    print(f"Indexed sources: {len(result['sources'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
