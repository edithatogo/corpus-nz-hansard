# Spec: SOTA CI/CD Code Quality And Rust Tooling

## Goal

Adopt SOTA CI/code-quality automation using Rust-backed tools where possible: uv, ruff, ty, typos, zizmor, taplo, plus actionlint.

## Acceptance Criteria

- Aligns with docs/bleeding-edge-versioning-ci-quality.md.
- Preserves corpus-nz-hansard and corpus-nz-legislation naming.
- Uses Rust-backed tooling where practical: uv, ruff, ty, typos, zizmor, taplo, and local ripgrep guidance.
- Records the current strict `ty` gate as the baseline and distinguishes it from still-pending CodeQL, Scorecard, Renovate, pre-commit, and package/`uv.lock` migration work.
- Documents the local commands and CI commands for uv, ruff, ty, typos, zizmor, taplo, actionlint, CodeQL, and Scorecard.
- Keeps publication to Hugging Face and Zenodo behind validation gates.
- For Zenodo work, uses or formally evaluates https://github.com/zenodraft/zenodraft.
