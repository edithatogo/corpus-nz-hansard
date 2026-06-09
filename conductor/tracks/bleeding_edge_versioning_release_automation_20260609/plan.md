# Plan: Bleeding Edge Versioning And Release Automation

## Tasks

- [x] Define current state and target state.
- [x] Define the authoritative version sources for code/package, dataset, schema, Hugging Face revision, Zenodo DOI snapshot, and manifest hash.
- [x] Add consistency checks across `VERSION`, release notes, `CITATION.cff`, dataset card text, manifests, and publication metadata.
- [x] Decide whether to use Release Please or an equivalent Conventional Commits release-note/tag workflow.
- [x] Add/update CI checks with least-privilege permissions.
- [x] Add/update local commands or Makefile targets.
- [x] Add documentation consistency and release evidence checks.
- [x] Add Renovate/package update policy where applicable.
- [x] Ensure dependency-update PRs cannot publish datasets or Zenodo records.
- [x] Record validation evidence.

## Tooling checklist

- [x] `uv` frozen install/lock checks.
- [x] `ruff check` and `ruff format --check`.
- [x] `ty check` with strict rules for Python modules and scripts.
- [x] `typos` spelling/identifier check.
- [x] `zizmor` workflow security audit.
- [x] `taplo` TOML formatting/linting where TOML config exists.
- [x] `actionlint` workflow syntax check.
- [x] CodeQL and OpenSSF Scorecard.
- [x] Artifact attestations or SLSA-style provenance for release artifacts.

## Verification

- [x] Metadata JSON parses.
- [x] Track is registered in `conductor/tracks.md`.
- [x] All added checks are documented before enforcement.
