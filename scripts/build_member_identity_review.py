"""Build the local member-identity review package from reviewed fixtures."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.canonical_ids import canonical_id, component_payload
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from scripts.canonical_ids import canonical_id, component_payload

ROOT = Path(__file__).resolve().parents[1]
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
AUTHORITY_PATH = ROOT / "derived/member_identity_authority.json"
REVIEW_PATH = ROOT / "samples/member-identity/member_identity_review.csv"
README_PATH = ROOT / "samples/member-identity/README.md"

AUTHORITY_RECORDS = [
    {
        "lookup_name": "CLAYTON COSGROVE",
        "authority_source_id": "nz-parliament-former-members",
        "authority_url": "https://www3.parliament.nz/en/mps-and-electorates/former-members-of-parliament/cosgrove-clayton/",
        "canonical_name": "Clayton Cosgrove",
        "aliases": ["CLAYTON COSGROVE", "Hon Clayton Cosgrove"],
        "source_stable_id": "nz-parliament-former-members",
    },
    {
        "lookup_name": "ROGER SOWRY",
        "authority_source_id": "nz-parliament-roll-of-members",
        "authority_url": "https://www3.parliament.nz/media/11482/roll-of-members-of-the-new-zealand-house-of-representatives-1854-onwards.pdf",
        "canonical_name": "Roger Morrison Sowry",
        "aliases": ["Hon Roger Sowry", "Roger Sowry"],
        "source_stable_id": "nz-parliament-roll-of-members",
    },
]

REVIEW_COLUMNS = [
    "sample_id",
    "example_class",
    "target_component_type",
    "target_component_id",
    "source_document_type",
    "parliament_number",
    "source_stable_id",
    "source_excerpt",
    "member_of_parliament_raw",
    "member_raw_token",
    "member_id",
    "member_display_name",
    "member_authority_source",
    "member_authority_url",
    "member_resolution_method",
    "member_resolution_confidence",
    "member_resolution_status",
    "dependency_state",
    "review_status",
    "release_status",
    "notes",
]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize_token(value: str) -> str:
    value = " ".join(value.replace(".", "").split())
    prefixes = ("RT HON ", "HON ", "DR ", "SIR ", "DAME ", "MR ", "MRS ", "MS ", "MISS ", "PROF ")
    upper = value.upper()
    for prefix in prefixes:
        if upper.startswith(prefix):
            return value[len(prefix) :].strip()
    return value.strip()


def _authority_lookup() -> dict[str, dict[str, Any]]:
    lookup: dict[str, dict[str, Any]] = {}
    for record in AUTHORITY_RECORDS:
        raw_aliases: list[str] = record["aliases"]  # ty:ignore[invalid-assignment]
        names: list[str] = [record["lookup_name"], record["canonical_name"], *raw_aliases]  # ty:ignore[invalid-assignment]
        for name in names:
            lookup[_normalize_token(name).upper()] = record
    return lookup


def _member_id(authority_source_id: str, local_key: str) -> str:
    payload = component_payload(
        release_version="0.1.0",
        component_type="member",
        source_stable_id=authority_source_id,
        local_key=local_key,
        validation_manifest="manifests/member_identity_resolution_validation.json",
    )
    return canonical_id("neutral-component", payload)


def build_authority_table() -> dict[str, Any]:
    return {
        "track_id": "member_identity_resolution_20260609",
        "generated_at": "2026-06-10",
        "purpose": "Local member identity authority table for the reviewed sample package.",
        "source_hashes": {
            "nz-parliament-former-members": "7a7e6c320aec15354287cf757bf930ed407d46faf60b4938243af5b9df2b6b10",
            "nz-parliament-roll-of-members": "61b3fb2a406769efbb0620700aedef497d00c8a7ff510a7b3eb0748f426230e8",
        },
        "authority_sources": [
            {
                "authority_source_id": "nz-parliament-former-members",
                "title": "Former Members of Parliament",
                "url": "https://www3.parliament.nz/en/mps-and-electorates/former-members-of-parliament/",
                "publisher": "New Zealand Parliament",
                "coverage_note": "Historical member register with service ranges for former MPs.",
                "source_hash": "7a7e6c320aec15354287cf757bf930ed407d46faf60b4938243af5b9df2b6b10",
            },
            {
                "authority_source_id": "nz-parliament-roll-of-members",
                "title": "Roll of members of the New Zealand House of Representatives, 1854 onwards",
                "url": "https://www3.parliament.nz/media/11482/roll-of-members-of-the-new-zealand-house-of-representatives-1854-onwards.pdf",
                "publisher": "New Zealand Parliament",
                "coverage_note": "Historical roll with dates of service for member identity resolution.",
                "source_hash": "61b3fb2a406769efbb0620700aedef497d00c8a7ff510a7b3eb0748f426230e8",
            },
        ],
        "resolution_rules": [
            "Exact member-name matches resolve to canonical member records.",
            "Honorifics such as Hon, Rt Hon, Dr, Sir, Dame, Mr, Mrs, Ms, Miss, and Prof are stripped before comparison.",
            "Semicolon-delimited raw member values are resolved as separate member tokens.",
            "Office titles and generic publication headings are not resolved as member identities.",
            "Ambiguous variants remain explicit and require authority matching before canonical publication.",
        ],
        "member_records": [
            {
                "component_id": _member_id("nz-parliament-former-members", "clayton-cosgrove"),
                "member_id": _member_id("nz-parliament-former-members", "clayton-cosgrove"),
                "display_name": "Clayton Cosgrove",
                "canonical_name": "Clayton Cosgrove",
                "aliases": ["CLAYTON COSGROVE", "Hon Clayton Cosgrove"],
                "authority_source_id": "nz-parliament-former-members",
                "authority_url": "https://www3.parliament.nz/en/mps-and-electorates/former-members-of-parliament/cosgrove-clayton/",
                "service_periods": [
                    {
                        "start_date": "1999-11-27",
                        "end_date": "2017-09-23",
                        "parliament_numbers": "46-51",
                    }
                ],
                "resolution_scope": "exact-name-match",
            },
            {
                "component_id": _member_id("nz-parliament-roll-of-members", "roger-morrison-sowry"),
                "member_id": _member_id("nz-parliament-roll-of-members", "roger-morrison-sowry"),
                "display_name": "Roger Morrison Sowry",
                "canonical_name": "Roger Morrison Sowry",
                "aliases": ["Hon Roger Sowry", "Roger Sowry"],
                "authority_source_id": "nz-parliament-roll-of-members",
                "authority_url": "https://www3.parliament.nz/media/11482/roll-of-members-of-the-new-zealand-house-of-representatives-1854-onwards.pdf",
                "service_periods": [
                    {
                        "start_date": "1990-10-27",
                        "end_date": "2005-09-17",
                        "parliament_numbers": "43-47",
                    }
                ],
                "resolution_scope": "honorific-normalized-match",
            },
        ],
        "review_notes": [
            "This authority table is local-review-only and does not publish a full corpus-wide member identity dataset.",
            "The sample package resolves the reviewed gold fixtures only.",
            "Broader publication still requires corpus-wide validation and the full historical authority surface.",
        ],
    }


def load_gold_member_samples() -> list[dict[str, Any]]:
    samples = _read_json(GOLD_PATH)["samples"]
    return [sample for sample in samples if sample["domain"] == "member_resolution"]


def _resolve_token(token: str) -> dict[str, Any] | None:
    normalized = _normalize_token(token)
    authority = _authority_lookup().get(normalized.upper())
    if authority is None:
        return None
    return {
        "member_id": _member_id(
            authority["source_stable_id"], authority["canonical_name"].lower().replace(" ", "-")
        ),
        "member_display_name": authority["canonical_name"],
        "member_authority_source": authority["authority_source_id"],
        "member_authority_url": authority["authority_url"],
        "member_resolution_method": "exact-name-match"
        if authority["canonical_name"] == "Clayton Cosgrove"
        else "honorific-normalized-match",
        "member_resolution_confidence": "high"
        if authority["canonical_name"] == "Clayton Cosgrove"
        else "medium",
        "member_resolution_status": "authoritative"
        if authority["canonical_name"] == "Clayton Cosgrove"
        else "ambiguous-match",
    }


def resolve_member_field(raw_value: str | None) -> list[dict[str, Any]]:
    if not raw_value:
        return []
    resolved: list[dict[str, Any]] = []
    for token in [part.strip() for part in raw_value.split(";") if part.strip()]:
        match = _resolve_token(token)
        if match is not None:
            match["member_raw_token"] = token
            resolved.append(match)
    return resolved


def build_review_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gold_index = {sample["sample_id"]: sample for sample in load_gold_member_samples()}
    for sample_id in [
        "gold-member-resolution-01",
        "gold-member-resolution-02",
        "gold-member-resolution-03",
        "gold-member-resolution-04",
        "gold-member-resolution-05",
    ]:
        sample = gold_index[sample_id]
        raw_value = sample["label"]["value"] or sample["text_excerpt"].split(":", 1)[0]
        resolved = resolve_member_field(raw_value)
        base = {
            "sample_id": sample_id,
            "example_class": sample["example_class"],
            "target_component_type": sample["target_component_type"],
            "target_component_id": sample["target_component_id"] or "",
            "source_document_type": sample["source_reference"]["document_type"],
            "parliament_number": sample["source_reference"]["parliament_number"],
            "source_stable_id": sample["source_reference"].get("parliament_document_id") or "",
            "source_excerpt": sample["text_excerpt"],
            "member_of_parliament_raw": raw_value,
            "member_raw_token": raw_value,
            "member_id": "",
            "member_display_name": "",
            "member_authority_source": "",
            "member_authority_url": "",
            "member_resolution_method": "",
            "member_resolution_confidence": "none",
            "member_resolution_status": "unresolved",
            "dependency_state": "authority-required",
            "review_status": "reviewed",
            "release_status": "sample-not-release",
            "notes": "",
        }
        if sample_id == "gold-member-resolution-01" and resolved:
            base.update(resolved[0])
            base["dependency_state"] = "validated-member-authority"
            base["notes"] = "Exact uppercase speaker name matches the former-members record."
        elif sample_id == "gold-member-resolution-03" and resolved:
            base.update(resolved[0])
            base["dependency_state"] = "validated-member-authority"
            base["notes"] = (
                "Honorific stripping preserves the raw variant while matching the historical roll."
            )
        elif sample_id == "gold-member-resolution-02":
            base["member_resolution_method"] = "office-title-no-match"
            base["member_resolution_status"] = "unresolved"
            base["dependency_state"] = "authority-required"
            base["notes"] = (
                "Do not resolve an office title to a member identity without dated authority."
            )
        elif sample_id == "gold-member-resolution-04":
            base["member_resolution_method"] = "heading-like-no-match"
            base["member_resolution_status"] = "unresolved"
            base["dependency_state"] = "not-applicable"
            base["notes"] = "Heading-like text is not a clear member identity."
        elif sample_id == "gold-member-resolution-05":
            base["member_resolution_method"] = "excluded-heading"
            base["member_resolution_status"] = "excluded"
            base["dependency_state"] = "not-applicable"
            base["notes"] = "Exclude generic publication headings from member-resolution metrics."
        rows.append(base)
    return rows


def write_csv(rows: list[dict[str, Any]], path: Path = REVIEW_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def build_package(output_root: Path = ROOT) -> dict[str, str]:
    authority = build_authority_table()
    review_rows = build_review_rows()
    authority_path = output_root / AUTHORITY_PATH.relative_to(ROOT)
    review_path = output_root / REVIEW_PATH.relative_to(ROOT)
    readme_path = output_root / README_PATH.relative_to(ROOT)
    authority_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    readme_path.parent.mkdir(parents=True, exist_ok=True)
    authority_path.write_text(
        json.dumps(authority, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_csv(review_rows, review_path)
    readme_path.write_text(
        "\n".join(
            [
                "# Member Identity Resolution Sample Package",
                "",
                "Maintainer-review package for the derived member-identity layer.",
                "This package is sample-not-release and is not release-readiness evidence.",
                "",
                "- `member_identity_review.csv`",
                "",
                "Validation and traceability:",
                "",
                "- Manifest: `manifests/member_identity_resolution_validation.json`",
                "- Package manifest: `manifests/member_identity_resolution_package.json`",
                "- Authority table: `derived/member_identity_authority.json`",
                "- Review table: `samples/member-identity/member_identity_review.csv`",
                "- Gold evaluation fixtures: `fixtures/gold_evaluation_samples.json`",
                "- Authority source discovery: `manifests/authority_sources.json`",
                "",
                "Rules:",
                "",
                "- Member identity is derived data, not a source column.",
                "- Exact-name and honorific-normalized matches are resolved only against official Parliament authority sources.",
                "- Semicolon-delimited raw values are split before matching.",
                "- Office titles and generic headings remain unresolved or excluded.",
                "- Ambiguous and unresolved cases remain explicit.",
                "",
                "Known limitations:",
                "",
                "- The package is local-review-only.",
                "- The repo does not claim a published corpus-wide member identity release.",
                "- Full publication still requires broader validation and historical authority coverage.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "authority": authority_path.as_posix(),
        "review": review_path.as_posix(),
        "readme": readme_path.as_posix(),
    }


def main() -> int:
    outputs = build_package()
    print(f"Wrote {outputs['authority']}")
    print(f"Wrote {outputs['review']}")
    print(f"Wrote {outputs['readme']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
