# Spec: Bleeding Edge Versioning And Release Automation

## Goal

Implement SemVer/dataset/schema version governance, Release Please-style changelog automation, and consistency checks.

## Acceptance Criteria

- Aligns with `docs/bleeding-edge-versioning-ci-quality.md`.
- Preserves `corpus-nz-hansard` and `corpus-nz-legislation` naming.
- Uses Rust-backed tooling where practical: `uv`, `ruff`, `ty`, `typos`, `zizmor`, `taplo`, and local `ripgrep` guidance.
- Defines separate code/package, dataset, schema, Hugging Face revision, Zenodo DOI snapshot, and manifest-hash version authorities.
- Adds consistency checks for version-bearing files such as `VERSION`, release notes, `CITATION.cff`, dataset card text, manifests, and Zenodo/Hugging Face metadata.
- Records whether Release Please or an equivalent changelog/tag automation is adopted, deferred, or rejected with reasons.
- Keeps publication to Hugging Face and Zenodo behind validation gates.
- For Zenodo work, uses or formally evaluates `https://github.com/zenodraft/zenodraft`.
