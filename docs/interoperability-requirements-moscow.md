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

### Should

- Add TEI/ParlaMint, Akoma Ntoso, Popolo/Open Civic Data, CAP/ParlaCAP, Universal Dependencies, PROV-O, DCAT, SKOS, and DataCite export contracts.
- Build endpoint exports from deterministic scripts that consume neutral intermediate artifacts.
- Maintain compatibility fixtures so a small representative sample can validate each endpoint before full corpus generation.
- Add automated schema validation for JSON Schema, TEI XML, RDF/SHACL, and tabular manifests where applicable.
- Align member and party authorities with official New Zealand Parliament sources when available.
- Add topic-coding support using the Comparative Agendas Project codebook and ParlaCAP-compatible outputs.
- Publish endpoint artifacts as separate versioned releases when their validation gates pass.

### Could

- Add entity-linking outputs for people, organizations, places, legislation, ministries, portfolios, and committees.
- Add semantic-search, embeddings, and topic-model outputs as exploratory artifacts with clear non-authoritative status.
- Add speech-act, question-answer, interjection, procedural-ruling, and debate-segment classifiers after speech-turn validation.
- Add researcher packages or client helpers for Python, R, DuckDB, and SPARQL/RDF use.
- Add static documentation pages showing the export model, validation status, and citation patterns.

### Won't

- Replace the neutral core schema with any single external ontology.
- Publish inferred member, party, speech-turn, vote, or topic fields as authoritative without provenance and validation.
- Treat generic NLP output as a substitute for official authority sources.
- Submit upstream contributions until the relevant endpoint passes its local contract and sample-validation gate.
- Backfill new derived fields into the immutable `v0.1.0` document-level release.

## Priority Order

1. Neutral component model and export architecture.
2. Authority-source discovery for members, parties, sittings, bills, and votes.
3. Shared derived-artifact validation manifests.
4. Member identity resolution.
5. Party attribution.
6. Speech-turn validation decision.
7. Vote, motion, bill, and question-answer extraction.
8. ParlaMint-NZ endpoint.
9. Popolo/Open Civic Data endpoint.
10. Akoma Ntoso endpoint.
11. CAP/ParlaCAP topic endpoint.
12. Universal Dependencies and NLP annotation endpoints.
13. Upstream contribution packages and submission evidence.

