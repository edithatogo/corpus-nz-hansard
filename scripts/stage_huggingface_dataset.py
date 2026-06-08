"""Stage a Hugging Face Datasets upload folder for the Hansard corpus."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

DEFAULT_OUTPUT_DIR = Path("generated/huggingface")
DEFAULT_PARQUET = Path("generated/parquet/hansard.parquet")

COPY_DIRS = ("docs", "manifests", "schemas")
COPY_FILES = ("README.md", "CITATION.cff", "LICENSE", "NOTICE.md", "VERSION", "DATASET_CARD.md")


def _copy_tree(source: Path, target: Path) -> None:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(
        source,
        target,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )


def stage_huggingface_dataset(
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    parquet_path: Path | str = DEFAULT_PARQUET,
) -> dict[str, str]:
    """Create a deterministic local folder ready for `hf upload-large-folder`."""
    output_dir = Path(output_dir)
    parquet_path = Path(parquet_path)
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet input not found: {parquet_path}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    for file_name in COPY_FILES:
        path = Path(file_name)
        if path.exists():
            target_name = "README.md" if file_name == "DATASET_CARD.md" else file_name
            shutil.copy2(path, output_dir / target_name)

    for dir_name in COPY_DIRS:
        path = Path(dir_name)
        if path.exists():
            _copy_tree(path, output_dir / dir_name)

    data_dir = output_dir / "data"
    data_dir.mkdir()
    shutil.copy2(parquet_path, data_dir / "hansard.parquet")

    return {
        "output_dir": str(output_dir),
        "parquet": str(data_dir / "hansard.parquet"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage a Hugging Face Datasets upload folder."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--parquet", type=Path, default=DEFAULT_PARQUET)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = stage_huggingface_dataset(args.output_dir, args.parquet)
    print(f"Staged {result['output_dir']}")
    print(f"Parquet: {result['parquet']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
