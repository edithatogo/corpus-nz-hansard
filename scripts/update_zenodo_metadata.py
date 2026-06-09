"""Update Zenodo metadata cross-references without publishing."""

from __future__ import annotations

import argparse
import json
import os
import time
from typing import Any, Protocol

import requests

DEFAULT_API_URL = "https://zenodo.org/api"
DEFAULT_DEPOSITION_ID = "20595194"

DEFAULT_DESCRIPTION = (
    "Document-level corpus pipeline for New Zealand Hansard records. "
    "This release excludes the source ZIP, does not claim official endorsement, "
    "and intentionally keeps member identity, party attribution, and speech-turn "
    "segmentation out of the canonical document-level dataset scope. "
    "Public surfaces: GitHub repository "
    "https://github.com/edithatogo/corpus-nz-hansard; GitHub release "
    "https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0; "
    "Hugging Face dataset https://huggingface.co/datasets/edithatogo/nz-hansard-corpus."
)

DEFAULT_RELATED_IDENTIFIERS = [
    {
        "identifier": "https://github.com/edithatogo/corpus-nz-hansard",
        "relation": "isSupplementedBy",
        "scheme": "url",
    },
    {
        "identifier": "https://github.com/edithatogo/corpus-nz-hansard/releases/tag/v0.1.0",
        "relation": "isSupplementedBy",
        "scheme": "url",
    },
    {
        "identifier": "https://huggingface.co/datasets/edithatogo/nz-hansard-corpus",
        "relation": "isIdenticalTo",
        "scheme": "url",
    },
]


def merge_related_identifiers(
    existing: list[dict[str, Any]] | None,
    required: list[dict[str, str]] | None = None,
) -> list[dict[str, Any]]:
    """Return existing related identifiers plus required cross-references.

    Zenodo records can contain DOI or source links that should not be removed
    when we only need to add repository and dataset cross-references.
    """
    required = required or DEFAULT_RELATED_IDENTIFIERS
    merged: list[dict[str, Any]] = []
    positions: dict[str, int] = {}
    for item in existing or []:
        identifier = item.get("identifier")
        if not identifier:
            merged.append(dict(item))
            continue
        positions[str(identifier)] = len(merged)
        merged.append(dict(item))
    for item in required:
        identifier = item["identifier"]
        if identifier in positions:
            merged[positions[identifier]] = {**merged[positions[identifier]], **item}
        else:
            positions[identifier] = len(merged)
            merged.append(dict(item))
    return merged


class HttpSession(Protocol):
    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        ...


class ZenodoMetadataClient:
    def __init__(
        self,
        api_url: str,
        token: str,
        session: HttpSession | None = None,
        *,
        max_retries: int = 3,
        retry_sleep: float = 2.0,
    ) -> None:
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self.retry_sleep = retry_sleep

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    @property
    def json_headers(self) -> dict[str, str]:
        return {**self.headers, "Content-Type": "application/json"}

    def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        last_error: requests.RequestException | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, timeout=120, **kwargs)
                if response.status_code < 500:
                    response.raise_for_status()
                    if not response.text:
                        return {}
                    return response.json()
                response.raise_for_status()
            except requests.RequestException as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    raise
                time.sleep(self.retry_sleep * (attempt + 1))
        if last_error:
            raise last_error
        raise RuntimeError("Zenodo request failed without a response.")

    def get_deposition(self, deposition_id: str) -> dict[str, Any]:
        return self.request(
            "GET",
            f"{self.api_url}/deposit/depositions/{deposition_id}",
            headers=self.headers,
        )

    def get_record(self, record_id: str) -> dict[str, Any]:
        return self.request(
            "GET",
            f"{self.api_url}/records/{record_id}",
            headers=self.headers,
        )

    def edit_deposition(self, deposition_id: str) -> dict[str, Any]:
        return self.request(
            "POST",
            f"{self.api_url}/deposit/depositions/{deposition_id}/actions/edit",
            headers=self.headers,
        )

    def put_metadata(self, deposition_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
        return self.request(
            "PUT",
            f"{self.api_url}/deposit/depositions/{deposition_id}",
            headers=self.json_headers,
            data=json.dumps({"metadata": metadata}),
        )

def update_zenodo_metadata(
    *,
    deposition_id: str,
    token: str,
    api_url: str = DEFAULT_API_URL,
    description: str = DEFAULT_DESCRIPTION,
    related_identifiers: list[dict[str, str]] | None = None,
    client: ZenodoMetadataClient | None = None,
) -> dict[str, Any]:
    client = client or ZenodoMetadataClient(api_url=api_url, token=token)
    try:
        deposition = client.get_deposition(deposition_id)
    except requests.HTTPError as exc:
        response = exc.response
        if response is None or response.status_code < 500:
            raise
        record = client.get_record(deposition_id)
        deposition = {
            "id": deposition_id,
            "submitted": True,
            "metadata": record.get("metadata", {}),
        }

    metadata = dict(deposition.get("metadata", {}))
    if not metadata:
        raise RuntimeError("Zenodo deposition did not include editable metadata.")

    if deposition.get("submitted"):
        editable = client.edit_deposition(deposition_id)
        editable_metadata = editable.get("metadata", {}) if editable else {}
        if editable_metadata:
            metadata = dict(editable_metadata)

    metadata["description"] = description
    metadata["related_identifiers"] = merge_related_identifiers(
        metadata.get("related_identifiers"),
        related_identifiers,
    )

    updated = client.put_metadata(deposition_id, metadata)
    return {
        "deposition_id": deposition_id,
        "updated": updated,
        "published": False,
        "publication": None,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update Zenodo record metadata cross-references."
    )
    parser.add_argument("--deposition-id", default=os.getenv("ZENODO_DEPOSITION_ID", DEFAULT_DEPOSITION_ID))
    parser.add_argument("--api-url", default=os.getenv("ZENODO_API_URL", DEFAULT_API_URL))
    parser.add_argument("--token", default=os.getenv("ZENODO_TOKEN"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.token:
        raise SystemExit("ZENODO_TOKEN is required.")
    result = update_zenodo_metadata(
        deposition_id=args.deposition_id,
        api_url=args.api_url,
        token=args.token,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
