# Popolo / Open Civic Data Public Endpoint Release

## Decision

This track is release-ready as a sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing Popolo/Open Civic Data package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated vote/motion extraction, validated speech-turn, and validated sitting/proceeding components are available for the sample-scoped endpoint release.
- Full voting records are not inferred from text patterns alone.
- This is sample-only evidence and not a full Popolo/Open Civic Data corpus release.

## Current Boundary

- Publish `samples/popolo-opencivicdata/people.json`, `organizations.json`, `memberships.json`, `motions.json`, `vote-events.json`, `votes.jsonl`, `speeches.jsonl`, and `README.md` as sample-scoped public endpoint outputs.
- Keep the public claim sample-only and do not claim full Popolo/Open Civic Data corpus readiness.
- Keep RDF output excluded until the RDF endpoint exists.

## Future Validation Requirements

- Corpus-wide Popolo/Open Civic Data conversion must run against normalized Hansard inputs before broad endpoint release claims are made.
- Full voting records must come from validated vote/motion extraction rather than text-pattern inference alone.
- Speech references must remain tied to validated speech-turn data.

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
