"""Validate the Universal Dependencies / CoNLL-U sample endpoint package."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "manifests/ud_conllu_validation_manifest.json"
MODEL_METADATA_PATH = ROOT / "manifests/ud_conllu_model_metadata.json"
FIXTURE_PATH = ROOT / "fixtures/neutral_components.json"
GOLD_PATH = ROOT / "fixtures/gold_evaluation_samples.json"
CONLLU_PATH = ROOT / "samples/ud-conllu/parliament_sample.conllu"
ALIGNMENT_PATH = ROOT / "samples/ud-conllu/parliament_sample.alignments.json"
README_PATH = ROOT / "samples/ud-conllu/README.md"
MAPPING_DOC_PATH = ROOT / "docs/ud-conllu-mapping.md"
ENDPOINT_DOC_PATH = ROOT / "docs/endpoint-contracts.md"
DEPENDENCY_MANIFEST_PATH = ROOT / "manifests/dependency_extras_policy.json"
RELEASE_LADDER_PATH = ROOT / "manifests/release_ladder.json"
TRACK_PATH = ROOT / "conductor/tracks/ud_conllu_endpoint_20260609/evidence.md"

REQUIRED_DEPENDENCY_GROUPS = {"nlp", "schema"}
REQUIRED_OUTPUTS = {
    "samples/ud-conllu/parliament_sample.conllu",
    "samples/ud-conllu/parliament_sample.alignments.json",
    "samples/ud-conllu/README.md",
}
REQUIRED_ML_TOOLS = {"stanza", "spacy"}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _json(path: Path) -> dict[str, Any]:
    return json.loads(_read(path))


def _component_ids(fixtures: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for rows in fixtures["components"].values():
        ids.update(row["component_id"] for row in rows)
    return ids


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


def _failures() -> list[str]:
    failures: list[str] = []
    for path in (
        MANIFEST_PATH,
        MODEL_METADATA_PATH,
        FIXTURE_PATH,
        GOLD_PATH,
        CONLLU_PATH,
        ALIGNMENT_PATH,
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
    gold = _json(GOLD_PATH)
    conllu_rows = _parse_conllu(CONLLU_PATH, failures)
    alignment = _json(ALIGNMENT_PATH)
    if failures:
        return failures

    if manifest["release_status"] != "sample-not-release":
        failures.append("UD manifest must remain sample-not-release.")
    if manifest["release_level"] != "upstream-contribution":
        failures.append("UD sample package must be upstream-contribution level.")
    if set(manifest["dependency_groups"]) != REQUIRED_DEPENDENCY_GROUPS:
        failures.append("UD dependency groups must match dependency extras policy.")
    if manifest["validation_results"]["component_metadata_validated"]:
        failures.append("UD sample must not claim validated component metadata yet.")
    if manifest["validation_results"]["readiness_status"] != "blocked-pending-validated-components":
        failures.append("UD readiness boundary must remain blocked on validated components.")
    if manifest["validation_results"]["blocking_errors"] != 0:
        failures.append("UD sample integrity check must have zero blocking errors.")

    if set(manifest["output_artifacts"]) != REQUIRED_OUTPUTS:
        failures.append("UD validation manifest output artifacts are incomplete.")

    if model_metadata["annotation_family"] != "Universal Dependencies / CoNLL-U":
        failures.append("UD model metadata must declare the annotation family.")
    if model_metadata["language"] != "en":
        failures.append("UD model metadata must declare English language.")
    if model_metadata["default_pipeline"] != "manual-fixture":
        failures.append("UD model metadata must preserve the manual-fixture default.")
    if set(model_metadata["prototype_tools"]) != REQUIRED_ML_TOOLS:
        failures.append("UD model metadata must record both stanza and spacy prototype tools.")

    component_ids = _component_ids(fixtures)
    expected_ids = {
        "nzhc-component-0000000000000001",
        "nzhc-component-0000000000000002",
        "nzhc-component-0000000000000005",
    }
    if not expected_ids.issubset(component_ids):
        failures.append("UD sample references unknown neutral component IDs.")
    trace_ids = set(manifest["traceability"][0]["neutral_component_ids"])
    if not trace_ids.issubset(component_ids):
        failures.append("UD traceability cites unknown neutral component IDs.")

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
        misc = conllu_token["misc"]
        expected_misc = f"StartChar={start}|EndChar={end}"
        if expected_misc not in misc:
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

    required_terms = (
        "Universal Dependencies",
        "CoNLL-U",
        "sample-not-release",
        "blocked-pending-validated-components",
        "manifests/ud_conllu_validation_manifest.json",
        "manifests/ud_conllu_model_metadata.json",
        "parliament_sample.conllu",
        "parliament_sample.alignments.json",
        "source offsets",
        "stanza",
        "spacy",
    )
    for relative_path, text in {
        "docs/ud-conllu-mapping.md": _read(MAPPING_DOC_PATH),
        "docs/endpoint-contracts.md": _read(ENDPOINT_DOC_PATH),
        "samples/ud-conllu/README.md": _read(README_PATH),
    }.items():
        for term in required_terms:
            if term not in text:
                failures.append(f"{relative_path} is missing UD term: {term}")

    track_text = _read(TRACK_PATH)
    for required in (
        "Annotation Units",
        "Model Metadata",
        "CoNLL-U Validation",
        "Source-Offset Alignment",
    ):
        if required not in track_text:
            failures.append(f"{TRACK_PATH.relative_to(ROOT).as_posix()} is missing: {required}")

    return failures


def main() -> int:
    failures = _failures()
    if failures:
        for failure in failures:
            print(f"UD-CONLLU: {failure}")
        return 1
    print("Universal Dependencies / CoNLL-U sample endpoint is consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
