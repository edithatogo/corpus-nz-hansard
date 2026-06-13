# Project Tracks

This file tracks major work items for `corpus-nz-hansard`.

---

## Status Key

- `[ ]`: pending.
- `[~]`: in progress.
- `[x]`: complete and evidence-backed.
- `[!]`: blocked.

## Active Tracks

### [!] Track: Corpus-Wide Member Identity Release

Track ID: `corpus_wide_member_identity_release_20260610`

Goal: promote the local member identity review package into a corpus-wide validated derived component with release gates, schemas, manifests, and non-overclaiming docs. Repo-side builder/checker are implemented; publication remains blocked pending normalized corpus input and authority coverage review.

Link: [conductor/tracks/corpus_wide_member_identity_release_20260610/](./tracks/corpus_wide_member_identity_release_20260610/)

### [!] Track: Corpus-Wide Party Attribution Release

Track ID: `corpus_wide_party_attribution_release_20260610`

Goal: promote party attribution from local/provenance fixtures into a temporal corpus-wide derived component that depends on validated member identity. Repo-side builder/checker are implemented; release remains blocked until corpus-wide member identity exists.

Link: [conductor/tracks/corpus_wide_party_attribution_release_20260610/](./tracks/corpus_wide_party_attribution_release_20260610/)

### [!] Track: Validated Speech-Turn Component Release

Track ID: `validated_speech_turn_component_release_20260610`

Goal: promote speech-turn candidates into a validated derived component only when the candidate artifact and validated member identity are both available. Repo-side builder/checker are implemented and candidate artifact exists (439 turns); release remains blocked pending validated member identity.

Link: [conductor/tracks/validated_speech_turn_component_release_20260610/](./tracks/validated_speech_turn_component_release_20260610/)

### [!] Track: Sitting And Proceeding Component Release

Track ID: `sitting_proceeding_component_release_20260610`

Goal: promote sitting/proceeding structures from design fixtures into validated corpus-wide neutral components reconciled to official sitting and proceeding evidence. Repo-side builder/checker and the comparison-ready historical ledger are implemented; release remains blocked until official historical comparison exists.

Link: [conductor/tracks/sitting_proceeding_component_release_20260610/](./tracks/sitting_proceeding_component_release_20260610/)

### [!] Track: Vote Motion Bill Question Extraction Release

Track ID: `vote_motion_bill_question_extraction_release_20260610`

Goal: implement validated corpus-wide extraction for votes, motions, bills, oral/written questions, answers, and procedural decisions with provenance. Repo-side builder/checker are implemented; release remains blocked until validated member identity, party attribution, and sitting/proceeding components exist.

Link: [conductor/tracks/vote_motion_bill_question_extraction_release_20260610/](./tracks/vote_motion_bill_question_extraction_release_20260610/)

### [!] Track: ParlaMint-NZ Public Endpoint Release

Track ID: `parlamint_nz_public_endpoint_release_20260610`

Goal: move ParlaMint-NZ from endpoint contract/sample readiness to a scope-declared public release package with schema validation and maintainer-facing evidence. Repo-side builder/checker are implemented; release remains blocked until validated member identity, party attribution, speech-turn, and sitting/proceeding components exist.

Link: [conductor/tracks/parlamint_nz_public_endpoint_release_20260610/](./tracks/parlamint_nz_public_endpoint_release_20260610/)

### [!] Track: Popolo/Open Civic Data Public Endpoint Release

Track ID: `popolo_opencivicdata_public_endpoint_release_20260610`

Goal: move Popolo/Open Civic Data from sample output to a validated public endpoint release. Repo-side builder/checker are implemented; release remains blocked pending validated member identity, party attribution, vote/motion extraction, and speech-turn components.

Link: [conductor/tracks/popolo_opencivicdata_public_endpoint_release_20260610/](./tracks/popolo_opencivicdata_public_endpoint_release_20260610/)

### [!] Track: Akoma Ntoso Public Endpoint Release

Track ID: `akoma_ntoso_public_endpoint_release_20260610`

Goal: move Akoma Ntoso from sample output to a validated public endpoint release with selected profile/schema evidence and source-span preservation. Repo-side builder/checker are implemented; release is blocked pending validated member identity, party attribution, speech-turn, motion, and vote components.

Link: [conductor/tracks/akoma_ntoso_public_endpoint_release_20260610/](./tracks/akoma_ntoso_public_endpoint_release_20260610/)

### [!] Track: CAP/ParlaCAP Public Endpoint Release

Track ID: `cap_parlacap_public_endpoint_release_20260610`

Goal: move CAP/ParlaCAP from sample topic output to a validated public release after topic codebooks, speech/proceeding units, and maintainer expectations are settled. Repo-side builder/checker are implemented; release is blocked pending validated speech-turn components and maintainer-confirmed codebook intake.

Link: [conductor/tracks/cap_parlacap_public_endpoint_release_20260610/](./tracks/cap_parlacap_public_endpoint_release_20260610/)

### [!] Track: UD/CoNLL-U Public Endpoint Release

Track ID: `ud_conllu_public_endpoint_release_20260610`

Goal: move UD/CoNLL-U from sample output to a validated NLP endpoint release with tokenizer/parser pinning, offset fidelity, and scope-declared coverage. Repo-side builder/checker are implemented; release is blocked pending validated speech-turn text and completed Stanza/spaCy comparison evidence.

Link: [conductor/tracks/ud_conllu_public_endpoint_release_20260610/](./tracks/ud_conllu_public_endpoint_release_20260610/)

### [!] Track: RDF Linked Data Public Endpoint Release

Track ID: `rdf_linked_data_public_endpoint_release_20260610`

Goal: move RDF/JSON-LD from sample graph output to a validated public linked-data release with SHACL, stable URIs, PROV-O/DCAT/SKOS/W3C Time, and SPARQL examples.

Link: [conductor/tracks/rdf_linked_data_public_endpoint_release_20260610/](./tracks/rdf_linked_data_public_endpoint_release_20260610/)

### [x] Track: DataCite Export Contract

Track ID: `datacite_export_contract_20260610`

Goal: add the missing DataCite export contract and generated metadata payload so publication packages can target DOI-hosting workflows cleanly.

Link: [conductor/tracks/datacite_export_contract_20260610/](./tracks/datacite_export_contract_20260610/)

### [x] Track: W3C Web Annotation Selector Contract

Track ID: `web_annotation_selector_contract_20260610`

Goal: standardize text/source-span selectors across derived components, endpoint annotations, search chunks, RDF links, and NLP outputs.

Link: [conductor/tracks/web_annotation_selector_contract_20260610/](./tracks/web_annotation_selector_contract_20260610/)

### [x] Track: Upstream Submission Execution

Track ID: `upstream_submission_execution_20260610`

Goal: convert maintainer-review package drafts into real upstream submission handoffs only after endpoint release gates pass, with submission and feedback evidence.

Link: [conductor/tracks/upstream_submission_execution_20260610/](./tracks/upstream_submission_execution_20260610/)

### [x] Track: Researcher Client Helpers

Track ID: `researcher_client_helpers_20260610`

Goal: add practical Python, R, DuckDB, and SPARQL helper examples for consuming document-level and endpoint artifacts without changing core data semantics.

Link: [conductor/tracks/researcher_client_helpers_20260610/](./tracks/researcher_client_helpers_20260610/)

### [x] Track: Static Documentation Portal

Track ID: `static_documentation_portal_20260610`

Goal: publish a static documentation surface showing export models, validation status, citation patterns, release ladder state, and endpoint readiness.

Link: [conductor/tracks/static_documentation_portal_20260610/](./tracks/static_documentation_portal_20260610/)

### [x] Track: Entity Linking Exploratory Outputs

Track ID: `entity_linking_exploratory_outputs_20260610`

Goal: add non-authoritative entity-linking outputs for people, organisations, places, legislation, ministries, portfolios, and committees with explicit exploratory status.

Link: [conductor/tracks/entity_linking_exploratory_outputs_20260610/](./tracks/entity_linking_exploratory_outputs_20260610/)

### [x] Track: Semantic Search Embeddings And Topic Models

Track ID: `semantic_search_embeddings_topics_20260610`

Goal: add exploratory embeddings and topic-model outputs with model cards, manifests, optional dependencies, and non-authoritative publication boundaries.

Link: [conductor/tracks/semantic_search_embeddings_topics_20260610/](./tracks/semantic_search_embeddings_topics_20260610/)

### [!] Track: Speech-Act And Procedure Classifiers

Track ID: `speech_act_procedure_classifiers_20260610`

Goal: add validated classifiers for speech acts, question/answer structure, interjections, procedural rulings, and debate segments after speech-turn components mature. Blocked until validated speech-turn components and procedure readiness are available.

Link: [conductor/tracks/speech_act_procedure_classifiers_20260610/](./tracks/speech_act_procedure_classifiers_20260610/)

### [!] Track: NIF/RDF Linguistic Annotation Views

Track ID: `nif_rdf_linguistic_views_20260610`

Goal: add NIF/RDF linguistic annotation views that connect token and sentence annotations to stable selectors once RDF and UD layers mature.

Link: [conductor/tracks/nif_rdf_linguistic_views_20260610/](./tracks/nif_rdf_linguistic_views_20260610/)

### [!] Track: W3C Time Temporal Model

Track ID: `w3c_time_temporal_model_20260610`

Goal: model parliamentary periods, sittings, offices, party memberships, and role intervals using W3C Time-compatible structures.

Link: [conductor/tracks/w3c_time_temporal_model_20260610/](./tracks/w3c_time_temporal_model_20260610/)

### [!] Track: OntoLex-Lemon Terminology Layer

Track ID: `ontolex_lemon_terminology_layer_20260610`

Goal: add an optional terminology/lexicon layer for NZ parliamentary and legal vocabulary if downstream RDF and NLP use cases need it.

Link: [conductor/tracks/ontolex_lemon_terminology_layer_20260610/](./tracks/ontolex_lemon_terminology_layer_20260610/)

### [!] Track: Full Historical Sitting Reconciliation

Track ID: `full_historical_sitting_reconciliation_20260610`

Goal: move from supplied-archive coverage auditing to official full historical sitting/proceeding reconciliation before making completeness claims.

Link: [conductor/tracks/full_historical_sitting_reconciliation_20260610/](./tracks/full_historical_sitting_reconciliation_20260610/)

### [!] Track: Package And CLI Migration Execution

Track ID: `package_cli_migration_execution_20260610`

Goal: execute the package/CLI migration plan from corpus-family engineering alignment while preserving existing quality gates and release behaviour.

Link: [conductor/tracks/package_cli_migration_execution_20260610/](./tracks/package_cli_migration_execution_20260610/)

### [x] Track: Akoma Ntoso Endpoint

Track ID: `akoma_ntoso_endpoint_20260609`

Goal: generate Akoma Ntoso-style legislative and parliamentary document structure from validated neutral proceeding components.

Link: [conductor/tracks/akoma_ntoso_endpoint_20260609/](./tracks/akoma_ntoso_endpoint_20260609/)

### [x] Track: CAP / ParlaCAP Topic Endpoint

Track ID: `cap_parlacap_topic_endpoint_20260609`

Goal: create Comparative Agendas Project and ParlaCAP-compatible topic outputs with codebook provenance and validation.

Link: [conductor/tracks/cap_parlacap_topic_endpoint_20260609/](./tracks/cap_parlacap_topic_endpoint_20260609/)

### [x] Track: Universal Dependencies / CoNLL-U Endpoint

Track ID: `ud_conllu_endpoint_20260609`

Goal: create validated Universal Dependencies and CoNLL-U linguistic annotation outputs with token-to-source alignment.

Link: [conductor/tracks/ud_conllu_endpoint_20260609/](./tracks/ud_conllu_endpoint_20260609/)

### [x] Track: RDF Linked Data Endpoint

Track ID: `rdf_linked_data_endpoint_20260609`

Goal: publish RDF/JSON-LD views with PROV-O, DCAT, SKOS, stable URIs, and SHACL validation.

Link: [conductor/tracks/rdf_linked_data_endpoint_20260609/](./tracks/rdf_linked_data_endpoint_20260609/)

### [x] Track: Upstream Contribution Packages

Track ID: `upstream_contribution_packages_20260609`

Goal: prepare validation-backed samples, mapping notes, and contribution evidence for ParlaMint/Parla-CLARIN, ParlaCAP/CAP, mySociety-style parser references, and related ecosystems.

Link: [conductor/tracks/upstream_contribution_packages_20260609/](./tracks/upstream_contribution_packages_20260609/)

### [x] Track: Member Identity Resolution

Track ID: `member_identity_resolution_20260609`

Goal: resolve raw `MemberOfParliament` values into authoritative, provenance-backed member identity fields as a derived dataset layer.

Link: [conductor/tracks/member_identity_resolution_20260609/](./tracks/member_identity_resolution_20260609/)

### [x] Track: Party Attribution With Provenance

Track ID: `party_attribution_provenance_20260609`

Goal: add provenance-backed party attribution as a temporal derived layer, dependent on validated member identity where needed.

Link: [conductor/tracks/party_attribution_provenance_20260609/](./tracks/party_attribution_provenance_20260609/)

### [x] Track: Speech-Turn Validated Artifact Decision

Track ID: `speech_turn_validated_artifact_20260609`

Goal: promote speech-turn candidates to a validated derived artifact or explicitly keep them excluded from published final scope.

Link: [conductor/tracks/speech_turn_validated_artifact_20260609/](./tracks/speech_turn_validated_artifact_20260609/)

### [x] Track: Derived Fields Validation Manifests

Track ID: `derived_fields_validation_manifests_20260609`

Goal: create shared validation tests and manifests for derived member, party, and speech-turn fields before any derived dataset publication.

Link: [conductor/tracks/derived_fields_validation_manifests_20260609/](./tracks/derived_fields_validation_manifests_20260609/)



### [~] Track: Bills API Integration

Track ID: ills_api_integration_20260612

Goal: Integrate open REST API from bills.parliament.nz as an authority source for bill-stage metadata, member sponsors, select committees, and legislation.govt.nz cross-references. 3,513 bills extracted, 351 unique member names.

Link: [conductor/tracks/bills_api_integration_20260612/](./tracks/bills_api_integration_20260612/)

### [~] Track: Wikipedia MP Lists Acquisition

Track ID: wikipedia_mp_lists_acquisition_20260612

Goal: Extract structured MP name, party, and electorate data from Wikipedia articles for Parliaments 47-53. 249 MPs extracted from Parliaments 52-53.

Link: [conductor/tracks/wikipedia_mp_lists_acquisition_20260612/](./tracks/wikipedia_mp_lists_acquisition_20260612/)

### [ ] Track: HathiTrust Hansard Acquisition

Track ID: hathitrust_hansard_acquisition_20260612

Goal: Acquire 510 full-view NZ Parliamentary Debates volumes (1854-1990) from HathiTrust collection 71329709 via OAuth API.

Link: [conductor/tracks/hathitrust_hansard_acquisition_20260612/](./tracks/hathitrust_hansard_acquisition_20260612/)

### [~] Track: Parliament Website Stealth Access

Track ID: parliament_website_stealth_access_20260612

Goal: Access Radware-protected NZ Parliament website pages using Playwright stealth browser techniques. All 5 target pages successfully fetched.

Link: [conductor/tracks/parliament_website_stealth_access_20260612/](./tracks/parliament_website_stealth_access_20260612/)

### [~] Track: Member Identity Triangulation

Track ID: member_identity_triangulation_20260612

Goal: Cross-reference multiple authority sources (Wikipedia, Wikidata, Bills API, Parliament website, Electoral Commission) to resolve and validate member identity. 51/51 names resolved (100%).

Link: [conductor/tracks/member_identity_triangulation_20260612/](./tracks/member_identity_triangulation_20260612/)

### [x] Track: Cross-Repo Dataset Architecture

Track ID: cross_repo_dataset_architecture_20260612

Goal: Define dataset ownership boundaries between corpus-nz-hansard, corpus-law-nz (legislation), and planned corpus-nlp (NLP). Documented in docs/cross-repo-dataset-architecture.md.

Link: [conductor/tracks/cross_repo_dataset_architecture_20260612/](./tracks/cross_repo_dataset_architecture_20260612/)

### [!] Track: NZLII Historical Acquisition

Track ID: 
zlii_historical_acquisition_20260612

Goal: Access historical NZ parliamentary content from NZLII (1854-2008 bills). Currently blocked (HTTP 403). Deferred in favour of HathiTrust.

Link: [conductor/tracks/nzlii_historical_acquisition_20260612/](./tracks/nzlii_historical_acquisition_20260612/)

## Completed Tracks

### [x] Track: Popolo / Open Civic Data Endpoint

Track ID: `popolo_opencivicdata_endpoint_20260609`

Goal: Generated a Popolo/Open Civic Data maintainer-review sample package, mapping notes, validation manifest, checker, and readiness boundary without inferring full voting records from text patterns alone.

Link: [conductor/tracks/popolo_opencivicdata_endpoint_20260609/](./tracks/popolo_opencivicdata_endpoint_20260609/)

### [x] Track: ParlaMint-NZ Endpoint

Track ID: `parlamint_nz_endpoint_20260609`

Goal: Generated a ParlaMint-NZ maintainer-review TEI sample package, mapping notes, validation manifest, checker, and readiness boundary without making ParlaMint the internal core schema.

Link: [conductor/tracks/parlamint_nz_endpoint_20260609/](./tracks/parlamint_nz_endpoint_20260609/)

### [x] Track: Neutral Parliamentary Component Model

Track ID: `neutral_component_model_20260609`

Goal: Defined machine-readable neutral component schemas, stable ID requirements, fixture rows, validation manifest, referential-integrity gates, and publication boundaries.

Link: [conductor/tracks/neutral_component_model_20260609/](./tracks/neutral_component_model_20260609/)

### [x] Track: NZ Parliamentary Procedure Model

Track ID: `nz_parliamentary_procedure_model_20260609`

Goal: Modelled NZ-specific procedure categories, authority-source requirements, boundary fixtures, uncertainty policy, release gates, and endpoint mappings.

Link: [conductor/tracks/nz_parliamentary_procedure_model_20260609/](./tracks/nz_parliamentary_procedure_model_20260609/)

### [x] Track: Dependency Extras Policy

Track ID: `dependency_extras_policy_20260609`

Goal: Kept the base runtime minimal with a validated optional dependency-group policy, endpoint dependency citations, deferred install-check rules, and release-artifact pinning requirements.

Link: [conductor/tracks/dependency_extras_policy_20260609/](./tracks/dependency_extras_policy_20260609/)

### [x] Track: Canonical ID and URI Policy

Track ID: `canonical_id_uri_policy_20260609`

Goal: Defined stable ID and URI patterns, deterministic examples, namespace guidance, deprecation mapping policy, and endpoint validation gates.

Link: [conductor/tracks/canonical_id_uri_policy_20260609/](./tracks/canonical_id_uri_policy_20260609/)

### [x] Track: Gold Evaluation Datasets

Track ID: `gold_evaluation_datasets_20260609`

Goal: Created reviewed evaluation schemas, fixtures, metrics, and gates for member resolution, party attribution, speech turns, votes, and topic coding.

Link: [conductor/tracks/gold_evaluation_datasets_20260609/](./tracks/gold_evaluation_datasets_20260609/)

### [x] Track: Release Ladder

Track ID: `release_ladder_20260609`

Goal: Defined document-level, authority-source, neutral-component, endpoint, and upstream-contribution release levels with artifact mappings, manifest fields, publication gates, checker, and docs.

Link: [conductor/tracks/release_ladder_20260609/](./tracks/release_ladder_20260609/)

### [x] Track: Historical Coverage Audit

Track ID: `historical_coverage_audit_20260609`

Goal: Distinguished supplied DocumentsDB extract completeness from full historical NZ Hansard completeness with coverage manifest, report, quality-gate checker, and release/endpoint guardrails.

Link: [conductor/tracks/historical_coverage_audit_20260609/](./tracks/historical_coverage_audit_20260609/)

### [x] Track: Authority Source Discovery

Track ID: `authority_source_discovery_20260609`

Goal: Identified official-first authority source candidates for members, parties, offices, sittings, bills, motions, votes, and procedure, with manifest schema, reuse/coverage notes, hashes, and downstream unblockers.

Link: [conductor/tracks/authority_source_discovery_20260609/](./tracks/authority_source_discovery_20260609/)

### [x] Track: Corpus Family Engineering Alignment

Track ID: `corpus_family_engineering_alignment_20260609`

Goal: Recorded the legislation-project engineering baseline and an implementation-ready package/CLI migration plan while preserving Hansard's strict script-workspace quality gate and publication boundaries.

Link: [conductor/tracks/corpus_family_engineering_alignment_20260609/](./tracks/corpus_family_engineering_alignment_20260609/)

### [x] Track: Zenodo Rights Metadata And Zenodraft Workflow

Track ID: `zenodo_rights_metadata_and_zenodraft_workflow_20260609`

Goal: Harmonised Zenodo rights metadata and completed sandbox draft/upload/update/readback proof for generated metadata packages while preserving the protected production publication gate.

Link: [conductor/tracks/zenodo_rights_metadata_and_zenodraft_workflow_20260609/](./tracks/zenodo_rights_metadata_and_zenodraft_workflow_20260609/)

### [x] Track: SOTA Metadata Packages

Track ID: `sota_metadata_packages_20260609`

Goal: Generated validated Croissant, RO-Crate, Frictionless, DCAT, and PROV-O metadata packages with checksums, deterministic exporter, and package-specific quality-gate validation. Live Zenodo Sandbox proof remains tracked by `zenodo_rights_metadata_and_zenodraft_workflow_20260609`.

Link: [conductor/tracks/sota_metadata_packages_20260609/](./tracks/sota_metadata_packages_20260609/)

### [x] Track: Corpus Family Naming And Publication Alignment

Track ID: `corpus_family_naming_publication_alignment_20260609`

Goal: keep `corpus-nz-hansard` aligned with preferred sibling label `corpus-nz-legislation` across GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.

Link: [conductor/tracks/corpus_family_naming_publication_alignment_20260609/](./tracks/corpus_family_naming_publication_alignment_20260609/)

### [x] Track: OSF Optional Mirror Policy

Track ID: `osf_optional_mirror_policy_20260609`

Goal: Decide whether OSF is unused, a review-bundle host, or an optional mirror with checksums and citation policy.

Link: [conductor/tracks/osf_optional_mirror_policy_20260609/](./tracks/osf_optional_mirror_policy_20260609/)

### [x] Track: Shared NZ Corpus Core Schema

Track ID: `shared_nz_corpus_core_schema_20260609`

Goal: Define shared core fields and compatibility expectations across legislation and Hansard.

Link: [conductor/tracks/shared_nz_corpus_core_schema_20260609/](./tracks/shared_nz_corpus_core_schema_20260609/)

### [x] Track: SOTA CI/CD Code Quality And Rust Tooling

Track ID: `sota_cicd_code_quality_rust_tooling_20260609`

Goal: Adopt SOTA CI/code-quality automation using Rust-backed tools where possible: uv, ruff, ty, typos, zizmor, taplo, plus actionlint.

Link: [conductor/tracks/sota_cicd_code_quality_rust_tooling_20260609/](./tracks/sota_cicd_code_quality_rust_tooling_20260609/)

### [x] Track: Hugging Face Viewer Layout Fix

Track ID: `huggingface_viewer_layout_fix_20260609`

Goal: Verify and fix any confirmed Hugging Face viewer split/cast or file-layout issue, then add layout regression checks.

Link: [conductor/tracks/huggingface_viewer_layout_fix_20260609/](./tracks/huggingface_viewer_layout_fix_20260609/)

### [x] Track: Public Surface Audit Evidence

Track ID: `public_surface_audit_evidence_20260609`

Goal: Create an evidence ledger for GitHub, Hugging Face, Zenodo, OSF, and future metadata surfaces.

Link: [conductor/tracks/public_surface_audit_evidence_20260609/](./tracks/public_surface_audit_evidence_20260609/)

### [x] Track: Artifact Provenance And Attestations

Track ID: `artifact_provenance_attestations_20260609`

Goal: Add release evidence ledgers, GitHub artifact attestations or SLSA-style provenance, and signed/checksummed artifact policy.

Link: [conductor/tracks/artifact_provenance_attestations_20260609/](./tracks/artifact_provenance_attestations_20260609/)

### [x] Track: Bleeding Edge Versioning And Release Automation

Track ID: `bleeding_edge_versioning_release_automation_20260609`

Goal: Implement SemVer/dataset/schema version governance, Release Please-style changelog automation, and consistency checks.

Link: [conductor/tracks/bleeding_edge_versioning_release_automation_20260609/](./tracks/bleeding_edge_versioning_release_automation_20260609/)

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
