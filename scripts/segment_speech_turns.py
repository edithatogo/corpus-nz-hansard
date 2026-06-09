"""Create heuristic speech-turn candidates from normalized Hansard content."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq

DEFAULT_INPUT = Path("generated/parquet/hansard.parquet")
DEFAULT_OUTPUT = Path("generated/parquet/hansard_speech_turns.parquet")
DEFAULT_VALIDATION = Path("manifests/speech_turn_segmentation_validation.json")
DEFAULT_BATCH_SIZE = 1000

SPEAKER_RE = re.compile(r"^[A-Z][A-Za-z .'\-]*(?:\s+[A-Z][A-Za-z .'\-]*){0,5}$")

TURN_SCHEMA = pa.schema(
    [
        ("parliament_document_id", pa.string()),
        ("parliament_number", pa.int64()),
        ("document_type", pa.string()),
        ("title", pa.string()),
        ("source_file", pa.string()),
        ("source_row_number", pa.int64()),
        ("turn_index", pa.int64()),
        ("speaker_candidate", pa.string()),
        ("speech_text", pa.string()),
        ("confidence", pa.string()),
        ("method", pa.string()),
    ]
)


def _clean_fragment(value: str) -> str:
    return value.replace("\xa0", " ").replace("\ufffd", "").strip()


def _speaker_like(value: str) -> bool:
    cleaned = _clean_fragment(value)
    if not cleaned or len(cleaned) > 120:
        return False
    if any(char.isdigit() for char in cleaned):
        return False
    if cleaned.lower().startswith(("to the", "minister for")):
        return False
    return bool(SPEAKER_RE.match(cleaned))


def extract_turns_from_content(content: str | None) -> list[dict[str, str]]:
    """Extract conservative `speaker : speech` candidates from content."""
    if not content:
        return []
    fragments = [_clean_fragment(part) for part in content.split("\t")]
    turns: list[dict[str, str]] = []
    for index, fragment in enumerate(fragments):
        if fragment != ":":
            continue
        if index == 0 or index + 1 >= len(fragments):
            continue
        speaker = fragments[index - 1]
        speech = fragments[index + 1]
        if not _speaker_like(speaker) or not speech:
            continue
        turns.append(
            {
                "speaker_candidate": speaker,
                "speech_text": speech,
                "confidence": "medium",
                "method": "tab_colon_marker_v1",
            }
        )
    return turns


def _table_from_turns(turns: list[dict[str, Any]]) -> pa.Table:
    columns = {field.name: [turn.get(field.name) for turn in turns] for field in TURN_SCHEMA}
    return pa.Table.from_pydict(columns, schema=TURN_SCHEMA)


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_segmentation(
    input_path: Path | str = DEFAULT_INPUT,
    output_path: Path | str = DEFAULT_OUTPUT,
    validation_path: Path | str = DEFAULT_VALIDATION,
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> dict[str, Any]:
    """Read normalized Parquet and write candidate speech-turn Parquet."""
    input_path = Path(input_path)
    output_path = Path(output_path)
    validation_path = Path(validation_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input Parquet not found: {input_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    documents_read = 0
    documents_with_turns = 0
    documents_without_turns = 0
    turns_written = 0
    confidence_counts: Counter[str] = Counter()
    turns_by_document_type: Counter[str] = Counter()
    examples: list[dict[str, Any]] = []
    writer: pq.ParquetWriter | None = None
    batch: list[dict[str, Any]] = []

    parquet_file = pq.ParquetFile(input_path)
    try:
        for record_batch in parquet_file.iter_batches(
            batch_size=batch_size,
            columns=[
                "parliament_document_id",
                "parliament_number",
                "document_type",
                "title",
                "source_file",
                "source_row_number",
                "content",
            ],
        ):
            for row in pa.Table.from_batches([record_batch]).to_pylist():
                documents_read += 1
                turns = extract_turns_from_content(row.get("content"))
                if turns:
                    documents_with_turns += 1
                else:
                    documents_without_turns += 1
                for turn_index, turn in enumerate(turns, start=1):
                    speech_text = turn["speech_text"]
                    output_row: dict[str, Any] = {
                        "parliament_document_id": row.get("parliament_document_id"),
                        "parliament_number": row.get("parliament_number"),
                        "document_type": row.get("document_type"),
                        "title": row.get("title"),
                        "source_file": row.get("source_file"),
                        "source_row_number": row.get("source_row_number"),
                        "turn_index": turn_index,
                        **turn,
                    }
                    confidence_counts[turn["confidence"]] += 1
                    turns_by_document_type[str(row.get("document_type"))] += 1
                    if len(examples) < 10:
                        examples.append(
                            {
                                "parliament_document_id": output_row["parliament_document_id"],
                                "speaker_candidate": output_row["speaker_candidate"],
                                "speech_text_prefix": speech_text[:160],
                            }
                        )
                    batch.append(output_row)
                    if len(batch) >= batch_size:
                        table = _table_from_turns(batch)
                        if writer is None:
                            writer = pq.ParquetWriter(
                                output_path,
                                TURN_SCHEMA,
                                compression="zstd",
                            )
                        writer.write_table(table)
                        turns_written += len(batch)
                        batch.clear()

        if batch:
            table = _table_from_turns(batch)
            if writer is None:
                writer = pq.ParquetWriter(output_path, TURN_SCHEMA, compression="zstd")
            writer.write_table(table)
            turns_written += len(batch)
            batch.clear()
    finally:
        if writer is not None:
            writer.close()

    validation = {
        "validation_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "input": str(input_path),
        "output": str(output_path),
        "summary": {
            "documents_read": documents_read,
            "documents_with_turns": documents_with_turns,
            "documents_without_turns": documents_without_turns,
            "turns_written": turns_written,
            "confidence_counts": dict(confidence_counts),
            "method": "tab_colon_marker_v1",
            "authoritative": False,
        },
        "turns_by_document_type": dict(turns_by_document_type),
        "examples": examples,
        "limitations": [
            "Heuristic candidates only.",
            "Speaker names are not identity-resolved.",
            "Party/electorate details are not extracted.",
            "Documents without tab-colon markers emit no turns.",
        ],
    }
    _write_json(validation, validation_path)
    return validation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build heuristic speech-turn candidates from normalized Hansard Parquet."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--validation", type=Path, default=DEFAULT_VALIDATION)
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validation = run_segmentation(
        input_path=args.input,
        output_path=args.output,
        validation_path=args.validation,
        batch_size=args.batch_size,
    )
    print(f"Wrote {validation['output']}")
    print(f"Documents read: {validation['summary']['documents_read']}")
    print(f"Turns written: {validation['summary']['turns_written']}")
    print(f"Authoritative: {validation['summary']['authoritative']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
