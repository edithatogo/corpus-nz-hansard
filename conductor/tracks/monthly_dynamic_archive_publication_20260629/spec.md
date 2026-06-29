# Spec: Monthly Dynamic Archive Publication

## Goal

Ensure the full current release archive can be rebuilt and published through GitHub Actions on a monthly cadence to Hugging Face and Zenodo, with evidence that each public surface reflects the same validated archive contents, manifest hashes, release metadata, and source-rights boundaries.

## Background

Existing Conductor tracks cover one-off publication, Zenodo rights metadata, protected Zenodo publishing, release automation hardening, and mirror activation. They do not explicitly require a scheduled monthly workflow that rebuilds the entire archive, validates it, publishes Hugging Face and Zenodo surfaces, and records cross-surface release evidence.

## Functional Requirements

- Add or update GitHub Actions so a monthly `schedule` event and manual `workflow_dispatch` can run the dynamic archive publication flow.
- Rebuild the full source-derived archive from the governed source archive input, including normalized Parquet, documentation, manifests, schemas, metadata packages, and release archive files.
- Publish or update the Hugging Face dataset with the full staged archive surface, including the canonical Parquet data and supporting docs/manifests/schemas.
- Create a Zenodo draft or new version from the latest published record, upload the full archive and manifest, and keep final production publication behind protected environment approval.
- Record public release evidence linking GitHub run ID, commit SHA, Hugging Face revision, Zenodo draft or DOI record, archive file hashes, manifest hashes, row counts, and publication boundaries.
- Keep source ZIP handling rights-safe: do not commit the source ZIP and do not publish prohibited source artifacts unless an explicit rights review approves it.
- Add validation/checker coverage for schedule configuration, required secrets, protected publication gates, manifest consistency, and cross-surface evidence.
- Document the monthly release process, rollback/retry procedure, and how to verify Hugging Face and Zenodo after a run.

## Non-Functional Requirements

- The workflow must use least-privilege GitHub permissions.
- Scheduled jobs must fail closed when required secrets, source archive access, or validation gates are missing.
- Zenodo publication must remain separated from draft creation/upload and require protected reviewer approval.
- The implementation must preserve existing `v0.1.0` DOI and Hugging Face URLs unless a new version is explicitly minted.
- Monthly releases must not overclaim full historical completeness beyond the validated source archive scope.

## Acceptance Criteria

- A scheduled monthly GitHub Actions workflow exists and can also be run manually.
- The workflow rebuilds the release archive and stages Hugging Face and Zenodo artifacts from current repository state.
- Hugging Face upload captures and records the resulting dataset revision.
- Zenodo draft/new-version upload captures and records the resulting draft or DOI details without bypassing protected publication.
- A machine-readable release evidence manifest validates with a repo-side checker.
- Documentation states what is published monthly, what remains excluded, and how to verify the public surfaces.
- Existing publication readiness checks include the monthly dynamic release path.

## Out Of Scope

- Live GitLab mirror activation; that remains tracked by `multi_git_archive_mirroring_20260614`.
- Claiming official New Zealand Parliament endorsement.
- Claiming full historical Hansard completeness beyond validated source and authority evidence.
- Publishing source ZIP contents unless a later rights-specific track approves that scope.
