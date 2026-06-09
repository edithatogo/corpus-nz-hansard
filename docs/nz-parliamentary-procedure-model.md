# NZ Parliamentary Procedure Model

## Purpose

Model NZ-specific parliamentary procedure before votes, questions, stages, rulings, interjections, or procedural units are published as validated derived components.

The policy authority is `manifests/nz_parliamentary_procedure_model.json`, validated by `scripts/check_nz_parliamentary_procedure_model.py`. Reviewed boundary fixtures live in `fixtures/nz_parliamentary_procedure_samples.json`.

## Procedural Categories

The governed categories are:

- `party_vote`
- `personal_vote`
- `question`
- `supplementary_question`
- `stage`
- `ruling`
- `interjection`
- `procedural_unit`

Each category records required component links to the neutral model: `document`, `sitting`, `member`, `party`, `motion`, `bill`, and `vote` where applicable. Each category also records `authority_source_ids` and uncertainty fields.

## Authority Sources

Procedure components must cite the relevant source IDs from `manifests/authority_sources.json`:

- `nz-parliament-parliamentary-rules`
- `nz-parliament-order-paper`
- `nz-parliament-hansard-current`
- `nz-parliament-daily-progress`
- `nz-parliament-bills-current`
- `nz-parliament-written-questions`
- `nz-parliament-oral-questions`

Surface text alone is candidate evidence. It is not enough to publish validated member, party, bill, motion, or vote links.

## Validation And Uncertainty

Every procedure component validation manifest must include:

- `category`
- `source_stable_id`
- `text_span`
- `authority_source_ids`
- `uncertainty_status`
- `component_links`
- `document_type`
- `not_speech_turn_by_default`

Uncertainty values are `validated`, `candidate`, `ambiguous`, `unresolved`, and `excluded`. Party and personal votes must not become validated voting records without motion/procedural-question linkage and authority validation. Procedural text must not be treated as a speech turn by default.

## Endpoint Mapping Notes

ParlaMint-NZ / TEI maps questions, supplementary questions, rulings, interjections, and procedural units to TEI event, note, and utterance structures while preserving NZ source order.

Popolo / Open Civic Data maps party votes, personal votes, questions, and stages to motion and vote structures only when voteable questions and party/member references are validated.

Akoma Ntoso maps stages, questions, rulings, procedural units, party votes, and personal votes into legislative-document hierarchy while preserving proceeding order.

CAP / ParlaCAP excludes procedural boilerplate from topic-coded units unless the text is linked to a substantive proceeding item.
