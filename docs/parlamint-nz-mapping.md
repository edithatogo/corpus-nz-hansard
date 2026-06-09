# ParlaMint-NZ Mapping

## Scope

`samples/parlamint-nz/` is a maintainer-review sample package generated from `fixtures/neutral_components.json` by `scripts/generate_parlamint_nz_sample.py`. It includes `samples/parlamint-nz/ParlaMint-NZ.sample.xml` and is `sample-not-release`, not a ParlaMint-NZ public endpoint release.

The endpoint validation authority is `manifests/parlamint_nz_validation_manifest.json`, checked by `scripts/check_parlamint_nz_endpoint.py`.

## Neutral Inputs

The ParlaMint-NZ sample consumes these neutral families from `manifests/neutral_component_model.json`:

- `sittings`
- `proceeding_items`
- `speech_turns`
- `members`
- `parties`
- `linguistic_annotations`

The sample also cites `manifests/nz_parliamentary_procedure_model.json`, `manifests/id_uri_policy.json`, `manifests/dependency_extras_policy.json`, and `manifests/release_ladder.json`.

## TEI Mapping

| Neutral field | TEI location | Notes |
| --- | --- | --- |
| `sitting_id` | `tei:div/@corresp` | Links sitting-level structure to the neutral component fixture. |
| `proceeding_item_id` | `tei:u/@corresp` | Preserves the agenda/proceeding link. |
| `speech_turn_id` | `tei:u/@xml:id` | Keeps the neutral speech-turn identifier. |
| `speaker_member_id` | `tei:u/@who` and `tei:person/@xml:id` | Must resolve to member metadata before readiness. |
| `party_id` | `tei:org/@xml:id` and `tei:affiliation/@ref` | Must resolve to party metadata before readiness. |
| `vote_event_id` | `tei:event/@xml:id` | Vote information remains sample-level until vote validation lands. |

## NZ-Specific Encoding Decisions

- Sittings and proceedings are encoded as TEI structural divisions while keeping neutral IDs in `@corresp`.
- Questions and supplementary questions will map through the NZ procedure model before being flattened into utterances.
- Party votes and personal votes remain event notes until motion/vote validation and member/party resolution are complete.
- Procedural rulings and interjections are not automatically speech turns; the procedure model controls whether they become utterances or notes.

## Readiness Boundary

The sample XML is well-formed TEI and every sample reference resolves to a neutral fixture component. ParlaMint-NZ readiness remains `blocked-pending-validated-components` until member identity, party attribution, and speech-turn validation tracks produce validated component metadata.
