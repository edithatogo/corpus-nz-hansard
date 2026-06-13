# Sitting And Proceeding Component Release

## Decision

This track is implemented as a blocked release surface rather than a published neutral component release.

## Basis

- The neutral component fixture set includes one sitting and one proceeding item, but the fixture rows are not official reconciliation evidence.
- `manifests/historical_coverage_audit.json` still marks sitting and proceeding completeness as unreconciled against the supplied extract.
- `manifests/authority_sources.json` contains authority-source candidates, but they have not been turned into a settled historical sitting/proceeding reconciliation.
- The track remains blocked until official sitting and proceeding reconciliation is complete.

## Current Boundary

- Keep `derived/sitting_proceeding_components/sitting_proceeding_review.csv` as a local review queue, not a public data release.
- Keep `derived/sitting_proceeding_components/sitting_proceeding_coverage.json` as a local coverage report.
- Keep `manifests/sitting_proceeding_component_validation.json` blocked until official sitting and proceeding evidence is aligned.

## Future Validation Requirements

- Official sitting and proceeding inventories must be reconciled against the supplied corpus extract.
- Missing, inferred, and reconciled sitting/proceeding counts must be reported explicitly.
- Downstream endpoint dependency docs must continue to point at the released neutral component boundary rather than the fixture scaffolding.

## Outputs

- `schemas/sitting_proceeding_component_validation.schema.json`
- `manifests/sitting_proceeding_component_validation.json`
- `derived/sitting_proceeding_components/sitting_proceeding_coverage.json`
- `derived/sitting_proceeding_components/sitting_proceeding_review.csv`
