# Release Ladder

## Purpose

The release ladder separates document-level dataset publication from later authority-source evidence, neutral component releases, standard-specific endpoint exports, and upstream contribution packages.

The current public dataset is `v0.1.0` at the `document-level` ladder step. That data snapshot is immutable except for metadata, documentation, cross-reference, and provenance corrections that do not alter public rows, columns, source hashes, or intended use.

## Levels

| Level | ID | Purpose |
| ---: | --- | --- |
| 1 | `document-level` | Normalized document records from the supplied DocumentsDB extract, plus release metadata and public-surface evidence. |
| 2 | `authority-source` | Official-first source inventories and retrieval evidence for future derived assertions. |
| 3 | `neutral-component` | Validated repository-owned components such as sittings, proceedings, speech turns, members, parties, motions, votes, bills, topics, and annotations. |
| 4 | `endpoint` | Generated standard-specific artifacts such as ParlaMint/TEI, Popolo/Open Civic Data, Akoma Ntoso, CAP/ParlaCAP, CoNLL-U, RDF, Croissant, RO-Crate, Frictionless, DCAT, and PROV-O. |
| 5 | `upstream-contribution` | Reviewed samples, fixtures, mapping notes, and contribution evidence for external maintainers or standards communities. |

## Current Artifact Map

The machine-readable artifact map is `manifests/release_ladder.json`.

Current public release artifacts remain at `document-level`:

- `manifests/public_dataset_release_manifest.json`
- `generated/parquet/hansard.parquet`
- `schemas/hansard_record.schema.json`

Current validated planning or evidence artifacts sit at later ladder levels:

- `manifests/authority_sources.json` is `authority-source`.
- `docs/component-contracts.md` is `neutral-component` planning.
- `docs/endpoint-contracts.md` and generated metadata packages are `endpoint`.
- `docs/derived-fields-validation.md` and the derived-field validation manifests are `endpoint`-adjacent planning and evidence artifacts for later derived releases.
- `conductor/tracks/upstream_contribution_packages_20260609` is `upstream-contribution` planning.

Candidate speech-turn output remains excluded until a later validation track promotes it.

Sitting and proceeding component release scaffolding remains blocked until official historical reconciliation is complete.

## Manifest Fields

Component and endpoint manifests must include release-series fields before publication:

- `release_series_id`
- `release_level`
- `artifact_name`
- `artifact_version`
- `input_release_versions`
- `validation_manifest`
- `publication_target`
- `known_exclusions`
- `release_status`
- `manifest_sha256`

These fields make each artifact's ladder position explicit and prevent endpoint releases from being confused with the canonical document-level dataset.

## Publication Surface Relationship

GitHub remains the home for source code, release manifests, schemas, docs, checks, issues, and lightweight assets.

Hugging Face hosts the canonical live document-level Parquet dataset and can host endpoint-specific layouts only after those endpoints pass their own ladder gates.

Zenodo is the immutable DOI-bearing archive for stable public release snapshots.

OSF remains optional mirror infrastructure and is inactive for current public claims.

Upstream contribution packages are maintainer-facing artifacts derived from validated endpoint or component releases; external acceptance does not retroactively change canonical release status.

## Gate Rule

Do not publish endpoint artifacts as part of document-level releases. A later endpoint release must cite its input document release, component release, validation manifest, known exclusions, and publication target.
