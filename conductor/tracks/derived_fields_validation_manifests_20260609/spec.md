# Spec: Derived Fields Validation Manifests

## Goal

Create a common validation framework for derived fields so member identity, party attribution, and speech-turn artifacts have consistent tests, manifests, and publication gates.

## MoSCoW Requirements

### Must

- Define schema validation for every derived output.
- Validate required provenance fields.
- Validate status/confidence enumerations.
- Validate source linkage back to canonical `stable_id`.
- Validate row count relationships against source documents.
- Emit machine-readable manifests for each derived artifact.
- Add tests for manifest shape and failure cases.
- Block publication when validation errors are nonzero.

### Should

- Provide shared helpers for manifest generation.
- Include quality thresholds for unresolved, ambiguous, and low-confidence outputs.
- Include deterministic sample reports for human review.
- Add cross-artifact consistency checks, for example party attribution cannot exist for unresolved member identity unless explicitly marked.

### Could

- Add drift checks against prior derived releases.
- Add dashboard-ready summaries.
- Add JSON Schema files for each validation manifest.

### Won't

- Decide the substantive authority source for member or party data.
- Fix data-quality issues by silently dropping records.
- Treat warning-free validation as proof of official endorsement.

## Design Amendments

- Add shared validation module, for example `scripts/validate_derived_fields.py`.
- Add manifest schemas under `schemas/` if useful.
- Add tracked manifests:
  - `manifests/member_identity_resolution_validation.json`
  - `manifests/party_attribution_validation.json`
  - `manifests/speech_turn_validated_artifact_validation.json`
- Add release gate docs under `docs/derived-fields-validation.md`.

## Acceptance Criteria

- Each derived artifact has schema tests, validation manifest tests, and failure-mode tests.
- Validation manifests include `ok`, counts, errors, warnings, source hashes, generated timestamp, and release gate status.
- Publication docs reference the validation manifests before any derived release.

