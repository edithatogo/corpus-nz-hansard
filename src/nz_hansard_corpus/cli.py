"""Compatibility CLI for New Zealand Hansard corpus maintenance commands."""

from __future__ import annotations

import argparse
import runpy
import sys
from collections.abc import Sequence
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = REPO_ROOT / "scripts"

COMMANDS: dict[tuple[str, ...], str] = {
    ("build-manifest",): "build_public_surface_audit.py",
    ("duckdb",): "build_duckdb.py",
    ("hf", "stage"): "stage_huggingface_dataset.py",
    ("hf", "upload"): "upload_huggingface_dataset.py",
    ("inventory",): "inventory_archive.py",
    ("metadata", "build"): "build_metadata_packages.py",
    ("normalize",): "normalize_hansard.py",
    ("quality-gate",): "check_quality_gate.py",
    ("release-package",): "build_release_package.py",
    ("schema",): "discover_schema.py",
    ("search-index",): "build_search_index.py",
    ("validate",): "check_quality_gate.py",
    ("validate-records",): "validate_hansard_records.py",
    ("zenodo", "build"): "build_zenodo_archive.py",
    ("zenodo", "draft"): "upload_zenodo_archive.py",
    ("zenodo", "upload"): "upload_zenodo_archive.py",
}


def command_table() -> dict[str, str]:
    """Return command aliases as display strings mapped to scripts."""
    return {" ".join(alias): script for alias, script in sorted(COMMANDS.items())}


def _match_command(tokens: Sequence[str]) -> tuple[tuple[str, ...], list[str]]:
    for width in (2, 1):
        candidate = tuple(tokens[:width])
        if candidate in COMMANDS:
            return candidate, list(tokens[width:])
    available = ", ".join(command_table())
    raise SystemExit(f"Unknown command: {' '.join(tokens)}. Available commands: {available}")


def _script_path(script: str) -> Path:
    path = SCRIPT_DIR / script
    if not path.is_file():
        raise SystemExit(f"Configured script is missing: {path.relative_to(REPO_ROOT)}")
    return path


def _run_script(path: Path, args: Sequence[str]) -> int:
    old_argv = sys.argv[:]
    try:
        sys.argv = [str(path), *args]
        runpy.run_path(str(path), run_name="__main__")
    finally:
        sys.argv = old_argv
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the compatibility CLI."""
    parser = argparse.ArgumentParser(prog="nzhc", description=__doc__)
    parser.add_argument("tokens", nargs="*", help="Command tokens followed by script arguments.")
    parser.add_argument("--list", action="store_true", help="List available command aliases.")
    ns = parser.parse_args(argv)
    if ns.list:
        for alias, script in command_table().items():
            print(f"{alias}\t{script}")  # noqa: T201
        return 0
    if not ns.tokens:
        parser.error("command is required unless --list is used")
    command, args = _match_command(ns.tokens)
    return _run_script(_script_path(COMMANDS[command]), args)


if __name__ == "__main__":
    raise SystemExit(main())
