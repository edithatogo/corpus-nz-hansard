"""Metadata extraction from Regulations Review Committee proceedings."""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Any


@dataclass
class ProceedingMetadata:
    """Extracted structured metadata from a committee proceeding document."""

    meeting_date: str | None = None
    agenda_items: list[str] = field(default_factory=list)
    committee_members: list[str] = field(default_factory=list)
    complaint_subjects: list[str] = field(default_factory=list)
    regulation_references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v is not None and v != []}


# Meeting date patterns
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

# Agenda item patterns
_RE_AGENDA_HEADER = re.compile(r"\b(?:agenda|order\s+of\s+business|items?\s+considered)\b", re.IGNORECASE)
_RE_AGENDA_ITEM = re.compile(r"^\d+[\.\)]\s*(.+)")

# Committee member patterns
_RE_MEMBERS = [
    re.compile(r"(?:Present|Members?\s+(?:Present|attending)):\s*(.+)", re.IGNORECASE),
    re.compile(r"Committee\s+(?:Members|members):\s*(.+)", re.IGNORECASE),
    re.compile(r"In\s+attendance:\s*(.+)", re.IGNORECASE),
]

# Complaint subject patterns
_RE_COMPLAINT = re.compile(
    r"(?:complaint|complaints?)\s*(?:\#|no\.?|number)?\s*(\d{4}/\d+)",
    re.IGNORECASE,
)

# Regulation reference patterns
_RE_REGULATION = re.compile(
    r"\b((?:SR|LI|NZLI|SL)\s*\d{4}/\d+(?:\.\d+)?)\b",
    re.IGNORECASE,
)
_RE_REGULATION_ALT = re.compile(
    r"\b(\d{4}/\d+)\s*(?:regulations?|instrument)", re.IGNORECASE
)


def extract_meeting_date(text: str) -> str | None:
    """Extract the meeting date from proceeding text."""
    if not text or not text.strip():
        return None
    for pat in _RE_DATE:
        m = pat.search(text)
        if m:
            raw = m.group(1).strip()
            # ISO format
            if re.match(r"^\d{4}-\d{2}-\d{2}$", raw):
                return raw
            # NZ format: "15 March 2024"
            try:
                cleaned = re.sub(r"(st|nd|rd|th)\b", "", raw)
                dt = datetime.strptime(cleaned, "%d %B %Y")
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass
            # DD/MM/YYYY
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


def extract_agenda_items(text: str) -> list[str]:
    """Extract agenda item titles from proceeding text."""
    if not text:
        return []
    items: list[str] = []
    in_agenda = False
    for line in text.splitlines():
        stripped = line.strip()
        if _RE_AGENDA_HEADER.search(stripped) and not in_agenda:
            in_agenda = True
            continue
        if in_agenda:
            m = _RE_AGENDA_ITEM.match(stripped)
            if m:
                items.append(m.group(1).strip())
            elif stripped and not stripped.startswith(("The ", "It was ", "Committee ")):
                if items and re.match(r"^[A-Z]", stripped):
                    break
    return items


def extract_committee_members(text: str) -> list[str]:
    """Extract committee member names from proceeding text."""
    if not text:
        return []
    members: list[str] = []
    for pat in _RE_MEMBERS:
        m = pat.search(text)
        if m:
            raw = m.group(1)
            # Remove parenthetical role qualifiers like (Chair)
            raw = re.sub(r"\s*\([^)]*\)\s*", " ", raw)
            parts = re.split(r",\s*|\s+and\s+", raw)
            for part in parts:
                name = part.strip().strip(".,;:")
                if name and len(name) > 2:
                    members.append(name)
            break
    return members


def extract_complaint_subjects(text: str) -> list[str]:
    """Extract complaint subjects/case numbers from proceeding text."""
    if not text:
        return []
    subjects: list[str] = []
    for m in _RE_COMPLAINT.finditer(text):
        ref = m.group(1).strip()
        label = f"Complaint {ref}"
        if label not in subjects:
            subjects.append(label)
    return subjects


def extract_regulation_references(text: str) -> list[str]:
    """Extract regulation references from proceeding text."""
    if not text:
        return []
    refs: list[str] = []
    for m in _RE_REGULATION.finditer(text):
        ref = m.group(1).strip().upper()
        if ref not in refs:
            refs.append(ref)
    for m in _RE_REGULATION_ALT.finditer(text):
        ref = m.group(1).strip()
        label = f"SR {ref}" if "/" in ref else ref
        if label not in refs:
            refs.append(label)
    return refs


def extract_all_metadata(text: str) -> ProceedingMetadata:
    """Extract all available metadata from proceeding document text."""
    return ProceedingMetadata(
        meeting_date=extract_meeting_date(text),
        agenda_items=extract_agenda_items(text),
        committee_members=extract_committee_members(text),
        complaint_subjects=extract_complaint_subjects(text),
        regulation_references=extract_regulation_references(text),
    )

