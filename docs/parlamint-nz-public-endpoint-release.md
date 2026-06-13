# ParlaMint-NZ Public Endpoint Release

## Decision

This track is implemented as a blocked public-endpoint release surface.

## Basis

- The existing ParlaMint-NZ package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated speech-turn, and validated sitting/proceeding components are not all available for a public endpoint release.
- Full ParlaMint schema validation is still deferred until validated neutral component releases exist.
- This remains sample-only evidence rather than a public endpoint release.

## Current Boundary

- Keep `samples/parlamint-nz/ParlaMint-NZ.sample.xml` as a maintainer-review sample, not a public endpoint release.
- Keep `samples/parlamint-nz/ParlaMint-NZ.metadata.xml` and `samples/parlamint-nz/README.md` as sample-package evidence.
- Keep `manifests/parlamint_nz_public_endpoint_validation.json` blocked until the dependent component releases are validated.

## Future Validation Requirements

- Member identity and party attribution must be validated before ParlaMint speaker/organization references can be treated as release-ready.
- Speech-turn validation must be complete before the TEI utterance layer can be treated as public endpoint output.
- Sitting and proceeding reconciliation must be complete before the endpoint can claim full structural release readiness.

## Outputs

- `manifests/parlamint_nz_public_endpoint_validation.json`
- `samples/parlamint-nz/ParlaMint-NZ.sample.xml`
- `samples/parlamint-nz/ParlaMint-NZ.metadata.xml`
- `samples/parlamint-nz/README.md`
