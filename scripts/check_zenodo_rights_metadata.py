"""Validate Zenodo rights metadata and zenodraft policy documentation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ZENODO_METADATA = ROOT / ".zenodo.json"
RIGHTS_DOC = ROOT / "docs/zenodo-rights-and-zenodraft.md"
ZENODO_SETUP = ROOT / "docs/ZENODO_SETUP.md"
LICENSING_DOC = ROOT / "docs/licensing-and-provenance.md"
NOTICE = ROOT / "NOTICE.md"
TRACK_EVIDENCE = (
    ROOT / "conductor/tracks/zenodo_rights_metadata_and_zenodraft_workflow_20260609/evidence.md"
)

REQUIRED_IDENTIFIERS = {
    "https://doi.org/10.5281/zenodo.20595194",
    "https://github.com/edithatogo/corpus-nz-hansard",
    "https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0",
    "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (ZENODO_METADATA, RIGHTS_DOC, ZENODO_SETUP, LICENSING_DOC, NOTICE, TRACK_EVIDENCE):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    metadata = _json(ZENODO_METADATA)
    for field in (
        "title",
        "upload_type",
        "description",
        "creators",
        "version",
        "license",
        "publication_date",
        "keywords",
        "related_identifiers",
    ):
        if field not in metadata:
            failures.append(f".zenodo.json is missing required field: {field}")

    if metadata.get("title") != "NZ Hansard Corpus":
        failures.append(".zenodo.json title must remain NZ Hansard Corpus.")
    if metadata.get("upload_type") != "dataset":
        failures.append(".zenodo.json upload_type must be dataset.")
    if metadata.get("version") != "0.1.0":
        failures.append(".zenodo.json version must match the canonical release.")
    if metadata.get("license") != "other-open":
        failures.append(
            ".zenodo.json license must remain other-open until a narrower rights statement is approved."
        )
    if not metadata.get("creators"):
        failures.append(".zenodo.json creators must be non-empty.")

    description = str(metadata.get("description", ""))
    for required in (
        "source ZIP is not redistributed",
        "New Zealand Parliamentary Debates/Hansard",
        "MIT licensed",
        "not endorsed by New Zealand Parliament",
    ):
        if required not in description:
            failures.append(f".zenodo.json description is missing rights text: {required}")

    identifiers = {
        item.get("identifier")
        for item in metadata.get("related_identifiers", [])
        if isinstance(item, dict)
    }
    missing_identifiers = sorted(REQUIRED_IDENTIFIERS - identifiers)
    if missing_identifiers:
        failures.append(
            ".zenodo.json related_identifiers missing: " + ", ".join(missing_identifiers)
        )

    rights_doc = _read(RIGHTS_DOC)
    for required in (
        "repository code",
        "documentation",
        "manifests",
        "source text",
        "normalized Parquet",
        "archive bundle",
        "other-open",
        "zenodraft/action@0.13.3",
        "ZENODO_ACCESS_TOKEN",
        "ZENODO_SANDBOX_ACCESS_TOKEN",
        "publish: false",
        "zenodo-production-publish",
    ):
        if required not in rights_doc:
            failures.append(f"{RIGHTS_DOC.relative_to(ROOT).as_posix()} is missing: {required}")

    zenodo_setup = _read(ZENODO_SETUP)
    for required in (
        ".zenodo.json",
        "ZENODO_SANDBOX_ACCESS_TOKEN",
        "zenodraft/action@0.13.3",
        "publish: false",
    ):
        if required not in zenodo_setup:
            failures.append(f"{ZENODO_SETUP.relative_to(ROOT).as_posix()} is missing: {required}")

    for workflow in (
        ".github/workflows/zenodo_archive.yml",
        ".github/workflows/zenodo_metadata.yml",
    ):
        text = _read(ROOT / workflow)
        if re.search(r"^\s+publish\s*:", text, flags=re.MULTILINE):
            failures.append(f"{workflow} must not expose a publish input.")
        if "--publish" in text:
            failures.append(f"{workflow} must not pass --publish.")

    publish_workflow = _read(ROOT / ".github/workflows/zenodo_publish.yml")
    if "environment: zenodo-production-publish" not in publish_workflow:
        failures.append("zenodo_publish.yml must use the protected Zenodo publication environment.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"ZENODO-RIGHTS: {failure}")
        return 1
    print("Zenodo rights metadata and zenodraft policy are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
