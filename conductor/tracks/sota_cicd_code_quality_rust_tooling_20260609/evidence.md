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

Follow-up completed:

- Artifact attestation/provenance checks were completed under `artifact_provenance_attestations_20260609`.

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

## CodeQL And Scorecard - 2026-06-09

Repo-side hardening applied:

- Added `.github/workflows/codeql.yml` for Python CodeQL analysis on pull requests, pushes to `main`, weekly schedule, and manual dispatch.
- Pinned `github/codeql-action/init` and `github/codeql-action/analyze` to commit SHA `8aad20d150bbac5944a9f9d289da16a4b0d87c1e` after resolving the `v4` tag on 2026-06-09.
- Added `.github/workflows/scorecard.yml` for OpenSSF Scorecard on pull requests, pushes to `main`, weekly schedule, and manual dispatch.
- Pinned `ossf/scorecard-action` to commit SHA `05b42c624433fc40578a4040d5cf5e36ddca8cde` after resolving the latest `v2.4.3` tag on 2026-06-09.
- Both workflows use least-privilege permissions for read-only checkout plus the security-event or OIDC permissions required by their scanners. Scorecard keeps global permissions read-only and scopes required write permissions to the job so Scorecard result publication can verify the workflow.

Verification:

- GitHub Actions run `27208394000` passed `CodeQL` on commit `f40de818db77f1f567fcf8b42eae65dd4b912913`.
- GitHub Actions run `27208394044` passed `OpenSSF Scorecard` on commit `f40de818db77f1f567fcf8b42eae65dd4b912913`.
- GitHub Actions runs `27208394030` and `27208394054` also passed `Quality` and `Tests` on the same commit.

## Quality Gate Command Surface - 2026-06-09

Repo-side hardening applied:

- Added `Makefile` targets for the full local quality gate and each individual tool: Ruff lint, Ruff format check, strict Ty type check, Typos, Zizmor, Taplo, Actionlint, quality configuration validation, and unit tests.
- Added `scripts/check_quality_gate.py` to validate the quality configuration itself: dev-tool pins, required Quality workflow commands, local Makefile targets, pinned GitHub Actions refs, and publication workflows staying manual-only.
- Added `tests/test_check_quality_gate.py` so the quality-gate configuration is covered by unit tests.
- Added `docs/quality-gate.md` with local commands, CI alignment, pre-commit deferral, and current Dependabot-versus-Renovate policy.
- Added the quality-gate configuration checker to `.github/workflows/quality.yml`.

Verification:

- `python scripts\check_quality_gate.py` passed.
- `python -m unittest tests.test_check_quality_gate` passed.
- `python -m ruff check --no-cache .` passed.
- `python -m ruff format --check --no-cache .` passed.
- `ty check --error all .` passed.
- `typos --config typos.toml` passed.
- `zizmor --min-severity medium .github/workflows` passed with no findings.
- `taplo format --check pyproject.toml typos.toml` passed.
- `actionlint -color` passed.
- `python -m unittest discover tests` passed with 43 tests.
- `make quality` passed.
- Conductor track `metadata.json` files parse as JSON.

## UV And Provenance Follow-Through - 2026-06-10

Repo-side hardening applied:

- Added `pyproject.toml` project/dependency metadata and committed `uv.lock`.
- Added `uv lock --check` and `uv sync --frozen --all-groups` to the Makefile and Quality workflow.
- Added release provenance ledger schema, builder, docs, and policy checks under `artifact_provenance_attestations_20260609`.
- Kept the uv CLI pinned in the pyproject dev dependency group and installed it explicitly in CI before frozen sync checks, avoiding GitHub Dependency Graph treating `/requirements` as a uv project.

Verification:

- Local `make quality` passed with uv lock check, frozen sync, Ruff, ty, typos, zizmor, taplo, actionlint, quality configuration, release provenance policy, and 45 unit tests.
- GitHub Actions for commit `86466f2f762a08fa5005760863d6a60beba2cea1` passed: Quality, Tests, CodeQL, OpenSSF Scorecard, and Dependency Graph.

## Completion Consistency Pass - 2026-06-10

Worker 1 scope was limited to `conductor/tracks/sota_cicd_code_quality_rust_tooling_20260609/`.

Consistency result:

- `plan.md` already had every task, tooling checklist item, and verification item checked.
- `evidence.md` already recorded local `make quality` and GitHub Actions readback for the SOTA toolchain, CodeQL, Scorecard, uv, and provenance follow-through.
- `metadata.json` still reported `status: pending`, which did not match the completed plan and evidence state.

Changes made:

- Updated `metadata.json` status from `pending` to `completed`.
- Updated `metadata.json` `updated_at` to `2026-06-10T00:00:00+10:00`.

Remaining blocker:

- None inside the Worker 1 ownership scope. Registry promotion in `conductor/tracks.md` is outside this worker's allowed edit boundary.

## Coordination Completion - 2026-06-10

Central integration promoted this track from Active to Completed in `conductor/tracks.md`.
