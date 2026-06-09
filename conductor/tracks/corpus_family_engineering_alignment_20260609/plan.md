# Plan: Corpus Family Engineering Alignment

## Phase 1: Baseline comparison

- [x] Task 0.1: Record the current strict quality-gate baseline separately from the still-pending package/CLI migration.
- [x] Task 1.1: Compare Hansard tooling with the legislation baseline: `pyproject.toml`, `uv.lock`, `src/`, Typer CLI, pytest, ruff, `ty`, pre-commit, Renovate, CodeQL, Scorecard.
- [x] Task 1.2: Identify backwards-compatible wrapper strategy for existing scripts.
- [x] Task 1.3: Define target CLI commands for `nz_hansard_corpus` or equivalent.
- [x] Task 1.4: Define what stays in `requirements.txt` during transition and what moves to `pyproject.toml`/`uv.lock`.

## Phase 2: CI and security alignment

- [x] Task 2.1: Plan Ubuntu primary CI with optional Windows compatibility.
- [x] Task 2.2: Plan pytest migration while preserving current unittest tests during transition.
- [x] Task 2.3: Plan CodeQL, Scorecard, Renovate, and pre-commit adoption.
- [x] Task 2.4: Keep publication jobs separate from dependency-update and quality-only jobs.

## Phase 3: Publication automation alignment

- [x] Task 3.1: Align Hugging Face publish workflow with Xet/access/viewer checks.
- [x] Task 3.2: Align Zenodo workflow with protected draft-first publication.
- [x] Task 3.3: Decide OSF and future metadata automation boundaries.
- [x] Task 3.4: Record sibling links and compatibility expectations with `corpus-nz-legislation`.

## Verification

- [x] Implementation-ready refactor plan exists.
- [x] Existing release commands remain documented until replaced.
- [x] Conductor tracks registry includes this track.
