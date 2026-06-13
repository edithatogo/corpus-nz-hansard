"""Validate the RDF linked-data sample endpoint package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:  # pragma: no cover - optional runtime dependency
    from pyshacl import validate  # type: ignore[import-unresolved]  # ty:ignore[unresolved-import]
except ImportError:  # pragma: no cover - fallback path is intentional
    validate = None

try:  # pragma: no cover - optional runtime dependency
    from rdflib import Graph
except ImportError:  # pragma: no cover - fallback path is intentional
    Graph = None  # type: ignore[assignment]  # ty:ignore[invalid-assignment]

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/rdf_linked_data_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/rdf_linked_data_model_metadata.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
TURTLE_PATH = ROOT / "samples/rdf-linked-data/linked-data.ttl"
JSONLD_PATH = ROOT / "samples/rdf-linked-data/linked-data.jsonld"
SHAPES_PATH = ROOT / "samples/rdf-linked-data/shapes.ttl"
SPARQL_PATH = ROOT / "samples/rdf-linked-data/sparql-queries.rq"
README_PATH = ROOT / "samples/rdf-linked-data/README.md"
MAPPING_DOC_PATH = ROOT / "docs/rdf-linked-data-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/rdf_linked_data_endpoint_20260609/evidence.md"

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


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        MODEL_METADATA_PATH,
        FIXTURE_PATH,
        TURTLE_PATH,
        JSONLD_PATH,
        SHAPES_PATH,
        SPARQL_PATH,
        README_PATH,
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
    model_metadata = _json(MODEL_METADATA_PATH)
    fixtures = _json(FIXTURE_PATH)
    component_ids = _component_ids(fixtures)

    if manifest["release_status"] != "sample-not-release":
        failures.append("RDF manifest must remain sample-not-release.")
    if manifest["release_level"] != "upstream-contribution":
        failures.append("RDF sample package must be upstream-contribution level.")
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("RDF dependency groups must match dependency extras policy.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append("RDF sample must not claim validated component metadata yet.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("RDF readiness boundary must remain blocked on validated components.")
    if manifest["validation_results"]["blocking_errors"] != 0:
        failures.append("RDF sample integrity check must have zero blocking errors.")
    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("RDF validation manifest output artifacts are incomplete.")

    if model_metadata["namespace"] != REQUIRED_NAMESPACE:
        failures.append("RDF model metadata must declare the planned namespace.")
    if model_metadata["comparison_status"] != "deferred-manual-fixture":
        failures.append("RDF model metadata must preserve the manual-fixture comparison status.")
    if set(model_metadata["prototype_tools"]) != {"rdflib", "pyshacl"}:
        failures.append("RDF model metadata must record rdflib and pyshacl as prototype tools.")
    traceability_ids = set(manifest["traceability"][0]["neutral_component_ids"])
    if not traceability_ids.issubset(component_ids):
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

    if Graph is not None:
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
    else:
        turtle_text = _read(TURTLE_PATH)
        jsonld_text = _read(JSONLD_PATH)
        shapes_text = _read(SHAPES_PATH)
        if "dcat:Dataset" not in turtle_text or "prov:Entity" not in turtle_text:
            failures.append("Turtle sample graph must declare the dataset and provenance types.")
        if "nzh:SpeechTurn" not in turtle_text or "skos:ConceptScheme" not in turtle_text:
            failures.append(
                "Turtle sample graph must declare speech-turn and concept-scheme resources."
            )
        if REQUIRED_NAMESPACE not in jsonld_text:
            failures.append("JSON-LD sample graph must stay within the planned namespace.")
        if (
            "sh:targetClass dcat:Dataset" not in shapes_text
            or "sh:targetClass nzh:SpeechTurn" not in shapes_text
        ):
            failures.append("SHACL shapes must cover the dataset and speech-turn resources.")

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

    required_terms = (
        "PROV-O",
        "DCAT",
        "SKOS",
        "sample-not-release",
        "blocked-pending-validated-components",
        "manifests/rdf_linked_data_validation_manifest.json",
        "manifests/rdf_linked_data_model_metadata.json",
        "samples/rdf-linked-data/linked-data.ttl",
        "samples/rdf-linked-data/linked-data.jsonld",
        "samples/rdf-linked-data/shapes.ttl",
        "samples/rdf-linked-data/sparql-queries.rq",
        "stanza",
        "spacy",
        "W3C Time",
    )
    for relative_path, text in {
        "docs/rdf-linked-data-mapping.md": _read(MAPPING_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "samples/rdf-linked-data/README.md": _read(README_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing RDF term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Namespace Policy",
        "Sample Graph",
        "SHACL Validation",
        "SPARQL Examples",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"RDF-LINKED-DATA: {failure}")
        return 1
    print("RDF linked-data sample endpoint is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
