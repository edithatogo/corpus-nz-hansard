# Evidence: SOTA CI/CD Code Quality And Rust Tooling

## Initial Evidence

Status: opened on 2026-06-09.

This track implements the corpus-family bleeding-edge versioning, CI/CD, code-quality, automation, and provenance standard.

## GitHub Actions Supply-Chain Hardening - 2026-06-09

Repo-side hardening applied:

- Replaced `windows-latest` with explicit `windows-2025-vs2026` across all workflows to avoid runner-image redirect drift. This incorporates the 2026-06-09 GitHub Actions notice that `windows-2025` requests are being redirected to `windows-2025-vs2026` by 2026-06-15.
- Updated `actions/checkout` from mutable `v4` to pinned `v6.0.3` commit SHA `df4cb1c069e1874edd31b4311f1884172cec0e10`.
- Updated `actions/setup-python` from mutable `v5` to pinned `v6.2.0` SHA `a309ff8b426b58ec0e2a45f0f869d46889d02405`.
- Updated `actions/upload-artifact` from mutable `v4` to pinned `v7.0.1` SHA `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`.
- Added `.github/dependabot.yml` for weekly `github-actions` and root `pip` update PRs.
- Dependabot PR #4 corrected the initial `actions/checkout` annotated tag object SHA to the peeled `v6.0.3` commit SHA; required checks passed and the correction was merged into `main`.

Verification:

- YAML parsing succeeded for all workflow files and `.github/dependabot.yml`.
- `rg` scan found no remaining `windows-latest` or mutable `actions/...@v*` references in `.github/workflows`.

Remaining follow-up:

- Add artifact attestation/provenance checks under the dedicated provenance track.

## Code Quality Tooling - 2026-06-09

Repo-side hardening applied:

- Added pinned dev requirements for `ruff==0.15.16`, `ty==0.0.46`, `typos==1.47.2`, `zizmor==1.25.2`, and `taplo==0.9.3`.
- Added pinned `actionlint` v1.7.12 Windows amd64 install in Quality CI, verified against SHA-256 `6e7241b51e6817ea6a047693d8e6fed13b31819c9a0dd6c5a726e1592d22f6e9`.
- Added `.github/actionlint.yaml` so local and CI `actionlint` accept GitHub's `windows-2025-vs2026` runner label while upstream actionlint label metadata catches up.
- Added `pyproject.toml` Ruff configuration and `typos.toml` spelling exclusions.
- Added `.gitattributes` LF normalization for source and config files so Windows CI checkouts match Ruff formatting expectations.
- Added `.github/workflows/quality.yml` for Ruff lint, Ruff format check, strict Ty type checking, Typos, Zizmor workflow audit, and Taplo TOML format check.
- Added `requirements/requirements.txt` as an aggregate optional-stack manifest so GitHub Dependency Graph has a supported pip manifest under `/requirements` without changing the base runtime install target.
- Hardened workflow checkout steps with `persist-credentials: false`, added explicit read-only permissions for the test workflow, and moved workflow-dispatch inputs out of shell template interpolation where Zizmor reported injection risk.

Verification:

- Tool versions were checked from PyPI on 2026-06-09 before pinning.
- `python -m ruff check --no-cache .` passed.
- `python -m ruff format --check --no-cache .` passed.
- `ty check --error all .` passed.
- `typos --config typos.toml` passed.
- `zizmor --min-severity medium .github/workflows` passed with no findings.
- `taplo format --check pyproject.toml typos.toml` passed.
- Pinned local `actionlint` v1.7.12 download verified the checksum and `actionlint -color` passed.
