"""Document download with integrity verification for submission PDFs."""

from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def download_pdf(
    *,
    url: str,
    output_path: Path | str,
    opener: Callable = urlopen,
) -> dict:
    """Download a PDF from *url* to *output_path* and return metadata.

    Parameters
    ----------
    url:
        The PDF URL to download.
    output_path:
        Local filesystem path to write the PDF to.
    opener:
        Callable used to open the URL (injectable for tests).

    Returns
    -------
    dict
        Keys: ``path``, ``bytes``, ``sha256``, ``status``
        On error: ``error`` key and status 0 or HTTP status.
    """
    output_path = Path(output_path)

    if not url:
        return {"error": "empty_url", "status": 0}

    try:
        request = Request(url)
        with opener(request) as response:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            digest = hashlib.sha256()
            with output_path.open("wb") as stream:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    stream.write(chunk)
                    digest.update(chunk)

            status = getattr(response, "status", None)
            if status is None:
                status = response.getcode() if hasattr(response, "getcode") else 200

            return {
                "path": str(output_path),
                "bytes": output_path.stat().st_size,
                "sha256": digest.hexdigest(),
                "status": status,
            }
    except HTTPError as e:
        return {"error": f"http_{e.code}", "status": e.code}
    except (URLError, ConnectionError, OSError) as e:
        return {"error": str(e), "status": 0}


def download_pdf_with_retry(
    *,
    url: str,
    output_path: Path | str,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    opener: Callable = urlopen,
) -> dict:
    """Download a PDF with retry logic for transient failures.

    Parameters
    ----------
    url:
        The PDF URL.
    output_path:
        Local path to write the file.
    max_retries:
        Maximum number of download attempts.
    delay:
        Initial delay between retries in seconds.
    backoff:
        Multiplier for exponential backoff.
    opener:
        Injectable URL opener (for testing).

    Returns
    -------
    dict
        Same as :func:`download_pdf` with additional ``attempts`` key.
        On exhaustion, includes ``error``: ``"retries_exhausted: ..."``.
    """
    last_result: dict = {}
    attempts = 0

    for attempt in range(1, max_retries + 1):
        attempts = attempt
        result = download_pdf(url=url, output_path=output_path, opener=opener)
        last_result = result

        if "error" not in result:
            result["attempts"] = attempts
            return result

        if attempt < max_retries:
            sleep_time = delay * (backoff ** (attempt - 1))
            time.sleep(sleep_time)

    last_result["attempts"] = attempts
    if "error" not in last_result:
        last_result["error"] = "retries_exhausted"
    else:
        last_result["error"] = f"retries_exhausted: {last_result['error']}"
    return last_result

