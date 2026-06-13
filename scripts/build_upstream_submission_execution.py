"""Build the upstream submission execution manifest."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "manifests/upstream_submission_execution_manifest.json"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_upstream_submission_execution(
    *, manifest_path: Path = DEFAULT_MANIFEST, generated_at: str | None = None
) -> dict[str, Any]:
    generated_at = generated_at or datetime.now(UTC).isoformat()
    manifest = json.loads(DEFAULT_MANIFEST.read_text(encoding="utf-8"))
    manifest["generated_at"] = generated_at
    _write_json(manifest_path, manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the upstream submission execution manifest."
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_upstream_submission_execution(manifest_path=args.manifest)
    print(f"Wrote {args.manifest}")
    print(f"Submission state: {manifest['submission_state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
