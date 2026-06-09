# Endpoint Contracts

## Purpose

Define the required contract surface for generated endpoint artifacts. Each endpoint consumes the neutral document core plus validated derived component artifacts.

## Shared Endpoint Requirements

Every endpoint must declare:

- endpoint name
- endpoint version
- external schema or ontology version
- input artifacts
- output artifacts
- validation command
- validation manifest
- publication target
- upstream contribution target
- known exclusions
- release status
- release ladder level
- authority-source dependencies
- stable ID or URI policy reference
- gold/evaluation dataset dependencies where applicable

## ParlaMint-NZ / TEI

Target users: corpus linguistics and comparative parliamentary researchers.

Inputs:

- normalized document records
- validated sitting components
- validated speech-turn components
- validated member and party components
- optional linguistic annotations

Outputs:

- ParlaMint-compatible TEI XML files
- ParlaMint metadata files
- validation manifest
- representative sample package for contribution review

Validation gates:

- TEI XML well-formedness.
- ParlaMint schema validation.
- Speaker references resolve to member metadata.
- Party references resolve to temporal party metadata.
- Sample package includes known NZ-specific encoding notes.

Upstream path:

- prepare ParlaMint-NZ samples and validation evidence before approaching ParlaMint maintainers.
- use Parla-CLARIN for schema examples, edge cases, or encoding feedback discovered during implementation.

## Popolo / Open Civic Data

Target users: civic technology, member-history, and voting-record consumers.

Inputs:

- member components
- party and membership components
- speech turns
- motions
- vote events
- bills or legislative items

Outputs:

- JSON or JSONL people, organizations, memberships, posts, motions, vote events, and votes.
- optional RDF linked-data view.
- validation manifest.

Validation gates:

- every vote references a valid motion or explicit procedural question.
- every individual vote references a resolved member.
- every party vote references a resolved party.
- date ranges for memberships are not contradictory.

Upstream path:

- publish NZ-compatible artifacts locally first.
- contribute parser patterns, fixtures, or schema notes to mySociety/parlparse only if maintainers accept the cross-jurisdiction scope.

## Akoma Ntoso

Target users: legal informatics and legislative-document workflows.

Inputs:

- document records
- sitting components
- proceeding items
- bills
- motions
- vote events
- questions and answers

Outputs:

- Akoma Ntoso XML documents or fragments.
- validation manifest.
- mapping notes for NZ parliamentary structures.

Validation gates:

- XML well-formedness.
- schema validation where a selected Akoma Ntoso profile is available.
- document hierarchy preserves source order and source provenance.

## CAP / ParlaCAP

Target users: agenda-setting, policy-topic, and comparative politics researchers.

Inputs:

- document records
- speech turns or proceeding items
- topic assignments
- coding authority metadata

Outputs:

- CAP-coded tabular artifacts.
- ParlaCAP-compatible speech/topic outputs when speech turns are validated.
- coding manifest.

Validation gates:

- every topic code references a declared codebook version.
- every coded unit references a source component.
- model-coded labels are clearly separated from human-coded labels.

## Universal Dependencies / CoNLL-U

Target users: NLP researchers.

Inputs:

- validated speech turns or document text segments.
- linguistic annotations.

Outputs:

- CoNLL-U files.
- token/sentence alignment manifests.
- validation manifest.

Validation gates:

- CoNLL-U parses with `conllu` or equivalent validator.
- token offsets map back to source text.
- language, tokenizer, parser, and model versions are recorded.

## RDF / Linked Data

Target users: semantic-web and linked-data researchers.

Inputs:

- neutral component tables.
- provenance artifacts.
- endpoint identifiers.

Outputs:

- RDF Turtle or JSON-LD.
- SHACL shapes.
- DCAT dataset metadata.
- PROV-O provenance graph.
- SKOS concept schemes.

Validation gates:

- RDF parses with `rdflib`.
- SHACL validation passes for required shapes.
- every generated URI is stable and documented.

## Croissant / RO-Crate / Frictionless

Target users: ML dataset consumers, archival users, and tabular-data tooling.

Inputs:

- release-series metadata.
- dataset files and manifests.
- DataCite, DCAT, provenance, and licensing metadata.

Outputs:

- Croissant JSON-LD metadata.
- RO-Crate metadata.
- Frictionless Data Package descriptors.
- validation manifest.

Validation gates:

- metadata parses with the relevant library or JSON validator.
- every described data file exists in the release package or is declared as externally hosted.
- citation, licence, DOI, repository, Hugging Face, Zenodo, and source-provenance links are present where applicable.

