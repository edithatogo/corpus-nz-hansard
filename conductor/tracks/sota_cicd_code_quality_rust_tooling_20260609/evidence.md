# Evidence: SOTA CI/CD Code Quality And Rust Tooling

## Initial Evidence

Status: opened on 2026-06-09.

This track implements the corpus-family bleeding-edge versioning, CI/CD, code-quality, automation, and provenance standard.

## GitHub Actions Supply-Chain Hardening - 2026-06-09

Repo-side hardening applied:

- Replaced `windows-latest` with explicit `windows-2025` across all workflows to avoid runner-image redirect drift.
- Updated `actions/checkout` from mutable `v4` to pinned `v6.0.3` commit SHA `df4cb1c069e1874edd31b4311f1884172cec0e10`.
- Updated `actions/setup-python` from mutable `v5` to pinned `v6.2.0` SHA `a309ff8b426b58ec0e2a45f0f869d46889d02405`.
- Updated `actions/upload-artifact` from mutable `v4` to pinned `v7.0.1` SHA `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`.
- Added `.github/dependabot.yml` for weekly `github-actions` and root `pip` update PRs.
- Dependabot PR #4 corrected the initial `actions/checkout` annotated tag object SHA to the peeled `v6.0.3` commit SHA; required checks passed and the correction was merged into `main`.

Verification:

- YAML parsing succeeded for all workflow files and `.github/dependabot.yml`.
- `rg` scan found no remaining `windows-latest` or mutable `actions/...@v*` references in `.github/workflows`.

Remaining follow-up:

- Add `ruff`, `typos`, `zizmor`, `taplo`, and `actionlint` jobs.
- Add artifact attestation/provenance checks under the dedicated provenance track.
