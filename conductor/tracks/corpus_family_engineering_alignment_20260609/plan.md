# Plan: Corpus Family Engineering Alignment

## Phase 1: Baseline comparison

- [ ] Task 1.1: Compare Hansard tooling with the legislation baseline: `pyproject.toml`, `uv.lock`, `src/`, Typer CLI, pytest, ruff, `ty`, pre-commit, Renovate, CodeQL, Scorecard.
- [ ] Task 1.2: Identify backwards-compatible wrapper strategy for existing scripts.
- [ ] Task 1.3: Define target CLI commands for `nz_hansard_corpus` or equivalent.

## Phase 2: CI and security alignment

- [ ] Task 2.1: Plan Ubuntu primary CI with optional Windows compatibility.
- [ ] Task 2.2: Plan pytest migration while preserving current unittest tests during transition.
- [ ] Task 2.3: Plan CodeQL, Scorecard, Renovate, and pre-commit adoption.

## Phase 3: Publication automation alignment

- [ ] Task 3.1: Align Hugging Face publish workflow with Xet/access/viewer checks.
- [ ] Task 3.2: Align Zenodo workflow with protected draft-first publication.
- [ ] Task 3.3: Decide OSF and future metadata automation boundaries.

## Verification

- [ ] Implementation-ready refactor plan exists.
- [ ] Existing release commands remain documented until replaced.
- [ ] Conductor tracks registry includes this track.
