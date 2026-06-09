"""Validate the ParlaMint-NZ sample endpoint package and readiness boundary."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/parlamint_nz_validation_manifest.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
SAMPLE_XML_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.sample.xml"
METADATA_XML_PATH = ROOT / "samples/parlamint-nz/ParlaMint-NZ.metadata.xml"
SAMPLE_README_PATH = ROOT / "samples/parlamint-nz/README.md"
MAPPING_DOC_PATH = ROOT / "docs/parlamint-nz-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/parlamint_nz_endpoint_20260609/evidence.md"
TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"

REQUIRED_DEPENDENCY_GROUPS = {"xml", "schema", "authority", "nlp"}
REQUIRED_OUTPUTS = {
    "samples/parlamint-nz/ParlaMint-NZ.sample.xml",
    "samples/parlamint-nz/ParlaMint-NZ.metadata.xml",
    "samples/parlamint-nz/README.md",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _component_ids(fixtures: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for rows in fixtures["components"].values():
        ids.update(row["component_id"] for row in rows)
    return ids


def _xml_id(element: ET.Element[str]) -> str | None:
    return element.attrib.get(f"{{{XML_NS}}}id")


def _strip_ref(value: str | None) -> str | None:
    if value is None:
        return None
    return value[1:] if value.startswith("#") else value


def _parse_xml(path: Path, failures: list[str]) -> ET.Element[str] | None:
    try:
        return ET.parse(path).getroot()
    except ET.ParseError as exc:
        failures.append(f"{path.relative_to(ROOT).as_posix()} is not well-formed XML: {exc}")
        return None


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        FIXTURE_PATH,
        SAMPLE_XML_PATH,
        METADATA_XML_PATH,
        SAMPLE_README_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
        DEPENDENCY_MANIFEST_PATH,
        RELEASE_LADDER_PATH,
        TRACK_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    fixtures = _json(FIXTURE_PATH)
    component_ids = _component_ids(fixtures)
    sample_root = _parse_xml(SAMPLE_XML_PATH, failures)
    metadata_root = _parse_xml(METADATA_XML_PATH, failures)
    if sample_root is None or metadata_root is None:
        return failures

    if sample_root.tag != f"{{{TEI_NS}}}TEI":
        failures.append("ParlaMint sample XML must use TEI root namespace.")
    if metadata_root.tag != f"{{{TEI_NS}}}teiCorpus":
        failures.append("ParlaMint metadata XML must use TEI corpus root namespace.")

    sample_ids = {
        _xml_id(element) for element in sample_root.iter() if _xml_id(element) is not None
    }
    fixture_refs: set[str] = set()
    for element in sample_root.iter():
        for attr in ("who", "corresp", "ref"):
            value = _strip_ref(element.attrib.get(attr))
            if value:
                fixture_refs.add(value)
    unresolved = {ref for ref in fixture_refs if ref not in component_ids}
    if unresolved:
        failures.append(f"ParlaMint sample has unresolved neutral references: {sorted(unresolved)}")

    required_trace_ids = set(manifest["traceability"][0]["neutral_component_ids"])
    if not required_trace_ids.issubset(component_ids):
        failures.append("ParlaMint traceability cites unknown neutral component IDs.")
    if not required_trace_ids.issubset(sample_ids | fixture_refs):
        failures.append("ParlaMint sample does not expose every traced neutral component ID.")

    if manifest["release_status"] != "sample-not-release":
        failures.append("ParlaMint manifest must remain sample-not-release.")
    if manifest["release_level"] != "upstream-contribution":
        failures.append("ParlaMint sample package must be upstream-contribution level.")
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("ParlaMint dependency groups must match dependency extras policy.")
    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("ParlaMint validation manifest output artifacts are incomplete.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append("ParlaMint sample must not claim validated component metadata yet.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("ParlaMint readiness boundary must remain blocked on validated components.")
    if manifest["validation_results"]["blocking_errors"] != 0:
        failures.append("ParlaMint sample integrity check must have zero blocking errors.")

    dependency_manifest = _json(DEPENDENCY_MANIFEST_PATH)
    parlamint_entry = next(
        item
        for item in dependency_manifest["endpoint_requirements"]
        if item["endpoint_track"] == "parlamint_nz_endpoint_20260609"
    )
    if set(parlamint_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Dependency extras policy and ParlaMint manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "ParlaMint-NZ sample package" not in artifacts:
        failures.append("Release ladder missing ParlaMint-NZ sample package mapping.")

    required_terms = (
        "ParlaMint-NZ",
        "sample-not-release",
        "manifests/parlamint_nz_validation_manifest.json",
        "samples/parlamint-nz/ParlaMint-NZ.sample.xml",
        "fixtures/neutral_components.json",
        "speaker_member_id",
        "party_id",
        "blocked-pending-validated-components",
        "member identity",
        "party attribution",
        "speech-turn validation",
    )
    for relative_path, text in {
        "docs/parlamint-nz-mapping.md": _read(MAPPING_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "samples/parlamint-nz/README.md": _read(SAMPLE_README_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing ParlaMint term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "TEI Mapping",
        "Sample Package",
        "Validation Manifest",
        "Readiness Boundary",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"PARLAMINT-NZ: {failure}")
        return 1
    print("ParlaMint-NZ sample endpoint is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
