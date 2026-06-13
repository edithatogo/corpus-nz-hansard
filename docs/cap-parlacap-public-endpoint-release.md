# CAP / ParlaCAP Public Endpoint Release

## Decision

This track is implemented as a blocked public endpoint release surface and remains sample-only evidence.

## Basis

- The existing CAP / ParlaCAP package is a sample package and remains `sample-not-release`.
- validated speech-turn exports are not yet available for public endpoint output.
- the repository-declared review map is not yet maintainer-confirmed.
- model-coded labels remain exploratory-only and non-authoritative.

## Current Boundary

- Keep `samples/cap-parlacap/cap_parlacap_topics.csv`, `samples/cap-parlacap/README.md`, and the codebook manifest as sample-package evidence, not public endpoint output.
- Keep `manifests/cap_parlacap_public_endpoint_validation.json` blocked until the dependent component releases are validated.

## Future Validation Requirements

- validated speech-turn data must exist before ParlaCAP-compatible speech/topic output can be treated as release-ready.
- maintainer-confirmed codebook intake must exist before the repository-declared review map can be treated as a public contract.
- human-coded and rule-coded review rows may be published only when the public boundary is explicit and non-overclaiming.

## Outputs

- `manifests/cap_parlacap_public_endpoint_validation.json`
- `samples/cap-parlacap/cap_parlacap_topics.csv`
- `samples/cap-parlacap/README.md`
- `docs/cap-parlacap-topic-mapping.md`
