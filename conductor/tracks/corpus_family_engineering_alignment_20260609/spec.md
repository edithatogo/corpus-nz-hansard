# Spec: Corpus Family Engineering Alignment

## Goal

Bring `corpus-nz-hansard` engineering practice into alignment with the legislation corpus baseline while retaining Hansard's parliamentary interoperability roadmap.

## Acceptance Criteria

- A future implementation track can move Hansard from script workspace to package/CLI without losing current release reproducibility.
- `pyproject.toml`, `uv.lock`, package layout, pytest, ruff, `ty`, pre-commit, Renovate, CodeQL, Scorecard, and protected Zenodo workflows are tracked as target standards.
- Current strict quality gates are recorded as a baseline, but package layout, `uv.lock`, and Typer CLI migration remain future implementation work until explicitly completed.
- Migration tasks preserve current `requirements.txt` and script commands, or document deprecation wrappers and replacement CLI commands before removal.
- GitHub, Hugging Face, Zenodo, OSF, and future metadata environments are considered in engineering changes.
- Existing `requirements.txt`/script commands remain supported or are deprecated with migration notes.

## Out of Scope

- Performing the package refactor in this planning track.
- Changing canonical data semantics without schema/publication sync approval.
