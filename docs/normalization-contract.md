# Normalization Contract

## Purpose

Normalize the source Hansard CSV rows into one document-level Parquet dataset without extracting the source ZIP to the repository root.

## Input Columns

The Phase 2 schema discovery found one consistent source header signature:

- `ParliamentNumber`
- `ParliamentDocumentId`
- `DocumentType`
- `Title`
- `AbbreviatedTitle`
- `Status`
- `Content`
- `MemberOfParliament`
- `Portfolio`
- `LastModified`
- `DocumentContentDate`

## Output Dataset

Output path: `generated/parquet/hansard.parquet`

Tracked metadata:

- `manifests/normalization_manifest.json`
- `manifests/normalization_validation.json`

## Output Columns

| Output column | Type | Source | Rule |
| --- | --- | --- | --- |
| `stable_id` | string | `ParliamentDocumentId` | Stable corpus identifier. Falls back to source file and row only if document ID is absent. |
| `jurisdiction` | string | constant | `New Zealand`. |
| `country` | string | constant | `NZ`. |
| `source` | string | constant | Human-readable source system label. |
| `source_archive` | string | input archive path | Source ZIP path used for normalization. |
| `source_file` | string | ZIP member name | Preserve exact member path. |
| `source_row_number` | integer | CSV stream position | 1-based source row number excluding header. |
| `parliament_number` | integer | `ParliamentNumber` | Parse as integer; null with warning if invalid. |
| `parliament_document_id` | string | `ParliamentDocumentId` | Trim whitespace; empty to null. |
| `document_type` | string | `DocumentType` | Trim whitespace; empty to null. |
| `title` | string | `Title` | Trim whitespace; if absent, fall back to abbreviated title, document ID, then stable ID. |
| `abbreviated_title` | string | `AbbreviatedTitle` | Trim whitespace; empty to null. |
| `status` | string | `Status` | Trim whitespace; empty to null. |
| `content` | string | `Content` | Preserve text after edge whitespace trim; empty to null with warning. |
| `member_of_parliament_raw` | string | `MemberOfParliament` | Preserve semicolon-separated source value after trim. |
| `member_of_parliament_count` | integer | `MemberOfParliament` | Count non-empty semicolon-separated values. |
| `portfolio_raw` | string | `Portfolio` | Preserve semicolon-separated source value after trim. |
| `last_modified` | string | `LastModified` | Parse timestamp and emit ISO string; null with warning if invalid. |
| `document_content_date` | string | `DocumentContentDate` | Parse timestamp and emit ISO string; null with warning if invalid. |
| `language` | string | constant | `en`. |
| `text_sha256` | string | `Content` | SHA-256 of normalized content text, empty string if content is missing. |
| `source_hash` | string | source metadata + content | SHA-256 over source archive, source file, source row, document ID, and content. |
| `pipeline_version` | string | pipeline config | Version string for the normalization code path. |

## Schema Alignment

The normalized record contract is machine-readable at `schemas/hansard_record.schema.json`. It follows the same pattern as `corpus-law-nz`: stable record identifiers, jurisdiction/country constants, source provenance, text hashes, source hashes, and pipeline version.

## Warnings

The pipeline records warning counts and up to five examples per code:

- `invalid_parliament_number`
- `invalid_last_modified`
- `invalid_document_content_date`
- `missing_content`

## Deferred Normalization

This MVP keeps `Content` at document level. Speaker-turn segmentation, party inference, member entity resolution, and portfolio normalization are later tracks because the source schema does not include explicit party or structured speech-turn fields.

## Interoperability Boundary

The normalization contract is the neutral document-level base for future endpoint generation. It deliberately does not encode ParlaMint, Popolo, Akoma Ntoso, CAP, Universal Dependencies, RDF, or other external ontology requirements directly into the core row.

Future endpoint-specific contracts must consume this neutral base plus validated derived component artifacts. They must not alter the meaning of the document-level columns in this contract.
