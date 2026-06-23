"""Validate the member identity triangulation track evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "member_identity_triangulation_20260612"
TRACK_DIR = ROOT / "conductor" / "tracks" / TRACK_ID
REGISTRY_PATH = ROOT / "derived" / "member_registry.json"
TRACKS_INDEX_PATH = ROOT / "conductor" / "tracks.md"

EXPECTED_TOTAL = 51
EXPECTED_RESOLVED = 51
EXPECTED_SOURCE_COUNTS = {
    "Wikipedia 54th Parliament": "41 | 80.4%",
    "Wikipedia 47th-53rd (manual)": "5 | 9.8%",
    "Wikidata SPARQL": "4 | 7.8%",
    "Bills API cross-reference": "1 | 2.0%",
}
EXPECTED_MAPPINGS = {
    "Laura Trask": {
        "canonical_name": "Laura McClure",
        "party": "ACT",
        "confidence": "medium",
        "source_fragments": ("Bills API", "Hansard Context"),
    },
    "Brent Hudson": {
        "canonical_name": "Brett Hudson",
        "party": "National",
        "confidence": "high",
        "source_fragments": ("Wikipedia", "Bills API", "Wikidata", "Triangulated Authority"),
    },
    "Anahila Kanongata'a": {
        "canonical_name": "Anahila Kanongata'a-Suisuiki",
        "party": "Labour",
        "confidence": "high",
        "source_fragments": ("Wikipedia", "Bills API", "Wikidata", "Triangulated Authority"),
    },
    "Richard Posser": {
        "canonical_name": "Richard Prosser",
        "party": "NZ First",
        "confidence": "high",
        "source_fragments": ("Wikipedia", "Wikidata", "Triangulated Authority"),
    },
}
REQUIRED_MEMBER_FIELDS = (
    "hansard_name",
    "canonical_name",
    "party",
    "parliament_numbers",
    "sources_used",
    "confidence",
    "resolved",
)


def _read(relative_path: str | Path) -> str:
    path = relative_path if isinstance(relative_path, Path) else ROOT / relative_path
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _failures() -> list[str]:
    failures: list[str] = []
    required_paths = (
        REGISTRY_PATH,
        TRACK_DIR / "plan.md",
        TRACK_DIR / "evidence.md",
        TRACK_DIR / "metadata.json",
        TRACK_DIR / "index.md",
        TRACKS_INDEX_PATH,
    )
    for path in required_paths:
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    registry = _json(REGISTRY_PATH)
    members = registry.get("members", {})
    if registry.get("total_members") != EXPECTED_TOTAL:
        failures.append(f"member_registry total_members must be {EXPECTED_TOTAL}.")
    if registry.get("resolved") != EXPECTED_RESOLVED:
        failures.append(f"member_registry resolved must be {EXPECTED_RESOLVED}.")
    if registry.get("unresolved") != 0:
        failures.append("member_registry unresolved must be 0.")
    if registry.get("resolution_rate_pct") != 100.0:
        failures.append("member_registry resolution_rate_pct must be 100.0.")
    if len(members) != EXPECTED_TOTAL:
        failures.append(f"member_registry members must contain {EXPECTED_TOTAL} entries.")

    source_text = "\\n".join(registry.get("sources_integrated", []))
    for required in (
        "unmatched_final_resolution.json (50/51 resolved)",
        "wikidata_nz_mps.json (1,514 records)",
        "bills_members API (351 unique members)",
        "triangulated_member_authority.json",
        "parliament_current_mps.json",
        "Hansard corpus (193,922 rows)",
    ):
        if required not in source_text:
            failures.append(f"member_registry sources_integrated is missing {required}.")

    for name, row in members.items():
        if not isinstance(row, dict):
            failures.append(f"member_registry row {name!r} must be an object.")
            continue
        for field in REQUIRED_MEMBER_FIELDS:
            if field not in row:
                failures.append(f"member_registry row {name!r} is missing {field}.")
        if row.get("hansard_name") != name:
            failures.append(f"member_registry row key {name!r} must match hansard_name.")
        if row.get("resolved") is not True:
            failures.append(f"member_registry row {name!r} must be resolved.")
        if row.get("confidence") not in {"high", "medium"}:
            failures.append(f"member_registry row {name!r} has unsupported confidence.")
        if not row.get("canonical_name"):
            failures.append(f"member_registry row {name!r} must have canonical_name.")
        if not row.get("sources_used"):
            failures.append(f"member_registry row {name!r} must have sources_used.")

    for hansard_name, expected in EXPECTED_MAPPINGS.items():
        row = members.get(hansard_name)
        if not row:
            failures.append(f"member_registry must include {hansard_name}.")
            continue
        for field in ("canonical_name", "party", "confidence"):
            if row.get(field) != expected[field]:
                failures.append(
                    f"{hansard_name} {field} must be {expected[field]!r}; found {row.get(field)!r}."
                )
        sources = "\\n".join(row.get("sources_used", []))
        for fragment in expected["source_fragments"]:
            if fragment not in sources:
                failures.append(f"{hansard_name} sources_used must include {fragment}.")

    metadata = _json(TRACK_DIR / "metadata.json")
    if metadata.get("status") != "complete":
        failures.append("member identity triangulation metadata status must be complete.")

    plan = _read(TRACK_DIR / "plan.md")
    if "- [ ]" in plan or "- [~]" in plan:
        failures.append("member identity triangulation plan must not contain open tasks.")
    for required in (
        "Cross-reference Bills API member sponsors",
        "Integrate resolutions into consolidated member registry",
        "Add automated triangulation evidence checker",
    ):
        if required not in plan:
            failures.append(f"member identity triangulation plan is missing: {required}")

    evidence = _read(TRACK_DIR / "evidence.md")
    for required in (
        "Final Resolution Rate: 51/51 (100.0%)",
        "Laura Trask -> Laura McClure",
        "Bills API cross-reference | 1 | 2.0%",
        "derived/member_registry.json",
        "scripts/check_member_identity_triangulation.py",
    ):
        if required not in evidence:
            failures.append(f"member identity triangulation evidence is missing: {required}")
    for source, count_text in EXPECTED_SOURCE_COUNTS.items():
        if source not in evidence or count_text not in evidence:
            failures.append(
                f"member identity triangulation evidence source count is missing: {source}"
            )

    index = _read(TRACK_DIR / "index.md")
    for required in (
        "Bills API member sponsors - integrated",
        "HathiTrust historical volumes - blocked/not required",
        "Total: 51 unmatched names",
        "Resolved: 51 (100.0%)",
        "Remaining: 0",
        "Laura Trask -> Laura McClure",
    ):
        if required not in index:
            failures.append(f"member identity triangulation index is missing: {required}")

    tracks_index = _read(TRACKS_INDEX_PATH)
    if (
        "### [x] Track: Member Identity Triangulation" not in tracks_index
        or TRACK_ID not in tracks_index
    ):
        failures.append("tracks.md must mark Member Identity Triangulation complete.")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"MEMBER-IDENTITY-TRIANGULATION: {failure}")
        return 1
    print("Member identity triangulation evidence is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
