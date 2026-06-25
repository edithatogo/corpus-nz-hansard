# Sitting And Proceeding Component Release

## Decision

This track is release-ready for date-level official reconciliation only. The public release gate is `release-ready-date-level-official-reconciliation-agent-review`.

## Basis

- `derived/historical_sitting_official_exports/historical_sitting_official_exports_coverage.json` reports 191 official dates, 409 ledger dates, and 29 shared dates available for date-level official reconciliation.
- `manifests/sitting_proceeding_component_validation.json` records 29 date-level reconciled sittings and 0 reconciled proceeding items.
- The neutral component fixture set still contains one sitting and one proceeding item; those fixture rows demonstrate shape and remain in the agent-review fallback review queue.
- `manifests/historical_coverage_audit.json` remains available-not-yet-reconciled for full sitting/proceeding historical completeness, so this track is not full historical completeness and must not claim full historical completeness.

## Current Boundary

- Publish the component as a date-level official reconciliation release surface.
- Keep `derived/sitting_proceeding_components/sitting_proceeding_review.csv` as the agent-review fallback queue for fixture/proceeding rows.
- Keep `derived/sitting_proceeding_components/sitting_proceeding_coverage.json` as the coverage evidence for 29 shared official/ledger dates.
- Do not infer proceeding-level validation or full historical completeness from the fixture scaffold.

## Future Validation Requirements

- Official sitting and proceeding inventories must be reconciled at row level against the supplied corpus extract before proceeding-level release claims are made.
- Missing, inferred, and reconciled sitting/proceeding counts must continue to be reported explicitly.
- Downstream endpoint dependency docs must continue to point at the released neutral component boundary rather than the fixture scaffolding.

## Outputs

- `schemas/sitting_proceeding_component_validation.schema.json`
- `manifests/sitting_proceeding_component_validation.json`
- `derived/sitting_proceeding_components/sitting_proceeding_coverage.json`
- `derived/sitting_proceeding_components/sitting_proceeding_review.csv`


