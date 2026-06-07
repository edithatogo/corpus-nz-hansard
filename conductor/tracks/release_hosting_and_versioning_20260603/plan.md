# Plan: Release Hosting and Versioning

## Phase 1: Versioning and Release Notes

- [x] Task: Create version and release review notes.
    - [x] Define version identifier.
    - [x] Describe included artifacts and publication boundary.
- [x] Task: Create hosting decision matrix.
    - [x] Compare likely hosting options.
    - [x] Keep upload/publish decision out of scope.

## Phase 2: Local Review Package

- [x] Task: Implement release package builder.
    - [x] Include lightweight review artifacts.
    - [x] Exclude source ZIP and large generated outputs by default.
    - [x] Emit package manifest with checksums.
- [x] Task: Validate package builder.
    - [x] Add tests.
    - [x] Build local package.
    - [x] Parse package manifest.

## Phase 3: Track Closure

- [x] Task: Final release-packaging review.
    - [x] Confirm no upload or publication occurred.
    - [x] Record generated package path and limitations.
    - [x] Update Conductor registry.
