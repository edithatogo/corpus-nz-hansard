# Party Attribution With Provenance

This repository keeps party attribution as a derived layer with explicit provenance and a blocked release boundary until member identity is validated.

Current implementation surface:

- `derived/party_attribution_authority.json`
- `samples/party-attribution/party_attribution_review.csv`
- `samples/party-attribution/README.md`
- `manifests/party_attribution_validation.json`
- `manifests/party_attribution_provenance_package.json`

## Corpus-Wide Release Gate

The corpus-wide release track is separate from the sample package:

- Builder: `scripts/build_corpus_wide_party_attribution.py`
- Checker: `scripts/check_corpus_wide_party_attribution.py`
- Schema: `schemas/corpus_wide_party_attribution.schema.json`
- Validation manifest: `manifests/corpus_wide_party_attribution_validation.json`
- Release-gate docs: `docs/corpus-wide-party-attribution-release.md`

The current corpus-wide gate is blocked until validated member identity exists. Explicit party-vote labels may still be extracted in blocked-review mode, but the release decision must remain `defer`.

Rules:

- Party attribution is derived data, not a source column.
- Date-bounded party attribution uses `document_content_date` when present.
- Party labels from explicit party-vote text are preserved with provenance.
- Unknown, ambiguous, unresolved, and excluded cases remain visible.
- No derived party attribution output is promoted until validated member identity exists.

Known limitations:

- The package is local-review-only.
- The repo does not claim external acceptance.
- No party attribution is inferred from speech content alone.
- No corpus-wide party attribution output is promoted until validated member identity exists.
