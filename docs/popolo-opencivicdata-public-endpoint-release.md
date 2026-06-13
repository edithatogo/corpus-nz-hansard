# Popolo / Open Civic Data Public Endpoint Release

## Decision

This track is implemented as a blocked public-endpoint release surface and remains sample-only evidence.

## Basis

- The existing Popolo/Open Civic Data package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated vote/motion extraction, and validated speech-turn components are not all available for a public endpoint release.
- Full voting records are not inferred from text patterns alone.

## Current Boundary

- Keep `samples/popolo-opencivicdata/people.json`, `organizations.json`, `memberships.json`, `motions.json`, `vote-events.json`, `votes.jsonl`, `speeches.jsonl`, and `README.md` as sample-package evidence, not public endpoint output.
- Keep `manifests/popolo_opencivicdata_public_endpoint_validation.json` blocked until the dependent component releases are validated.

## Future Validation Requirements

- validated member identity and validated party attribution must exist before person and organization references can be treated as release-ready.
- validated vote/motion extraction must be complete before votes and motions can be treated as public endpoint output.
- validated speech-turn data must exist before speech references can be treated as public endpoint output.

## Outputs

- `manifests/popolo_opencivicdata_public_endpoint_validation.json`
- `samples/popolo-opencivicdata/people.json`
- `samples/popolo-opencivicdata/organizations.json`
- `samples/popolo-opencivicdata/memberships.json`
- `samples/popolo-opencivicdata/motions.json`
- `samples/popolo-opencivicdata/vote-events.json`
- `samples/popolo-opencivicdata/votes.jsonl`
- `samples/popolo-opencivicdata/speeches.jsonl`
- `samples/popolo-opencivicdata/README.md`
