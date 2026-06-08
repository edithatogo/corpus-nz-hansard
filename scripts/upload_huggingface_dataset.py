"""Upload a staged Hansard corpus folder to Hugging Face Datasets."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any, Protocol

from huggingface_hub import HfApi, hf_hub_download
from huggingface_hub.utils import EntryNotFoundError, RepositoryNotFoundError

DEFAULT_FOLDER = Path("generated/huggingface")
DEFAULT_REPO_ID = "edithatogo/nz-hansard-corpus"


class HuggingFaceApi(Protocol):
    def create_repo(self, **kwargs: Any) -> Any:
        ...

    def update_repo_settings(self, **kwargs: Any) -> Any:
        ...

    def upload_folder(self, **kwargs: Any) -> Any:
        ...


def _read_local_manifest(folder: Path) -> dict[str, Any] | None:
    path = folder / "manifests" / "public_dataset_release_manifest.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _remote_manifest(repo_id: str, token: str, revision: str) -> dict[str, Any] | None:
    try:
        path = hf_hub_download(
            repo_id=repo_id,
            repo_type="dataset",
            filename="manifests/public_dataset_release_manifest.json",
            token=token,
            revision=revision,
        )
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (EntryNotFoundError, RepositoryNotFoundError, FileNotFoundError):
        return None


def upload_huggingface_dataset(
    *,
    repo_id: str,
    folder: Path,
    token: str,
    private: bool = False,
    revision: str = "main",
    force: bool = False,
    api: HuggingFaceApi | None = None,
) -> dict[str, Any]:
    """Create/update a dataset repository and upload a staged folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Staged folder not found: {folder}")
    if not (folder / "data" / "hansard.parquet").exists():
        raise FileNotFoundError(f"Staged Parquet not found under: {folder / 'data'}")

    api = api or HfApi(token=token)
    api.create_repo(
        repo_id=repo_id,
        repo_type="dataset",
        private=private,
        exist_ok=True,
        token=token,
    )
    api.update_repo_settings(
        repo_id=repo_id,
        repo_type="dataset",
        private=private,
        gated=False,
        token=token,
    )

    local_manifest = _read_local_manifest(folder)
    remote_manifest = None if api is not None and type(api).__name__ != "HfApi" else _remote_manifest(repo_id, token, revision)
    if (
        not force
        and local_manifest
        and remote_manifest
        and local_manifest == remote_manifest
    ):
        return {
            "repo_id": repo_id,
            "gated": False,
            "private": private,
            "uploaded": False,
            "reason": "remote_manifest_matches_local",
            "url": f"https://huggingface.co/datasets/{repo_id}/tree/{revision}",
        }

    api.upload_folder(
        repo_id=repo_id,
        repo_type="dataset",
        folder_path=str(folder),
        path_in_repo=".",
        revision=revision,
        token=token,
        commit_message="Publish NZ Hansard corpus dataset",
    )
    return {
        "repo_id": repo_id,
        "gated": False,
        "private": private,
        "uploaded": True,
        "url": f"https://huggingface.co/datasets/{repo_id}/tree/{revision}",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload staged Hansard data to Hugging Face.")
    parser.add_argument("--repo-id", default=os.getenv("HF_REPO_ID", DEFAULT_REPO_ID))
    parser.add_argument("--folder", type=Path, default=DEFAULT_FOLDER)
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"))
    parser.add_argument("--revision", default="main")
    parser.add_argument("--private", action="store_true")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.token:
        raise SystemExit("HF_TOKEN is required.")
    result = upload_huggingface_dataset(
        repo_id=args.repo_id,
        folder=args.folder,
        token=args.token,
        private=args.private,
        revision=args.revision,
        force=args.force,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
