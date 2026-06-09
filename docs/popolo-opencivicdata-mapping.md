# Popolo / Open Civic Data Mapping

## Scope

`samples/popolo-opencivicdata/` is a maintainer-review civic-data sample package generated from `fixtures/neutral_components.json` by `scripts/generate_popolo_opencivicdata_sample.py`. It includes `samples/popolo-opencivicdata/vote-events.json` and is `sample-not-release`, not a public civic-data endpoint release.

The endpoint validation authority is `manifests/popolo_opencivicdata_validation_manifest.json`, checked by `scripts/check_popolo_opencivicdata_endpoint.py`.

## Neutral Inputs

The sample consumes these neutral families from `manifests/neutral_component_model.json`:

- `members`
- `parties`
- `motions`
- `votes`
- `speech_turns`
- `proceeding_items`

It also cites `manifests/nz_parliamentary_procedure_model.json`, `manifests/id_uri_policy.json`, `manifests/dependency_extras_policy.json`, and `manifests/release_ladder.json`.

## Field Mapping

| Neutral field | Civic-data artifact | Notes |
| --- | --- | --- |
| `member_id` | `people.json[].id` | Candidate person object only until member identity validation passes. |
| `party_id` | `organizations.json[].id` | Candidate party organization only until party attribution validation passes. |
| `service_periods` | `memberships.json[]` | Date ranges must validate and link person to organization. |
| `motion_id` | `motions.json[].id` | Required for every vote event. |
| `vote_event_id` | `vote-events.json[].id` | Vote event must link to a motion or procedural question. |
| `party_votes[].party_id` | `votes.jsonl[].voter_id` | `voter_type=organization` distinguishes party votes from individual votes. |
| `speech_turn_id` | `speeches.jsonl[].id` | Speech references stay candidate until speech-turn validation passes. |

## Readiness Boundary

The sample validates JSON/JSONL syntax, date ranges, provenance, and referential integrity. Readiness remains `blocked-pending-validated-components` until member identity, party attribution, vote/motion extraction, and speech-turn validation tracks produce validated component metadata. No full voting record is inferred from text patterns alone.
