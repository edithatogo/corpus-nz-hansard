"""Metadata extraction from submission document text."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class SubmissionMetadata:
    """Extracted metadata from a submission document."""

    submitter: str | None = None
    date: str | None = None
    committee: str | None = None
    bill_reference: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None}


# Submitter patterns
_RE_SUBMITTER = [
    re.compile(
        r"(?:submission\s+(?:by|from|of)|submitted\s+by)\s*[:\-]?\s*(.+?)[\r\n]",
        re.IGNORECASE,
    ),
    re.compile(r"^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s+submits?\b", re.MULTILINE),
    re.compile(
        r"^([A-Z][A-Za-z\s&]+(?:Inc|Ltd|Trust|Society|Iwi|Authority|"
        r"Board|Council|Committee|Law Society))",
        re.MULTILINE,
    ),
]

# Date patterns
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

# Committee patterns
_RE_COMMITTEE = [
    re.compile(
        r"(?:submitted\s+to\s+the\s+|to\s+the\s+)([\w\s]+(?:Select\s+)?Committee)",
        re.IGNORECASE,
    ),
    re.compile(r"([\w\s]+(?:Committee))\s*(?:on|re:|regarding)", re.IGNORECASE),
]

# Bill reference patterns
_RE_BILL = [
    re.compile(
        r"(?:submission\s+(?:on|regarding|re:|concerning)\s+(?:the\s+)?(?:draft\s+)?)?"
        r"([A-Z][A-Za-z\s&]+(?:Amendment|Reform|Review|Bill))(?:\s+Bill)?",
        re.IGNORECASE,
    ),
    re.compile(r"([A-Z][A-Za-z\s&]+(?:Bill))\s+\d{4}", re.IGNORECASE),
]


def extract_submitter_name(text: str) -> str | None:
    """Extract the submitter name from submission document text."""
    if not text or not text.strip():
        return None
    for pat in _RE_SUBMITTER:
        m = pat.search(text)
        if m:
            name = m.group(1).strip().rstrip(".,;:-")
            if len(name) >= 2:
                return name
    return None


def extract_date(text: str) -> str | None:
    """Extract the submission date from document text."""
    if not text or not text.strip():
        return None
    for pat in _RE_DATE:
        m = pat.search(text)
        if m:
            raw = m.group(1).strip()
            if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
                return raw
            # Try NZ format
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


def extract_committee_reference(text: str) -> str | None:
    """Extract the committee name from submission document text."""
    if not text or not text.strip():
        return None
    for pat in _RE_COMMITTEE:
        m = pat.search(text)
        if m:
            c = m.group(1).strip()
            if len(c) >= 3:
                return c
    return None


def extract_bill_reference(text: str) -> str | None:
    """Extract the bill reference from submission document text."""
    if not text or not text.strip():
        return None
    for pat in _RE_BILL:
        m = pat.search(text)
        if m:
            ref = m.group(1).strip().rstrip(".,;:")
            if len(ref) >= 5:
                return ref
    return None


def extract_all_metadata(text: str) -> SubmissionMetadata:
    """Extract all available metadata from submission document text."""
    return SubmissionMetadata(
        submitter=extract_submitter_name(text),
        date=extract_date(text),
        committee=extract_committee_reference(text),
        bill_reference=extract_bill_reference(text),
    )

