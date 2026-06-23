# Bills API Integration

## Status

The Bills API integration is metadata-ready. It captures complete, non-truncated NZ
Parliament Bills API summary and detail records, preserves member cross-reference
evidence, and emits a governed bill-stage metadata artifact for downstream corpus
integration.

## Captured Extraction

- The current live extraction fetched 3,516 bill summaries.
- The current live extraction processed 3,516 bill detail records.
- The valid member artifact records 351 unique member names.
- `derived/bills_api/facets.json` is retained as the bill-stage vocabulary source.
- `derived/bills_api/bills_summary_20260623T090254Z.json` is valid non-truncated JSON.
- `derived/bills_api/bills_details_20260623T090254Z.json` is valid non-truncated JSON.
- `derived/bills_api/bills_members_20260623T090254Z.json` is retained as valid member evidence.

## Bill-Stage Metadata

`derived/bills_api/bill_stage_metadata.json` is generated from the complete detail capture.
It contains one normalized bill record per API detail response and one normalized stage
record per Bills API stage entry. The artifact is metadata-ready for governed downstream
integration; it does not infer Hansard debate linkage from bill titles alone.

## Member Cross-Reference

`derived/bills_api/member_hansard_cross_reference.json` compares the 351 Bills API
member names with the corpus-wide Hansard member identity surface using exact and
honorific-normalized names.

This cross-reference is evidence only. The corpus-wide member identity component remains
blocked pending authority coverage review.

`derived/crossref_bills_api.json` is retained as a compatibility summary and points
to the full cross-reference artifact.

## Corpus Metadata Integration

Bill-stage metadata is registered as a metadata-ready source from
`nz-parliament-bills-api`. Downstream release publication still has to pass the governed
vote/motion/bill/question extraction gates, but the previous blocker caused by truncated
summary/detail artifacts is resolved.