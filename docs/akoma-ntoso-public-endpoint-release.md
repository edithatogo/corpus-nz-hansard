# Akoma Ntoso Public Endpoint Release

## Decision

This track is release-ready as a sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing Akoma Ntoso package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated speech-turn, validated motion, and validated vote components are available for the sample-scoped endpoint release.
- The sample uses a narrow debate-oriented profile subset and does not claim broader schema coverage.
- This is sample-only evidence and not full Akoma Ntoso corpus or schema coverage.

## Current Boundary

- Publish `samples/akoma-ntoso/Akoma-Ntoso.sample.xml`, `Akoma-Ntoso.metadata.xml`, and `README.md` as sample-scoped public endpoint outputs.
- Keep the public claim sample-only and do not claim full Akoma Ntoso corpus readiness.
- Keep full Akoma Ntoso schema coverage deferred until corpus-wide endpoint artifacts exist.

## Future Validation Requirements

- Corpus-wide Akoma Ntoso conversion must run against normalized Hansard inputs before broad endpoint release claims are made.
- Full Akoma Ntoso schema validation must pass on corpus-wide artifacts before full endpoint readiness is claimed.
- Debate outcomes must remain tied to validated motion and validated vote extraction.

## Outputs

- `manifests/akoma_ntoso_public_endpoint_validation.json`
- `samples/akoma-ntoso/Akoma-Ntoso.sample.xml`
- `samples/akoma-ntoso/Akoma-Ntoso.metadata.xml`
- `samples/akoma-ntoso/README.md`

## Release Notes

The endpoint manifest and sample examples are published as sample-scoped public-release evidence under `release-ready-sample-public-endpoint`.
They are suitable for maintainer review of the declared Akoma Ntoso boundary, but they are not full Akoma Ntoso corpus or schema coverage.

## Examples

- `samples/akoma-ntoso/Akoma-Ntoso.sample.xml` records the debate-oriented sample structure.
- `samples/akoma-ntoso/Akoma-Ntoso.metadata.xml` records sample-level metadata in the same namespace.
