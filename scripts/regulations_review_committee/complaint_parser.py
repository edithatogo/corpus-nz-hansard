"""Complaint parsing for Regulations Review Committee proceedings.
Extracts structured complaint data from committee proceeding text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ComplaintRecord:
    """A single complaint considered by the Regulations Review Committee."""

    subject: str
    challenged_regulation: str | None = None
    grounds: str | None = None
    recommendation: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {}
        for field in ("subject", "challenged_regulation", "grounds", "recommendation"):
            val = getattr(self, field, None)
            if val is not None:
                d[field] = val
        return d


# Complaint subject patterns

_RE_COMPLAINT_SUBJECT = re.compile(
    r"(?:complaint\s*(?:#|no\.?\s*|number\s*)?)(\d{4}/\d+)",
    re.IGNORECASE,
)

_RE_BARE_YEAR_SLASH = re.compile(r"\b(\d{4}/\d+)\b")


def parse_complaint_subject(text: str | None) -> str | None:
    """Extract a complaint subject from a line or heading."""
    if not text:
        return None
    m = _RE_COMPLAINT_SUBJECT.search(text)
    if m:
        return f"Complaint {m.group(1)}"
    m = _RE_BARE_YEAR_SLASH.search(text)
    if m:
        return f"Complaint {m.group(1)}"
    return None


# Challenged regulation patterns

_RE_SL_CODE = re.compile(
    r"\b((?:SR|LI|NZLI|SL|SI)\s*\d{4}/\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)

_RE_BARE_SL = re.compile(r"\b(\d{4}/\d+)\b")

_RE_NAMED_REG = re.compile(
    r"\b(?:The\s+)?([A-Z][A-Za-z\s(,)]+?)\s+(Regulations?|Rules?|Order|Instrument|Notice)\s+(\d{4})\b",
)

_RE_SI_NAMED = re.compile(
    r"\bstatutory\s+instrument\s+(\d{4}/\d+)\b", re.IGNORECASE,
)


def extract_challenged_regulation(text: str | None) -> str | None:
    """Extract the regulation/statutory instrument being challenged."""
    if not text:
        return None
    m = _RE_SL_CODE.search(text)
    if m:
        return m.group(1).strip().upper()
    m = _RE_SI_NAMED.search(text)
    if m:
        return f"SI {m.group(1)}"
    m = _RE_NAMED_REG.search(text)
    if m:
        name = m.group(1).strip().rstrip(",")
        kind = m.group(2)
        year = m.group(3)
        return f"{name} {kind} {year}"
    m = _RE_BARE_SL.search(text)
    if m:
        return f"SR {m.group(1)}"
    return None


# Grounds patterns

_RE_GROUNDS_HEADER = re.compile(
    r"(?:Grounds?|Grounds?\s+for\s+complaint|"
    r"Grounds?\s*[:\-]|complaint\s+is\s+grounded\s+in)\s*",
    re.IGNORECASE,
)

_GROUNDS_KEYWORDS = [
    r"ultra\s+vires",
    r"procedural\s+(unfairness|defect|impropriety)",
    r"inconsistent\s+with",
    r"regulatory\s+impact",
    r"defective\s+consultation",
    r"lack\s+of\s+consultation",
    r"exceeds?\s+(statutory\s+)?authority",
    r"not\s+within\s+(the\s+)?power",
]


def extract_complaint_grounds(text: str | None) -> str | None:
    """Extract the grounds for complaint from text."""
    if not text:
        return None
    m = _RE_GROUNDS_HEADER.search(text)
    if m:
        start = m.end()
        rest = text[start:].strip()
        end_cut = re.search(r"\n\n|\n(?=[A-Z][a-z]+[\:\s])|\.\s*[A-Z]", rest)
        if end_cut:
            grounds = rest[: end_cut.start() + 1].strip()
        else:
            grounds = rest[:500].strip()
        return grounds if grounds else None
    for kw in _GROUNDS_KEYWORDS:
        km = re.search(kw, text, re.IGNORECASE)
        if km:
            start = max(0, km.start() - 40)
            end = min(len(text), km.end() + 200)
            return text[start:end].strip()[:500]
    return None


# Recommendation patterns

_RE_RECOMMENDATION_HEADER = re.compile(
    r"(?:Recommendation|recommendation|"
    r"(?:The\s+)?committee\s+recommends?)\s*[:\-]?\s*",
    re.IGNORECASE,
)

_RECOMMENDATION_KEYWORDS = re.compile(
    r"(?:recommends?\s+that\s+(?:the\s+)?(?:regulation|instrument)\s+"
    r"(?:be\s+)?(?:revoked|amended|invalidated|cancelled|"
    r"brought\s+to\s+the\s+attention)|"
    r"recommends?\s+no\s+further\s+action)",
    re.IGNORECASE,
)


def extract_committee_recommendation(text: str | None) -> str | None:
    """Extract the committee's recommendation from text."""
    if not text:
        return None
    m = _RE_RECOMMENDATION_HEADER.search(text)
    if m:
        start = m.end()
        rest = text[start:].strip()
        end_cut = re.search(r"\n\n|\n(?=[A-Z][a-z]+[\:\s])", rest)
        if end_cut:
            rec = rest[: end_cut.start()].strip()
        else:
            rec = rest[:300].strip()
        if rec:
            if not rec.lower().startswith("recommend"):
                rec = f"Recommendation: {rec}"
            return rec
    fm = _RECOMMENDATION_KEYWORDS.search(text)
    if fm:
        return fm.group(0).strip()
    return None


# Top-level orchestrator


def parse_complaints_from_text(text: str | None) -> list[ComplaintRecord]:
    """Parse all complaints from a committee proceeding text."""
    if not text:
        return []
    records: list[ComplaintRecord] = []
    sections = re.split(r"(?=\bComplaint\s+#?\d{4}/\d+)", text)
    for section in sections:
        section = section.strip()
        if not section or not re.search(r"\d{4}/\d+", section):
            continue
        subject = parse_complaint_subject(section)
        if not subject:
            continue
        records.append(
            ComplaintRecord(
                subject=subject,
                challenged_regulation=extract_challenged_regulation(section),
                grounds=extract_complaint_grounds(section),
                recommendation=extract_committee_recommendation(section),
            )
        )
    return records
