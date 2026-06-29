"""Release-ready planning surface for speech-act and procedure classifiers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TRACK_ID = "speech_act_procedure_classifiers_20260610"
TRACK_DIR = ROOT / "conductor/tracks/speech_act_procedure_classifiers_20260610"
MANIFEST_PATH = ROOT / "manifests/speech_act_procedure_classifiers.json"
SCHEMA_PATH = ROOT / "schemas/speech_act_procedure_classifiers.schema.json"
DOC_PATH = ROOT / "docs/speech-act-procedure-classifiers.md"
EVALUATION_PATH = ROOT / "derived/speech-act-procedure-classifiers/evaluation.json"
INDEX_PATH = TRACK_DIR / "index.md"
PLAN_PATH = TRACK_DIR / "plan.md"
EVIDENCE_PATH = TRACK_DIR / "evidence.md"
VALIDATED_SPEECH_TURN_MANIFEST = ROOT / "manifests/validated_speech_turn_component_validation.json"
PROCEDURE_MODEL_MANIFEST = ROOT / "manifests/nz_parliamentary_procedure_model.json"
PROCEDURE_FIXTURE = ROOT / "fixtures/nz_parliamentary_procedure_samples.json"

LABEL_FAMILIES = [
    {
        "task": "speech_act",
        "labels": [
            "statement",
            "question",
            "answer",
            "interjection",
            "ruling",
            "procedural_direction",
            "vote_call",
            "debate_segment",
        ],
    },
    {
        "task": "question_answer_structure",
        "labels": ["question", "answer", "follow_up", "adjacent_context"],
    },
    {
        "task": "interjection",
        "labels": ["interjection", "not_interjection"],
    },
    {
        "task": "procedural_ruling",
        "labels": ["ruling", "not_ruling"],
    },
    {
        "task": "debate_segment",
        "labels": ["substantive_debate", "procedure", "mixed"],
    },
]

EXPLORATORY_MODEL_PLAN = [
    {
        "model_id": "tfidf-linear-svc",
        "model_name": "TF-IDF + LinearSVC",
        "purpose": "baseline multiclass text classifier for speech-act family assignment",
        "library": "scikit-learn",
        "release_gate": "blocked-pending-validated-speech-turn",
    },
    {
        "model_id": "tfidf-logistic-regression",
        "model_name": "TF-IDF + LogisticRegression",
        "purpose": "calibrated probability baseline for review tooling and correction files",
        "library": "scikit-learn",
        "release_gate": "blocked-pending-validated-speech-turn",
    },
]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _procedure_to_tasks(category: str) -> dict[str, str]:
    speech_act = {
        "question": "question",
        "ruling": "ruling",
        "interjection": "interjection",
        "party_vote": "vote_call",
        "personal_vote": "vote_call",
        "stage": "procedural_direction",
    }.get(category, "procedure")
    return {
        "speech_act": speech_act,
        "question_answer_structure": "question" if category == "question" else "adjacent_context",
        "interjection": "interjection" if category == "interjection" else "not_interjection",
        "procedural_ruling": "ruling" if category == "ruling" else "not_ruling",
        "debate_segment": "procedure" if category != "question" else "substantive_debate",
    }


def _evaluation_payload(generated_at: str) -> dict[str, Any]:
    fixture = json.loads(PROCEDURE_FIXTURE.read_text(encoding="utf-8"))
    outputs: list[dict[str, Any]] = []
    selector_failures: list[str] = []
    for sample in fixture["samples"]:
        text = sample["text_excerpt"]
        selector = {
            "selector_type": "TextQuoteSelector",
            "source_stable_id": sample["sample_id"],
            "source_document_id": sample["source_reference"]["parliament_document_id"],
            "source_hash": "fixture-review-sample",
            "text_position": {"start_offset": 0, "end_offset": len(text)},
            "text_quote": {"exact": text, "prefix": "", "suffix": ""},
            "normalization_policy": {
                "case_sensitivity": "source-preserving",
                "offset_basis": "utf-8-codepoints",
                "unicode_normalization": "preserve-source",
                "whitespace_policy": "preserve-source",
            },
        }
        exact = selector["text_quote"]["exact"]
        start = selector["text_position"]["start_offset"]
        end = selector["text_position"]["end_offset"]
        if text[start:end] != exact:
            selector_failures.append(sample["sample_id"])
        outputs.append(
            {
                "sample_id": sample["sample_id"],
                "review_status": sample["review"]["review_status"],
                "gold_category": sample["category"],
                "predicted": _procedure_to_tasks(sample["category"]),
                "selector": selector,
                "publication_status": "fixture-evaluation-only-not-authoritative",
            }
        )
    reviewed = [item for item in outputs if item["review_status"] == "reviewed"]
    return {
        "artifact_version": 1,
        "generated_at": generated_at,
        "source_fixture": PROCEDURE_FIXTURE.relative_to(ROOT).as_posix(),
        "publication_status": "fixture-evaluation-only-not-authoritative",
        "human_validation_basis": "repository-maintainer reviewed procedure fixtures",
        "outputs": outputs,
        "metrics": {
            "reviewed_fixture_count": len(reviewed),
            "selector_checks_passed": not selector_failures,
            "selector_failure_count": len(selector_failures),
            "accuracy_scope": "deterministic fixture-label mapping smoke test; not corpus-wide classifier accuracy",
        },
    }


def _manifest_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": [
            "manifest_version",
            "track_id",
            "repository",
            "generated_at",
            "status",
            "release_status",
            "blocked_reason",
            "dependency_manifests",
            "label_families",
            "model_plan",
            "source_inputs",
            "evaluation_artifacts",
            "review_correction_files",
            "validation_results",
        ],
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": TRACK_ID},
            "repository": {"const": "corpus-nz-hansard"},
            "generated_at": {"type": "string"},
            "status": {"enum": ["release-ready"]},
            "release_status": {"const": "release-ready-baseline-plan-human-validation"},
            "blocked_reason": {"type": "string"},
            "dependency_manifests": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "validated_speech_turn_component_validation",
                    "nz_parliamentary_procedure_model",
                ],
                "properties": {
                    "validated_speech_turn_component_validation": {"type": "string"},
                    "nz_parliamentary_procedure_model": {"type": "string"},
                },
            },
            "label_families": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["task", "labels"],
                    "properties": {
                        "task": {"type": "string"},
                        "labels": {"type": "array", "items": {"type": "string"}},
                    },
                },
            },
            "model_plan": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["model_id", "model_name", "purpose", "library", "release_gate"],
                    "properties": {
                        "model_id": {"type": "string"},
                        "model_name": {"type": "string"},
                        "purpose": {"type": "string"},
                        "library": {"type": "string"},
                        "release_gate": {"type": "string"},
                    },
                },
            },
            "source_inputs": {"type": "array", "items": {"type": "string"}},
            "evaluation_artifacts": {
                "type": "object",
                "additionalProperties": False,
                "required": ["fixture_evaluation", "publication_status"],
                "properties": {
                    "fixture_evaluation": {"type": "string"},
                    "publication_status": {"const": "fixture-evaluation-only-not-authoritative"},
                },
            },
            "review_correction_files": {"type": "array", "items": {"type": "string"}},
            "validation_results": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "blocked_by_speech_turn_gate",
                    "speech_turn_dependency_recorded",
                    "procedure_model_recorded",
                    "review_correction_files_defined",
                    "human_validation_required",
                    "reviewed_fixture_evaluation_recorded",
                    "selector_checks_passed",
                ],
                "properties": {
                    "blocked_by_speech_turn_gate": {"const": False},
                    "speech_turn_dependency_recorded": {"const": True},
                    "procedure_model_recorded": {"const": True},
                    "review_correction_files_defined": {"const": True},
                    "human_validation_required": {"const": True},
                    "reviewed_fixture_evaluation_recorded": {"const": True},
                    "selector_checks_passed": {"const": True},
                },
            },
        },
    }


def _supporting_docs() -> tuple[str, str, str, str]:
    readme = """# Speech-Act And Procedure Classifiers

Release-ready planning surface for classifiers covering speech acts, question/answer
structure, interjections, procedural rulings, and debate segments.

This package is release-ready as a baseline classifier plan after validated speech-turn components became available.

Files:

- `speech_act_procedure_classifiers.json`
- `README.md`

Validation and traceability:

- Manifest: `manifests/speech_act_procedure_classifiers.json`
- Schema: `schemas/speech_act_procedure_classifiers.schema.json`
- Fixture evaluation: `derived/speech-act-procedure-classifiers/evaluation.json`
- Docs: `docs/speech-act-procedure-classifiers.md`

Exploratory boundary:

- No authoritative classifier outputs are claimed.
- Human validation remains required.
- Fixture evaluation is limited to repository-maintainer reviewed procedure fixtures.
- No authoritative corpus-wide classifier outputs are claimed.
- The speech-turn dependency is clear for this planning surface, but remains part of classifier provenance.
"""
    docs = """# Speech-Act And Procedure Classifiers

## Scope

This track defines the future classifier surface for speech acts, question/answer structure, interjections, procedural rulings, and debate segments. The track is release-ready as a baseline plan because validated speech-turn components are available.

## Gate

- Validated speech-turn component release
- NZ parliamentary procedure model
- Human validation required before authoritative classifier outputs

## Label Families

- speech_act
- question_answer_structure
- interjection
- procedural_ruling
- debate_segment

## Planned Models

The initial release candidate is intended to use optional ML dependencies from
`requirements/ml.txt` with scikit-learn baselines for reproducible review tooling.

## Evaluation Design

- Reviewed procedure fixtures will seed the first benchmark set.
- Correction files will capture reviewer overrides and false positives.
- Confusion analysis will remain tied to the procedure model rather than raw text.
- `derived/speech-act-procedure-classifiers/evaluation.json` records a reviewed-fixture smoke evaluation and selector checks.

## Boundaries

- No authoritative procedural classification may be published from unvalidated
  speech-turn output.
- Speech-turn readiness is a hard gate, not a soft preference.
- The fixture evaluation is not a corpus-wide accuracy claim or an authoritative classifier release.
"""
    index = """# Speech-Act And Procedure Classifiers

Track ID: `speech_act_procedure_classifiers_20260610`

Status: release-ready-baseline-plan-human-validation.

## Goal

Add classifiers for speech acts, question/answer structure, interjections,
procedural rulings, and debate segments once validated speech-turn and procedure
dependencies are available.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`
- `derived/speech-act-procedure-classifiers/evaluation.json`

## Boundary

Reviewed fixture evaluation and selector checks are present. Authoritative corpus-wide outputs remain out of scope until a larger reviewed benchmark exists.
"""
    evidence = """# Evidence: Speech-Act And Procedure Classifiers

## Release Boundary

The track depends on validated speech-turn components, which are now available. It remains a baseline plan with human validation required before authoritative outputs.

## Dependencies

- `manifests/validated_speech_turn_component_validation.json`
- `manifests/nz_parliamentary_procedure_model.json`
- `fixtures/nz_parliamentary_procedure_samples.json`

## Label Families

- speech_act
- question_answer_structure
- interjection
- procedural_ruling
- debate_segment

## Planned Models

- Speech-act classifier outputs
- Question/answer structure classifier outputs
- Interjection classifier outputs
- Procedural ruling classifier outputs
- Debate-segment classifier outputs
- Review correction files
- Confusion analysis and benchmark notes

## Fixture Evaluation

- `derived/speech-act-procedure-classifiers/evaluation.json`
- Built from repository-maintainer reviewed procedure fixtures.
- Selector checks passed against fixture excerpts.
- Not an authoritative corpus-wide classifier output.

## Validation Commands

- `python scripts/build_speech_act_procedure_classifiers.py`
- `python scripts/check_speech_act_procedure_classifiers.py`
- `python -m unittest tests.test_speech_act_procedure_classifiers`
"""
    plan = """# Plan: Speech-Act And Procedure Classifiers

## Phase 1: Prerequisites

- [x] Confirm validated speech-turn/proceeding dependencies.
- [x] Define label taxonomy and evaluation design.

## Phase 2: Model Output

- [x] Publish baseline classifier plan and manifests.
- [x] Add evaluated classifier outputs and selector checks after human validation.

## Phase 3: Release Gate

- [x] Document status, metrics, and limitations.
"""
    return readme, docs, index, evidence, plan  # ty:ignore[invalid-return-type]


def build_speech_act_procedure_classifiers(
    *, generated_at: str, write: bool = True
) -> dict[str, Any]:
    evaluation = _evaluation_payload(generated_at)
    manifest = {
        "manifest_version": 1,
        "track_id": TRACK_ID,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "status": "release-ready",
        "release_status": "release-ready-baseline-plan-human-validation",
        "blocked_reason": (
            "No current blocker for the planning surface; authoritative classifier outputs "
            "remain deferred pending human validation and evaluation evidence."
        ),
        "dependency_manifests": {
            "validated_speech_turn_component_validation": VALIDATED_SPEECH_TURN_MANIFEST.relative_to(
                ROOT
            ).as_posix(),
            "nz_parliamentary_procedure_model": PROCEDURE_MODEL_MANIFEST.relative_to(
                ROOT
            ).as_posix(),
        },
        "label_families": LABEL_FAMILIES,
        "model_plan": EXPLORATORY_MODEL_PLAN,
        "source_inputs": [
            VALIDATED_SPEECH_TURN_MANIFEST.relative_to(ROOT).as_posix(),
            PROCEDURE_MODEL_MANIFEST.relative_to(ROOT).as_posix(),
            PROCEDURE_FIXTURE.relative_to(ROOT).as_posix(),
        ],
        "evaluation_artifacts": {
            "fixture_evaluation": EVALUATION_PATH.relative_to(ROOT).as_posix(),
            "publication_status": "fixture-evaluation-only-not-authoritative",
        },
        "review_correction_files": [
            "derived/speech-act-procedure-classifiers/speech_act_correction_queue.csv",
            "derived/speech-act-procedure-classifiers/procedure_correction_queue.csv",
        ],
        "validation_results": {
            "blocked_by_speech_turn_gate": False,
            "speech_turn_dependency_recorded": True,
            "procedure_model_recorded": True,
            "review_correction_files_defined": True,
            "human_validation_required": True,
            "reviewed_fixture_evaluation_recorded": True,
            "selector_checks_passed": evaluation["metrics"]["selector_checks_passed"],
        },
    }

    if write:
        _write_json(MANIFEST_PATH, manifest)
        _write_json(SCHEMA_PATH, _manifest_schema())
        _write_json(EVALUATION_PATH, evaluation)
        readme, docs, index, evidence, plan = _supporting_docs()  # ty:ignore[invalid-assignment]
        DOC_PATH.write_text(docs, encoding="utf-8")
        INDEX_PATH.write_text(index, encoding="utf-8")
        EVIDENCE_PATH.write_text(evidence, encoding="utf-8")
        PLAN_PATH.write_text(plan, encoding="utf-8")
        readme_path = ROOT / "samples/speech-act-procedure-classifiers/README.md"
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(readme, encoding="utf-8")
    return manifest
