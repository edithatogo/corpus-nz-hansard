# Project Tracks

This file tracks major work items for `corpus-nz-hansard`.

---

## Status Key

- `[ ]`: pending.
- `[~]`: in progress.
- `[x]`: complete and evidence-backed.
- `[!]`: blocked.

## Active Tracks

### [ ] Track: Authority Source Discovery

Track ID: `authority_source_discovery_20260609`

Goal: identify, retrieve, version, hash, and assess reuse constraints for official authority sources covering members, parties, offices, sittings, bills, motions, votes, and procedure.

Link: [conductor/tracks/authority_source_discovery_20260609/](./tracks/authority_source_discovery_20260609/)

### [ ] Track: Historical Coverage Audit

Track ID: `historical_coverage_audit_20260609`

Goal: distinguish supplied DocumentsDB extract completeness from full historical NZ Hansard completeness and publish coverage claims with evidence.

Link: [conductor/tracks/historical_coverage_audit_20260609/](./tracks/historical_coverage_audit_20260609/)

### [ ] Track: Release Ladder

Track ID: `release_ladder_20260609`

Goal: define document-level, authority-source, neutral-component, endpoint, and upstream-contribution release levels with publication gates.

Link: [conductor/tracks/release_ladder_20260609/](./tracks/release_ladder_20260609/)

### [ ] Track: Gold Evaluation Datasets

Track ID: `gold_evaluation_datasets_20260609`

Goal: create reviewed evaluation fixtures for member resolution, party attribution, speech turns, votes, and topic coding.

Link: [conductor/tracks/gold_evaluation_datasets_20260609/](./tracks/gold_evaluation_datasets_20260609/)

### [ ] Track: Canonical ID and URI Policy

Track ID: `canonical_id_uri_policy_20260609`

Goal: define stable identifier and URI policies before RDF, Popolo/Open Civic Data, ParlaMint, Akoma Ntoso, and metadata endpoint publication.

Link: [conductor/tracks/canonical_id_uri_policy_20260609/](./tracks/canonical_id_uri_policy_20260609/)

### [ ] Track: Dependency Extras Policy

Track ID: `dependency_extras_policy_20260609`

Goal: keep the base runtime minimal while governing optional XML, RDF, NLP, ML, metadata, schema, and authority-matching dependency groups.

Link: [conductor/tracks/dependency_extras_policy_20260609/](./tracks/dependency_extras_policy_20260609/)

### [ ] Track: NZ Parliamentary Procedure Model

Track ID: `nz_parliamentary_procedure_model_20260609`

Goal: model NZ-specific parliamentary procedure for party votes, personal votes, questions, supplementary questions, stages, rulings, interjections, and procedural units.

Link: [conductor/tracks/nz_parliamentary_procedure_model_20260609/](./tracks/nz_parliamentary_procedure_model_20260609/)

### [ ] Track: Neutral Parliamentary Component Model

Track ID: `neutral_component_model_20260609`

Goal: define schemas, identifiers, provenance, and validation manifests for neutral derived components that feed all endpoint exports.

Link: [conductor/tracks/neutral_component_model_20260609/](./tracks/neutral_component_model_20260609/)

### [ ] Track: ParlaMint-NZ Endpoint

Track ID: `parlamint_nz_endpoint_20260609`

Goal: generate validated ParlaMint-NZ / TEI artifacts from neutral components without making ParlaMint the internal core schema.

Link: [conductor/tracks/parlamint_nz_endpoint_20260609/](./tracks/parlamint_nz_endpoint_20260609/)

### [ ] Track: Popolo / Open Civic Data Endpoint

Track ID: `popolo_opencivicdata_endpoint_20260609`

Goal: generate civic-data member, party, membership, speech, motion, and vote artifacts compatible with Popolo/Open Civic Data patterns.

Link: [conductor/tracks/popolo_opencivicdata_endpoint_20260609/](./tracks/popolo_opencivicdata_endpoint_20260609/)

### [ ] Track: Akoma Ntoso Endpoint

Track ID: `akoma_ntoso_endpoint_20260609`

Goal: generate Akoma Ntoso-style legislative and parliamentary document structure from validated neutral proceeding components.

Link: [conductor/tracks/akoma_ntoso_endpoint_20260609/](./tracks/akoma_ntoso_endpoint_20260609/)

### [ ] Track: CAP / ParlaCAP Topic Endpoint

Track ID: `cap_parlacap_topic_endpoint_20260609`

Goal: create Comparative Agendas Project and ParlaCAP-compatible topic outputs with codebook provenance and validation.

Link: [conductor/tracks/cap_parlacap_topic_endpoint_20260609/](./tracks/cap_parlacap_topic_endpoint_20260609/)

### [ ] Track: Universal Dependencies / CoNLL-U Endpoint

Track ID: `ud_conllu_endpoint_20260609`

Goal: create validated Universal Dependencies and CoNLL-U linguistic annotation outputs with token-to-source alignment.

Link: [conductor/tracks/ud_conllu_endpoint_20260609/](./tracks/ud_conllu_endpoint_20260609/)

### [ ] Track: RDF Linked Data Endpoint

Track ID: `rdf_linked_data_endpoint_20260609`

Goal: publish RDF/JSON-LD views with PROV-O, DCAT, SKOS, stable URIs, and SHACL validation.

Link: [conductor/tracks/rdf_linked_data_endpoint_20260609/](./tracks/rdf_linked_data_endpoint_20260609/)

### [ ] Track: Upstream Contribution Packages

Track ID: `upstream_contribution_packages_20260609`

Goal: prepare validation-backed samples, mapping notes, and contribution evidence for ParlaMint/Parla-CLARIN, ParlaCAP/CAP, mySociety-style parser references, and related ecosystems.

Link: [conductor/tracks/upstream_contribution_packages_20260609/](./tracks/upstream_contribution_packages_20260609/)

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
