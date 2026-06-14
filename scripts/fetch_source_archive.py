"""Download and verify the Hansard source archive."""

from __future__ import annotations

import argparse
import hashlib
import os
import time
from pathlib import Path
from typing import Protocol
from urllib.error import HTTPError
from urllib.request import Request, urlopen

DEFAULT_OUTPUT = Path("2024-09-06 Hansard Extract from DocumentsDB.zip")
DEFAULT_SHA256 = "2ac02c0042a4fb291fd8e401db5f469de2539e42c9e07c4c72eca16be9a17299"


class BinaryResponse(Protocol):
    def read(self, size: int = -1) -> bytes: ...


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_source_archive(
    *,
    url: str,
    output_path: Path | str = DEFAULT_OUTPUT,
    expected_sha256: str = DEFAULT_SHA256,
    token: str | None = None,
    opener=urlopen,
    max_attempts: int = 5,
    retry_sleep_seconds: float = 10.0,
) -> dict[str, str | int]:
    """Download the source archive and fail if the SHA-256 does not match."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, max_attempts + 1):
        request = Request(url)
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with opener(request) as response:
                with output_path.open("wb") as stream:
                    while True:
                        chunk = response.read(1024 * 1024)
                        if not chunk:
                            break
                        stream.write(chunk)
            break
        except HTTPError as exc:
            output_path.unlink(missing_ok=True)
            if exc.code != 429 or attempt >= max_attempts:
                raise
            retry_after = exc.headers.get("Retry-After")
            try:
                sleep_seconds = float(retry_after) if retry_after else retry_sleep_seconds
            except ValueError:
                sleep_seconds = retry_sleep_seconds
            print(
                f"Source archive download rate-limited with HTTP 429; "
                f"retrying attempt {attempt + 1}/{max_attempts} after {sleep_seconds:g}s."
            )
            time.sleep(sleep_seconds)

    actual_sha256 = sha256_path(output_path)
    if actual_sha256.lower() != expected_sha256.lower():
        output_path.unlink(missing_ok=True)
        raise ValueError(
            f"Source archive SHA-256 mismatch: expected {expected_sha256}, got {actual_sha256}"
        )
    return {
        "path": str(output_path),
        "bytes": output_path.stat().st_size,
        "sha256": actual_sha256,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download and verify the Hansard source ZIP.")
    parser.add_argument("--url", default=os.getenv("SOURCE_ARCHIVE_URL"))
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sha256", default=DEFAULT_SHA256)
    parser.add_argument("--max-attempts", type=int, default=5)
    parser.add_argument("--retry-sleep-seconds", type=float, default=10.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.url:
        raise SystemExit("SOURCE_ARCHIVE_URL or --url is required.")
    result = fetch_source_archive(
        url=args.url,
        output_path=args.output,
        expected_sha256=args.sha256,
        token=os.getenv("HF_TOKEN"),
        max_attempts=args.max_attempts,
        retry_sleep_seconds=args.retry_sleep_seconds,
    )
    print(f"Wrote {result['path']}")
    print(f"Bytes: {result['bytes']}")
    print(f"SHA-256: {result['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
