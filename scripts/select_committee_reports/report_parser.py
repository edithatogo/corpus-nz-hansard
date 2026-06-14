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


@dataclass
class LegislationRef:
    """A reference to an Act of Parliament or other legislation."""
    name: str
    year: int | None = None
    type: str = "act"
    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name, "type": self.type}
        if self.year is not None:
            d["year"] = self.year
        return d


@dataclass
class BillRef:
    """A reference to a Bill before Parliament."""
    name: str
    bill_number: str | None = None
    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name}
        if self.bill_number is not None:
            d["bill_number"] = self.bill_number
        return d


# Enhanced regex patterns and functions (Track 8 Phase 2)

_RE_TITLE_INQUIRY = re.compile(
    r"(?:Inquiry\s+into\s+(?:the\s+)?(.+?))(?:\\n|$)",
    re.IGNORECASE,
)
_RE_TITLE_PETITION = re.compile(
    r"(Petition\s+of\s+.+?)(?:\\n|$)",
    re.IGNORECASE,
)

_RE_RECOMMENDATIONS_SECTION = re.compile(
    r"^Recommendations?\s*$",
    re.IGNORECASE | re.MULTILINE,
)
_RE_FINDINGS_SECTION = re.compile(
    r"^Findings?\s*$",
    re.IGNORECASE | re.MULTILINE,
)

_RE_NUMBERED_ITEM = re.compile(
    r"^\s*(?:\d+[\.\)]|[a-z][\.\)])\s*(.+)$",
    re.MULTILINE,
)

_RE_LEGISLATION = re.compile(
    r"([A-Z][a-zA-Z]+(?:\s+(?:[A-Z][a-zA-Z]+|[a-z]+))*"
    r"(?:\s+(?:of|and|in|for|to|at|on|by|with)\s+[A-Z][a-zA-Z]+)?)"
    r"\s+(Act|Regulations?|Ordinance)\s+(\d{4})",
)

_RE_BILL = re.compile(
    r"([A-Z][a-zA-Z]+(?:\s+(?:[A-Z][a-zA-Z]+|[a-z]+))*"
    r"(?:\s+\([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\))?"
    r"\s+Bill)(?:\s*\((\d{4}/\d+)\))?",
)

_RE_SUBMISSIONS_SECTION = re.compile(
    r"^(?:Submissions?\s*(?:received|made)?|Witnesses?\s*(?:appeared|heard)?|"
    r"List\s+of\s+(?:submitters?|witnesses?))\s*",
    re.IGNORECASE | re.MULTILINE,
)

_RE_SUBMITTER_LINE = re.compile(
    r"^\s*(?:[-\*\d]+[\.\)]\s*)?"
    r"([A-Za-z][A-Za-z\s,\.]+?)(?:\s*\(([^)]+)\))?\s*$",
    re.MULTILINE,
)


def extract_report_title(text: str | None) -> str | None:
    """Extract the report title / subject matter."""
    if not text or not text.strip():
        return None
    m = _RE_TITLE_INQUIRY.search(text)
    if m:
        title = m.group(1).strip()
        title = re.sub(r"\s*[\.\\n]+$", "", title)
        return f"Inquiry into the {title}"
    m = _RE_TITLE_PETITION.search(text)
    if m:
        return m.group(1).strip()
    return None


def _extract_section_text(text: str, pat: re.Pattern) -> list[str]:
    lines = text.split(chr(10))
    in_section = False
    items: list[str] = []
    for line in lines:
        if pat.match(line.strip()):
            in_section = True
            continue
        if in_section:
            if re.match(r"^[A-Z][a-z]+(?:s|ion)?\s*$", line.strip()):
                if items and len(line.strip()) < 60:
                    break
            m = _RE_NUMBERED_ITEM.match(line)
            if m:
                items.append(m.group(1).strip())
            elif line.strip() and not line.strip().startswith(("Contents", "Appendix")):
                stripped = line.strip()
                if stripped and stripped[0].isupper():
                    if items and not items[-1].rstrip().endswith((".", "!", "?")):
                        items[-1] = items[-1] + " " + stripped
                    else:
                        items.append(stripped)
                elif stripped and items:
                    items[-1] = items[-1] + " " + stripped
    return items


def extract_recommendations(text: str | None) -> list[str]:
    if not text:
        return []
    return _extract_section_text(text, _RE_RECOMMENDATIONS_SECTION)


def extract_findings(text: str | None) -> list[str]:
    if not text:
        return []
    return _extract_section_text(text, _RE_FINDINGS_SECTION)


@dataclass
class WitnessSubmitter:
    """An individual or organisation that made a submission or appeared as witness."""
    name: str
    affiliation: str | None = None
    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name}
        if self.affiliation is not None:
            d["affiliation"] = self.affiliation
        return d


@dataclass
class ParsedReport:
    """Fully parsed and structured data from a select committee report."""
    committee_name: str | None = None
    report_title: str | None = None
    report_date: str | None = None
    recommendations: list[str] = field(default_factory=list)
    findings: list[str] = field(default_factory=list)
    referenced_legislation: list[str] = field(default_factory=list)
    referenced_bills: list[str] = field(default_factory=list)
    witnesses_submitters: list[WitnessSubmitter] = field(default_factory=list)
    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.committee_name is not None:
            result["committee_name"] = self.committee_name
        if self.report_title is not None:
            result["report_title"] = self.report_title
        if self.report_date is not None:
            result["report_date"] = self.report_date
        if self.recommendations:
            result["recommendations"] = self.recommendations
        if self.findings:
            result["findings"] = self.findings
        if self.referenced_legislation:
            result["referenced_legislation"] = self.referenced_legislation
        if self.referenced_bills:
            result["referenced_bills"] = self.referenced_bills
        if self.witnesses_submitters:
            result["witnesses_submitters"] = [w.to_dict() for w in self.witnesses_submitters]
        return result


# Remaining enhanced functions

_LEADING_WORDS = {"the", "this", "these", "that", "a", "an", "references",
    "including", "related", "such", "other", "all",
    "relevant", "applicable", "committee", "considered", "report"}


def _clean_name(full_match, suffix):
    idx = full_match.rfind(suffix)
    if idx < 0:
        return None
    before = full_match[:idx].strip()
    words = before.split()
    filtered = [w for w in words if w.lower() not in _LEADING_WORDS]
    if filtered:
        name = " ".join(filtered)
        if len(name) > 3:
            return name + " " + suffix
    return None


def extract_referenced_legislation(text):
    if not text:
        return []
    refs = []
    for m in _RE_LEGISLATION.finditer(text):
        full = m.group(0)
        if chr(10) in full or chr(13) in full:
            continue
        act_type = m.group(2)
        year = m.group(3)
        name = _clean_name(full, act_type)
        if name:
            full_ref = f"{name} {year}"
            if full_ref not in refs:
                refs.append(full_ref)
    return refs


def extract_referenced_bills(text):
    if not text:
        return []
    bills = []
    for m in _RE_BILL.finditer(text):
        full = m.group(0)
        name = _clean_name(full, "Bill")
        if name and name not in bills and len(name) > 10:
            bills.append(name)
    return bills


def extract_witnesses_submitters(text):
    if not text:
        return []
    witnesses = []
    in_submissions = False
    for line in text.split(chr(10)):
        stripped = line.strip()
        if _RE_SUBMISSIONS_SECTION.match(stripped):
            in_submissions = True
            continue
        if in_submissions:
            if not stripped:
                continue
            if re.match(r"^[A-Z][a-z]+\s*$", stripped) and len(stripped) <= 50:
                if witnesses:
                    break
            if stripped.startswith(("The committee", "The total", "A list", "Appendix")):
                if witnesses:
                    break
            m = _RE_SUBMITTER_LINE.match(stripped)
            if m:
                name = m.group(1).strip().strip(".",)
                affiliation = m.group(2).strip() if m.group(2) else None
                if name and len(name) > 2:
                    witnesses.append(WitnessSubmitter(name=name, affiliation=affiliation))
    return witnesses


def parse_report_text(text):
    """Parse a full select committee report text into structured data."""
    if not text or not text.strip():
        return ParsedReport()
    return ParsedReport(
        committee_name=extract_committee_name(text),
        report_title=extract_report_title(text),
        report_date=extract_report_date(text),
        recommendations=extract_recommendations(text),
        findings=extract_findings(text),
        referenced_legislation=extract_referenced_legislation(text),
        referenced_bills=extract_referenced_bills(text),
        witnesses_submitters=extract_witnesses_submitters(text),
    )
