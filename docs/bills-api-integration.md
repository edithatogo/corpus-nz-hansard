# Bills API Integration

## Status

The Bills API integration is implemented as review evidence and deferred corpus metadata
integration. It does not publish full bill-stage corpus metadata yet.

## Captured Extraction

- The recorded extraction run fetched 3,513 bill summaries.
- The recorded extraction run processed 3,513 bill detail requests.
- The valid member artifact records 351 unique member names.
- `derived/bills_api/facets.json` is retained as the bill-stage vocabulary source.
- `derived/bills_api/bills_members_20260613T021002Z.json` is retained as valid member evidence.

## Truncated Artifacts

`bills_summary_20260613T021002Z.json` and `bills_details_20260613T021002Z.json`
are truncated review artifacts. They preserve extraction evidence but are not complete
machine-readable Bills API record captures.

## Member Cross-Reference

`derived/bills_api/member_hansard_cross_reference.json` compares the 351 Bills API
member names with the corpus-wide Hansard member identity surface using exact and
honorific-normalized names.

This cross-reference is evidence only. The corpus-wide member identity component remains
blocked pending authority coverage review.

`derived/crossref_bills_api.json` is retained as a compatibility summary and now points
to the full cross-reference artifact instead of reporting a zero-member stale result.

## Corpus Metadata Integration

Bill-stage metadata is registered as a deferred corpus metadata source from
`nz-parliament-bills-api`. Full integration into released corpus metadata requires a
non-truncated Bills API detail capture before publication.
