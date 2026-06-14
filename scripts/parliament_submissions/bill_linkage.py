"""Bill ID linkage for parliament submissions."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _normalize_bill_title(title: str | None) -> str:
    if not title:
        return ""
    t = title.lower().strip()
    t = re.sub(r"[.,;:!?]+", "", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


_RE_BILL_IN_TEXT = re.compile(
    r"(?:submission\s+(?:on|regarding|re:|concerning|about)\s+)"
    r"(?:the\s+)?(?:draft\s+)?"
    r"([A-Z][A-Za-z\s&]+?(?:Amendment|Reform|Review|Bill))"
    r"(?:\s+Bill)?(?:\s+\d{4})?",
    re.IGNORECASE,
)

_RE_BILL_SUFFIX = re.compile(
    r"(?:^|\s)([A-Z][A-Za-z]*(?:\s+[A-Z][A-Za-z]+)*\s+Bill)(?:\s+\d{4})?"
)


def parse_bill_reference_from_text(text: str | None) -> str | None:
    if not text or not text.strip():
        return None
    m = _RE_BILL_IN_TEXT.search(text)
    if m:
        ref = m.group(1).strip().rstrip(".,;:")
        if len(ref) >= 5:
            return ref
    m = _RE_BILL_SUFFIX.search(text)
    if m:
        ref = m.group(1).strip().rstrip(".,;:")
        if len(ref) >= 5:
            return ref
    return None

_DEFAULT_CATALOG_PATH = (
    Path(__file__).resolve().parents[2]
    / "derived" / "bills_api" / "bills_summary_20260613T021002Z.json"
)

_BILLS_CATALOG_CACHE: list[dict[str, Any]] | None = None


def _load_default_catalog() -> list[dict[str, Any]]:
    global _BILLS_CATALOG_CACHE
    if _BILLS_CATALOG_CACHE is not None:
        return _BILLS_CATALOG_CACHE
    path = _DEFAULT_CATALOG_PATH
    if path.exists():
        try:
            with open(str(path), "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                _BILLS_CATALOG_CACHE = data
                return _BILLS_CATALOG_CACHE
        except (json.JSONDecodeError, OSError):
            pass
    _BILLS_CATALOG_CACHE = []
    return _BILLS_CATALOG_CACHE


class BillLinkageIndex:
    """Maps submission IDs to bill IDs using a catalog of known bills."""

    def __init__(
        self,
        bills_catalog: list[dict[str, Any]] | None = None,
    ) -> None:
        self.bills_catalog: list[dict[str, Any]] = bills_catalog or []
        self._lookup: dict[str, str] = {}
        self.linkage_map: dict[str, dict[str, Any]] = {}

        for bill in self.bills_catalog:
            bill_id = bill.get("id", "")
            title = bill.get("title", "")
            if bill_id and title:
                key = _normalize_bill_title(title)
                if key:
                    self._lookup[key] = bill_id

    def lookup(self, bill_reference: str | None) -> str | None:
        if not bill_reference:
            return None
        key = _normalize_bill_title(bill_reference)
        if not key:
            return None
        return self._lookup.get(key)

    def add_linkage(
        self,
        submission_id: str,
        bill_id: str,
        *,
        confidence: float = 1.0,
        method: str = "exact",
    ) -> None:
        self.linkage_map[submission_id] = {
            "submission_id": submission_id,
            "bill_id": bill_id,
            "confidence": confidence,
            "method": method,
        }

    def export_linkage_index(self) -> list[dict[str, Any]]:
        return list(self.linkage_map.values())

    def __repr__(self) -> str:
        return (
            f"BillLinkageIndex("
            f"{len(self.bills_catalog)} bills, "
            f"{len(self.linkage_map)} linkages)"
        )


def cross_reference_bills(
    submissions: list[dict[str, Any]],
    bills_catalog: list[dict[str, Any]],
) -> BillLinkageIndex:
    idx = BillLinkageIndex(bills_catalog)
    for sub in submissions:
        sid = sub.get("submission_id") or sub.get("id")
        if not sid:
            continue
        ref = sub.get("bill_reference_normalized") or sub.get("bill_reference")
        bill_id = idx.lookup(ref)
        if bill_id:
            idx.add_linkage(str(sid), bill_id, confidence=1.0, method="exact")
    return idx


def build_linkage_index(
    normalized_submissions: list[dict[str, Any]],
    bills_catalog: list[dict[str, Any]] | None = None,
) -> BillLinkageIndex:
    if bills_catalog is None:
        bills_catalog = DEFAULT_BILLS_CATALOG

    idx = cross_reference_bills(normalized_submissions, bills_catalog)

    for sub in normalized_submissions:
        sid = sub.get("submission_id") or sub.get("id")
        if not sid or sid in idx.linkage_map:
            continue
        text = sub.get("text_content", "")
        if text:
            parsed_ref = parse_bill_reference_from_text(text)
            if parsed_ref:
                bill_id = idx.lookup(parsed_ref)
                if bill_id:
                    idx.add_linkage(str(sid), bill_id, confidence=0.8, method="text_parse")

    return idx


DEFAULT_BILLS_CATALOG: list[dict[str, Any]] = _load_default_catalog()
