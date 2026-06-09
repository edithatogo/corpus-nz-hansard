"""Validate authority-source discovery manifest and downstream gates."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/authority_sources.json"
SCHEMA_PATH = ROOT / "schemas/authority_sources.schema.json"
DOC_PATH = ROOT / "docs/authority-source-discovery.md"
TRACK_PATH = ROOT / "conductor/tracks/authority_source_discovery_20260609/evidence.md"

REQUIRED_DOMAINS = {
    "members",
    "parties",
    "offices",
    "sittings",
    "bills",
    "motions",
    "votes",
    "procedure",
}
REQUIRED_DOWNSTREAM_TRACKS = {
    "member_identity_resolution_20260609",
    "party_attribution_provenance_20260609",
    "neutral_component_model_20260609",
    "nz_parliamentary_procedure_model_20260609",
    "popolo_opencivicdata_endpoint_20260609",
    "akoma_ntoso_endpoint_20260609",
    "derived_fields_validation_manifests_20260609",
    "historical_coverage_audit_20260609",
}
OFFICIAL_PUBLISHER = "New Zealand Parliament"


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

    domains = set(manifest["domains"])
    if domains != REQUIRED_DOMAINS:
        failures.append(
            "authority domains must include exactly: " + ", ".join(sorted(REQUIRED_DOMAINS))
        )

    sources = {source["id"]: source for source in manifest["sources"]}
    for source in sources.values():
        unknown_domains = set(source["domains"]) - REQUIRED_DOMAINS
        if unknown_domains:
            failures.append(
                f"{source['id']} uses unknown domains: {', '.join(sorted(unknown_domains))}"
            )
        if (
            source["classification"] == "authoritative"
            and source["publisher"] != OFFICIAL_PUBLISHER
        ):
            failures.append(
                f"{source['id']} is authoritative but not an official Parliament source."
            )
        if source["classification"] == "rejected" and source["downstream_tracks"]:
            failures.append(f"{source['id']} is rejected but still unblocks downstream tracks.")
        if len(source["source_hash"]) != 64:
            failures.append(f"{source['id']} source_hash must be a SHA-256 hex string.")

    domain_coverage = manifest["domain_coverage"]
    if set(domain_coverage) != REQUIRED_DOMAINS:
        failures.append("domain_coverage must cover every authority domain.")
    for domain, coverage in domain_coverage.items():
        for source_id in coverage["primary_source_ids"]:
            if source_id not in sources:
                failures.append(f"{domain} references missing source id: {source_id}")
            elif domain not in sources[source_id]["domains"]:
                failures.append(f"{domain} references source without matching domain: {source_id}")
        if coverage["downstream_track"] not in REQUIRED_DOWNSTREAM_TRACKS:
            failures.append(
                f"{domain} downstream track is not recognised: {coverage['downstream_track']}"
            )

    downstream_tracks = {
        track for source in sources.values() for track in source.get("downstream_tracks", [])
    }
    missing_tracks = REQUIRED_DOWNSTREAM_TRACKS - downstream_tracks
    if missing_tracks:
        failures.append(
            "downstream tracks missing from source inventory: " + ", ".join(sorted(missing_tracks))
        )

    for domain in REQUIRED_DOMAINS:
        domain_sources = [source for source in sources.values() if domain in source["domains"]]
        if not any(
            source["classification"] in {"authoritative", "supporting", "candidate"}
            for source in domain_sources
        ):
            failures.append(f"{domain} has no candidate-or-better source.")
        if not any(source["publisher"] == OFFICIAL_PUBLISHER for source in domain_sources):
            failures.append(f"{domain} has no official Parliament source.")

    doc = _read(DOC_PATH)
    track = _read(TRACK_PATH)
    for required in (
        "Text-derived inference is not an authority source",
        "Official New Zealand Parliament sources come first",
        "member_identity_resolution_20260609",
        "party_attribution_provenance_20260609",
        "historical_coverage_audit_20260609",
    ):
        if required not in doc:
            failures.append(f"{DOC_PATH.relative_to(ROOT).as_posix()} is missing: {required}")
    for required in (
        "Authority Inventory",
        "Retrieval And Hashing",
        "Reuse And Coverage",
        "Downstream Unblockers",
        "Focused Validation",
    ):
        if required not in track:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"AUTHORITY-SOURCES: {failure}")
        return 1
    print("Authority source discovery manifest is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
