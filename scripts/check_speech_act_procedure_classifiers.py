"""Validate the blocked speech-act and procedure classifier surface."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.speech_act_procedure_classifiers import (  # noqa: E402, I001
    DOC_PATH,
    EVIDENCE_PATH,
    INDEX_PATH,
    MANIFEST_PATH,
    PLAN_PATH,
    SCHEMA_PATH,
    PROCEDURE_FIXTURE,
    PROCEDURE_MODEL_MANIFEST,
    VALIDATED_SPEECH_TURN_MANIFEST,
)

TRACK_PATH = ROOT / "conductor/tracks/speech_act_procedure_classifiers_20260610/index.md"
TRACKS_PATH = ROOT / "conductor/tracks.md"
SAMPLE_README_PATH = ROOT / "samples/speech-act-procedure-classifiers/README.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = [
        MANIFEST_PATH,
        SCHEMA_PATH,
        DOC_PATH,
        INDEX_PATH,
        PLAN_PATH,
        EVIDENCE_PATH,
        TRACK_PATH,
        SAMPLE_README_PATH,
        PROCEDURE_MODEL_MANIFEST,
        PROCEDURE_FIXTURE,
        VALIDATED_SPEECH_TURN_MANIFEST,
    ]
    for path in required_paths:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    for error in sorted(
        Draft202012Validator(schema).iter_errors(manifest), key=lambda item: list(item.path)
    ):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    if manifest["status"] != "blocked":
        failures.append("Track status must remain blocked.")
    if manifest["release_status"] != "blocked-pending-validated-speech-turn":
        failures.append("Release status must remain blocked-pending-validated-speech-turn.")
    if manifest["validation_results"]["blocked_by_speech_turn_gate"] is not True:
        failures.append("Manifest must record the speech-turn gate blocker.")

    procedure_model = _json(PROCEDURE_MODEL_MANIFEST)
    categories = {item["category"] for item in procedure_model["procedural_categories"]}
    if not {"question", "supplementary_question", "ruling", "interjection"}.issubset(categories):
        failures.append(
            "Procedure model must cover question, supplementary_question, ruling, and interjection."
        )

    doc = _read(DOC_PATH)
    for required in (
        "speech acts",
        "question/answer structure",
        "interjections",
        "procedural rulings",
        "debate segments",
        "blocked until validated speech-turn components are available",
        "requirements/ml.txt",
    ):
        if required.lower() not in doc.lower():
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    readme = _read(SAMPLE_README_PATH)
    for required in (
        "blocked future-track surface",
        "speech-act and procedure classifiers",
        "human validation",
        "speech-turn dependency",
    ):
        if required.lower() not in readme.lower():
            failures.append(
                f"{SAMPLE_README_PATH.relative_to(ROOT).as_posix()} is missing: {required}"
            )

    track = _read(TRACK_PATH)
    for required in ("Status: blocked.", "Primary Artifacts", "Blocker"):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    for required in ("Blocked", "Dependencies", "Label Families", "Planned Models"):
        if required not in _read(EVIDENCE_PATH):
            failures.append(f"{EVIDENCE_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    if "speech_act_procedure_classifiers_20260610" not in _read(TRACKS_PATH):
        failures.append(
            "Track registry must include the speech-act and procedure classifier track."
        )
    if "[!]" not in _read(TRACKS_PATH):
        failures.append("Track registry must expose blocked status markers.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"SPEECH-ACT-PROCEDURE-CLASSIFIERS: {failure}")
        return 1
    print("Speech-act and procedure classifier track is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
