"""Shared utilities for NZ Parliament committee scrapers."""
from __future__ import annotations
import hashlib, json, logging, random, re, time
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
log = logging.getLogger(__name__)
DEFAULT_USER_AGENT = "corpus-nz-hansard/1.0 (research; +https://github.com/edithatogo/corpus-nz-hansard)"
DEFAULT_TIMEOUT = 30
DEFAULT_MIN_DELAY = 0.25
DEFAULT_MAX_RETRIES = 5
DEFAULT_HEADERS: dict[str, str] = {"User-Agent": DEFAULT_USER_AGENT, "Accept": "application/json"}

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))

def sha256_file(path: Path, chunk_size: int = 1_048_576) -> str:
    if not path.exists():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()

def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return rows

def append_jsonl(path: Path, rows: list[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
            count += 1
    return count


class CommitteeFetcher:
    """Rate-limit aware HTTP fetcher for NZ Parliament committee APIs."""
    def __init__(self, min_delay: float = DEFAULT_MIN_DELAY, max_retries: int = DEFAULT_MAX_RETRIES, base_headers: dict[str, str] | None = None, opener: Callable = urlopen) -> None:
        self.min_delay = min_delay
        self.max_retries = max_retries
        self.base_headers = dict(base_headers or DEFAULT_HEADERS)
        self.opener = opener
        self.last_request_at = 0.0
    def _pace(self) -> None:
        elapsed = time.monotonic() - self.last_request_at
        wait = self.min_delay - elapsed
        if wait > 0:
            time.sleep(wait)
        self.last_request_at = time.monotonic()

    @staticmethod
    def _retry_after(headers: Any, fallback: int) -> float:
        raw = None
        if isinstance(headers, dict):
            raw = headers.get("Retry-After")
        elif hasattr(headers, "get"):
            raw = headers.get("Retry-After")
        if raw is not None:
            try:
                return max(0.0, float(raw))
            except (ValueError, TypeError):
                pass
        return min(120, (2**fallback) + random.random())

    def fetch_json(self, url: str, **kwargs: Any) -> dict[str, Any]:
        params = kwargs.pop("params", None)
        extra_headers = kwargs.pop("headers", None)
        timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT)
        if params:
            from urllib.parse import urlencode
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}{urlencode(params)}"
        merged = dict(self.base_headers)
        if extra_headers:
            merged.update(extra_headers)
        for attempt in range(1, self.max_retries + 1):
            self._pace()
            try:
                req = Request(url, headers=merged)
                with self.opener(req, timeout=timeout) as resp:
                    status = getattr(resp, "status", None) or (resp.getcode() if hasattr(resp, "getcode") else 200)
                    body = resp.read().decode("utf-8")
                    if 200 <= status < 300:
                        return json.loads(body)
                    if status in (429, 403) and attempt < self.max_retries:
                        wait = self._retry_after(getattr(resp, "headers", {}), attempt)
                        log.warning("HTTP %d %s; retry %.1fs (%d/%d)", status, url, wait, attempt, self.max_retries)
                        time.sleep(wait)
                        continue
                    return {"error": f"http_{status}", "status": status, "results": []}
            except HTTPError as e:
                if e.code in (429, 403) and attempt < self.max_retries:
                    wait = self._retry_after(e.headers, attempt)
                    log.warning("HTTP %d %s; retry %.1fs (%d/%d)", e.code, url, wait, attempt, self.max_retries)
                    time.sleep(wait)
                    continue
                return {"error": f"http_{e.code}", "status": e.code, "results": []}
            except (URLError, OSError, json.JSONDecodeError) as e:
                if attempt < self.max_retries:
                    wait = min(60, (2**attempt) + random.random())
                    log.warning("Error %s %s; retry %.1fs (%d/%d)", e, url, wait, attempt, self.max_retries)
                    time.sleep(wait)
                    continue
                return {"error": str(e), "status": 0, "results": []}
        return {"error": "retries_exhausted", "status": 0, "results": []}
    def download_file(self, *, url: str, output_path: Path | str, **kwargs: Any) -> dict[str, Any]:
        output_path = Path(output_path)
        extra_headers = kwargs.pop("headers", None)
        timeout = kwargs.pop("timeout", DEFAULT_TIMEOUT)
        skip_dups = kwargs.pop("skip_duplicates", True)
        if not url:
            return {"error": "empty_url", "status": 0}
        if skip_dups and url in self._seen_urls:
            return {"path": str(output_path), "bytes": 0, "sha256": "", "status": "duplicate"}
        merged = dict(self.base_headers)
        if extra_headers:
            merged.update(extra_headers)
        for attempt in range(1, self.max_retries + 1):
            self._pace()
            try:
                req = Request(url, headers=merged)
                with self.opener(req, timeout=timeout) as resp:
                    status = getattr(resp, "status", None) or (resp.getcode() if hasattr(resp, "getcode") else 200)
                    if 200 <= status < 300:
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        digest = hashlib.sha256()
                        with output_path.open("wb") as stream:
                            while True:
                                chunk = resp.read(1_048_576)
                                if not chunk:
                                    break
                                stream.write(chunk)
                                digest.update(chunk)
                        self._seen_urls.add(url)
                        return {"path": str(output_path), "bytes": output_path.stat().st_size, "sha256": digest.hexdigest(), "status": status}

_DATE_ISO = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_NZ_FULL = re.compile(r"(\d{1,2})(?:st|nd|rd|th)?\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})", re.IGNORECASE)
_DATE_DM_SLASH = re.compile(r"(\d{2})[/-](\d{2})[/-](\d{4})")
_MONTH_MAP = {"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}

def normalize_date(raw: str | None) -> str | None:
    if not raw or not raw.strip():
        return None
    raw = raw.strip()
    if _DATE_ISO.match(raw):
        return raw
    m = _DATE_NZ_FULL.match(raw)
    if m:
        day = int(m.group(1))
        month = _MONTH_MAP.get(m.group(2).lower())
        year = int(m.group(3))
        if month:
            return f"{year:04d}-{month:02d}-{day:02d}"
    m = _DATE_DM_SLASH.match(raw)
    if m:
        return f"{m.group(3)}-{m.group(2):0>2}-{m.group(1):0>2}"
    return None

                    if status in (429, 403) and attempt < self.max_retries:
                        wait = self._retry_after(getattr(resp, "headers", {}), attempt)
                        log.warning("Download HTTP %d; retry %.1fs (%d/%d)", status, wait, attempt, self.max_retries)
                        time.sleep(wait)
                        continue
                    return {"error": f"http_{status}", "status": status}
            except HTTPError as e:
                if e.code in (429, 403) and attempt < self.max_retries:
                    wait = self._retry_after(e.headers, attempt)
                    log.warning("Download HTTP %d; retry %.1fs (%d/%d)", e.code, wait, attempt, self.max_retries)
                    time.sleep(wait)
                    continue
                return {"error": f"http_{e.code}", "status": e.code}
            except (URLError, ConnectionError, OSError) as e:
                if attempt < self.max_retries:
                    wait = min(60, (2**attempt) + random.random())
                    log.warning("Download error %s; retry %.1fs (%d/%d)", e, wait, attempt, self.max_retries)
                    time.sleep(wait)
                    continue
                return {"error": str(e), "status": 0}
        return {"error": "retries_exhausted", "status": 0}

    def has_seen(self, url: str) -> bool:
        return url in self._seen_urls

    def mark_seen(self, url: str) -> None:
        self._seen_urls.add(url)

    def reset_seen(self) -> None:
        self._seen_urls.clear()


        self._seen_urls: set[str] = set()
