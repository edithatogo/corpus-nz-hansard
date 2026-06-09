# Spec: SOTA CI/CD Code Quality And Rust Tooling

## Goal

Adopt SOTA CI/code-quality automation using Rust-backed tools where possible: uv, ruff, typos, zizmor, taplo, plus actionlint.

## Acceptance Criteria

- Aligns with docs/bleeding-edge-versioning-ci-quality.md.
- Preserves corpus-nz-hansard and corpus-nz-legislation naming.
- Uses Rust-backed tooling where practical: uv, ruff, typos, zizmor, taplo, and local ripgrep guidance.
- Keeps publication to Hugging Face and Zenodo behind validation gates.
- For Zenodo work, uses or formally evaluates https://github.com/zenodraft/zenodraft.
