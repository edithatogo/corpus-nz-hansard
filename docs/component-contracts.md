# Parliamentary Component Contracts

## Purpose

Define neutral derived component contracts that can feed multiple endpoint standards without binding the repository core to any one ontology.

Each component artifact must be versioned, generated, validated, and traceable to the document-level core.

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

## Component Families

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

