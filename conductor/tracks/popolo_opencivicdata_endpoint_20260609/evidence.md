# Evidence: Popolo / Open Civic Data Endpoint

## Civic-Data Mapping

- Added `docs/popolo-opencivicdata-mapping.md`.
- The mapping records neutral `members`, `parties`, `motions`, `votes`, `speech_turns`, and `proceeding_items` into Popolo/Open Civic Data-like people, organizations, memberships, motions, vote events, votes, and speech references.

## Sample Package

- Added `scripts/generate_popolo_opencivicdata_sample.py`.
- Generated `samples/popolo-opencivicdata/people.json`.
- Generated `samples/popolo-opencivicdata/organizations.json`.
- Generated `samples/popolo-opencivicdata/memberships.json`.
- Generated `samples/popolo-opencivicdata/motions.json`.
- Generated `samples/popolo-opencivicdata/vote-events.json`.
- Generated `samples/popolo-opencivicdata/votes.jsonl`.
- Generated `samples/popolo-opencivicdata/speeches.jsonl`.
- The package is explicitly `sample-not-release`.

## Referential Integrity

- Added `manifests/popolo_opencivicdata_validation_manifest.json`.
- Added `scripts/check_popolo_opencivicdata_endpoint.py`.
- Added `tests/test_popolo_opencivicdata_endpoint.py`.
- The checker validates JSON/JSONL syntax, membership date ranges, person/organization/motion/vote-event/speech references, party-vote distinction, provenance, dependency groups, and release-ladder mapping.

## Readiness Boundary

- Full Popolo/Open Civic Data readiness remains `blocked-pending-validated-components`.
- Member identity, party attribution, vote/motion extraction, and speech-turn validation are still required before public endpoint publication.
- Full voting records are not inferred from text patterns alone.
