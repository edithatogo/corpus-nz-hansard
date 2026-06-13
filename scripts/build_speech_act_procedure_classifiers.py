"""Build the blocked speech-act and procedure classifier surface."""

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

from scripts.speech_act_procedure_classifiers import (  # noqa: E402
    DOC_PATH,
    EVIDENCE_PATH,
    INDEX_PATH,
    MANIFEST_PATH,
    PLAN_PATH,
    SCHEMA_PATH,
    build_speech_act_procedure_classifiers,
)


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build the blocked speech-act procedure classifier surface."
    )
    parser.add_argument("--manifest", type=Path, default=MANIFEST_PATH)
    args = parser.parse_args()
    manifest = build_speech_act_procedure_classifiers(
        generated_at=datetime.now(UTC).isoformat(), write=True
    )
    _write_json(args.manifest, manifest)
    print(f"Wrote {args.manifest}")
    print(f"Wrote {SCHEMA_PATH}")
    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {INDEX_PATH}")
    print(f"Wrote {PLAN_PATH}")
    print(f"Wrote {EVIDENCE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
