"""Validate release version, DOI, and publication metadata consistency."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

REPOSITORY_URL = "https://github.com/edithatogo/corpus-nz-hansard"
HUGGINGFACE_URL = "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus"
VERSIONING_DOC = "docs/bleeding-edge-versioning-ci-quality.md"
REQUIRED_DOC_SNIPPETS = (
    "Current state",
    "Target state",
    "Code/package version authority",
    "Dataset version authority",
    "Schema version authority",
    "Hugging Face revision authority",
    "Zenodo DOI snapshot authority",
    "Manifest hash authority",
    "Release Please decision",
    "Publication safety gates",
)


def _read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def _json(relative_path: str) -> dict[str, Any]:
    return json.loads(_read(relative_path))


def _toml(relative_path: str) -> dict[str, Any]:
    return tomllib.loads(_read(relative_path))


def _field(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*\"?([^\"\n]+)\"?\s*$", text, flags=re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip()


def _contains_all(text: str, values: tuple[str, ...]) -> list[str]:
    return [value for value in values if value not in text]


def _failures() -> list[str]:
    failures: list[str] = []

    version = _read("VERSION").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        failures.append(f"VERSION is not SemVer-compatible: {version}")

    pyproject = _toml("pyproject.toml")
    project = pyproject.get("project", {})
    if project.get("version") != version:
        failures.append("pyproject.toml [project].version must match VERSION.")
    if project.get("name") != "corpus-nz-hansard":
        failures.append("pyproject.toml [project].name must remain corpus-nz-hansard.")

    citation = _read("CITATION.cff")
    citation_version = _field(citation, "version")
    citation_doi = _field(citation, "doi")
    citation_url = _field(citation, "url")
    citation_date = _field(citation, "date-released")
    if citation_version != version:
        failures.append("CITATION.cff version must match VERSION.")
    if _field(citation, "repository-code") != REPOSITORY_URL:
        failures.append("CITATION.cff repository-code must match the canonical GitHub URL.")
    if _field(citation, "repository-artifact") != HUGGINGFACE_URL:
        failures.append(
            "CITATION.cff repository-artifact must match the canonical Hugging Face URL."
        )

    manifest = _json("manifests/public_dataset_release_manifest.json")
    publication = manifest.get("publication", {})
    manifest_doi = publication.get("doi")
    manifest_doi_url = publication.get("doi_url")
    manifest_record = publication.get("zenodo_record")
    manifest_date = publication.get("publication_date")
    manifest_release = publication.get("github_release")
    if manifest.get("publication_status") != "published" or manifest.get("published") is not True:
        failures.append("public release manifest must record the canonical release as published.")
    if manifest_release != f"{REPOSITORY_URL}/releases/tag/v{version}":
        failures.append("public release manifest GitHub release URL must match VERSION.")
    if publication.get("github_repository") != REPOSITORY_URL:
        failures.append("public release manifest GitHub repository URL is not canonical.")
    if publication.get("huggingface_dataset") != HUGGINGFACE_URL:
        failures.append("public release manifest Hugging Face URL is not canonical.")

    if citation_doi != manifest_doi:
        failures.append("CITATION.cff DOI must match public release manifest DOI.")
    if citation_url != manifest_record:
        failures.append("CITATION.cff url must match public release manifest Zenodo record.")
    if manifest_doi and manifest_doi_url != f"https://doi.org/{manifest_doi}":
        failures.append("public release manifest DOI URL must derive from publication.doi.")
    if manifest_doi:
        record_id = manifest_doi.rsplit(".", maxsplit=1)[-1]
        if manifest_record != f"https://zenodo.org/records/{record_id}":
            failures.append(
                "public release manifest Zenodo record must derive from publication.doi."
            )
    if citation_date != manifest_date:
        failures.append("CITATION.cff date-released must match manifest publication_date.")

    release_notes = _read("RELEASE_NOTES.md")
    dataset_card = _read("DATASET_CARD.md")
    required_release_text = (
        f"# Release Notes: {version}",
        f"{REPOSITORY_URL}/releases/tag/v{version}",
        HUGGINGFACE_URL,
    )
    required_dataset_text = (
        f"{REPOSITORY_URL}/releases/tag/v{version}",
        HUGGINGFACE_URL,
    )
    if citation_doi:
        required_release_text += (f"https://doi.org/{citation_doi}",)
        required_dataset_text += (f"https://doi.org/{citation_doi}",)
    if citation_url:
        required_dataset_text += (citation_url,)
    for missing in _contains_all(release_notes, required_release_text):
        failures.append(f"RELEASE_NOTES.md is missing: {missing}")
    for missing in _contains_all(dataset_card, required_dataset_text):
        failures.append(f"DATASET_CARD.md is missing: {missing}")

    if not (ROOT / VERSIONING_DOC).exists():
        failures.append(f"{VERSIONING_DOC} must exist.")
    else:
        versioning_doc = _read(VERSIONING_DOC)
        for missing in _contains_all(versioning_doc, REQUIRED_DOC_SNIPPETS):
            failures.append(f"{VERSIONING_DOC} is missing section or term: {missing}")
        for value in (
            version,
            REPOSITORY_URL,
            HUGGINGFACE_URL,
            manifest_doi or "",
            manifest_release or "",
        ):
            if value and value not in versioning_doc:
                failures.append(f"{VERSIONING_DOC} is missing release authority value: {value}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"RELEASE-VERSION: {failure}")
        return 1
    print("Release version metadata is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
