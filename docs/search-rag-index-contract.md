# Search and RAG Index Contract

## Purpose

The search index is a local, lexical retrieval surface for the normalized New Zealand Hansard corpus. It is intended for repeatable source discovery and citation-ready downstream retrieval experiments before any embedding or vector index work.

## Inputs

- Source Parquet: `generated/parquet/hansard.parquet`
- Required content field: `content`
- Required identity fields: `parliament_document_id`, `source_file`, `source_row_number`
- Supporting metadata: `parliament_number`, `document_type`, `title`, `document_content_date`

## Outputs

- SQLite database: `generated/search/hansard_search.sqlite`
- Validation manifest: `manifests/search_index_validation.json`

The SQLite database contains:

- `chunks`: one row per generated content chunk with document metadata, character offsets, chunk text, and citation.
- `chunks_fts`: SQLite FTS5 index over chunk text, title, and citation.

## Chunking

Chunks are generated from cleaned document text with deterministic character offsets. The default configuration is:

- `max_chars`: 1600
- `overlap`: 200

Offsets are measured against the cleaned text used for indexing. Each chunk includes `chunk_index`, `start_char`, and `end_char`.

## Citation

Each chunk citation includes:

- `parliament_document_id`
- title
- document content date
- source file
- source row number
- chunk index
- character offset range

The citation is designed to make a search hit traceable back to the normalized row and source archive member. It is not an official parliamentary citation format.

## Validation Surface

`manifests/search_index_validation.json` records:

- source rows read
- indexed documents
- indexed chunks
- chunking configuration
- sample lexical query counts
- chunks by document type
- example chunk citations

## Boundaries

This is not an embedding index, vector database, or externally hosted search service. It does not add authoritative speaker attribution, party identity, or semantic ranking.
