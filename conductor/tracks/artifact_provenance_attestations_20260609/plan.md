# Plan: Artifact Provenance And Attestations

## Tasks

- [ ] Define current state and target state.
- [ ] Add/update CI checks with least-privilege permissions.
- [ ] Add/update local commands or Makefile targets.
- [ ] Add documentation consistency and release evidence checks.
- [ ] Add Renovate/package update policy where applicable.
- [ ] Ensure dependency-update PRs cannot publish datasets or Zenodo records.
- [ ] Record validation evidence.

## Tooling checklist

- [ ] `uv` frozen install/lock checks.
- [ ] `ruff check` and `ruff format --check`.
- [ ] `typos` spelling/identifier check.
- [ ] `zizmor` workflow security audit.
- [ ] `taplo` TOML formatting/linting where TOML config exists.
- [ ] `actionlint` workflow syntax check.
- [ ] CodeQL and OpenSSF Scorecard.
- [ ] Artifact attestations or SLSA-style provenance for release artifacts.

## Verification

- [ ] Metadata JSON parses.
- [ ] Track is registered in `conductor/tracks.md`.
- [ ] All added checks are documented before enforcement.
