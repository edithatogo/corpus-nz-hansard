"""Blocked future-track surface for speech-act and procedure classifiers."""

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
            "review_correction_files",
            "validation_results",
        ],
        "properties": {
            "manifest_version": {"const": 1},
            "track_id": {"const": TRACK_ID},
            "repository": {"const": "corpus-nz-hansard"},
            "generated_at": {"type": "string"},
            "status": {"enum": ["blocked"]},
            "release_status": {"const": "blocked-pending-validated-speech-turn"},
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
                ],
                "properties": {
                    "blocked_by_speech_turn_gate": {"const": True},
                    "speech_turn_dependency_recorded": {"const": True},
                    "procedure_model_recorded": {"const": True},
                    "review_correction_files_defined": {"const": True},
                    "human_validation_required": {"const": True},
                },
            },
        },
    }


def _supporting_docs() -> tuple[str, str, str, str]:
    readme = """# Speech-Act And Procedure Classifiers

Blocked future-track surface for classifiers covering speech acts, question/answer
structure, interjections, procedural rulings, and debate segments.

This package is blocked pending validated speech-turn components.

Files:

- `speech_act_procedure_classifiers.json`
- `README.md`

Validation and traceability:

- Manifest: `manifests/speech_act_procedure_classifiers.json`
- Schema: `schemas/speech_act_procedure_classifiers.schema.json`
- Docs: `docs/speech-act-procedure-classifiers.md`

Exploratory boundary:

- No authoritative classifier outputs are claimed.
- Human validation remains required.
- The speech-turn dependency must clear before any release artifact can be produced.
"""
    docs = """# Speech-Act And Procedure Classifiers

## Scope

This track defines the future classifier surface for speech acts, question/answer structure, interjections, procedural rulings, and debate segments. The track is blocked until validated speech-turn components are available.

## Gate

- Validated speech-turn component release
- NZ parliamentary procedure model

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

## Boundaries

- No authoritative procedural classification may be published from unvalidated
  speech-turn output.
- Speech-turn readiness is a hard gate, not a soft preference.
- The track stays blocked until the dependency manifests are satisfied.
"""
    index = """# Speech-Act And Procedure Classifiers

Track ID: `speech_act_procedure_classifiers_20260610`

Status: blocked.

## Goal

Add classifiers for speech acts, question/answer structure, interjections,
procedural rulings, and debate segments once validated speech-turn and procedure
dependencies are available.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`

## Blocker

Validated speech-turn components are not yet available in this workspace.
"""
    evidence = """# Evidence: Speech-Act And Procedure Classifiers

## Blocked

The track depends on validated speech-turn components that are not yet available.

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

- [ ] Build classifier outputs and manifests.
- [ ] Add evaluation and selector checks.

## Phase 3: Release Gate

- [x] Document status, metrics, and limitations.
"""
    return readme, docs, index, evidence, plan  # ty:ignore[invalid-return-type]


def build_speech_act_procedure_classifiers(
    *, generated_at: str, write: bool = True
) -> dict[str, Any]:
    manifest = {
        "manifest_version": 1,
        "track_id": TRACK_ID,
        "repository": "corpus-nz-hansard",
        "generated_at": generated_at,
        "status": "blocked",
        "release_status": "blocked-pending-validated-speech-turn",
        "blocked_reason": (
            "Validated speech-turn components are not available, so classifier outputs "
            "remain blocked pending the upstream release gate."
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
        "review_correction_files": [
            "derived/speech-act-procedure-classifiers/speech_act_correction_queue.csv",
            "derived/speech-act-procedure-classifiers/procedure_correction_queue.csv",
        ],
        "validation_results": {
            "blocked_by_speech_turn_gate": True,
            "speech_turn_dependency_recorded": True,
            "procedure_model_recorded": True,
            "review_correction_files_defined": True,
            "human_validation_required": True,
        },
    }

    if write:
        _write_json(MANIFEST_PATH, manifest)
        _write_json(SCHEMA_PATH, _manifest_schema())
        readme, docs, index, evidence, plan = _supporting_docs()  # ty:ignore[invalid-assignment]
        DOC_PATH.write_text(docs, encoding="utf-8")
        INDEX_PATH.write_text(index, encoding="utf-8")
        EVIDENCE_PATH.write_text(evidence, encoding="utf-8")
        PLAN_PATH.write_text(plan, encoding="utf-8")
        readme_path = ROOT / "samples/speech-act-procedure-classifiers/README.md"
        readme_path.parent.mkdir(parents=True, exist_ok=True)
        readme_path.write_text(readme, encoding="utf-8")
    return manifest
