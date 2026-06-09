# Parliamentary Component Contracts

## Purpose

Define neutral derived component contracts that can feed multiple endpoint standards without binding the repository core to any one ontology.

Each component artifact must be versioned, generated, validated, and traceable to the document-level core.

The machine-readable neutral component authority is `manifests/neutral_component_model.json`, with fixtures in `fixtures/neutral_components.json` and the fixture validation manifest in `manifests/neutral_component_validation_manifest.json`. These artifacts cover `sittings`, `proceeding_items`, `speech_turns`, `members`, `parties`, `motions`, `votes`, `bills`, `topics`, and `linguistic_annotations`. They require `derivation_method`, `derivation_version`, `validation_status`, `provenance`, and referential integrity checks while staying `not-published-derived-fixtures-only`.

## Common Fields

Every derived component row must include:

| Field | Requirement |
| --- | --- |
| `component_id` | Stable repository-owned identifier. |
| `component_type` | Neutral component type, for example `speech_turn`, `member`, `vote_event`. |
| `source_stable_id` | Document-level `stable_id` where applicable. |
| `source_archive` | Source archive path or release source identifier. |
| `source_file` | ZIP member or source file. |
| `source_row_number` | Source row number where applicable. |
| `derived_from` | Input artifact names and versions. |
| `derivation_method` | Rule, parser, model, or authority mapping used. |
| `derivation_version` | Version of the derivation pipeline. |
| `validation_status` | `validated`, `candidate`, `excluded`, or `failed`. |
| `confidence` | Numeric confidence when a non-authoritative method is used. |
| `provenance` | Structured provenance object or pointer to provenance artifact. |
| `authority_source_id` | Authority source reference when the row depends on an external authority. |
| `text_selector` | W3C Web Annotation-style selector or pointer when the row targets a text span. |

Component IDs and URIs must follow `manifests/id_uri_policy.json`. New component identifiers must include a hash-backed payload and must not depend on transient file paths or row positions alone. RDF, Popolo, and other endpoint consumers should use the planned `https://w3id.org/nz-hansard/` namespace and the SPARQL-friendly prefixes documented in `docs/canonical-id-uri-policy.md`. Identifier replacements require `manifests/id_uri_deprecations.json`.

## Component Families

### Procedure Component

Procedure components are governed by `manifests/nz_parliamentary_procedure_model.json`, with reviewed boundary fixtures in `fixtures/nz_parliamentary_procedure_samples.json`. They model `party_vote`, `personal_vote`, `question`, `supplementary_question`, `stage`, `ruling`, `interjection`, and `procedural_unit` categories before endpoint exports consume NZ-specific procedure.

Minimum neutral fields:

- `procedure_component_id`
- `category`
- `source_stable_id`
- `text_span`
- `authority_source_ids`
- `uncertainty_status`
- `component_links`
- `document_type`
- `not_speech_turn_by_default`

Procedure components link to `document`, `sitting`, `member`, `party`, `motion`, `bill`, and `vote` components where applicable. Surface text alone remains candidate evidence; votes, questions, stages, rulings, interjections, and procedural units require authority-source references before publication as validated derived fields.

### Document

The existing normalized record remains the document component. It is governed by `docs/normalization-contract.md` and `schemas/hansard_record.schema.json`.

### Sitting

Sitting components represent parliamentary sitting dates or sitting events derived from document metadata, content markers, or official schedule sources.

Minimum neutral fields:

- `sitting_id`
- `sitting_date`
- `parliament_number`
- `session_label`
- `house_or_chamber`
- `source_status`

### Proceeding Item

Proceeding items represent agenda units inside a sitting, such as questions, debates, bills, motions, rulings, and votes.

Minimum neutral fields:

- `proceeding_item_id`
- `sitting_id`
- `source_stable_id`
- `item_type`
- `title`
- `order_index`
- `text_span`

### Speech Turn

Speech turns represent validated speaker-attributed speech segments. Candidate speech turns remain excluded from authoritative endpoint exports.

Minimum neutral fields:

- `speech_turn_id`
- `source_stable_id`
- `proceeding_item_id`
- `speaker_member_id`
- `speaker_raw`
- `speech_text`
- `text_span`
- `turn_order`
- `speaker_resolution_status`

### Member

Member components represent authoritative parliamentary identities.

Minimum neutral fields:

- `member_id`
- `display_name`
- `canonical_name`
- `aliases`
- `authority_source`
- `authority_url`
- `service_periods`

### Party And Membership

Party and membership components represent political organizations and temporal member-party relationships.

Minimum neutral fields:

- `party_id`
- `party_name`
- `party_aliases`
- `membership_id`
- `member_id`
- `start_date`
- `end_date`
- `membership_source`

### Motion And Vote

Motion and vote components represent voteable questions and outcomes.

Minimum neutral fields:

- `motion_id`
- `vote_event_id`
- `source_stable_id`
- `motion_text`
- `vote_type`
- `ayes_count`
- `noes_count`
- `abstentions_count`
- `result`
- `party_votes`
- `individual_votes`

### Bill Or Legislative Item

Bill components link debate material to legislative records.

Minimum neutral fields:

- `bill_id`
- `bill_title`
- `stage`
- `related_motion_id`
- `authority_source`
- `authority_url`

### Topic Code

Topic components support Comparative Agendas Project and ParlaCAP-compatible outputs.

Minimum neutral fields:

- `topic_assignment_id`
- `target_component_id`
- `topic_scheme`
- `topic_code`
- `topic_label`
- `coding_method`
- `coder_or_model`
- `validation_status`

### Linguistic Annotation

Linguistic annotations support Universal Dependencies and other NLP outputs.

Minimum neutral fields:

- `annotation_id`
- `target_component_id`
- `annotation_scheme`
- `token_index`
- `sentence_index`
- `surface`
- `lemma`
- `upos`
- `xpos`
- `features`
- `head`
- `deprel`

### Authority Source

Authority-source components represent official or curated sources used to validate derived assertions.

Minimum neutral fields:

- `authority_source_id`
- `authority_type`
- `title`
- `publisher`
- `source_url`
- `retrieved_at`
- `licence_or_reuse_note`
- `source_hash`
- `coverage_start`
- `coverage_end`

### Gold Or Evaluation Sample

Gold/evaluation samples support precision, recall, ambiguity, and exclusion testing before publication.

The current evaluation fixture authority is `manifests/gold_evaluation_datasets.json` with samples in `fixtures/gold_evaluation_samples.json`. It covers `member_resolution`, `party_attribution`, `speech_turn`, `vote`, and `topic_coding`, and every domain includes `positive`, `negative`, `ambiguous`, `unresolved`, and `excluded` examples. Treat model-generated labels as non-gold unless separately reviewed.

Minimum neutral fields:

- `sample_id`
- `target_component_type`
- `target_component_id`
- `label`
- `review_status`
- `reviewer`
- `reviewed_at`
- `sampling_frame`
- `notes`

### Release Series

Release-series components record which ladder step an artifact belongs to.

The release ladder authority is `manifests/release_ladder.json`; the current public `v0.1.0` release remains an immutable `document-level` release, authority-source evidence uses the `authority-source` level, and future component artifacts use the `neutral-component` level unless a dedicated release manifest maps them otherwise. Component manifests must not describe themselves as `endpoint` or `upstream-contribution` artifacts.

Minimum neutral fields:

- `release_series_id`
- `release_level`
- `artifact_name`
- `artifact_version`
- `input_release_versions`
- `validation_manifest`
- `publication_target`
- `known_exclusions`
- `release_status`
- `manifest_sha256`
