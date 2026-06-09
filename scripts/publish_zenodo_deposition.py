"""Publish an already-prepared Zenodo draft deposition."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Protocol

import requests

DEFAULT_API_URL = "https://zenodo.org/api"


class HttpSession(Protocol):
    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response: ...


class ZenodoPublishClient:
    def __init__(self, api_url: str, token: str, session: HttpSession | None = None) -> None:
        self.api_url = api_url.rstrip("/")
        self.token = token
        self.session = session or requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def request(self, method: str, url: str, **kwargs: Any) -> dict[str, Any]:
        response = self.session.request(method, url, timeout=120, **kwargs)
        response.raise_for_status()
        if not response.text:
            return {}
        return response.json()

    def publish(self, deposition_id: str) -> dict[str, Any]:
        return self.request(
            "POST",
            f"{self.api_url}/deposit/depositions/{deposition_id}/actions/publish",
            headers=self.headers,
        )


def publish_zenodo_deposition(
    *,
    deposition_id: str,
    token: str,
    api_url: str = DEFAULT_API_URL,
    client: ZenodoPublishClient | None = None,
) -> dict[str, Any]:
    client = client or ZenodoPublishClient(api_url=api_url, token=token)
    publication = client.publish(deposition_id)
    return {
        "deposition_id": deposition_id,
        "published": True,
        "publication": publication,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Publish an already-prepared Zenodo draft deposition."
    )
    parser.add_argument("--deposition-id", default=os.getenv("ZENODO_DEPOSITION_ID"))
    parser.add_argument("--api-url", default=os.getenv("ZENODO_API_URL", DEFAULT_API_URL))
    parser.add_argument("--token", default=os.getenv("ZENODO_TOKEN"))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.deposition_id:
        raise SystemExit("ZENODO_DEPOSITION_ID or --deposition-id is required.")
    if not args.token:
        raise SystemExit("ZENODO_TOKEN is required.")
    result = publish_zenodo_deposition(
        deposition_id=args.deposition_id,
        api_url=args.api_url,
        token=args.token,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
