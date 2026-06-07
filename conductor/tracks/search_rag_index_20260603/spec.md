# Search and RAG Index MVP Spec

## Problem

The corpus has normalized document-level Parquet and DuckDB outputs, but no first-class local search or retrieval index. Researchers and downstream RAG workflows need repeatable chunks with stable citations before any embedding or external retrieval work is appropriate.

## Scope

- Build a local SQLite FTS5 lexical index from `generated/parquet/hansard.parquet`.
- Generate deterministic content chunks with document metadata, offsets, and citation strings.
- Produce a validation manifest with row, chunk, and sample-search evidence.
- Document the chunking and citation contract.

## Non-Scope

- No external embedding API calls.
- No vector database.
- No authoritative speaker attribution.
- No web publishing or dataset upload.

## Acceptance Criteria

- A script builds `generated/search/hansard_search.sqlite` from normalized Parquet.
- The index contains one metadata table for chunks and one FTS5 table for lexical search.
- Chunks include `parliament_document_id`, `source_file`, `source_row_number`, `chunk_index`, character offsets, title, document type, date, and citation.
- A validation JSON records source rows, indexed documents, indexed chunks, configuration, and sample query counts.
- Unit tests cover chunking, SQLite index creation, and lexical search.
- Documentation explains that the index is local, lexical, and citation-ready but not an embedding index.
