# Popolo / Open Civic Data Sample Package

Maintainer-review civic-data sample generated from `fixtures/neutral_components.json`.
This package is sample-not-release and remains blocked-pending-validated-components.

- `people.json`
- `organizations.json`
- `memberships.json`
- `motions.json`
- `vote-events.json`
- `votes.jsonl`
- `speeches.jsonl`

Vote records distinguish `party_vote` organization rows from future individual member votes.
No full voting record is inferred from text patterns alone.
Validation manifest: `manifests/popolo_opencivicdata_validation_manifest.json`.
Vote event path: `samples/popolo-opencivicdata/vote-events.json`.
Voter type boundary: `organization` rows represent party votes; future `person` rows represent individual votes.
Readiness remains `blocked-pending-validated-components`.
Blockers: member identity, party attribution, vote/motion extraction, and speech-turn validation.
