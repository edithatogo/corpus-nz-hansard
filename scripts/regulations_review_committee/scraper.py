"""Scraper connectors for Regulations Review Committee proceedings."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urljoin


@dataclass
class ProceedingEntry:
    """A single Regulations Review Committee proceeding listing."""

    id: str
    title: str | None = None
    meeting_date: str | None = None
    committee: str | None = None
    document_url: str | None = None
    document_type: str | None = None
    agenda_items: list[str] = field(default_factory=list)
    status: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {k: v for k, v in asdict(self).items() if v is not None and v != []}
        d.pop("extra", None)
        if self.extra:
            d.update(self.extra)
        return d

    def absolute_url(self, base: str = "https://www.parliament.nz") -> str | None:
        if not self.document_url:
            return None
        return urljoin(base.rstrip("/") + "/", self.document_url.lstrip("/"))


_DEFAULT_PROCEEDINGS_URL = (
    "https://committees.parliament.nz/api/committees/regulations-review/proceedings"
)
_DEFAULT_HEADERS = {
    "User-Agent": (
        "corpus-nz-hansard/1.0 (research; "
        "+https://github.com/edithatogo/corpus-nz-hansard)"
    ),
    "Accept": "application/json",
}


def fetch_proceedings_index(
    url: str = _DEFAULT_PROCEEDINGS_URL,
    *,
    page: int = 1,
    page_size: int = 50,
    from_date: str | None = None,
    to_date: str | None = None,
    source: str = "json",
    opener: Callable = urlopen,
) -> dict[str, Any]:
    """Fetch a page of committee proceedings from the Parliament API."""
    if source == "json":
        params: dict[str, str | int] = {"page": page, "pageSize": page_size}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        full_url = f"{url}?{urlencode(params)}"
        try:
            request = Request(full_url, headers=_DEFAULT_HEADERS)
            with opener(request) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except HTTPError as e:
            return {"error": f"http_{e.code}", "status": e.code, "results": []}
        except (URLError, OSError, json.JSONDecodeError) as e:
            return {"error": str(e), "status": 0, "results": []}
    # HTML fallback
    try:
        request = Request(url, headers=_DEFAULT_HEADERS)
        with opener(request) as resp:
            html = resp.read().decode("utf-8")
    except HTTPError as e:
        return {"error": f"http_{e.code}", "status": e.code, "results": []}
    except (URLError, OSError) as e:
        return {"error": str(e), "status": 0, "results": []}
    entries = parse_proceeding_list(html, source="html")
    return {
        "results": [e.to_dict() for e in entries],
        "totalResults": len(entries),
        "source": "html",
    }



def parse_proceeding_list(
    data: dict[str, Any] | str,
    source: str = "json",
) -> list[ProceedingEntry]:
    """Parse a proceeding list response into ProceedingEntry objects."""
    if isinstance(data, str):
        if source == "html":
            return _parse_html_list(data)
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return []
    if not isinstance(data, dict):
        return []
    raw_results = data.get("results", [])
    if not isinstance(raw_results, list):
        return []
    entries: list[ProceedingEntry] = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        agenda = item.get("agendaItems", [])
        if isinstance(agenda, list):
            agenda = [str(a) for a in agenda]
        else:
            agenda = []
        entries.append(
            ProceedingEntry(
                id=item.get("id", ""),
                title=item.get("title"),
                meeting_date=item.get("meetingDate"),
                committee=item.get("committee"),
                document_url=item.get("documentUrl"),
                document_type=item.get("documentType"),
                agenda_items=agenda,
                status=item.get("status"),
            )
        )
    return entries


def fetch_proceeding_document(
    *,
    url: str,
    output_path: Path | str,
    opener: Callable = urlopen,
) -> dict[str, Any]:
    """Download a proceeding document from url to output_path."""
    output_path = Path(output_path)
    if not url:
        return {"error": "empty_url", "status": 0}
    try:
        request = Request(url, headers=_DEFAULT_HEADERS)
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


def _parse_html_list(html: str) -> list[ProceedingEntry]:
    """Parse an HTML page of proceeding listings using regex."""
    entries: list[ProceedingEntry] = []
    items = re.findall(
        r'<div\s+class="proceeding-item"[^>]*>(.*?)</div>', html, re.DOTALL
    )
    for idx, item_html in enumerate(items):
        entries.append(
            ProceedingEntry(
                id=f"html-{idx}",
                title=_tag_text(item_html, "h3"),
                meeting_date=_class_text(item_html, "meeting-date"),
                committee=_class_text(item_html, "committee"),
                document_url=_link_href(item_html),
                agenda_items=_list_items(item_html),
            )
        )
    return entries


def _tag_text(html: str, tag: str) -> str | None:
    m = re.search(f"<{tag}[^>]*>(.*?)</{tag}>", html, re.DOTALL)
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return text or None
    return None


def _class_text(html: str, cls: str) -> str | None:
    m = re.search(
        r'<[^>]+class="[^"]*' + re.escape(cls) + r'[^"]*"[^>]*>(.*?)</\w+>',
        html, re.DOTALL,
    )
    if m:
        text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        return text or None
    return None


def _link_href(html: str) -> str | None:
    m = re.search(r'<a\s+[^>]*href="([^"]+)"', html)
    return m.group(1) if m else None


def _list_items(html: str) -> list[str]:
    """Extract text from <li> elements."""
    items = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL)
    return [re.sub(r"<[^>]+>", "", it).strip() for it in items if it.strip()]
