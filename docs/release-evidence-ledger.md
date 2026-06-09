# Release Evidence Ledger

Public corpus releases need a machine-readable ledger that links each released artifact to the repository state, publication surfaces, checksums, and provenance strategy used for the release.

The ledger schema is `schemas/release_evidence_ledger.schema.json`. Build a ledger with:

```powershell
python scripts/build_release_evidence_ledger.py `
  --manifest generated/zenodo/nz-hansard-corpus-0.1.0.manifest.json `
  --artifact generated/zenodo/nz-hansard-corpus-0.1.0.tar.gz `
  --huggingface-repo-id edithatogo/corpus-nz-hansard `
  --huggingface-revision <revision> `
  --zenodo-doi <doi> `
  --zenodo-concept-doi <concept-doi> `
  --record-count <records> `
  --coverage-statement "Document-level New Zealand Hansard corpus release."
```

Each ledger records the commit SHA, workflow run, Hugging Face revision, Zenodo DOI, Zenodo concept DOI, manifest hash through SHA-256 file evidence, artifact checksums, schema version, record count, and coverage statement.

## Artifact Classes

| Artifact class | Strategy | Status | Evidence |
| --- | --- | --- | --- |
| Zenodo archive tarball | GitHub artifact attestation | Enforced | `.github/workflows/zenodo_archive.yml` grants `attestations: write` and `id-token: write`, then attests `generated/zenodo/*.tar.gz`. |
| Zenodo archive manifest | GitHub artifact attestation | Enforced | The manifest is part of the attestation subject path and carries per-file SHA-256 checksums. |
| Hugging Face dataset revision | Revision and manifest hash | Documented | Hugging Face releases are verified by immutable revision plus the manifest hash/checksums recorded in the ledger. |
| GitHub review package | Signed/checksummed artifact | Documented | `scripts/build_release_package.py` emits a checksum manifest; stronger release signing is deferred to release automation. |
| Derived candidate outputs | Documented deferral | Deferred | Search indexes, DuckDB exports, speech-turn candidates, and other derived outputs are not final artifacts until validation tracks promote them. |

## Publication Gates

Publication workflows remain manually dispatched and must not run from `pull_request` or `push`. Dependency-update PRs can run quality checks, but cannot publish datasets or Zenodo records.

`scripts/check_release_provenance_policy.py` enforces the policy wiring: ledger schema requirements, documentation coverage, Zenodo attestation permissions, pinned attestation action, attestation subject paths, and manual-only publication workflows.

## Zenodo Tooling

The current workflow uses the Zenodo REST API scripts already in this repository. `zenodraft` remains a formal evaluation candidate for a future Zenodo tooling track, but it is not introduced here because the existing scripts are already wired to the repository metadata, source-archive gate, draft-upload controls, and attested archive artifact.
