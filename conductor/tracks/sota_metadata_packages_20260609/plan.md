# Plan: SOTA Metadata Packages

## Tasks

- [x] Confirm current public-surface state and existing local implementation.
- [x] Define the intended target state and migration constraints.
- [x] Update docs and tests or validation scripts needed for this area.
- [x] Record GitHub/Hugging Face/Zenodo/OSF/future-metadata implications.
- [x] Generate Croissant, RO-Crate, Frictionless, DCAT, and PROV-O package files.
- [x] Populate SHA-256 checksums for generated package files.
- [x] Wire package-specific validation into the shared metadata-package gate.
- [x] For Zenodo-related work, preserve sandbox-first token mapping and protected publish gate. Live Zenodo Sandbox proof remains governed by `zenodo_rights_metadata_and_zenodraft_workflow_20260609`.
- [x] Record evidence and command outputs.

## Verification

- [x] Metadata JSON parses.
- [x] Track is registered in conductor/tracks.md.
- [x] Acceptance criteria are linked to release or maintenance docs.
