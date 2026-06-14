"""Regulation cross-referencing for the Regulations Review Committee.

Maps challenged regulations to secondary legislation keys,
cross-references with the NZ Legislation API,
and builds a correlation index between complaints and legislation.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, asdict
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from scripts.regulations_review_committee.complaint_parser import ComplaintRecord

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SecondaryLegislationKey:
    """A structured key for referencing NZ secondary legislation."""

    prefix: str | None
    year: int
    number: int | None = None

    def __str__(self) -> str:
        if self.prefix and self.number is not None:
            return f"{self.prefix} {self.year}/{self.number}"
        return f"{self.prefix or ''} {self.year}".strip()

    def to_dict(self) -> dict[str, Any]:
        return {
            "prefix": self.prefix,
            "year": self.year,
            "number": self.number,
            "key": str(self),
        }

    @classmethod
    def from_string(cls, raw: str | None) -> SecondaryLegislationKey | None:
        """Parse a secondary legislation key from a string."""
        if not raw:
            return None
        raw = raw.strip()
        if not raw:
            return None
        m = re.match(
            r"^\s*((?:SR|LI|NZLI|SL|SI))\s+(\d{4})/(\d+)\s*$",
            raw,
            re.IGNORECASE,
        )
        if m:
            return cls(
                prefix=m.group(1).upper(),
                year=int(m.group(2)),
                number=int(m.group(3)),
            )
        m = re.match(r"^\s*(\d{4})/(\d+)\s*$", raw)
        if m:
            return cls(prefix="SR", year=int(m.group(1)), number=int(m.group(2)))
        m = re.match(
            r"^(.+?)\s+(Regulations?|Rules?|Order|Instrument|Notice)\s+(\d{4})$",
            raw,
            re.IGNORECASE,
        )
        if m:
            return cls(prefix=m.group(1).strip(), year=int(m.group(3)))
        return None



# Mapping


def map_to_legislation_key(
    regulation_ref: str | None,
) -> SecondaryLegislationKey | None:
    """Map a regulation reference string to a SecondaryLegislationKey."""
    if not regulation_ref:
        return None
    return SecondaryLegislationKey.from_string(regulation_ref)


# NZ Legislation API lookup

_DEFAULT_API_BASE = "https://api.legislation.govt.nz"
_DEFAULT_API_HEADERS = {
    "User-Agent": (
        "corpus-nz-hansard/1.0 (research; "
        "+https://github.com/edithatogo/corpus-nz-hansard)"
    ),
    "Accept": "application/json",
}


def lookup_nz_legislation(
    key: SecondaryLegislationKey | None,
    *,
    api_base: str = _DEFAULT_API_BASE,
    opener: Callable = urlopen,
) -> dict[str, Any] | None:
    """Look up a secondary legislation instrument via the NZ Legislation API."""
    if key is None:
        return None

    if key.prefix and key.number is not None:
        url = (
            f"{api_base.rstrip('/')}/v1/regulation/{key.year}/"
            f"{key.number:04d}.json"
        )
    else:
        from urllib.parse import urlencode

        params = urlencode({
            "q": str(key),
            "type": "regulation",
            "year": str(key.year),
        })
        url = f"{api_base.rstrip('/')}/v1/search.json?{params}"

    try:
        request = Request(url, headers=_DEFAULT_API_HEADERS)
        with opener(request) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data
    except HTTPError as e:
        logger.warning("API HTTP error %s for %s", e.code, url)
        return {"error": f"http_{e.code}", "url": url, "status": e.code}
    except (URLError, OSError, json.JSONDecodeError) as e:
        logger.warning("API error for %s: %s", url, e)
        return {"error": str(e), "url": url}


# Correlation index


@dataclass
class CorrelationEntry:
    """An entry in the complaint-to-legislation correlation index.

    Attributes
    ----------
    complaint_subject:
        The complaint subject identifier.
    legislation_key:
        The mapped secondary legislation key.
    api_result:
        Optional API response data from the NZ Legislation lookup.
    """

    complaint_subject: str
    legislation_key: SecondaryLegislationKey
    api_result: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dict for export."""
        d: dict[str, Any] = {
            "complaint_subject": self.complaint_subject,
            "legislation_key": self.legislation_key.to_dict(),
        }
        if self.api_result is not None:
            d["api_result"] = self.api_result
        return d


def build_correlation_index(
    complaints: list[ComplaintRecord],
    *,
    with_api_lookup: bool = False,
    opener: Callable = urlopen,
) -> list[CorrelationEntry]:
    """Build a correlation index from parsed complaints.

    Maps each complaint's challenged regulation to a
    SecondaryLegislationKey and optionally performs an
    API lookup against the NZ Legislation service.

    Parameters
    ----------
    complaints:
        Parsed complaint records.
    with_api_lookup:
        If True, perform an API lookup for each mapped key.
    opener:
        URL opener callable (injectable for testing).

    Returns
    -------
    list[CorrelationEntry]
        Correlation entries for complaints with parseable regulation refs.
    """
    index: list[CorrelationEntry] = []

    for complaint in complaints:
        if not complaint.challenged_regulation:
            continue

        leg_key = map_to_legislation_key(complaint.challenged_regulation)
        if leg_key is None:
            continue

        api_result = None
        if with_api_lookup:
            api_result = lookup_nz_legislation(leg_key, opener=opener)

        index.append(
            CorrelationEntry(
                complaint_subject=complaint.subject,
                legislation_key=leg_key,
                api_result=api_result,
            )
        )

    return index
