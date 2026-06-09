"""Validate corpus-family engineering-alignment planning evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/corpus_family_engineering_alignment.json"
SCHEMA_PATH = ROOT / "schemas/corpus_family_engineering_alignment.schema.json"
DOC_PATH = ROOT / "docs/corpus-family-engineering-alignment.md"
TRACK_PATH = ROOT / "conductor/tracks/corpus_family_engineering_alignment_20260609/evidence.md"
SIBLING_PATH = Path("C:/Users/60217257/OneDrive - Flinders/repos/corpus-law-nz")

REQUIRED_STANDARDS = {
    "pyproject",
    "uv-lock",
    "src-layout",
    "typer-cli",
    "pytest",
    "ruff",
    "ty",
    "pre-commit",
    "renovate",
    "codeql",
    "scorecard",
    "zenodo-protection",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (MANIFEST_PATH, SCHEMA_PATH, DOC_PATH, TRACK_PATH):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{MANIFEST_PATH.relative_to(ROOT).as_posix()} {location}: {error.message}")

    standard_ids = {standard["id"] for standard in manifest["standards"]}
    if standard_ids != REQUIRED_STANDARDS:
        failures.append(
            "engineering standards must include exactly: " + ", ".join(sorted(REQUIRED_STANDARDS))
        )

    future_standards = {
        standard["id"] for standard in manifest["standards"] if standard["status"] == "future"
    }
    for required_future in ("src-layout", "typer-cli", "pytest", "pre-commit", "renovate"):
        if required_future not in future_standards:
            failures.append(f"{required_future} must remain marked future in this planning track.")

    adopted_standards = {
        standard["id"] for standard in manifest["standards"] if standard["status"] == "adopted"
    }
    for required_adopted in ("uv-lock", "ruff", "ty", "codeql", "scorecard", "zenodo-protection"):
        if required_adopted not in adopted_standards:
            failures.append(f"{required_adopted} must be marked adopted.")

    if not (ROOT / "uv.lock").exists():
        failures.append("Hansard uv.lock must remain committed.")
    if (ROOT / "src").exists():
        failures.append(
            "src/ package layout exists; update this planning track to implementation mode."
        )
    if (ROOT / ".pre-commit-config.yaml").exists():
        failures.append("pre-commit exists; update this planning track to implementation mode.")
    if (ROOT / "renovate.json").exists():
        failures.append("renovate exists; update this planning track to implementation mode.")

    if SIBLING_PATH.exists():
        sibling_checks = {
            "sibling pyproject": SIBLING_PATH / "pyproject.toml",
            "sibling uv.lock": SIBLING_PATH / "uv.lock",
            "sibling src layout": SIBLING_PATH / "src/nz_legislation_corpus",
            "sibling pre-commit": SIBLING_PATH / ".pre-commit-config.yaml",
            "sibling renovate": SIBLING_PATH / "renovate.json",
            "sibling CodeQL": SIBLING_PATH / ".github/workflows/codeql.yml",
            "sibling Scorecard": SIBLING_PATH / ".github/workflows/scorecard.yml",
        }
        for label, path in sibling_checks.items():
            if not path.exists():
                failures.append(f"{label} baseline path missing: {path.as_posix()}")

    target_commands = {item["command"] for item in manifest["migration"]["target_commands"]}
    for required_command in (
        "nzhc build-manifest",
        "nzhc validate",
        "nzhc metadata build",
        "nzhc hf stage",
        "nzhc zenodo draft",
    ):
        if required_command not in target_commands:
            failures.append(f"missing target CLI command: {required_command}")

    surfaces = {item["surface"] for item in manifest["publication_surfaces"]}
    if surfaces != {"github", "huggingface", "zenodo", "osf", "future_metadata"}:
        failures.append(
            "publication surfaces must cover GitHub, Hugging Face, Zenodo, OSF, and future metadata."
        )

    doc = _read(DOC_PATH)
    track = _read(TRACK_PATH)
    for required in (
        "nz_hansard_corpus",
        "nzhc",
        "requirements.txt",
        "pre-commit",
        "Renovate",
        "CodeQL",
        "Scorecard",
        "Zenodo",
        "Hugging Face",
        "OSF",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")
    for required in (
        "Current Baseline",
        "Migration Target",
        "CI And Security",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"CORPUS-FAMILY-ENGINEERING: {failure}")
        return 1
    print("Corpus-family engineering alignment is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
