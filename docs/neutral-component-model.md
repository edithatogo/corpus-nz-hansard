# Neutral Parliamentary Component Model

## Purpose

The neutral component model defines derived parliamentary component families without binding the repository core to ParlaMint, Popolo, Akoma Ntoso, CAP, Universal Dependencies, RDF, or metadata-package assumptions.

The machine-readable authority is `manifests/neutral_component_model.json`. Fixture rows are in `fixtures/neutral_components.json`, and the fixture validation manifest is `manifests/neutral_component_validation_manifest.json`. These fixtures are `not-published-derived-fixtures-only`; they prove schema and referential integrity boundaries but do not publish new derived data.

## Component Families

The governed families are:

- `sittings`
- `proceeding_items`
- `speech_turns`
- `members`
- `parties`
- `motions`
- `votes`
- `bills`
- `topics`
- `linguistic_annotations`

Each family uses a stable `nzhc-component-<hash>` identifier pattern governed by `manifests/id_uri_policy.json`. The model records the family-specific ID field, required fields, endpoint consumers, and current planning status.

## Common Required Fields

Every derived component fixture and future component row must carry:

- `component_id`
- `component_type`
- `derived_from`
- `derivation_method`
- `derivation_version`
- `validation_status`
- `provenance`
- `authority_source_ids`

The validation manifest must record `artifact_name`, `artifact_version`, `component_families`, `input_release_versions`, `schema_paths`, `fixture_paths`, `validation_command`, `referential_integrity_status`, `blocking_errors`, and `publication_status`.

## Referential Integrity

The current fixture set validates referential integrity examples across:

- `proceeding_items.sitting_id` to `sittings`
- `speech_turns.proceeding_item_id` to `proceeding_items`
- `speech_turns.speaker_member_id` to `members`
- `motions.proceeding_item_id` to `proceeding_items`
- `votes.motion_id` to `motions`
- `bills.related_motion_id` to `motions`
- `topics.target_component_id` to `proceeding_items`
- `linguistic_annotations.target_component_id` to `speech_turns`

Validated component releases must expand these fixture checks into artifact-level checks before publication.

## Endpoint Consumption

ParlaMint-NZ / TEI consumes `sittings`, `speech_turns`, `members`, `parties`, and `linguistic_annotations`.

Popolo / Open Civic Data consumes `members`, `parties`, `motions`, `votes`, `bills`, and selected `speech_turns`.

Akoma Ntoso consumes `proceeding_items`, `motions`, `votes`, `bills`, and procedure-linked document structure.

CAP / ParlaCAP consumes `proceeding_items`, `speech_turns`, and `topics`.

Universal Dependencies / CoNLL-U consumes validated `speech_turns` and `linguistic_annotations`.

RDF / Linked Data and Croissant / RO-Crate / Frictionless metadata packages consume neutral component descriptors after their validation manifests pass.
