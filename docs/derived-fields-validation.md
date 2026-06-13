# Derived Fields Validation

This repository uses shared validation manifests for derived member identity, party attribution, and speech-turn artifacts.

## Shared Contract

Each derived-field validation manifest records:

- `artifact_name`
- `artifact_version`
- `generated_at`
- `ok`
- `validation_status`
- `release_gate_status`
- `counts`
- `errors`
- `warnings`
- `source_hashes`
- `source_manifests`

## Manifests

- `manifests/member_identity_resolution_validation.json`
- `manifests/corpus_wide_member_identity_validation.json`
- `manifests/corpus_wide_party_attribution_validation.json`
- `manifests/party_attribution_validation.json`
- `manifests/sitting_proceeding_component_validation.json`
- `manifests/vote_motion_bill_question_extraction_validation.json`
- `manifests/validated_speech_turn_component_validation.json`
- `manifests/speech_turn_validated_artifact_validation.json`
- `manifests/speech_turn_release_decision.json`
- `docs/speech-turn-release-decision.md`

## Gate Rules

- `ok: false` means the artifact is not ready for publication.
- `release_gate_status` must state whether the artifact is blocked, excluded, or ready.
- Publication is blocked until the relevant derived track reaches validated status.
- Corpus-wide member identity remains blocked until normalized corpus input is available and authority coverage review passes.
- Corpus-wide party attribution remains blocked until validated member identity exists.
- Sitting and proceeding components remain blocked until official historical reconciliation is complete.
- Vote, motion, bill, and question extraction remains blocked until validated member identity, party attribution, and sitting/proceeding inputs are all available.
- Validated speech-turn remains blocked until candidate turns and validated member identity are both available.
- Speech-turn candidate output remains non-authoritative. The release decision track explicitly keeps it excluded from the public final scope.

## Source Inputs

- `manifests/authority_sources.json`
- `manifests/gold_evaluation_datasets.json`
- `fixtures/gold_evaluation_samples.json`
- `manifests/speech_turn_segmentation_validation.json`
- `docs/speech-turn-segmentation-report.md`
