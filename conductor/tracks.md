# Project Tracks

This file tracks major work items for `corpus-nz-hansard`.

---

## Status Key

- `[ ]`: pending.
- `[~]`: in progress.
- `[x]`: complete and evidence-backed.
- `[!]`: blocked.

## Active Tracks

### [ ] Track: Member Identity Resolution

Track ID: `member_identity_resolution_20260609`

Goal: resolve raw `MemberOfParliament` values into authoritative, provenance-backed member identity fields as a derived dataset layer.

Link: [conductor/tracks/member_identity_resolution_20260609/](./tracks/member_identity_resolution_20260609/)

### [ ] Track: Party Attribution With Provenance

Track ID: `party_attribution_provenance_20260609`

Goal: add provenance-backed party attribution as a temporal derived layer, dependent on validated member identity where needed.

Link: [conductor/tracks/party_attribution_provenance_20260609/](./tracks/party_attribution_provenance_20260609/)

### [ ] Track: Speech-Turn Validated Artifact Decision

Track ID: `speech_turn_validated_artifact_20260609`

Goal: promote speech-turn candidates to a validated derived artifact or explicitly keep them excluded from published final scope.

Link: [conductor/tracks/speech_turn_validated_artifact_20260609/](./tracks/speech_turn_validated_artifact_20260609/)

### [ ] Track: Derived Fields Validation Manifests

Track ID: `derived_fields_validation_manifests_20260609`

Goal: create shared validation tests and manifests for derived member, party, and speech-turn fields before any derived dataset publication.

Link: [conductor/tracks/derived_fields_validation_manifests_20260609/](./tracks/derived_fields_validation_manifests_20260609/)

## Completed Tracks

### [x] Track: Repository SOTA Hardening

Track ID: `repository_sota_hardening_20260608`

Goal: hardened the published GitHub and Hugging Face repository surfaces for discoverability, citation, provenance, release posture, and metadata quality after Zenodo DOI publication.

Link: [conductor/tracks/repository_sota_hardening_20260608/](./tracks/repository_sota_hardening_20260608/)

### [x] Track: Search and RAG Index MVP

Track ID: `search_rag_index_20260603`

Goal: built a local lexical search and citation-ready chunk index from the normalized Hansard Parquet without external embedding services.

Link: [conductor/tracks/search_rag_index_20260603/](./tracks/search_rag_index_20260603/)

### [x] Track: Speech Turn Segmentation MVP

Track ID: `speech_turn_segmentation_20260603`

Goal: built conservative document-level speech-turn segmentation tooling and validation outputs without claiming authoritative speaker attribution.

Link: [conductor/tracks/speech_turn_segmentation_20260603/](./tracks/speech_turn_segmentation_20260603/)

### [x] Track: Release Hosting and Versioning

Track ID: `release_hosting_and_versioning_20260603`

Goal: created local release/versioning artifacts and a review package without uploading or publishing any dataset.

Link: [conductor/tracks/release_hosting_and_versioning_20260603/](./tracks/release_hosting_and_versioning_20260603/)

### [x] Track: Public Dataset Readiness

Track ID: `public_dataset_readiness_20260602`

Goal: prepared repo-side public dataset release documentation, provenance, limitations, and release manifest without uploading or publishing.

Link: [conductor/tracks/public_dataset_readiness_20260602/](./tracks/public_dataset_readiness_20260602/)

### [x] Track: Hansard Corpus Pipeline MVP

Track ID: `hansard_corpus_pipeline_mvp_20260602`

Goal: built the first evidence-backed corpus pipeline from source inventory through schema discovery to manifest, Parquet, and DuckDB outputs.

Link: [conductor/tracks/hansard_corpus_pipeline_mvp_20260602/](./tracks/hansard_corpus_pipeline_mvp_20260602/)

### [x] Track: Source Inventory Verification and Manifest Generation

Track ID: `source_inventory_20260602`

Goal: auxiliary source-inventory track created during Phase 1. Implementation evidence is aligned with `hansard_corpus_pipeline_mvp_20260602` Phase 1.

Link: [conductor/tracks/source_inventory_20260602/](./tracks/source_inventory_20260602/)

## Archived Tracks

None.
