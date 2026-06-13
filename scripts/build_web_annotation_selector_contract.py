"""Build the W3C Web Annotation selector contract manifest."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "manifests/web_annotation_selector_contract.json"
TRACK_ID = "web_annotation_selector_contract_20260610"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_web_annotation_selector_contract(
    *, manifest_path: Path | None = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    manifest = json.loads(
        (ROOT / "manifests/web_annotation_selector_contract.json").read_text(encoding="utf-8")
    )
    manifest["generated_at"] = generated_at
    if manifest_path is not None:
        _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the W3C Web Annotation selector contract manifest."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_web_annotation_selector_contract(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Contract id: {manifest['contract_id']}")
    print(f"Track id: {TRACK_ID}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
