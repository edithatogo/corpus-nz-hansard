# Plan: Package And CLI Migration Execution

Status: complete for the compatibility-layer migration.

Release status: release-ready-package-cli-compatibility-layer.

## Phase 1: Migration Plan

- [x] Inventory scripts and shared helpers.
- [x] Map priority commands to package CLI dispatch.
- [x] Define package layout and CLI command names.
- [x] Confirm the package root, CLI namespace, and wrapper policy.

## Phase 2: Incremental Refactor

- [x] Add `src/nz_hansard_corpus` package namespace.
- [x] Add `nzhc` CLI entry point and compatibility console routes.
- [x] Keep existing script entry points working.
- [x] Add tests and checker coverage for both package and CLI surfaces.

## Phase 3: Validation

- [x] Validate the package/CLI migration checker.
- [x] Validate CLI command discovery.
- [x] Update developer docs and track evidence.

Boundary: legacy scripts remain supported and the publication boundary is preserved. This track does not run live publication commands.
