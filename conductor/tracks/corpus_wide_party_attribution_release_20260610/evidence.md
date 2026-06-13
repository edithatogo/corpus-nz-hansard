# Evidence: Corpus-Wide Party Attribution Release

## Status

Blocked.

Repo-side implementation is present and now emits a corpus-wide party attribution CSV from the normalized corpus, but publication is deferred because the repository does not yet have a validated corpus-wide member identity release.

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

Decision: defer.

Reasons:

- Validated corpus-wide member identity is not available.
- Member-linked party attribution cannot be promoted without that dependency.
- Explicit party-vote extraction can run in blocked-review mode, but not as a validated release.
- The generated CSV remains a blocked derived component and is not a validated public release.

## Validation Commands

- `python scripts\build_corpus_wide_party_attribution.py`
- `python scripts\check_corpus_wide_party_attribution.py`
- `python scripts\validate_derived_fields.py`
- `python -m unittest tests.test_corpus_wide_party_attribution tests.test_party_attribution_provenance`
- `ruff check scripts\build_corpus_wide_party_attribution.py scripts\check_corpus_wide_party_attribution.py tests\test_corpus_wide_party_attribution.py`
