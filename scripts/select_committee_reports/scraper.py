"""Scraper connectors for NZ Parliament select committee reports."""

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
class ReportEntry:
    """A single select committee report listing."""

    id: str
    title: str | None = None
    committee: str | None = None
    report_date: str | None = None
    bill_reference: str | None = None
    document_url: str | None = None
    document_type: str | None = None
    document_formats: list[str] = field(default_factory=list)
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


_DEFAULT_REPORTS_URL = "https://committees.parliament.nz/api/reports"
_DEFAULT_HEADERS = {
    "User-Agent": (
        "corpus-nz-hansard/1.0 (research; "
        "+https://github.com/edithatogo/corpus-nz-hansard)"
    ),
    "Accept": "application/json",
}

DEFAULT_COMMITTEE_LIST = [
    "Justice Committee",
    "Health Committee",
    "Education and Workforce Committee",
    "Environment Committee",
    "Finance and Expenditure Committee",
    "Foreign Affairs, Defence and Trade Committee",
    "Governance and Administration Committee",
    "Māori Affairs Committee",
    "Primary Production Committee",
    "Regulations Review Committee",
    "Social Services and Community Committee",
    "Transport and Infrastructure Committee",
]


def fetch_reports_index(
    url: str = _DEFAULT_REPORTS_URL,
    *,
    page: int = 1,
    page_size: int = 50,
    from_date: str | None = None,
    to_date: str | None = None,
    committee: str | None = None,
    source: str = "json",
    opener: Callable = urlopen,
) -> dict[str, Any]:
    """Fetch a page of select committee reports from the Parliament API.

    Parameters
    ----------
    url:
        Base URL for the reports API endpoint.
    page:
        Page number to fetch.
    page_size:
        Number of results per page.
    from_date:
        Filter reports from this date (ISO format YYYY-MM-DD).
    to_date:
        Filter reports up to this date (ISO format YYYY-MM-DD).
    committee:
        Filter by committee name.
    source:
        ``"json"`` for API, ``"html"`` for HTML scraping fallback.
    opener:
        Injectable URL opener (for testing).

    Returns
    -------
    dict
        Parsed JSON with ``results``, ``totalResults``.
        On error returns a dict with ``error`` and ``status`` keys.
    """
    if source == "json":
        params: dict[str, str | int] = {"page": page, "pageSize": page_size}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if committee:
            params["committee"] = committee
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

    entries = parse_report_list(html, source="html")
    return {
        "results": [e.to_dict() for e in entries],
        "totalResults": len(entries),
        "source": "html",
    }


def parse_report_list(
    data: dict[str, Any] | str,
    source: str = "json",
) -> list[ReportEntry]:
    """Parse a report list response into ``ReportEntry`` objects.

    Parameters
    ----------
    data:
        Parsed JSON dict, JSON string, or HTML string.
    source:
        ``"json"`` for API responses, ``"html"`` for scraped HTML pages.
    """
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

    entries: list[ReportEntry] = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        doc_formats = item.get("documentFormats", [])
        if isinstance(doc_formats, list):
            doc_formats = [str(f) for f in doc_formats]
        else:
            doc_formats = []
        entries.append(
            ReportEntry(
                id=item.get("id", ""),
                title=item.get("title"),
                committee=item.get("committee"),
                report_date=item.get("reportDate"),
                bill_reference=item.get("billReference"),
                document_url=item.get("documentUrl"),
                document_type=item.get("documentType"),
                document_formats=doc_formats,
                status=item.get("status"),
            )
        )
    return entries


def fetch_report_document(
    *,
    url: str,
    output_path: Path | str,
    opener: Callable = urlopen,
) -> dict[str, Any]:
    """Download a report document from *url* to *output_path*.

    Parameters
    ----------
    url:
        The document URL to download.
    output_path:
        Local filesystem path to write the document to.
    opener:
        Injectable URL opener (for testing).

    Returns
    -------
    dict
        Keys: ``path``, ``bytes``, ``sha256``, ``status``.
        On error returns dict with ``error`` and ``status``.
    """
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


def _parse_html_list(html: str) -> list[ReportEntry]:
    """Parse an HTML page of report listings using regex."""
    entries: list[ReportEntry] = []
    items = re.findall(
        r'<div\s+class="report-item"[^>]*>(.*?)</div>', html, re.DOTALL
    )
    for idx, item_html in enumerate(items):
        entries.append(
            ReportEntry(
                id=f"html-{idx}",
                title=_tag_text(item_html, "h3"),
                committee=_class_text(item_html, "committee"),
                report_date=_class_text(item_html, "report-date"),
                document_url=_link_href(item_html),
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
