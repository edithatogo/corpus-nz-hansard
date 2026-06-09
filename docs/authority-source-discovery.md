# Authority Source Discovery

This document records candidate authority sources for derived parliamentary
components in `corpus-nz-hansard`.

The machine-readable inventory is `manifests/authority_sources.json`, validated
by `schemas/authority_sources.schema.json` and
`scripts/check_authority_sources.py`.

## Policy

Text-derived inference is not an authority source. Derived member, party, bill,
vote, motion, sitting, office, or procedure fields may not be published as
authoritative unless the output cites declared authority source IDs and coverage
notes from this inventory.

Official New Zealand Parliament sources come first. Supporting civic or archive
sources are allowed only where official coverage is incomplete or unavailable.

## Domains

| Domain | Primary source posture |
| --- | --- |
| Members | Current member identity starts from the official Parliament members list. |
| Parties | Current parliamentary parties start from the official Parliament parties page. |
| Offices | Contact and office downloads support current office/contact fields only. |
| Sittings | Hansard, Order Paper, and Daily Progress must be reconciled. |
| Bills | Current bills start from Parliament; historical bills need NZLII reconciliation. |
| Motions | Motions require Hansard, Order Paper, Daily Progress, and rules context. |
| Votes | Votes require Hansard/Daily Progress plus bill-stage or procedural context. |
| Procedure | Parliamentary Rules and Standing Orders govern procedure-derived fields. |

## Coverage Gaps

- The supplied DocumentsDB extract is not a member, party, vote, bill, sitting,
  or procedure authority source.
- Current Parliament web pages do not by themselves provide complete historical
  coverage.
- Dynamic web applications need future retrieval tooling before content hashes
  can replace discovery-record hashes.
- Mid-term member and party changes require dated snapshots.
- Historical bills from 1854 to 2008 require NZLII/archive reconciliation before
  authoritative publication.

## Downstream Unblockers

The following tracks may cite authority source IDs from
`manifests/authority_sources.json`:

- `member_identity_resolution_20260609`
- `party_attribution_provenance_20260609`
- `neutral_component_model_20260609`
- `nz_parliamentary_procedure_model_20260609`
- `popolo_opencivicdata_endpoint_20260609`
- `akoma_ntoso_endpoint_20260609`
- `derived_fields_validation_manifests_20260609`
- `historical_coverage_audit_20260609`

## Validation

```powershell
python scripts\check_authority_sources.py
python -m unittest tests.test_authority_sources
```
