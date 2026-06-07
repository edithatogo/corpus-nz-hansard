# Search and RAG Index Report

Generated: 2026-06-07

## Summary

The local Hansard search index was built from `generated/parquet/hansard.parquet` into `generated/search/hansard_search.sqlite`.

Validation summary:

- Source rows: 193,922
- Indexed documents: 193,922
- Indexed chunks: 1,018,955
- Index type: SQLite FTS5
- Embedding index: false
- Citation-ready: true

## Configuration

- `max_chars`: 1600
- `overlap`: 200
- `batch_size`: 1000
- Sample queries: `health`, `budget`, `education`, `housing`, `climate`

## Sample Query Counts

- `health`: 95,897
- `budget`: 77,683
- `education`: 76,241
- `housing`: 40,537
- `climate`: 24,388

## Verification

The generated SQLite database contains matching row counts in `chunks` and `chunks_fts`: 1,018,955 rows each.

A read-only lexical query for `budget` returned citation-bearing results, including Budget Debate documents from the normalized corpus.

## Boundaries

This is a local lexical index only. It is not a vector database, embedding index, hosted search service, or authoritative speaker attribution layer.
