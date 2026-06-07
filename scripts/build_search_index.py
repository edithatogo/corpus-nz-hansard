"""Build a local SQLite FTS5 search index from normalized Hansard Parquet."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

DEFAULT_PARQUET = Path("generated/parquet/hansard.parquet")
DEFAULT_DATABASE = Path("generated/search/hansard_search.sqlite")
DEFAULT_VALIDATION = Path("manifests/search_index_validation.json")
DEFAULT_MAX_CHARS = 1600
DEFAULT_OVERLAP = 200
DEFAULT_BATCH_SIZE = 1000
DEFAULT_SAMPLE_QUERIES = ["health", "budget", "education", "housing", "climate"]


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _clean_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.replace("\xa0", " ").replace("\ufffd", "").split())


def _right_word_boundary(text: str, limit: int) -> int:
    if limit >= len(text):
        return len(text)
    boundary = text.rfind(" ", 0, limit + 1)
    if boundary <= 0:
        return limit
    return boundary


def _left_word_boundary(text: str, start: int) -> int:
    if start <= 0:
        return 0
    while start < len(text) and text[start] == " ":
        start += 1
    boundary = text.find(" ", start)
    if boundary == -1:
        return start
    return start


def chunk_text(
    text: str | None,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap: int = DEFAULT_OVERLAP,
) -> list[dict[str, Any]]:
    """Split text into deterministic overlapping chunks with character offsets."""
    cleaned = _clean_text(text)
    if not cleaned:
        return []
    if max_chars <= 0:
        raise ValueError("max_chars must be positive")
    if overlap < 0:
        raise ValueError("overlap must be non-negative")
    if overlap >= max_chars:
        raise ValueError("overlap must be smaller than max_chars")

    chunks: list[dict[str, Any]] = []
    start = 0
    while start < len(cleaned):
        hard_end = min(len(cleaned), start + max_chars)
        end = _right_word_boundary(cleaned, hard_end)
        if end <= start:
            end = hard_end
        chunk = cleaned[start:end].strip()
        if chunk:
            actual_start = start
            while actual_start < end and cleaned[actual_start] == " ":
                actual_start += 1
            chunks.append(
                {
                    "chunk_index": len(chunks) + 1,
                    "start_char": actual_start,
                    "end_char": end,
                    "text": cleaned[actual_start:end],
                }
            )
        if end >= len(cleaned):
            break
        next_start = max(0, end - overlap)
        next_start = _left_word_boundary(cleaned, next_start)
        if next_start <= start:
            next_start = end
        start = next_start
    return chunks


def _connect_database(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    if database_path.exists():
        database_path.unlink()
    connection = sqlite3.connect(database_path)
    connection.execute("pragma journal_mode=delete;")
    connection.execute("pragma synchronous=normal;")
    return connection


def _create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        create table chunks (
            chunk_id integer primary key,
            parliament_document_id text not null,
            source_file text,
            source_row_number integer,
            parliament_number integer,
            document_type text,
            title text,
            document_content_date text,
            chunk_index integer not null,
            start_char integer not null,
            end_char integer not null,
            citation text not null,
            text text not null
        );

        create virtual table chunks_fts using fts5(
            text,
            title,
            citation,
            content='chunks',
            content_rowid='chunk_id'
        );

        create index idx_chunks_document_id on chunks(parliament_document_id);
        create index idx_chunks_source on chunks(source_file, source_row_number);
        create index idx_chunks_date on chunks(document_content_date);
        """
    )


def _citation(row: dict[str, Any], chunk_index: int, start_char: int, end_char: int) -> str:
    title = row.get("title") or "Untitled"
    document_id = row.get("parliament_document_id") or "unknown-document"
    source_file = row.get("source_file") or "unknown-source"
    source_row = row.get("source_row_number")
    date = row.get("document_content_date") or "unknown-date"
    return (
        f"{document_id}; {title}; {date}; {source_file} row {source_row}; "
        f"chunk {chunk_index}; chars {start_char}-{end_char}"
    )


def _insert_chunk(
    connection: sqlite3.Connection,
    row: dict[str, Any],
    chunk: dict[str, Any],
) -> None:
    citation = _citation(
        row,
        int(chunk["chunk_index"]),
        int(chunk["start_char"]),
        int(chunk["end_char"]),
    )
    cursor = connection.execute(
        """
        insert into chunks (
            parliament_document_id,
            source_file,
            source_row_number,
            parliament_number,
            document_type,
            title,
            document_content_date,
            chunk_index,
            start_char,
            end_char,
            citation,
            text
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row.get("parliament_document_id"),
            row.get("source_file"),
            row.get("source_row_number"),
            row.get("parliament_number"),
            row.get("document_type"),
            row.get("title"),
            row.get("document_content_date"),
            chunk["chunk_index"],
            chunk["start_char"],
            chunk["end_char"],
            citation,
            chunk["text"],
        ),
    )
    chunk_id = cursor.lastrowid
    connection.execute(
        "insert into chunks_fts(rowid, text, title, citation) values (?, ?, ?, ?)",
        (chunk_id, chunk["text"], row.get("title") or "", citation),
    )


def _sample_query_counts(
    connection: sqlite3.Connection,
    sample_queries: list[str],
) -> dict[str, int]:
    counts: dict[str, int] = {}
    for query in sample_queries:
        counts[query] = int(
            connection.execute(
                "select count(*) from chunks_fts where chunks_fts match ?",
                (query,),
            ).fetchone()[0]
        )
    return counts


def build_search_index(
    parquet_path: Path | str = DEFAULT_PARQUET,
    database_path: Path | str = DEFAULT_DATABASE,
    validation_path: Path | str = DEFAULT_VALIDATION,
    max_chars: int = DEFAULT_MAX_CHARS,
    overlap: int = DEFAULT_OVERLAP,
    batch_size: int = DEFAULT_BATCH_SIZE,
    sample_queries: list[str] | None = None,
) -> dict[str, Any]:
    """Create a local FTS5 index and validation report from normalized Parquet."""
    parquet_path = Path(parquet_path)
    database_path = Path(database_path)
    validation_path = Path(validation_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet input not found: {parquet_path}")

    sample_queries = sample_queries or DEFAULT_SAMPLE_QUERIES
    source_rows = 0
    indexed_documents = 0
    indexed_chunks = 0
    chunks_by_document_type: dict[str, int] = {}
    examples: list[dict[str, Any]] = []

    with _connect_database(database_path) as connection:
        _create_schema(connection)
        parquet_file = pq.ParquetFile(parquet_path)
        for record_batch in parquet_file.iter_batches(batch_size=batch_size):
            for row in pa.Table.from_batches([record_batch]).to_pylist():
                source_rows += 1
                chunks = chunk_text(row.get("content"), max_chars=max_chars, overlap=overlap)
                if not chunks:
                    continue
                indexed_documents += 1
                document_type = str(row.get("document_type"))
                for chunk in chunks:
                    _insert_chunk(connection, row, chunk)
                    indexed_chunks += 1
                    chunks_by_document_type[document_type] = (
                        chunks_by_document_type.get(document_type, 0) + 1
                    )
                    if len(examples) < 10:
                        examples.append(
                            {
                                "parliament_document_id": row.get(
                                    "parliament_document_id"
                                ),
                                "chunk_index": chunk["chunk_index"],
                                "start_char": chunk["start_char"],
                                "end_char": chunk["end_char"],
                                "citation": _citation(
                                    row,
                                    int(chunk["chunk_index"]),
                                    int(chunk["start_char"]),
                                    int(chunk["end_char"]),
                                ),
                                "text_prefix": chunk["text"][:160],
                            }
                        )
            connection.commit()

        sample_counts = _sample_query_counts(connection, sample_queries)
        connection.execute("insert into chunks_fts(chunks_fts) values ('optimize')")

    validation = {
        "validation_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(parquet_path),
        "database": str(database_path),
        "config": {
            "max_chars": max_chars,
            "overlap": overlap,
            "batch_size": batch_size,
            "sample_queries": sample_queries,
            "index_type": "sqlite_fts5",
            "embedding_index": False,
        },
        "summary": {
            "source_rows": source_rows,
            "indexed_documents": indexed_documents,
            "indexed_chunks": indexed_chunks,
            "lexical": True,
            "citation_ready": True,
        },
        "sample_queries": sample_counts,
        "chunks_by_document_type": chunks_by_document_type,
        "examples": examples,
        "limitations": [
            "Local SQLite FTS5 lexical index only.",
            "No embeddings or external retrieval services are used.",
            "Chunks preserve document-level metadata but do not add speaker attribution.",
            "Search ranking uses SQLite bm25 over chunk text, title, and citation fields.",
        ],
    }
    _write_json(validation, validation_path)
    return validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local SQLite FTS5 search index from normalized Hansard Parquet."
    )
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--sample-query", action="append", dest="sample_queries")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validation = build_search_index(
        parquet_path=args.parquet,
        database_path=args.database,
        validation_path=args.validation,
        max_chars=args.max_chars,
        overlap=args.overlap,
        batch_size=args.batch_size,
        sample_queries=args.sample_queries,
    )
    print(f"Wrote {validation['database']}")
    print(f"Source rows: {validation['summary']['source_rows']}")
    print(f"Indexed documents: {validation['summary']['indexed_documents']}")
    print(f"Indexed chunks: {validation['summary']['indexed_chunks']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
