"""Create and upload the private Hugging Face source archive asset."""

from __future__ import annotations

import argparse
import getpass
from pathlib import Path

from huggingface_hub import HfApi

DEFAULT_REPO_ID = "edithatogo/nz-hansard-source-archive"
DEFAULT_ARCHIVE = Path("2024-09-06 Hansard Extract from DocumentsDB.zip")
DEFAULT_PATH_IN_REPO = "source/2024-09-06 Hansard Extract from DocumentsDB.zip"


def upload_source_archive(
    *,
    token: str,
    repo_id: str = DEFAULT_REPO_ID,
    archive_path: Path | str = DEFAULT_ARCHIVE,
    path_in_repo: str = DEFAULT_PATH_IN_REPO,
    private: bool = True,
    api_factory=HfApi,
) -> str:
    archive_path = Path(archive_path)
    if not archive_path.exists():
        raise FileNotFoundError(f"Source archive not found: {archive_path}")
    api = api_factory(token=token)
    api.create_repo(repo_id=repo_id, repo_type="dataset", private=private, exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(archive_path),
        path_in_repo=path_in_repo,
        repo_id=repo_id,
        repo_type="dataset",
        commit_message="Add Hansard source archive",
    )
    return (
        f"https://huggingface.co/datasets/{repo_id}/resolve/main/{path_in_repo.replace(' ', '%20')}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload the Hansard source ZIP to Hugging Face.")
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID)
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--path-in-repo", default=DEFAULT_PATH_IN_REPO)
    parser.add_argument(
        "--public", action="store_true", help="Create the source archive repo as public."
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = getpass.getpass("HF token: ")
    source_url = upload_source_archive(
        token=token,
        repo_id=args.repo_id,
        archive_path=args.archive,
        path_in_repo=args.path_in_repo,
        private=not args.public,
    )
    print(source_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
