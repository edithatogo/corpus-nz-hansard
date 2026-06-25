# ParlaMint-NZ Public Endpoint Release

## Decision

This track is release-ready as a sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing ParlaMint-NZ package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated speech-turn, and validated sitting/proceeding components are available for the sample-scoped endpoint release.
- Full ParlaMint schema validation remains deferred until corpus-wide endpoint artifacts exist.
- This is sample-only evidence and not a full ParlaMint corpus release.

## Current Boundary

- Publish `samples/parlamint-nz/ParlaMint-NZ.sample.xml` as the sample-scoped public endpoint artifact.
- Keep `samples/parlamint-nz/ParlaMint-NZ.metadata.xml` and `samples/parlamint-nz/README.md` as sample-package evidence.
- Keep the public claim sample-only and do not claim full ParlaMint corpus readiness.

## Future Validation Requirements

- Corpus-wide ParlaMint conversion must run against normalized Hansard inputs before broad endpoint release claims are made.
- Full ParlaMint schema validation must pass on corpus-wide artifacts before full endpoint readiness is claimed.
- Optional linguistic annotations remain excluded until UD/CoNLL-U artifacts exist.

## Outputs

- `manifests/parlamint_nz_public_endpoint_validation.json`
- `samples/parlamint-nz/ParlaMint-NZ.sample.xml`
- `samples/parlamint-nz/ParlaMint-NZ.metadata.xml`
- `samples/parlamint-nz/README.md`
