"""Fetch MP lists from Wikipedia for Parliaments 47-53.

The 54th Parliament list is already curated in fetch_parliament_current_mps.py.
This script extends coverage to earlier parliaments (2002-2023).

Output: derived/wikipedia_mp_lists.json
"""

from __future__ import annotations

import json
import re
import time
from datetime import UTC, datetime
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "derived" / "wikipedia_mp_lists.json"

PARLIAMENTS = {
    47: "47th_New_Zealand_Parliament",
    48: "48th_New_Zealand_Parliament",
    49: "49th_New_Zealand_Parliament",
    50: "50th_New_Zealand_Parliament",
    51: "51st_New_Zealand_Parliament",
    52: "52nd_New_Zealand_Parliament",
    53: "53rd_New_Zealand_Parliament",
}

USER_AGENT = "corpus-nz-hansard/1.0 (research; +https://github.com/edithatogo/corpus-nz-hansard)"

# Known party names used in Wikipedia <th> headers (case-insensitive matching)
PARTY_HEADERS = {
    "labour": "Labour",
    "national": "National",
    "green party": "Green",
    "act new zealand": "ACT",
    "maori party": "Maori Party",
    "new zealand first": "NZ First",
    "united future": "United Future",
    "progressive": "Progressive",
    "mana": "Mana",
    "independent": "Independent",
}

# Words that indicate a link is NOT an MP name (combined with context)
SKIP_WORDS = {
    "New Zealand",
    "Parliament",
    "Election",
    "Wikipedia",
    "Minister",
    "Cabinet",
    "Speaker",
    "Whip",
    "Leader",
    "Electoral",
    "Aotearoa",
    "Party",
    "House",
    "Representatives",
    "General",
    "Political",
    "Electorate",
    "Monarch",
    "Governor-General",
    "Sovereign",
    "Website",
    "Overview",
    "File",
    "Template",
    "Category",
    "List of",
    "Main article",
}


def fetch_article(title: str) -> str | None:
    """Fetch Wikipedia article content via the REST API."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/html/{title}"
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html; charset=utf-8"}
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  Error fetching {title}: {e}")
        return None


def extract_party_from_th(th_text: str) -> str | None:
    """Detect party name from a <th> element's text content.

    The Parsoid HTML uses <th> elements like: ``<th ...>Labour (62)</th>``
    or ``<th ...>Green Party of Aotearoa New Zealand (9)</th>``.
    """
    text = th_text.strip()
    count_match = re.search(r"\(\d+\)\s*$", text)
    if not count_match:
        return None
    text = re.sub(r"\s*\(\d+\)\s*$", "", text).strip()
    text_lower = text.lower()
    for key, party in PARTY_HEADERS.items():
        if key in text_lower:
            return party
    return None


def extract_mp_tables(html: str) -> list[dict]:
    """Extract MP names, parties, and electorates from Wikipedia Parsoid HTML."""
    mps = []

    # Locate party header <th> elements containing e.g. "Labour (62)"
    party_markers: list[tuple[int, str]] = []
    for m in re.finditer(
        r"<th[^>]*>(.*?)</th>",
        html,
        re.IGNORECASE | re.DOTALL,
    ):
        party = extract_party_from_th(m.group(1))
        if party:
            party_markers.append((m.start(), party))

    if not party_markers:
        # Fallback: <span> elements with background colors
        for m in re.finditer(
            r'<span[^>]*style="[^"]*background[^"]*"[^>]*>([^<]+)</span>',
            html,
            re.IGNORECASE,
        ):
            party = extract_party_from_th(m.group(1))
            if party:
                party_markers.append((m.start(), party))

    party_markers.sort(key=lambda x: x[0])

    if not party_markers:
        return _extract_mp_tables_per_row(html)

    print(f"    Found {len(party_markers)} party sections: {[p for _, p in party_markers]}")

    # For each party section, extract MP names from the following content
    # Scope to enclosing <table> boundaries to avoid non-MP rows
    for i, (pos, party) in enumerate(party_markers):
        tbl_start = html.rfind("<table", 0, pos)
        tbl_end = html.find("</table>", pos)
        if tbl_start >= 0 and tbl_end > tbl_start:
            end_pos = tbl_end + 8
        else:
            end_pos = party_markers[i + 1][0] if i + 1 < len(party_markers) else len(html)
        section_html = html[pos:end_pos]

        # Find all <tr> rows in this section that contain MP name links
        _extract_mp_rows(section_html, party, mps)

    return mps


def _extract_mp_rows(section_html: str, party: str, mps: list[dict]) -> None:
    """Extract MP rows from a section of HTML scoped to a single party header."""
    for tr_match in re.finditer(
        r"<tr[^>]*>(.*?)</tr>", section_html, re.IGNORECASE | re.DOTALL
    ):
        tr_content = tr_match.group(1)

        # Skip header rows and sub-headers
        if "<th" in tr_content or "<td" not in tr_content:
            continue

        # Find MP name link: <a href="/wiki/Name" ...>Name</a>
        for a_match in re.finditer(
            r'<a\s+(?:[^>]*?\s)?href="(?:\./|/wiki/)([^"]+)"[^>]*>([^<]+)</a>',
            tr_content,
            re.IGNORECASE,
        ):
            name = a_match.group(2).strip()
            wiki_slug = a_match.group(1).strip()

            # Filter out non-MP links
            words = name.split()
            if len(words) < 2 or len(name) > 60 or len(name) < 4:
                continue
            if any(w in SKIP_WORDS for w in words[:2]):
                continue
            if name.startswith(("List of", "Template:", "Category:", "File:")):
                continue

            # Extract electorate from the next <td> after the name link
            electorate = ""
            after_name = tr_content[a_match.end() :]
            td_match = re.search(r"<td[^>]*>(.*?)</td>", after_name, re.IGNORECASE | re.DOTALL)
            if td_match:
                td_content = td_match.group(1).strip()
                elec_link = re.search(r"<a[^>]*>([^<]+)</a>", td_content, re.IGNORECASE)
                if elec_link:
                    electorate = elec_link.group(1).strip()
                elif td_content and td_content not in ("\u2014", "\u2013", ""):
                    electorate = td_content

            if not electorate or electorate.lower() == "list":
                electorate = "List"

            mps.append(
                {
                    "name": name,
                    "party": party,
                    "electorate": electorate,
                    "wiki_slug": wiki_slug,
                }
            )
            # Only take the first name link per row
            break


def main():
    all_mps: dict[int, list[dict]] = {}

    for parliament, article in PARLIAMENTS.items():
        print(f"\nFetching {parliament}th Parliament ({article})...")
        html = fetch_article(article)
        if not html:
            continue

        mps = extract_mp_tables(html)
        all_mps[parliament] = mps
        print(f"  Extracted {len(mps)} MP references")
        time.sleep(1)

    # Save
    output = {
        "source": "Wikipedia",
        "fetched_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "parliaments_covered": list(PARLIAMENTS.keys()),
        "total_mps": sum(len(v) for v in all_mps.values()),
        "members_by_parliament": {str(k): v for k, v in all_mps.items()},
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"\nSaved to {OUTPUT_PATH}")
    print(f"Total MP references: {output['total_mps']}")
    for p, mps in all_mps.items():
        parties = {mp["party"] for mp in mps if mp["party"]}
        print(f"  Parliament {p}: {len(mps)} MPs, parties: {parties}")


if __name__ == "__main__":
    main()
