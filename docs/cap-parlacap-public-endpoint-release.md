# CAP / ParlaCAP Public Endpoint Release

## Decision

This track is release-ready as a sample-only public endpoint package under `release-ready-sample-public-endpoint`.

## Basis

- The existing CAP / ParlaCAP package is a sample package and remains `sample-not-release`.
- validated speech-turn exports are available for the sample-scoped endpoint release.
- the repository-declared review map is not maintainer-confirmed.
- model-coded labels remain exploratory-only and non-authoritative.

## Current Boundary

- Publish `samples/cap-parlacap/cap_parlacap_topics.csv`, `samples/cap-parlacap/README.md`, and the codebook manifest as sample-scoped public endpoint outputs.
- Keep the public claim sample-only and do not claim full CAP / ParlaCAP corpus readiness.
- Keep the codebook explicitly not maintainer-confirmed.

## Future Validation Requirements

- Corpus-wide CAP / ParlaCAP topic output must run against normalized Hansard inputs before broad endpoint release claims are made.
- maintainer-confirmed codebook intake must exist before the repository-declared review map can be treated as an external public contract.
- human-coded and rule-coded review rows may be published only when the public boundary is explicit and non-overclaiming.

## Outputs

- `manifests/cap_parlacap_public_endpoint_validation.json`
- `samples/cap-parlacap/cap_parlacap_topics.csv`
- `samples/cap-parlacap/README.md`
- `docs/cap-parlacap-topic-mapping.md`
