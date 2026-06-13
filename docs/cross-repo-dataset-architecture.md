# Cross-Repo Dataset Architecture

## Corpus family

Three sibling corpora sharing naming conventions, publication-surface rules, and a compatibility core schema:

| Corpus | Repo | Preferred label | Focus | Primary source |
|---|---|---|---|---|
| Hansard | corpus-nz-hansard | corpus-nz-hansard | Parliamentary debates | DocumentsDB extract + Bills API + Hathi Trust + Parliament website |
| Legislation | corpus-law-nz | corpus-nz-legislation | Enacted legislation | NZ Legislation API (api.legislation.govt.nz) |
| NLP | (planned) | corpus-nz-nlp | NLP outputs, embeddings | Derived from Hansard and Legislation |

**Important naming note**: The legislation repo is locally at corpus-law-nz and currently published on GitHub as edithatogo/corpus-legislation-nz, but the **preferred systematic label** (used in shared metadata, schemas, and cross-references) is **corpus-nz-legislation**. The Hansard repo is locally at corpus-nz-hansard, matching its GitHub and preferred label. See manifests/corpus_family_publication_alignment.json and the legislation corpus docs at docs/naming_publication_alignment.md for migration assessment (Track 28).

## Dataset ownership

### corpus-nz-hansard (this repo)

| Dataset | Domain | Access | Priority |
|---|---|---|---|
| DocumentsDB extract | Hansard text (Parliaments 47-54) | Local ZIP archive | Core (done) |
| Bills API (bills.parliament.nz/api/) | Bill stages, members, committees | Open REST API | High |
| Hathi Trust (coll. 71329709) | Hansard text (1854-1990) | API + web | High |
| Wikipedia MP lists (47th-54th) | Member identity, party, electorate | Web scraping | High (partial done) |
| Wikidata SPARQL | Member identity, provenance | SPARQL endpoint | High (partial done) |
| Parliament members page | Current/historical members | Radware-blocked (Playwright) | Medium |
| Roll of Members PDF | MP register (1854-) | Radware-blocked (Playwright) | Medium |
| Daily Progress / Order Paper | Sitting outcomes, agendas | Radware-blocked (Playwright) | Medium |
| Electoral Commission | Election results, candidates | Web scraping | Medium |
| Papers Past / Te Ara | Historical MP biographies | Public API | Low |

### corpus-law-nz / corpus-nz-legislation (legislation repo)

| Dataset | Domain | Access | Priority |
|---|---|---|---|
| NZ Legislation API (api.legislation.govt.nz) | Acts, regulations, bills | API key | Core (done) |
| Bills API cross-ref | Bill -> legislation.govt.nz links | Open REST API | Medium |
| NZLII | Historical bills (1854-2008) | Partially blocked | Low |
| Historical bootstrap | Legacy legislation texts (pre-API) | Batch download | Medium (Track 21-23) |

**Published surfaces** (legislation corpus):
- GitHub: https://github.com/edithatogo/corpus-legislation-nz
- Hugging Face live: https://huggingface.co/datasets/edithatogo/corpus-legislation-nz
- Hugging Face historical: https://huggingface.co/datasets/edithatogo/corpus-legislation-nz-historical
- Zenodo DOI: 10.5281/zenodo.20592540

**Notable**: The legislation corpus does **not** maintain a manifests/authority_sources.json. Its source inventory is managed through docs/source_discovery_strategy.md and docs/source_inventory_status.md. See gap note below.

### corpus-nlp (planned)

| Dataset | Source |
|---|---|
| Hansard embeddings | Derived from hansard corpus |
| Legislation embeddings | Derived from legislation corpus |
| UD/CoNLL-U linguistic annotations | Derived from both corpora |
| NIF/RDF linked data | Derived from both corpora |

## Integration scripts in this repo

| Script | Sources | Output |
|---|---|---|
| fetch_bills_api.py | Bills API | Structured bill records with member sponsors |
| fetch_hathitrust.py | Hathi Trust API | Hansard volume metadata and text |
| fetch_wikipedia_mps.py | Wikipedia 47th-54th Parliaments | MP name, party, electorate tables |
| fetch_wikidata_nz_mps.py | Wikidata SPARQL | 1,500+ MP records with provenance |
| fetch_parliament_stealth.py | Parliament website (Playwright) | Current member lists, sitting data |
| triangulate_member_identity.py | All of the above | Merged member identity records |

## Authority source IDs

See manifests/authority_sources.json for the full inventory (Hansard corpus only).

| Source ID | Corpus | Status |
|---|---|---|
| nz-parliament-members-current | hansard | Blocked (Radware) |
| nz-parliament-former-members | hansard | Open |
| nz-parliament-roll-of-members | hansard | Open (PDF, Radware-blocked) |
| nz-parliament-member-contact-downloads | hansard | Open |
| nz-parliament-parties-current | hansard | Open |
| nz-parliament-house-seating-plan | hansard | Open |
| nz-parliament-bills-current | hansard | Open (REST API) |
| nz-parliament-bills-api | hansard | Open (REST API) |
| nz-parliament-hansard-current | hansard | Blocked (Radware) |
| nz-parliament-order-paper | hansard | Open |
| nz-parliament-daily-progress | hansard | Open |
| nz-parliament-parliamentary-business-hub | hansard | Open |
| nz-parliament-weekly-journals-archive | hansard | Open |
| nz-parliament-how-to-explore-hansard | hansard | Open |
| nz-parliament-written-questions | hansard | Open |
| nz-parliament-oral-questions | hansard | Open |
| nz-parliament-parliamentary-rules | hansard | Open |
| wikipedia-nz-parliaments | hansard | Open |
| wikidata-nz-mps | hansard | Open (SPARQL) |
| hathitrust-nz-hansard | hansard | Open (API available) |
| electoral-commission-nz | hansard | Open |
| electoral-commission-election-results | hansard | Open |
| nzlii-historical-bills | both | Partially blocked |

**Gap**: The legislation corpus (corpus-law-nz) does not have an authority_sources.json manifest. Its source inventory is tracked via docs/source_discovery_strategy.md and docs/source_inventory_status.md. A future alignment track should consider adding an authority source manifest in the legislation corpus using the same schema as schemas/authority_sources.schema.json from this repo.

## Shared NZ Corpus Core Schema

Both corpora have implemented a compatible shared core schema (Track 29 in both repos):

| Field | Hansard schema | Legislation schema | Alignment |
|---|---|---|---|
| corpus_id | enum: corpus-nz-hansard, corpus-nz-legislation | Same | Aligned |
| record_id | required, string | required, string | Aligned |
| source_id | required, string | required, string | Aligned |
| jurisdiction | const: New Zealand | Same | Aligned |
| country | const: NZ | Same | Aligned |
| display_title | NOT present | required | **Gap: missing from Hansard** |
| language | NOT present | required | **Gap: missing from Hansard** |
| coverage_status | NOT present | required | **Gap: missing from Hansard** |
| rights_note | NOT present | required | **Gap: missing from Hansard** |
| document_type | smaller enum | richer enum | **Partial: legislation has more values** |
| record_schema_version | pattern requires v prefix | pattern allows optional v | **Gap: different regex** |
| effective_date | nullable date | nullable date | Aligned |
| published_date | nullable date | nullable date | Aligned |
| last_modified_date | nullable date | nullable date | Aligned |
| content_sha256 | SHA-256 hex | SHA-256 hex | Aligned |
| manifest_sha256 | SHA-256 hex | SHA-256 hex | Aligned |
| provenance | 8 required sub-fields | Same 8 sub-fields | Aligned |
| canonical_uri | required URI | required URI | Aligned |
| source_url | nullable URI | nullable URI | Aligned |
| source_version | nullable string | nullable string | Aligned |

**Schema files**:
- Hansard: schemas/shared_nz_corpus_core.schema.json
- Legislation: schemas/shared_nz_corpus_core.schema.json

**Action needed**: The Hansard shared schema should be updated to match the legislation version required fields (display_title, language, coverage_status, rights_note) and the richer document_type enum. The record_schema_version pattern should be reconciled (prefer the legislation version optional v prefix for flexibility).

## Track overlap between repos

Both repositories have independently implemented analogous tracks. The following table maps the overlap:

| Theme | Hansard track | Legislation track | Status |
|---|---|---|---|
| Corpus family naming and publication | corpus_family_naming_publication_alignment_20260609 | track_24_corpus_family_naming_and_publication_alignment | Both done |
| Cross-corpus interoperability | cross_repo_dataset_architecture_20260612 | track_25_cross_corpus_interoperability_and_metadata | Both done |
| Shared NZ corpus core schema | shared_nz_corpus_core_schema_20260609 | track_29_shared_nz_corpus_core_schema | Both done |
| Zenodo rights and zenodraft | zenodo_rights_metadata_and_zenodraft_workflow_20260609 | track_27_zenodo_rights_metadata_and_zenodraft_workflow | Both done |
| Corpus family engineering alignment | corpus_family_engineering_alignment_20260609 | (implicit in tracks 01-33) | Hansard has explicit manifest |
| Publication surface audit | (docs/corpus-family-naming-publication-alignment.md) | track_26_public_surface_audit_evidence | Legislation has dedicated track |

**Key difference - track naming convention**:
- Hansard uses: {short_descriptive_name}_{YYYYMMDD}
- Legislation uses: track_{NN}_{short_descriptive_name}

This is an acknowledged divergence. Both are valid; the legislation numbering reflects its sequential track start. Cross-repo references should use the descriptive name, not the number.

## Cross-repo document cross-references

### From Hansard to legislation corpus

The legislation corpus maintains these docs relevant to cross-repo alignment:

| Legislation doc | Relevance to Hansard |
|---|---|
| docs/cross_corpus_interoperability_hansard.md | Maps Hansard patterns to legislation decisions |
| docs/corpus-family-design.md | Publication surface model, release gates, environment alignment matrix |
| docs/corpus-family-requirements-moscow.md | MoSCoW requirements for cross-repo alignment |
| docs/shared_nz_corpus_core_schema.md | Legislation-side shared core schema definition |
| docs/naming_publication_alignment.md | Track 24 naming/publication decision |
| docs/github_repository_name_migration_assessment.md | Track 28 migration assessment |

### From legislation to Hansard

The legislation corpus references these Hansard docs:

| Hansard doc referenced by legislation | Purpose |
|---|---|
| docs/search-rag-index-contract.md | Pattern reference for optional search/RAG artifact |
| docs/rdf-linked-data-mapping.md | Pattern reference for RDF/linked data |
| docs/akoma-ntoso-mapping.md | Pattern reference for legal-document export |
| docs/endpoint-contracts.md | Pattern reference for optional derived artifacts |
| docs/interoperability-design.md | Pattern reference for interoperability design |
| docs/interoperability-requirements-moscow.md | Pattern reference for MoSCoW requirements |
| docs/sota-metadata-packages.md | Pattern reference for metadata packages |
| docs/shared-nz-corpus-core-schema.md | Shared core schema contract |
| docs/duckdb-analysis.md | DuckDB analysis examples |
| docs/generated-output-policy.md | Generated artifact policy |
| docs/canonical-id-uri-policy.md | Stable ID and URI policy |

## Identified gaps and recommended fixes

### Gap 1: Shared schema - Hansard missing four required fields
- **Issue**: Hansard schemas/shared_nz_corpus_core.schema.json missing display_title, language, coverage_status, rights_note from required list
- **Fix**: Update Hansard shared schema to match legislation version required list

### Gap 2: Shared schema - document_type enum differs
- **Issue**: Legislation has richer enum (secondary_legislation, amendment_paper, sitting, proceeding_item)
- **Fix**: Merge enum values so both schemas accept full set

### Gap 3: Shared schema - record_schema_version pattern differs
- **Issue**: Hansard requires v prefix; legislation allows optional v
- **Fix**: Adopt more flexible legislation pattern (^v?[0-9]+(\.[0-9]+){0,2}$)

### Gap 4: Legislation corpus has no manifests/authority_sources.json
- **Issue**: Legislation manages source inventory through docs, not structured manifest
- **Fix**: Evaluate adding authority source manifest using schema from this repo

### Gap 5: URI namespace not defined for legislation corpus
- **Issue**: Hansard defines https://w3id.org/nz-hansard/; legislation has no parallel namespace
- **Fix**: Define https://w3id.org/nz-legislation/ or similar in legislation corpus

### Gap 6: Naming inconsistency in cross-references
- **Issue**: Inconsistent references (corpus-law-nz vs corpus-legislation-nz vs corpus-nz-legislation)
- **Fix**: Use agreement: preferred label corpus-nz-legislation, local dir corpus-law-nz, GitHub corpus-legislation-nz

### Gap 7: No cross-repo NLP corpus planning
- **Issue**: Planned NLP corpus (corpus-nz-nlp) has no implementation or shared schema
- **Fix**: When started, establish as third sibling using same core schema and conventions

## Publication surface alignment

Both corpora follow the same publication surface model:

| Surface | Hansard | Legislation | Alignment status |
|---|---|---|---|
| GitHub (code/docs) | edithatogo/corpus-nz-hansard | edithatogo/corpus-legislation-nz | Aligned (keep-existing-url) |
| Hugging Face (datasets) | edithatogo/nz-hansard-corpus | edithatogo/corpus-legislation-nz | Aligned (keep-existing-url) |
| Zenodo (DOI archive) | 10.5281/zenodo.20595194 | 10.5281/zenodo.20592540 | Aligned |
| OSF (mirror) | Not claimed (policy-gated) | Not claimed (policy-gated) | Aligned |
| Future metadata | Not published (roadmap) | Not published (roadmap) | Aligned |

Cross-references between sibling surfaces should be maintained in GitHub repo descriptions, Hugging Face dataset card sibling links, Zenodo related identifiers, and README/CITATION.cff files in both repos.

## Conductor track conventions

### Hansard naming
`
{short_descriptive_name}_{YYYYMMDD}
`
Examples: shared_nz_corpus_core_schema_20260609, cross_repo_dataset_architecture_20260612

### Legislation naming
`
track_{NN}_{short_descriptive_name}
`
Examples: track_24_corpus_family_naming_and_publication_alignment, track_29_shared_nz_corpus_core_schema

Both conventions are accepted. Cross-repo references should use the descriptive name portion rather than the numbered prefix or date suffix.
