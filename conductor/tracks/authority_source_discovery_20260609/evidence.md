# Evidence: Authority Source Discovery

## Authority Inventory

Added `manifests/authority_sources.json` as the authority-source discovery
inventory for members, parties, offices, sittings, bills, motions, votes, and
procedure.

The inventory records official New Zealand Parliament sources first:

- `nz-parliament-members-current`
- `nz-parliament-member-contact-downloads`
- `nz-parliament-parties-current`
- `nz-parliament-house-seating-plan`
- `nz-parliament-bills-current`
- `nz-parliament-hansard-current`
- `nz-parliament-order-paper`
- `nz-parliament-daily-progress`
- `nz-parliament-written-questions`
- `nz-parliament-oral-questions`
- `nz-parliament-parliamentary-rules`

It also records fallback/supporting non-Parliament sources for known coverage
gaps:

- `nzlii-historical-bills`
- `electoral-commission-election-results`

## Retrieval And Hashing

Sources were discovered from current public official surfaces on 2026-06-10:

- Parliament home page links to Track legislation, Read Hansard, contact an MP,
  House seating plan, Order Paper, Daily Progress, written questions, and oral
  questions.
- The current members page reports the 54th Parliament has 123 MPs, six
  parliamentary parties, 65 general electorate seats, seven Māori electorates,
  and 51 list MPs.
- The bills page records current bills and states that historical bills from
  1854 to 2008 are available from NZLII.

`source_hash` values are deterministic discovery-record SHA-256 values. Future
automated retrieval may replace them with downloaded-content hashes once access,
licence, and dynamic-page handling are implemented.

## Reuse And Coverage

Added `schemas/authority_sources.schema.json` and
`docs/authority-source-discovery.md` to record source URL, publisher,
retrieval date, hash, coverage period, reuse note, access constraints, refresh
cadence, coverage gaps, and source classification.

The policy explicitly preserves the acceptance boundary:

- text-derived inference is not an authority source;
- official New Zealand Parliament sources come first;
- authoritative member, party, bill, vote, sitting, office, motion, and
  procedure fields require declared authority inputs before publication.

## Downstream Unblockers

Downstream tracks may now cite authority source IDs and coverage notes:

- `member_identity_resolution_20260609`
- `party_attribution_provenance_20260609`
- `neutral_component_model_20260609`
- `nz_parliamentary_procedure_model_20260609`
- `popolo_opencivicdata_endpoint_20260609`
- `akoma_ntoso_endpoint_20260609`
- `derived_fields_validation_manifests_20260609`
- `historical_coverage_audit_20260609`

## Focused Validation

- `python scripts\check_authority_sources.py`
- `python -m unittest tests.test_authority_sources`
