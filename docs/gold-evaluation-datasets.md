# Gold Evaluation Datasets

## Purpose

Gold evaluation fixtures define reviewed examples for later derived member, party, speech-turn, vote, and topic outputs. They are validation inputs only. They do not publish derived fields, do not change the immutable `v0.1.0` document-level release, and do not treat model-generated labels as gold.

Machine-readable files:

- `manifests/gold_evaluation_datasets.json`
- `fixtures/gold_evaluation_samples.json`
- `schemas/gold_evaluation_datasets.schema.json`
- `schemas/gold_evaluation_sample.schema.json`

## Domains And Classes

Each domain has at least one reviewed fixture for every required example class:

| Domain | Target track |
| --- | --- |
| `member_resolution` | `member_identity_resolution_20260609` |
| `party_attribution` | `party_attribution_provenance_20260609` |
| `speech_turn` | `speech_turn_validated_artifact_20260609` |
| `vote` | `popolo_opencivicdata_endpoint_20260609` |
| `topic_coding` | `cap_parlacap_topic_endpoint_20260609` |

Required classes:

- `positive`
- `negative`
- `ambiguous`
- `unresolved`
- `excluded`

Every fixture records sampling frame, review status, reviewer, reviewed date, label provenance, source reference, and expected behavior.

## Metrics Supported

The fixtures support small-regression checks for:

- precision
- recall
- ambiguity rate
- unresolved rate
- exclusion regression

The first fixture set is intentionally compact and Git-friendly. It is suitable for release gating and regression tests, not for final benchmark claims.

## Publication Gate

Endpoint contracts must cite `manifests/gold_evaluation_datasets.json` before publishing derived member, party, speech-turn, vote, or topic artifacts. Future endpoint manifests must list the relevant fixture IDs or a refreshed evaluation manifest under their gold/evaluation dataset dependencies.

Derived-field validation manifests are defined in `docs/derived-fields-validation.md` and tracked in:

- `manifests/member_identity_resolution_validation.json`
- `manifests/party_attribution_validation.json`
- `manifests/speech_turn_validated_artifact_validation.json`
