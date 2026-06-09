# Spec: Corpus Family Engineering Alignment

## Goal

Bring `corpus-nz-hansard` engineering practice into alignment with the legislation corpus baseline while retaining Hansard's parliamentary interoperability roadmap.

## Acceptance Criteria

- A future implementation track can move Hansard from script workspace to package/CLI without losing current release reproducibility.
- `pyproject.toml`, `uv.lock`, package layout, pytest, ruff, mypy, pre-commit, Renovate, CodeQL, Scorecard, and protected Zenodo workflows are tracked as target standards.
- GitHub, Hugging Face, Zenodo, OSF, and future metadata environments are considered in engineering changes.
- Existing `requirements.txt`/script commands remain supported or are deprecated with migration notes.

## Out of Scope

- Performing the package refactor in this planning track.
- Changing canonical data semantics without schema/publication sync approval.
