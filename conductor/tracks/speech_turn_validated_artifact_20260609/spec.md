# Spec: Speech-Turn Validated Artifact Decision

## Goal

Determine whether speech-turn segmentation can be promoted from candidate output to a validated derived dataset artifact, and implement the chosen path.

## MoSCoW Requirements

### Must

- Preserve the canonical document-level corpus unchanged.
- Review the existing candidate segmentation algorithm and validation report.
- Define measurable validation thresholds before any promotion.
- Keep source document linkage for every turn.
- Record whether the release decision is "validated derived artifact" or "explicitly excluded".
- If promoted, emit schema, tests, validation manifest, dataset card section, and release notes for the derived artifact.
- If excluded, update docs to state why candidate turns remain local/non-authoritative.

### Should

- Validate against hand-reviewed stratified samples across parliaments and document types.
- Distinguish segmentation correctness from speaker identity correctness.
- Provide confidence categories and error taxonomy.
- Add regression fixtures for known difficult Hansard structures.

### Could

- Use member identity resolution to improve speaker matching after identity validation exists.
- Add a human-review correction file for high-value documents.
- Publish a sample-only preview before a full derived release.

### Won't

- Claim authoritative speech-turn attribution from heuristic candidates alone.
- Mix validated and candidate-only turns without an explicit status field.
- Publish speech-turn data inside the document-level `v0.1.0` release.

## Design Amendments

- Add an explicit decision document, for example `docs/speech-turn-release-decision.md`.
- If promoted:
  - Add `schemas/hansard_speech_turn.schema.json`.
  - Add `manifests/speech_turn_validated_artifact_validation.json`.
  - Add generated output `generated/derived/hansard_speech_turns_validated.parquet`.
- If excluded:
  - Keep candidate output under generated/local policy.
  - Add a tracked exclusion rationale and future validation requirements.

## Acceptance Criteria

- The decision is documented and evidence-backed.
- Tests pass for segmentation fixtures and validation manifest shape.
- Public docs do not overclaim speech-turn authority.
- Any public derived artifact has clear status, confidence, and source-document linkage.

