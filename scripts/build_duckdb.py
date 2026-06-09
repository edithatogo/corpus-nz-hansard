"""Build a DuckDB analysis database from normalized Hansard Parquet."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

DEFAULT_PARQUET = Path("generated/parquet/hansard.parquet")
DEFAULT_DATABASE = Path("generated/duckdb/hansard.duckdb")
DEFAULT_VALIDATION = Path("manifests/duckdb_validation.json")


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _fetch_mapping(
    connection: duckdb.DuckDBPyConnection,
    query: str,
) -> dict[str, int]:
    return {str(key): int(value) for key, value in connection.execute(query).fetchall()}


def build_duckdb_database(
    parquet_path: Path | str = DEFAULT_PARQUET,
    database_path: Path | str = DEFAULT_DATABASE,
    validation_path: Path | str = DEFAULT_VALIDATION,
    expected_rows: int | None = None,
) -> dict[str, Any]:
    """Create a DuckDB database and validation report from normalized Parquet."""
    parquet_path = Path(parquet_path)
    database_path = Path(database_path)
    validation_path = Path(validation_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet input not found: {parquet_path}")

    database_path.parent.mkdir(parents=True, exist_ok=True)
    wal_path = database_path.with_name(f"{database_path.name}.wal")
    if wal_path.exists():
        wal_path.unlink()
    if database_path.exists():
        database_path.unlink()

    parquet_sql_path = str(parquet_path).replace("'", "''")
    checkpoint_status = "not_run"
    checkpoint_error = None
    with duckdb.connect(str(database_path)) as connection:
        connection.execute(
            f"""
            create table hansard as
            select * from read_parquet('{parquet_sql_path}');
            """
        )
        connection.execute(
            "create index idx_hansard_document_id on hansard(parliament_document_id);"
        )
        connection.execute(
            "create index idx_hansard_parliament_number on hansard(parliament_number);"
        )

        row_count_result = connection.execute("select count(*) from hansard").fetchone()
        if row_count_result is None:
            raise RuntimeError("DuckDB row-count query did not return a row.")
        row_count = int(row_count_result[0])
        columns = [row[1] for row in connection.execute("pragma table_info('hansard')").fetchall()]
        rows_by_source_file = _fetch_mapping(
            connection,
            """
            select source_file, count(*) as rows
            from hansard
            group by source_file
            order by source_file
            """,
        )
        rows_by_parliament_number = _fetch_mapping(
            connection,
            """
            select parliament_number, count(*) as rows
            from hansard
            group by parliament_number
            order by parliament_number
            """,
        )
        sample_documents = [
            {
                "parliament_document_id": row[0],
                "parliament_number": row[1],
                "title": row[2],
                "content_length": row[3],
            }
            for row in connection.execute(
                """
                select
                  parliament_document_id,
                  parliament_number,
                  title,
                  length(content) as content_length
                from hansard
                order by source_file, source_row_number
                limit 5
                """
            ).fetchall()
        ]
        try:
            connection.execute("checkpoint;")
            checkpoint_status = "succeeded"
        except Exception as exc:  # DuckDB may be unable to delete WAL on OneDrive.
            checkpoint_status = "failed"
            checkpoint_error = str(exc)

    validation = {
        "validation_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "database": str(database_path),
        "parquet": str(parquet_path),
        "summary": {
            "row_count": row_count,
            "expected_rows": expected_rows,
            "row_count_matches_expected": (
                None if expected_rows is None else row_count == expected_rows
            ),
            "column_count": len(columns),
            "columns": columns,
            "checkpoint_status": checkpoint_status,
            "checkpoint_error": checkpoint_error,
        },
        "rows_by_source_file": rows_by_source_file,
        "rows_by_parliament_number": rows_by_parliament_number,
        "sample_documents": sample_documents,
    }
    _write_json(validation, validation_path)
    return validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a DuckDB analysis database from normalized Parquet."
    )
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    parser.add_argument("--database", type=Path, default=DEFAULT_DATABASE)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--expected-rows", type=int, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validation = build_duckdb_database(
        parquet_path=args.parquet,
        database_path=args.database,
        validation_path=args.validation,
        expected_rows=args.expected_rows,
    )
    print(f"Wrote {validation['database']}")
    print(f"Rows: {validation['summary']['row_count']}")
    print(f"Columns: {validation['summary']['column_count']}")
    print(f"Row count matches expected: {validation['summary']['row_count_matches_expected']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
