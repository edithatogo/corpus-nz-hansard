"""Metadata extraction from select committee reports."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any


@dataclass
class ReportMetadata:
    """Extracted structured metadata from a select committee report document."""

    report_date: str | None = None
    committee_name: str | None = None
    bill_reference: str | None = None
    subject: str | None = None
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None and v != []}


_RE_DATE = [
    re.compile(r"\b(\d{4}-\d{2}-\d{2})\b"),
    re.compile(
        r"\b(\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{4})\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b"),
]


_RE_COMMITTEE = [
    re.compile(r"^Report of the (\w+(?:\s+\w+)*\s+Committee)", re.IGNORECASE | re.MULTILINE),
    re.compile(r"^(\w+(?:\s+\w+)*\s+Committee)\s*$", re.MULTILINE),
    re.compile(r"(\w+(?:\s+\w+){1,4}\s+Committee)", re.IGNORECASE),
]


_RE_BILL = [
    re.compile(r"(?:Inquiry\s+into\s+the\s+)?([A-Z][A-Za-z]+(?:\s+(?:[A-Za-z]+|\([A-Za-z]+(?:\s+[A-Za-z]+)*\)))*\s+Bill)"),
    re.compile(r"Bill\s+(?:referred|reference)[:\s]+(.+)", re.IGNORECASE),
]


_RE_SUBJECT = re.compile(
    r"^(?:Subject|Topic|Regarding)[:\s]+(.+)$", re.IGNORECASE | re.MULTILINE
)


_RE_RECOMMENDATION = re.compile(
    r"(?:recommends?|recommendation)[:\s]+(.+)", re.IGNORECASE
)


def extract_report_date(text: str) -> str | None:
    """Extract the report date from document text."""
    if not text or not text.strip():
        return None
    for pat in _RE_DATE:
        m = pat.search(text)
        if m:
            raw = m.group(1).strip()
            if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
                return raw
            try:
                cleaned = re.sub(r"(st|nd|rd|th)\b", "", raw)
                dt = datetime.strptime(cleaned, "%d %B %Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
            try:
                dt = datetime.strptime(raw, "%d/%m/%Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
            try:
                dt = datetime.strptime(raw, "%d-%m-%Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                return raw
    return None


def extract_committee_name(text: str) -> str | None:
    """Extract the committee name from report text."""
    if not text or not text.strip():
        return None
    for pat in _RE_COMMITTEE:
        m = pat.search(text)
        if m:
            name = m.group(1).strip()
            if len(name) > 5:
                return name
    return None


def extract_bill_reference(text: str) -> str | None:
    """Extract the bill reference from report text."""
    if not text or not text.strip():
        return None
    for pat in _RE_BILL:
        m = pat.search(text)
        if m:
            ref = m.group(1).strip()
            if ref and len(ref) > 5:
                # Remove trailing parenthetical like (2024/123)
                ref = re.sub(r"\s*\([^)]*\)\s*$", "", ref).strip()
                return ref
    return None


def extract_report_subject(text: str) -> str | None:
    """Extract the report subject line."""
    if not text:
        return None
    m = _RE_SUBJECT.search(text)
    if m:
        subject = m.group(1).strip().rstrip(".")
        return subject or None
    return None


def extract_member_recommendations(text: str) -> list[str]:
    """Extract member recommendations from report text."""
    if not text:
        return []
    recs: list[str] = []
    for m in _RE_RECOMMENDATION.finditer(text):
        rec = m.group(1).strip().rstrip(".")
        if rec and len(rec) > 5:
            recs.append(rec)
    return recs


def extract_all_metadata(text: str) -> ReportMetadata:
    """Extract all available metadata from report document text."""
    return ReportMetadata(
        report_date=extract_report_date(text),
        committee_name=extract_committee_name(text),
        bill_reference=extract_bill_reference(text),
        subject=extract_report_subject(text),
        recommendations=extract_member_recommendations(text),
    )
