"""Validate the UD / CoNLL-U public endpoint release boundary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/ud_conllu_public_endpoint_validation.json"
SAMPLE_MANIFEST_PATH = ROOT / "manifests/ud_conllu_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/ud_conllu_model_metadata.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
CONLLU_PATH = ROOT / "samples/ud-conllu/parliament_sample.conllu"
ALIGNMENT_PATH = ROOT / "samples/ud-conllu/parliament_sample.alignments.json"
README_PATH = ROOT / "samples/ud-conllu/README.md"
MAPPING_DOC_PATH = ROOT / "docs/ud-conllu-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DOC_PATH = ROOT / "docs/ud-conllu-public-endpoint-release.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/ud_conllu_public_endpoint_release_20260610/index.md"
SCHEMA_PATH = ROOT / "schemas/ud_conllu_public_endpoint_validation.schema.json"

REQUIRED_DEPENDENCY_GROUPS = {"nlp", "schema"}
REQUIRED_OUTPUTS = {
    "samples/ud-conllu/parliament_sample.conllu",
    "samples/ud-conllu/parliament_sample.alignments.json",
    "samples/ud-conllu/README.md",
}


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


def _parse_conllu(path: Path, failures: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(_read(path).splitlines(), start=1):
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 10:
            failures.append(
                f"{path.relative_to(ROOT).as_posix()} line {line_number} must have 10 tab-separated columns."
            )
            continue
        token_id = parts[0]
        if "-" in token_id or "." in token_id:
            failures.append(
                f"{path.relative_to(ROOT).as_posix()} line {line_number} uses unsupported token id {token_id}."
            )
            continue
        try:
            token_int = int(token_id)
            head = int(parts[6])
        except ValueError:
            failures.append(
                f"{path.relative_to(ROOT).as_posix()} line {line_number} must use integer token and head IDs."
            )
            continue
        rows.append(
            {
                "id": token_int,
                "form": parts[1],
                "lemma": parts[2],
                "upos": parts[3],
                "xpos": parts[4],
                "feats": parts[5],
                "head": head,
                "deprel": parts[7],
                "deps": parts[8],
                "misc": parts[9],
            }
        )
    return rows


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
        GOLD_PATH,
        CONLLU_PATH,
        ALIGNMENT_PATH,
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
    gold = _json(GOLD_PATH)
    conllu_rows = _parse_conllu(CONLLU_PATH, failures)
    alignment = _json(ALIGNMENT_PATH)
    if failures:
        return failures

    failures.extend(_validate_schema(manifest))

    if manifest["artifact_name"] != "UD / CoNLL-U public endpoint release":
        failures.append("artifact_name must be UD / CoNLL-U public endpoint release.")
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
        failures.append("dependency groups must match nlp/schema.")
    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("output artifacts must remain the sample package outputs.")

    if model_metadata["annotation_family"] != "Universal Dependencies / CoNLL-U":
        failures.append("UD model metadata must declare the annotation family.")
    if model_metadata["language"] != "en":
        failures.append("UD model metadata must declare English language.")
    if model_metadata["default_pipeline"] != "manual-fixture":
        failures.append("UD model metadata must preserve the manual-fixture default.")
    if set(model_metadata["prototype_tools"]) != {"stanza", "spacy"}:
        failures.append("UD model metadata must record both stanza and spacy prototype tools.")

    if alignment["source_text"] != "This bill is set down for committee stage immediately.":
        failures.append("UD alignment manifest must preserve the source text.")
    if alignment["target_text_unit"] != "speech_turn":
        failures.append("UD alignment manifest must target speech_turn text.")
    if len(alignment["tokens"]) != len(conllu_rows):
        failures.append("UD alignment token count must match the CoNLL-U sample.")

    for alignment_token, conllu_token in zip(alignment["tokens"], conllu_rows, strict=True):
        if alignment_token["id"] != conllu_token["id"]:
            failures.append("UD alignment token IDs must match the CoNLL-U sample.")
        if alignment_token["form"] != conllu_token["form"]:
            failures.append("UD alignment token forms must match the CoNLL-U sample.")
        start = alignment_token["start_offset"]
        end = alignment_token["end_offset"]
        if alignment["source_text"][start:end] != alignment_token["form"]:
            failures.append(f"UD token {alignment_token['id']} does not match source offsets.")
        expected_misc = f"StartChar={start}|EndChar={end}"
        if expected_misc not in conllu_token["misc"]:
            failures.append(f"UD token {alignment_token['id']} must preserve char offsets.")

    if not any(token["deprel"] == "root" for token in conllu_rows):
        failures.append("UD sample must contain a root token.")
    if conllu_rows[0]["form"] != "This" or conllu_rows[-1]["form"] != ".":
        failures.append("UD sample must preserve the expected token order.")

    gold_domain = {
        sample["example_class"] for sample in gold["samples"] if sample["domain"] == "topic_coding"
    }
    if gold_domain != {"positive", "negative", "ambiguous", "unresolved", "excluded"}:
        failures.append(
            "UD checker expects the gold evaluation manifest to retain all topic-coding classes."
        )

    component_ids = {
        row["component_id"] for rows in fixtures["components"].values() for row in rows
    }
    if manifest["traceability"][0]["neutral_component_ids"][0] not in component_ids:
        failures.append("UD traceability cites unknown neutral component IDs.")

    dependency_manifest = _json(DEPENDENCY_MANIFEST_PATH)
    ud_entry = next(
        item
        for item in dependency_manifest["endpoint_requirements"]
        if item["endpoint_track"] == "ud_conllu_endpoint_20260609"
    )
    if set(ud_entry["required_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("Dependency extras policy and UD manifest disagree.")

    release_ladder = _json(RELEASE_LADDER_PATH)
    artifacts = {item["artifact"]: item for item in release_ladder["artifact_map"]}
    if "UD / CoNLL-U sample package" not in artifacts:
        failures.append("Release ladder missing UD / CoNLL-U sample package mapping.")

    for relative_path, terms in {
        "docs/ud-conllu-public-endpoint-release.md": (
            "sample-only",
            "validated speech-turn text",
            "Stanza/spaCy",
            "public endpoint release",
        ),
        "conductor/tracks/ud_conllu_public_endpoint_release_20260610/index.md": (
            "sample-only",
            "validated speech-turn text",
            "Stanza/spaCy",
        ),
        "docs/ud-conllu-mapping.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "source offsets",
        ),
        "docs/endpoint-contracts.md": (
            "Universal Dependencies / CoNLL-U",
            "sample-not-release",
            "manifests/ud_conllu_validation_manifest.json",
            "manifests/ud_conllu_model_metadata.json",
        ),
        "samples/ud-conllu/README.md": (
            "sample-not-release",
            "blocked-pending-validated-components",
            "Universal Dependencies / CoNLL-U",
        ),
    }.items():
        failures.extend(_doc_terms(ROOT / relative_path, terms))

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"UD-CONLLU-PUBLIC: {failure}")
        return 1
    print("UD / CoNLL-U public endpoint release boundary is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
