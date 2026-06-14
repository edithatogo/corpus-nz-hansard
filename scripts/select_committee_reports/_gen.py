import os

HERE = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(HERE, 'report_parser.py')

# Write all content at once
content = """
"""Enhanced report parsing for select committee reports (Track 8, Phase 2)."""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class LegislationRef:
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
    name: str
    bill_number: str | None = None
    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name}
        if self.bill_number is not None:
            d["bill_number"] = self.bill_number
        return d

@dataclass
class WitnessSubmitter:
    name: str
    affiliation: str | None = None
    def to_dict(self) -> dict[str, Any]:
        d = {"name": self.name}
        if self.affiliation is not None:
            d["affiliation"] = self.affiliation
        return d

@dataclass
class ParsedReport:
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
"""

with open(path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Base written')
