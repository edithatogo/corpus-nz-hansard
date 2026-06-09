# Shared NZ Corpus Core Schema

This document defines the shared core record contract for `corpus-nz-hansard` and `corpus-nz-legislation`. It is a compatibility layer for future generated endpoint exports, not a replacement for corpus-specific schemas such as `schemas/hansard_record.schema.json`.

## Scope

The shared core covers stable identity, source provenance, dates, canonical links, and release traceability. Corpus-specific fields remain outside this contract:

| Corpus | Corpus-specific examples |
| --- | --- |
| `corpus-nz-hansard` | parliament number, debate title, speaker/member fields, speech-turn segmentation fields. |
| `corpus-nz-legislation` | Act/regulation identifiers, assent or commencement fields, amendment/version status, legislative instrument hierarchy. |

The preferred family labels are `corpus-nz-hansard` and `corpus-nz-legislation`. Existing published GitHub, Hugging Face, Zenodo DOI, and any OSF mirror URLs must not be renamed or broken without a migration plan that preserves redirects or explicit compatibility notes.

## Required core fields

| Field | Purpose |
| --- | --- |
| `corpus_id` | Corpus-family identifier. Must be `corpus-nz-hansard` or `corpus-nz-legislation`. |
| `record_id` | Stable record identifier within the corpus release. |
| `source_id` | Stable upstream source identity used by the corpus pipeline. |
| `jurisdiction` | Jurisdiction label. Current NZ family value is `New Zealand`. |
| `country` | ISO-like country shortcut. Current NZ family value is `NZ`. |
| `document_type` | Corpus-neutral document class, such as `hansard_document`, `speech_turn`, `act`, or `regulation`. |
| `record_schema_version` | Version of the emitted record schema contract. |
| `canonical_uri` | Canonical corpus URI for the record, suitable for endpoint exports. |
| `source_url` | Public source URL when available. Null is allowed only where an upstream source has no direct public URL. |
| `source_version` | Upstream version, source file revision, or equivalent version label. |
| `effective_date` | Date the record applies from, where known. |
| `published_date` | Public publication date, where known. |
| `last_modified_date` | Upstream or local last-modified date, where known. |
| `content_sha256` | SHA-256 hash of normalized content for the record. |
| `manifest_sha256` | SHA-256 hash of the release manifest that accounts for the record. |
| `provenance` | Object containing pipeline, source, and release traceability fields. |

Date fields use `YYYY-MM-DD` when present. Hash fields are lowercase hex SHA-256 values.

## Provenance object

The `provenance` object records the minimum traceability needed across public surfaces:

| Field | Purpose |
| --- | --- |
| `pipeline_name` | Pipeline or builder family that emitted the record. |
| `pipeline_version` | Local pipeline version or release version. |
| `source_name` | Human-readable upstream source. |
| `source_record_id` | Upstream source record identifier. |
| `source_retrieved_at` | Retrieval timestamp or null when the source package is historical/offline. |
| `release_version` | Corpus release version containing the record. |
| `release_commit` | Git commit SHA for the release. |
| `license_note` | Rights/provenance note suitable for public metadata surfaces. |

Additional corpus-specific provenance fields are allowed, but these shared keys must remain stable once endpoint exports depend on them.

## Public surface implications

GitHub remains the source-code and manifest home for the schema, scripts, tests, and migration notes. Hugging Face dataset cards should preserve the corpus-family labels and document whether the exposed viewer rows are document-level or endpoint-specific records. Zenodo metadata should describe the shared schema as a compatibility contract without changing existing DOI records unless a new version is minted. OSF remains optional mirror infrastructure and should use the same labels and manifest hashes if adopted. Future metadata packages should reference this schema rather than duplicating incompatible field names.

## Migration constraints

Generated endpoint work and future metadata packages can add fields around this core, but should not rename or remove the shared fields after publication without:

1. documenting the old and new field names;
2. publishing a compatibility window;
3. preserving existing published URLs and DOI records where possible;
4. recording the manifest hash and release commit that introduced the change.

Stable ID and URI policy is governed by `manifests/id_uri_policy.json`. Reuse `stable_id` for document-level identity; new component and endpoint IDs must not depend on transient file paths or row positions alone. RDF, Popolo, and linked metadata outputs use the planned `https://w3id.org/nz-hansard/` namespace with SPARQL-friendly prefixes, and replacements must be recorded in `manifests/id_uri_deprecations.json`.
