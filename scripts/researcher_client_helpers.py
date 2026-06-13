"""Read-only helper examples for researcher workflows."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DOCUMENT_SAMPLE_PATH = ROOT / "samples/researcher-client-helpers/hansard-mini.csv"
RDF_SAMPLE_PATH = ROOT / "samples/rdf-linked-data/linked-data.ttl"


def _sql_literal(path: Path) -> str:
    return path.as_posix().replace("'", "''")


def python_document_summary(sample_path: Path = DOCUMENT_SAMPLE_PATH) -> dict[str, Any]:
    """Summarize the small document-level sample with Python only."""

    with sample_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    document_types = sorted({row["document_type"] for row in rows})
    titles = [row["title"] for row in rows]
    return {
        "sample_path": sample_path.as_posix(),
        "row_count": len(rows),
        "document_types": document_types,
        "titles": titles,
    }


def duckdb_document_summary(sample_path: Path = DOCUMENT_SAMPLE_PATH) -> dict[str, Any]:
    """Summarize the sample with DuckDB, using CSV or Parquet input."""

    suffix = sample_path.suffix.lower()
    if suffix == ".parquet":
        table_expr = f"read_parquet('{_sql_literal(sample_path)}')"
    elif suffix == ".csv":
        table_expr = f"read_csv_auto('{_sql_literal(sample_path)}')"
    else:
        raise ValueError(f"Unsupported sample type: {sample_path.suffix}")

    with duckdb.connect(":memory:") as connection:
        row_count = connection.execute(f"select count(*) from {table_expr}").fetchone()[0]  # ty:ignore[not-subscriptable]
        rows_by_type = connection.execute(
            f"""
            select document_type, count(*) as rows
            from {table_expr}
            group by document_type
            order by rows desc, document_type
            """
        ).fetchall()
        titles = connection.execute(
            f"""
            select title
            from {table_expr}
            order by source_row_number, title
            """
        ).fetchall()

    return {
        "sample_path": sample_path.as_posix(),
        "row_count": int(row_count),
        "rows_by_document_type": [
            {"document_type": row[0], "rows": int(row[1])} for row in rows_by_type
        ],
        "titles": [row[0] for row in titles],
    }


def rdf_sample_summary(sample_path: Path = RDF_SAMPLE_PATH) -> dict[str, Any]:
    """Summarize the RDF sample graph with rdflib and SPARQL."""

    from rdflib import Graph

    graph = Graph()
    graph.parse(sample_path)
    query = """
        PREFIX dcat: <http://www.w3.org/ns/dcat#>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        SELECT ?title
        WHERE {
          ?dataset a dcat:Dataset ;
                   dcterms:title ?title .
        }
    """
    titles = sorted({str(row.title) for row in graph.query(query)})
    return {
        "sample_path": sample_path.as_posix(),
        "triple_count": len(graph),
        "dataset_titles": titles,
    }
