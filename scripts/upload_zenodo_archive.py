"""Upload a staged Hansard corpus archive to a Zenodo draft deposition."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date
from pathlib import Path
from typing import Any, Protocol

import requests

DEFAULT_API_URL = "https://zenodo.org/api"
DEFAULT_VERSION = "0.1.0-review.20260603"
DEFAULT_ARCHIVE = Path("generated/zenodo/nz-hansard-corpus-0.1.0-review.20260603.tar.gz")
DEFAULT_MANIFEST = Path(
    "generated/zenodo/nz-hansard-corpus-0.1.0-review.20260603.manifest.json"
)


class HttpSession(Protocol):
    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        ...


class ZenodoDraftClient:
    """Minimal Zenodo deposition client with publication default-off."""

    def __init__(self, api_url: str, token: str, session: HttpSession | None = None) -> None:
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.session = session or requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    @property
    def json_headers(self) -> dict[str, str]:
        return {**self.headers, "Content-Type": "application/json"}

    def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        response = self.session.request(method, url, timeout=120, **kwargs)
        response.raise_for_status()
        if not response.text:
            return {}
        return response.json()

    def create_deposition(self) -> dict[str, Any]:
        return self.request(
            "POST",
            f"{self.api_url}/deposit/depositions",
            headers=self.json_headers,
            data="{}",
        )

    def get_deposition(self, deposition_id: str) -> dict[str, Any]:
        return self.request(
            "GET",
            f"{self.api_url}/deposit/depositions/{deposition_id}",
            headers=self.headers,
        )

    def ensure_draft(self, deposition_id: str | None = None) -> dict[str, Any]:
        if not deposition_id:
            return self.create_deposition()
        deposition = self.get_deposition(deposition_id)
        if deposition.get("submitted"):
            raise RuntimeError(
                "Existing deposition is already submitted; create a new version manually first."
            )
        return deposition

    def update_metadata(
        self,
        deposition_id: str,
        *,
        title: str,
        creators: list[dict[str, Any]],
        description: str,
        version: str,
        license_id: str,
        related_identifiers: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "title": title,
            "upload_type": "dataset",
            "description": description,
            "creators": creators,
            "version": version,
            "license": license_id,
            "publication_date": date.today().isoformat(),
            "keywords": ["New Zealand", "Hansard", "Parliament", "corpus", "open data"],
        }
        if related_identifiers:
            metadata["related_identifiers"] = related_identifiers
        return self.request(
            "PUT",
            f"{self.api_url}/deposit/depositions/{deposition_id}",
            headers=self.json_headers,
            data=json.dumps({"metadata": metadata}),
        )

    def upload_file(self, deposition: dict[str, Any], path: Path) -> dict[str, Any]:
        bucket = deposition.get("links", {}).get("bucket")
        if not bucket:
            raise RuntimeError("Zenodo draft does not expose a bucket URL.")
        with path.open("rb") as stream:
            return self.request(
                "PUT",
                f"{bucket.rstrip('/')}/{path.name}",
                headers=self.headers,
                data=stream,
            )

    def publish(self, deposition_id: str) -> dict[str, Any]:
        return self.request(
            "POST",
            f"{self.api_url}/deposit/depositions/{deposition_id}/actions/publish",
            headers=self.headers,
        )


def upload_zenodo_archive(
    *,
    archive_path: Path,
    manifest_path: Path,
    token: str,
    creators: list[dict[str, Any]],
    api_url: str = DEFAULT_API_URL,
    deposition_id: str | None = None,
    version: str = DEFAULT_VERSION,
    publish: bool = False,
    client: ZenodoDraftClient | None = None,
) -> dict[str, Any]:
    """Create/update a Zenodo draft, upload files, and optionally publish."""
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    if publish:
        raise RuntimeError(
            "Publication is intentionally not automated here. "
            "Review the Zenodo draft and publish through the web UI or a separate approved step."
        )

    client = client or ZenodoDraftClient(api_url=api_url, token=token)
    draft = client.ensure_draft(deposition_id)
    draft_id = str(draft["id"])
    uploaded = [
        client.upload_file(draft, archive_path),
        client.upload_file(draft, manifest_path),
    ]
    metadata = client.update_metadata(
        draft_id,
        title="NZ Hansard Corpus",
        creators=creators,
        description=(
            "Review-stage document-level corpus pipeline for New Zealand Hansard records. "
            "This draft excludes the source ZIP and does not claim official endorsement."
        ),
        version=version,
        license_id="other-open",
        related_identifiers=[
            {
                "identifier": "https://github.com/edithatogo/corpus-nz-hansard",
                "relation": "isSupplementTo",
                "scheme": "url",
            }
        ],
    )
    return {
        "deposition_id": draft_id,
        "draft": metadata,
        "uploaded": uploaded,
        "published": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Upload Hansard archive files to a Zenodo draft.")
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--api-url", default=os.getenv("ZENODO_API_URL", DEFAULT_API_URL))
    parser.add_argument("--token", default=os.getenv("ZENODO_TOKEN"))
    parser.add_argument("--deposition-id", default=os.getenv("ZENODO_DEPOSITION_ID"))
    parser.add_argument("--creators-json", default=os.getenv("ARCHIVE_CREATORS_JSON"))
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Reserved for a separate approved publication step; currently rejected.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.token:
        raise SystemExit("ZENODO_TOKEN is required.")
    if not args.creators_json:
        raise SystemExit("ARCHIVE_CREATORS_JSON is required.")
    creators = json.loads(args.creators_json)
    result = upload_zenodo_archive(
        archive_path=args.archive,
        manifest_path=args.manifest,
        api_url=args.api_url,
        token=args.token,
        deposition_id=args.deposition_id,
        creators=creators,
        version=args.version,
        publish=args.publish,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
