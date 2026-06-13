# Parliamentary Corpus Interoperability Requirements

## Purpose

Define the long-term requirements for making `corpus-nz-hansard` a neutral parliamentary corpus core with programmatic export endpoints for multiple research, civic-data, and legal-document ecosystems.

The core dataset must remain source-faithful and standard-agnostic. ParlaMint-NZ is a core target, but it is an endpoint generated from neutral contracts rather than the primary internal schema.

## MoSCoW Requirements

### Must

- Preserve the current document-level core as the authoritative neutral base.
- Keep source archive, source file, source row, stable ID, text hash, and pipeline version provenance on every core record.
- Define derived outputs as separate, versioned artifacts with their own schema, validation manifest, and publication decision.
- Treat ParlaMint-NZ as a first-class export target for scholarly parliamentary corpus use.
- Model members, parties, speeches, votes, bills, questions, motions, sittings, and proceedings in neutral intermediate contracts before exporting to external standards.
- Record source, rule, model, confidence, validation status, and timestamp for every derived assertion.
- Keep `v0.1.0` document-level release immutable except for metadata and cross-reference corrections.
- Include explicit contribution-readiness checks for ParlaMint/Parla-CLARIN, ParlaCAP/CAP, and civic-data formats before upstream submission.
- Avoid claiming authoritative speech turns, party attribution, member identity, or voting records until validated against declared authority sources.
- Discover and version official authority sources for members, parties, offices, sittings, bills, motions, votes, and procedural structures before authoritative derived releases.
- Distinguish supplied-archive completeness from full historical NZ Hansard completeness in all release and endpoint claims.
- Define stable ID and URI policies before publishing RDF, Popolo/Open Civic Data, ParlaMint, Akoma Ntoso, or linked metadata exports.
- Maintain a release ladder that separates document-level releases, neutral component releases, endpoint releases, and upstream contribution packages.

### Should

- Add TEI/ParlaMint, Akoma Ntoso, Popolo/Open Civic Data, CAP/ParlaCAP, Universal Dependencies, PROV-O, DCAT, SKOS, and DataCite export contracts.
- Build endpoint exports from deterministic scripts that consume neutral intermediate artifacts.
- Maintain compatibility fixtures so a small representative sample can validate each endpoint before full corpus generation.
- Add automated schema validation for JSON Schema, TEI XML, RDF/SHACL, and tabular manifests where applicable.
- Align member and party authorities with official New Zealand Parliament sources when available.
- Add topic-coding support using the Comparative Agendas Project codebook and ParlaCAP-compatible outputs.
- Publish endpoint artifacts as separate versioned releases when their validation gates pass.
- Add gold/evaluation datasets for member resolution, party attribution, speech turns, votes, and topic coding.
- Add MLCommons Croissant, RO-Crate, and Frictionless Data Package metadata for dataset discovery and research-object packaging.
- Use W3C Web Annotation selectors for source text spans and offsets in speech, topic, and NLP annotation layers.
- Model NZ parliamentary procedure explicitly before treating votes, questions, stages, rulings, and interjections as validated components.

### Could

- Add entity-linking outputs for people, organizations, places, legislation, ministries, portfolios, and committees.
- Add semantic-search, embeddings, and topic-model outputs as exploratory artifacts with clear non-authoritative status.
- Add speech-act, question-answer, interjection, procedural-ruling, and debate-segment classifiers after speech-turn validation.
- Add researcher packages or client helpers for Python, R, DuckDB, and SPARQL/RDF use.
- Add static documentation pages showing the export model, validation status, and citation patterns.
- Add NIF/RDF linguistic annotation views when RDF and UD/CoNLL-U layers are mature.
- Add W3C Time modeling for temporal memberships, offices, sittings, and parliamentary periods.
- Add OntoLex-Lemon terminology or lexicon layers if a later controlled-vocabulary track needs lexical semantics.

### Won't

- Replace the neutral core schema with any single external ontology.
- Publish inferred member, party, speech-turn, vote, or topic fields as authoritative without provenance and validation.
- Treat generic NLP output as a substitute for official authority sources.
- Submit upstream contributions until the relevant endpoint passes its local contract and sample-validation gate.
- Backfill new derived fields into the immutable `v0.1.0` document-level release.
- Add heavy NLP, ML, XML, or RDF dependencies to the base install when they can be scoped to optional endpoint groups.

## Priority Order

1. Neutral component model and export architecture.
2. Authority-source discovery for members, parties, sittings, bills, and votes.
3. Historical coverage and completeness audit.
4. Stable ID and URI policy.
5. Release ladder and dependency/extras policy.
6. Shared derived-artifact validation manifests.
7. Gold/evaluation datasets.
8. Member identity resolution.
9. Party attribution.
10. Speech-turn validation decision.
11. NZ parliamentary procedure model.
12. Vote, motion, bill, and question-answer extraction.
13. ParlaMint-NZ endpoint.
14. Popolo/Open Civic Data endpoint.
15. Akoma Ntoso endpoint.
16. CAP/ParlaCAP topic endpoint.
17. Universal Dependencies and NLP annotation endpoints.
18. RDF and metadata endpoints.
19. Upstream contribution packages and submission evidence.

## Dataset Integration Requirements

### Must

- Integrate Bills API (ills.parliament.nz/api/) as an open REST authority source for bill-stage metadata, member sponsors, select committees, and legislation.govt.nz cross-references.
- Integrate HathiTrust collection 71329709 (510 full-view NZ Hansard volumes, 1854-1990) for pre-Parliament-47 coverage.
- Integrate Wikipedia MP lists (47th-54th Parliaments) as a supporting member identity source.
- Integrate Wikidata SPARQL (1,500+ NZ MP records) as a supporting member identity source with provenance chains.
- Use Playwright stealth browser for Radware-protected Parliament website pages (members list, former members, Daily Progress, Order Paper, Hansard).
- Maintain manifests/authority_sources.json as the single source of truth for all dataset sources.
- Cross-reference all member identity sources (Wikipedia, Wikidata, Bills API, Parliament website, Electoral Commission) before publishing authoritative member fields.

### Should

- Integrate Electoral Commission (elections.nz) candidate and election result data for member-term resolution.
- Integrate HathiTrust full-text OCR for historical Hansard volumes once OAuth access is obtained.
- Add Papers Past and Te Ara biographical data for historical MP verification.
- Convert older Wikipedia Parliament articles (47th-51st) from wikitable format to structured MP records.

### Could

- Access NZLII historical bills (1854-2008) as a supplementary parliamentary record source.
- Add DNZB (Dictionary of New Zealand Biography) as a supporting biographical source.

### Won't

- Claim official Parliament endorsement for any scraped or derived data.
- Replace official Parliament sources with Wikipedia or Wikidata as primary authorities.
- Attempt to bypass Radware protection through exploits or non-public methods.


## Cross-Corpus Naming And Publication-Surface Requirements

Preferred project labels:

- Hansard corpus: `corpus-nz-hansard`.
- Legislation corpus sibling: `corpus-nz-legislation` for future systematic naming, currently local path `C:\Users\60217257\OneDrive - Flinders\repos\corpus-law-nz` and published GitHub name `nz-legislation-corpus-pipeline`.

Additional MoSCoW requirements for the corpus family:

### Must

- Cross-reference `corpus-nz-legislation` in naming, publication-surface, and interoperability planning.
- Keep existing published GitHub, Hugging Face, and Zenodo URLs stable unless a migration plan protects citations, redirects, and DOI metadata.
- Include GitHub, Hugging Face, Zenodo, OSF, and future metadata environments in release-readiness tasks.
- Align README, DATASET_CARD, CITATION, release notes, manifests, DOI records, and repository metadata before declaring a release complete.
- Keep Hugging Face public access, gating state, file layout, and dataset-viewer health explicit, and fix any confirmed dataset-viewer layout issue before declaring endpoint publication complete.

### Should

- Use the legislation project as the engineering/tooling baseline for package structure, `uv`, pytest, ruff, `ty`, pre-commit, CodeQL, Scorecard, Renovate, and protected Zenodo workflows.
- Add sibling-corpus links on GitHub, Hugging Face, and Zenodo where metadata formats allow.
- Add Croissant, RO-Crate, Frictionless, DCAT, and PROV-O metadata as generated artifacts once release metadata stabilises.

### Could

- Add OSF review bundles or mirrors after file-size, checksum, citation, and update policy are documented.
- Create a common corpus-family documentation page or Hugging Face collection.

### Won't

- Rename or delete published DOI records.
- Treat OSF as the canonical operational dataset host.
- Replace source-faithful corpus records with external-standard endpoint schemas.

## Additional Implementation Recommendations

The following recommendations are part of the corpus-family roadmap and should be converted into implementation evidence before release polish is considered complete:

- Add a public-surface audit evidence ledger for GitHub, Hugging Face, Zenodo, OSF, and future metadata environments.
- Add Zenodo rights/metadata harmonisation, including license-scope review for code, docs, manifests, source text, normalized Parquet, and archive bundles.
- Add a GitHub repository-name migration assessment before moving from `nz-legislation-corpus-pipeline` toward `corpus-nz-legislation`.
- Add a shared NZ corpus core schema compatibility track covering `record_schema_version`, canonical `text`, timestamps, hashes, and provenance fields.
- Add generated SOTA metadata packages only through validated exporters: Croissant, RO-Crate, Frictionless Data Package, DCAT, and PROV-O.
- Add dataset-viewer and machine-consumability gates: dataset card parses, files are public if intended, Hugging Face viewer works or is intentionally disabled, DuckDB/PyArrow examples work, and manifest hashes are cited.
- Treat OSF as inactive until a standalone optional mirror policy is approved.

## Zenodo tooling requirement

Future Zenodo draft/archive implementation work should use or formally evaluate `zenodraft` from `https://github.com/zenodraft/zenodraft`.

Required planning points:

- `zenodraft` is a Node/npm CLI for Zenodo and Zenodo Sandbox depositions.
- It supports creating concept/version drafts, adding/deleting files, validating/updating metadata, showing draft/prereserved DOI details, and publishing drafts.
- It supports sandbox operations with `--sandbox`.
- It expects `ZENODO_ACCESS_TOKEN` and/or `ZENODO_SANDBOX_ACCESS_TOKEN` rather than this repository's current `ZENODO_TOKEN` naming, so workflows must map secrets deliberately without printing values.
- Use `npx zenodraft ...` or a pinned npm install in CI; document Node/npm version requirements before adoption.
- Publication must remain draft-first and reviewer-approved; `zenodraft deposition publish` must be gated separately from upload/update steps.
