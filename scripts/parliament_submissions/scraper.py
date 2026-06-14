"""Scraper connectors for NZ Parliament select committee submissions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urljoin


@dataclass
class SubmissionEntry:
    """A single select committee submission listing."""

    id: str
    title: str | None = None
    submitter: str | None = None
    committee: str | None = None
    bill_reference: str | None = None
    submission_date: str | None = None
    document_url: str | None = None
    status: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = {k: v for k, v in asdict(self).items() if v is not None}
        d.pop("extra", None)
        if self.extra:
            d.update(self.extra)
        return d

    def absolute_url(self, base: str = "https://www.parliament.nz") -> str | None:
        if not self.document_url:
            return None
        return urljoin(base.rstrip("/") + "/", self.document_url.lstrip("/"))


_DEFAULT_API_URL = "https://committees.parliament.nz/api/submissions"
_DEFAULT_HEADERS = {
    "User-Agent": (
        "corpus-nz-hansard/1.0 (research; "
        "+https://github.com/edithatogo/corpus-nz-hansard)"
    ),
    "Accept": "application/json",
}


def fetch_submissions_list(
    url: str = _DEFAULT_API_URL,
    *,
    page: int = 1,
    page_size: int = 50,
    committee: str | None = None,
    opener: Callable = urlopen,
) -> dict[str, Any]:
    """Fetch a page of select committee submissions from the Parliament API.

    Returns parsed JSON with keys ``results``, ``totalResults``.
    On error returns a dict with ``error`` and ``status``.
    """
    params: dict[str, str | int] = {"page": page, "pageSize": page_size}
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


def parse_submission_list(
    data: dict[str, Any] | str,
    source: str = "json",
) -> list[SubmissionEntry]:
    """Parse a submission list response into ``SubmissionEntry`` objects.

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

    entries: list[SubmissionEntry] = []
    for item in raw_results:
        if not isinstance(item, dict):
            continue
        entries.append(
            SubmissionEntry(
                id=item.get("id", ""),
                title=item.get("title"),
                submitter=item.get("submitter"),
                committee=item.get("committee"),
                bill_reference=item.get("billReference"),
                submission_date=item.get("submissionDate"),
                document_url=item.get("documentUrl"),
                status=item.get("status"),
            )
        )
    return entries


def _parse_html_list(html: str) -> list[SubmissionEntry]:
    """Parse an HTML page of submission listings using regex."""
    entries: list[SubmissionEntry] = []
    items = re.findall(
        r'<div\s+class="submission-item"[^>]*>(.*?)</div>', html, re.DOTALL
    )
    for idx, item_html in enumerate(items):
        entries.append(
            SubmissionEntry(
                id=f"html-{idx}",
                title=_tag_text(item_html, "h3"),
                submitter=_class_text(item_html, "submitter"),
                committee=_class_text(item_html, "committee"),
                submission_date=_class_text(item_html, "date"),
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

