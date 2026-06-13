"""Validate the RDF / Linked Data public endpoint release boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional runtime dependency
    from pyshacl import validate  # ty:ignore[unresolved-import]
except ImportError:  # pragma: no cover - fallback path is intentional
    validate = None

try:  # pragma: no cover - optional runtime dependency
    from rdflib import Graph
except ImportError:  # pragma: no cover - fallback path is intentional
    Graph = None  # ty:ignore[invalid-assignment]

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/rdf_linked_data_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/rdf_linked_data_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/rdf_linked_data_model_metadata.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
TURTLE_PATH = ROOT / "samples/rdf-linked-data/linked-data.ttl"
JSONLD_PATH = ROOT / "samples/rdf-linked-data/linked-data.jsonld"
SHAPES_PATH = ROOT / "samples/rdf-linked-data/shapes.ttl"
SPARQL_PATH = ROOT / "samples/rdf-linked-data/sparql-queries.rq"
README_PATH = ROOT / "samples/rdf-linked-data/README.md"
MAPPING_DOC_PATH = ROOT / "docs/rdf-linked-data-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/rdf-linked-data-public-endpoint-release.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/index.md"
SCHEMA_PATH = ROOT / "schemas/rdf_linked_data_public_endpoint_validation.schema.json"

REQUIRED_DEPENDENCY_GROUPS = {"authority", "metadata", "rdf", "schema"}
REQUIRED_OUTPUTS = {
    "samples/rdf-linked-data/linked-data.ttl",
    "samples/rdf-linked-data/linked-data.jsonld",
    "samples/rdf-linked-data/shapes.ttl",
    "samples/rdf-linked-data/sparql-queries.rq",
    "samples/rdf-linked-data/README.md",
}
REQUIRED_NAMESPACE = "https://w3id.org/nz-hansard/"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _validate_schema(manifest: dict[str, Any]) -> list[str]:
    schema = _json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    failures: list[str] = []
    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"{location}: {error.message}")
    return failures


def _component_ids(fixtures: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for rows in fixtures["components"].values():
        ids.update(row["component_id"] for row in rows)
    return ids


def _graph(path: Path, format_name: str, failures: list[str]) -> Graph | None:
    if Graph is None:
        return None
    graph = Graph()
    try:
        graph.parse(path, format=format_name)
    except Exception as exc:  # pragma: no cover - parse library behavior varies by backend
        failures.append(f"{path.relative_to(ROOT).as_posix()} failed RDF parsing: {exc}")
        return None
    return graph


def _doc_terms(path: Path, terms: tuple[str, ...]) -> list[str]:
    text = _read(path)
    return [
        f"{path.relative_to(ROOT).as_posix()} is missing: {term}"
        for term in terms
        if term not in text
    ]


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        SAMPLE_MANIFEST_PATH,
        MODEL_METADATA_PATH,
        FIXTURE_PATH,
        TURTLE_PATH,
        JSONLD_PATH,
        SHAPES_PATH,
        SPARQL_PATH,
        README_PATH,
        MAPPING_DOC_PATH,
        ENDPOINT_DOC_PATH,
        DOC_PATH,
        DEPENDENCY_MANIFEST_PATH,
        RELEASE_LADDER_PATH,
        TRACK_PATH,
        SCHEMA_PATH,
    ):
        if not path.exists():
            failures.append(f"{path.relative_to(ROOT).as_posix()} must exist.")
    if failures:
        return failures

    manifest = _json(MANIFEST_PATH)
    sample_manifest = _json(SAMPLE_MANIFEST_PATH)
    model_metadata = _json(MODEL_METADATA_PATH)
    fixtures = _json(FIXTURE_PATH)
    failures.extend(_validate_schema(manifest))

    if manifest["artifact_name"] != "RDF / Linked Data public endpoint release":
        failures.append("artifact_name must be RDF / Linked Data public endpoint release.")
    if manifest["release_level"] != "endpoint":
        failures.append("release_level must be endpoint.")
    if manifest["release_status"] != "blocked-pending-validated-components":
        failures.append("release_status must be blocked-pending-validated-components.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("readiness_status must remain blocked-pending-validated-components.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append("component_metadata_validated must remain false.")
    if manifest["public_claim"]["sample_only"] is not True:
        failures.append("public_claim.sample_only must be true.")
    if sample_manifest["release_status"] != "sample-not-release":
        failures.append("sample manifest must remain sample-not-release.")
    if (
        sample_manifest["validation_results"]["readiness_status"]
        != "blocked-pending-validated-components"
    ):
        failures.append("sample readiness must remain blocked-pending-validated-components.")
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("dependency groups must match authority/metadata/rdf/schema.")
    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("output artifacts must remain the sample package outputs.")
    if model_metadata["namespace"] != REQUIRED_NAMESPACE:
        failures.append("RDF model metadata must declare the planned namespace.")
    if model_metadata["comparison_status"] != "deferred-manual-fixture":
        failures.append("RDF model metadata must preserve the manual-fixture comparison status.")
    if set(model_metadata["prototype_tools"]) != {"rdflib", "pyshacl"}:
        failures.append("RDF model metadata must record rdflib and pyshacl as prototype tools.")

    component_ids = _component_ids(fixtures)
    if not set(manifest["traceability"][0]["neutral_component_ids"]).issubset(component_ids):
        failures.append("RDF traceability ids must be present in the neutral component fixtures.")

    dependency_manifest = _json(DEPENDENCY_MANIFEST_PATH)
    rdf_entry = next(
        item
        for item in dependency_manifest["endpoint_requirements"]
        if item["endpoint_track"] == "rdf_linked_data_endpoint_20260609"
    )
    if set(rdf_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Dependency extras policy and RDF manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "RDF / Linked Data sample package" not in artifacts:
        failures.append("Release ladder missing RDF / Linked Data sample package mapping.")

    turtle_graph = _graph(TURTLE_PATH, "turtle", failures)
    jsonld_graph = _graph(JSONLD_PATH, "json-ld", failures)
    shapes_graph = _graph(SHAPES_PATH, "turtle", failures)
    if failures:
        return failures

    assert turtle_graph is not None and jsonld_graph is not None and shapes_graph is not None
    if len(turtle_graph) == 0:
        failures.append("Turtle sample graph must not be empty.")
    if len(jsonld_graph) == 0:
        failures.append("JSON-LD sample graph must not be empty.")
    if len(shapes_graph) == 0:
        failures.append("SHACL shape graph must not be empty.")
    if set(turtle_graph) != set(jsonld_graph):
        failures.append("Turtle and JSON-LD samples must describe the same RDF graph.")

    if validate is None:
        if "sh:targetClass dcat:Dataset" not in _read(SHAPES_PATH):
            failures.append(
                "SHACL fallback checks require dataset target classes in the shapes graph."
            )
        if "sh:targetClass nzh:SpeechTurn" not in _read(SHAPES_PATH):
            failures.append(
                "SHACL fallback checks require speech-turn target classes in the shapes graph."
            )
        if "sh:path prov:wasDerivedFrom" not in _read(SHAPES_PATH):
            failures.append(
                "SHACL fallback checks require provenance path coverage in the shapes graph."
            )
    else:
        conforms, results_graph, results_text = validate(
            data_graph=turtle_graph,
            shacl_graph=shapes_graph,
            inference="rdfs",
            abort_on_first=False,
            allow_infos=False,
            allow_warnings=False,
            meta_shacl=False,
        )
        if not conforms:
            failures.append("RDF sample does not conform to the SHACL shapes.")
        if results_graph is None or len(results_graph) == 0:
            failures.append("SHACL validation must return a results graph.")
        if "Validation Report" not in results_text:
            failures.append("SHACL validation output must include a validation report.")

    for uri in (
        "https://w3id.org/nz-hansard/sample/rdf-linked-data-sample",
        "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000005",
        "https://w3id.org/nz-hansard/component/nzhc-component-0000000000000009",
    ):
        if (uri not in _read(TURTLE_PATH)) and (uri not in _read(JSONLD_PATH)):
            failures.append(f"RDF sample missing expected URI: {uri}")

    if REQUIRED_NAMESPACE not in _read(TURTLE_PATH):
        failures.append("RDF Turtle sample must stay within the planned namespace.")
    if REQUIRED_NAMESPACE not in _read(JSONLD_PATH):
        failures.append("RDF JSON-LD sample must stay within the planned namespace.")

    for relative_path, terms in {
        "docs/rdf-linked-data-public-endpoint-release.md": (
            "sample-only",
            "validated component exports",
            "stable URI review",
            "public endpoint release",
        ),
        "conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/index.md": (
            "sample-only",
            "validated component exports",
            "stable URI review",
        ),
        "docs/rdf-linked-data-mapping.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "PROV-O",
            "DCAT",
            "SKOS",
            "W3C Time",
        ),
        "docs/endpoint-contracts.md": (
            "RDF / Linked Data",
            "sample-not-release",
            "manifests/rdf_linked_data_validation_manifest.json",
            "manifests/rdf_linked_data_model_metadata.json",
        ),
        "samples/rdf-linked-data/README.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "RDF Linked Data",
        ),
    }.items():
        failures.extend(_doc_terms(ROOT / relative_path, terms))

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"RDF-LINKED-DATA-PUBLIC: {failure}")
        return 1
    print("RDF linked-data public endpoint release boundary is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
