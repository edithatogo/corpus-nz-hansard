# Track sitting_proceeding_component_release_20260610 Context

Promote sitting and proceeding structures from design fixtures into validated corpus-wide neutral components.

Repo-side builder/checker are implemented with gate `release-ready-date-level-official-reconciliation-agent-review`.

Current implementation surface:

- `schemas/sitting_proceeding_component_validation.schema.json`
- `manifests/sitting_proceeding_component_validation.json`
- `derived/sitting_proceeding_components/sitting_proceeding_coverage.json`
- `derived/sitting_proceeding_components/sitting_proceeding_review.csv`
- `docs/sitting-proceeding-component-release.md`
- `scripts/build_sitting_proceeding_component.py`
- `scripts/check_sitting_proceeding_component.py`

Release boundary:

- 29 shared official/ledger dates are release-ready as date-level official reconciliation.
- Proceeding-level and fixture rows remain agent-review fallback.
- The track does not claim full historical completeness.
