"""Cross-corpus indexing for select committee reports (Track 8, Phase 2).

Links reports to Hansard debates and legislation bills/acts,'nand provides a structured Parquet schema for the correlation index.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HansardLink:
    """A link from a report to a Hansard debate."""
    hansard_id: str
    sitting_date: str | None = None
    debate_title: str | None = None
    relevance: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"hansard_id": self.hansard_id}
        if self.sitting_date is not None:
            d["sitting_date"] = self.sitting_date
        if self.debate_title is not None:
            d["debate_title"] = self.debate_title
        d["relevance"] = self.relevance
        return d


@dataclass
class LegislationLink:
    """A link from a report to an Act or Bill."""
    legislation_id: str
    legislation_type: str | None = None
    legislation_url: str | None = None

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"legislation_id": self.legislation_id}
        if self.legislation_type is not None:
            d["legislation_type"] = self.legislation_type
        if self.legislation_url is not None:
            d["legislation_url"] = self.legislation_url
        return d


@dataclass
class CorrelationEntry:
    """A single correlation index entry linking a report to Hansard/legislation."""
    report_id: str
    committee_name: str | None = None
    report_title: str | None = None
    report_date: str | None = None
    hansard_links: list[HansardLink] = field(default_factory=list)
    legislation_links: list[LegislationLink] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"report_id": self.report_id}
        if self.committee_name is not None:
            d["committee_name"] = self.committee_name
        if self.report_title is not None:
            d["report_title"] = self.report_title
        if self.report_date is not None:
            d["report_date"] = self.report_date
        if self.hansard_links:
            d["hansard_links"] = [h.to_dict() for h in self.hansard_links]
        if self.legislation_links:
            d["legislation_links"] = [l.to_dict() for l in self.legislation_links]
        return d

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CorrelationEntry):
            return NotImplemented
        return self.report_id == other.report_id

    def __hash__(self) -> int:
        return hash(self.report_id)


@dataclass
class CorrelationIndex:
    """A collection of correlation index entries.
    Provides serialisation to dicts and metadata about the index.
    """
    entries: list[CorrelationEntry] = field(default_factory=list)

    def to_dicts(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self.entries]

    def metadata(self) -> dict[str, Any]:
        committees = sorted(set(
            e.committee_name for e in self.entries
            if e.committee_name is not None
        ))
        return {
            "total_entries": len(self.entries),
            "corpus": "corpus-nz-hansard",
            "committees": committees,
        }


_DEFAULT_DEBATES: list[dict[str, str]] = []


def build_hansard_links(
    report_title: str | None = None,
    committee_name: str | None = None,
    report_date: str | None = None,
    available_debates: list[dict[str, str]] | None = None,
) -> list[HansardLink]:
    """Build links from a report to Hansard debates by title matching."""
    import re
    if available_debates is None:
        available_debates = _DEFAULT_DEBATES

    links: list[HansardLink] = []
    if not report_title:
        return links

    title_lower = report_title.lower()

    for debate in available_debates:
        debate_title = debate.get("title", "")
        debate_id = debate.get("id", "")
        debate_date = debate.get("date")

        score = 0.0
        for word in re.findall(r"[A-Z][a-z]+", report_title)[:5]:
            if word.lower() in debate_title.lower():
                score += 0.3

        if committee_name and committee_name.lower() in debate_title.lower():
            score += 0.4

        if score > 0.3:
            links.append(HansardLink(
                hansard_id=debate_id,
                sitting_date=debate_date,
                debate_title=debate_title,
                relevance=min(score, 1.0),
            ))

    return links


def build_legislation_links(
    legislation_refs: list[str] | None = None,
    bill_refs: list[str] | None = None,
) -> list[LegislationLink]:
    """Build links from a report to legislation and bills."""
    links: list[LegislationLink] = []
    if legislation_refs:
        for ref in legislation_refs:
            links.append(LegislationLink(
                legislation_id=ref,
                legislation_type="act",
            ))
    if bill_refs:
        for ref in bill_refs:
            links.append(LegislationLink(
                legislation_id=ref,
                legislation_type="bill",
            ))
    return links


def build_correlation_index(
    parsed_reports: list[dict[str, Any]],
    available_debates: list[dict[str, str]] | None = None,
) -> CorrelationIndex:
    """Build a correlation index from parsed report dicts."""
    index = CorrelationIndex()
    for report in parsed_reports:
        report_id = report.get("report_id", "")
        if not report_id:
            continue

        committee_name = report.get("committee_name")
        report_title = report.get("report_title")
        report_date = report.get("report_date")

        hansard_links = build_hansard_links(
            report_title=report_title,
            committee_name=committee_name,
            report_date=report_date,
            available_debates=available_debates,
        )

        legislation_links = build_legislation_links(
            legislation_refs=report.get("referenced_legislation"),
            bill_refs=report.get("referenced_bills"),
        )

        entry = CorrelationEntry(
            report_id=report_id,
            committee_name=committee_name,
            report_title=report_title,
            report_date=report_date,
            hansard_links=hansard_links,
            legislation_links=legislation_links,
        )
        index.entries.append(entry)

    return index


# Parquet-style schema definition
CORRELATION_INDEX_SCHEMA: dict[str, Any] = {
    "title": "Select Committee Report Correlation Index",
    "description": "Cross-corpus index linking reports to debates and legislation.",
    "type": "struct",
    "fields": [
        {"name": "report_id", "type": "string", "nullable": False},
        {"name": "committee_name", "type": "string", "nullable": True},
        {"name": "report_title", "type": "string", "nullable": True},
        {"name": "report_date", "type": "string", "nullable": True},
        {"name": "hansard_links", "type": {
            "type": "array",
            "items": {
                "type": "struct",
                "fields": [
                    {"name": "hansard_id", "type": "string", "nullable": False},
                    {"name": "sitting_date", "type": "string", "nullable": True},
                    {"name": "debate_title", "type": "string", "nullable": True},
                    {"name": "relevance", "type": "float", "nullable": False},
                ],
            },
        }, "nullable": True},
        {"name": "legislation_links", "type": {
            "type": "array",
            "items": {
                "type": "struct",
                "fields": [
                    {"name": "legislation_id", "type": "string", "nullable": False},
                    {"name": "legislation_type", "type": "string", "nullable": True},
                    {"name": "legislation_url", "type": "string", "nullable": True},
                ],
            },
        }, "nullable": True},
    ],
}
