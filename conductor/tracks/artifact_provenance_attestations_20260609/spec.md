# Spec: Artifact Provenance And Attestations

## Goal

Add release evidence ledgers, GitHub artifact attestations or SLSA-style provenance, and signed/checksummed artifact policy.

## Acceptance Criteria

- Aligns with docs/bleeding-edge-versioning-ci-quality.md.
- Preserves corpus-nz-hansard and corpus-nz-legislation naming.
- Uses Rust-backed tooling where practical: uv, ruff, typos, zizmor, taplo, and local ripgrep guidance.
- Keeps publication to Hugging Face and Zenodo behind validation gates.
- For Zenodo work, uses or formally evaluates https://github.com/zenodraft/zenodraft.
