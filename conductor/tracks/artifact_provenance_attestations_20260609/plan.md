# Plan: Artifact Provenance And Attestations

## Tasks

- [x] Define current state and target state.
- [x] Define the release evidence ledger schema and required fields.
- [x] Map artifact classes to provenance strategy: GitHub artifact attestation, SLSA-style provenance, signed checksum, or documented deferral.
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
