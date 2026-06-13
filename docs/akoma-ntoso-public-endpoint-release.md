# Akoma Ntoso Public Endpoint Release

## Decision

This track is implemented as a blocked public-endpoint release surface and remains sample-only evidence.

## Basis

- The existing Akoma Ntoso package is a sample package and remains `sample-not-release`.
- validated member identity, validated party attribution, validated speech-turn, validated motion, and validated vote components are not all available for a public endpoint release.
- The sample uses a narrow debate-oriented profile subset and does not claim broader schema coverage.

## Current Boundary

- Keep `samples/akoma-ntoso/Akoma-Ntoso.sample.xml`, `Akoma-Ntoso.metadata.xml`, and `README.md` as sample-package evidence, not public endpoint output.
- Keep `manifests/akoma_ntoso_public_endpoint_validation.json` blocked until the dependent component releases are validated.

## Future Validation Requirements

- validated member identity and validated party attribution must exist before person and organization references can be treated as release-ready.
- validated speech-turn data must exist before speech references can be treated as public endpoint output.
- validated motion and validated vote components must exist before debate outcomes can be treated as public endpoint output.

## Outputs

- `manifests/akoma_ntoso_public_endpoint_validation.json`
- `samples/akoma-ntoso/Akoma-Ntoso.sample.xml`
- `samples/akoma-ntoso/Akoma-Ntoso.metadata.xml`
- `samples/akoma-ntoso/README.md`
