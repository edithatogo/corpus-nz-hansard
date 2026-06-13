# Package And CLI Migration Execution

Track ID: `package_cli_migration_execution_20260610`

Status: blocked.

## Goal

Execute the package/CLI migration plan from corpus-family engineering
alignment.

## Primary Artifacts

- `spec.md`
- `plan.md`
- `evidence.md`

## Blocker

The repository is still explicitly configured as a non-package uv project with
script entrypoints in transition. The future `src/nz_hansard_corpus` package
and `nzhc` CLI are documented as migration targets, not current behavior, so
executing the migration here would overstate the repo state.
