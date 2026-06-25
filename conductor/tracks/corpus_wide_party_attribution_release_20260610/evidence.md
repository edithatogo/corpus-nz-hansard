# Evidence: Corpus-Wide Party Attribution Release

## Status

Complete. Release-ready under `release-ready-explicit-party-labels-member-identity-triangulated`.

## Implemented

- `scripts/build_corpus_wide_party_attribution.py`
- `scripts/check_corpus_wide_party_attribution.py`
- `schemas/corpus_wide_party_attribution.schema.json`
- `docs/corpus-wide-party-attribution-release.md`
- `tests/test_corpus_wide_party_attribution.py`
- `manifests/corpus_wide_party_attribution_validation.json`
- `derived/corpus_wide_party_attribution/party_attribution.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_queue.csv`
- `derived/corpus_wide_party_attribution/party_attribution_review_overrides.csv`

## Release Decision

Decision: release.

Reasons:

- Member identity dependency is satisfied by `release-ready-triangulated-agent-review`.
- Explicit party-vote labels are direct source-text claims.
- Speech-text party inference and member-identity fallback rows remain excluded from authoritative party claims.

## Validation Commands

- `python scripts/check_corpus_wide_party_attribution.py`
- `python -m pytest tests/test_corpus_wide_party_attribution.py`
- `python scripts/validate_derived_fields.py`
