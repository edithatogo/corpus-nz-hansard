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
from hashlib import sha256
from html import unescape
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
    "labour party": "Labour",
    "national": "National",
    "national party": "National",
    "green party": "Green",
    "green party of aotearoa new zealand": "Green",
    "act new zealand": "ACT",
    "maori party": "Maori Party",
    "new zealand first": "NZ First",
    "new zealand labour party": "Labour",
    "new zealand national party": "National",
    "united future": "United Future",
    "united future new zealand": "United Future",
    "progressive": "Progressive",
    "mana": "Mana",
    "independent": "Independent",
}

PARTY_LABELS = {
    "act": "ACT",
    "act new zealand": "ACT",
    "green": "Green",
    "green party": "Green",
    "green party of aotearoa new zealand": "Green",
    "labour": "Labour",
    "maori party": "Maori Party",
    "māori party": "Maori Party",
    "mana": "Mana",
    "national": "National",
    "new zealand first": "NZ First",
    "new zealand labour party": "Labour",
    "new zealand national party": "National",
    "nz first": "NZ First",
    "progressive": "Progressive",
    "united future": "United Future",
    "united future new zealand": "United Future",
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


def article_url(title: str) -> str:
    return f"https://en.wikipedia.org/api/rest_v1/page/html/{title}"


def fetch_article(title: str) -> tuple[str | None, dict[str, str]]:
    """Fetch Wikipedia article content via the REST API."""
    url = article_url(title)
    headers = {"User-Agent": USER_AGENT, "Accept": "text/html; charset=utf-8"}
    fetched_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text, {
            "article": title,
            "url": url,
            "fetched_at": fetched_at,
            "status": "ok",
            "html_sha256": sha256(resp.text.encode("utf-8")).hexdigest(),
        }
    except Exception as e:
        print(f"  Error fetching {title}: {e}")
        return None, {
            "article": title,
            "url": url,
            "fetched_at": fetched_at,
            "status": "error",
            "error": str(e),
        }


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


def normalize_party_label(value: str) -> str:
    """Normalize visible Wikipedia party labels into canonical short labels."""
    text = clean_html_text(value).strip()
    return PARTY_LABELS.get(text.lower(), text)


def extract_party_from_cell(cell_html: str) -> str:
    """Extract canonical party label from a visible cell or Parsoid template metadata."""
    text = normalize_party_label(cell_html)
    if text in set(PARTY_LABELS.values()):
        return text

    metadata_text = unescape(cell_html)
    for data_mw_match in re.finditer(r'"wt"\s*:\s*"([^"]+)"', metadata_text, re.IGNORECASE):
        metadata_label = normalize_party_label(data_mw_match.group(1))
        if metadata_label in set(PARTY_LABELS.values()):
            return metadata_label

    metadata_lower = metadata_text.lower()
    for key, party in sorted(PARTY_LABELS.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = rf"(?<![a-z]){re.escape(key)}(?![a-z])"
        if re.search(pattern, metadata_lower):
            return party

    return text if text in set(PARTY_LABELS.values()) else ""


def clean_html_text(value: str) -> str:
    """Remove simple tags and collapse whitespace from an HTML fragment."""
    text = re.sub(r"<[^>]+>", " ", value)
    return re.sub(r"\s+", " ", unescape(text)).strip()


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
        next_marker = party_markers[i + 1][0] if i + 1 < len(party_markers) else len(html)
        if tbl_start >= 0 and tbl_end > tbl_start:
            end_pos = min(tbl_end + len("</table>"), next_marker)
        else:
            end_pos = next_marker
        section_html = html[pos:end_pos]

        # Find all <tr> rows in this section that contain MP name links
        _extract_mp_rows(section_html, party, mps)

    return mps


def _extract_mp_rows(section_html: str, party: str, mps: list[dict]) -> None:
    """Extract MP rows from a section of HTML scoped to a single party header."""
    for tr_match in re.finditer(r"<tr[^>]*>(.*?)</tr>", section_html, re.IGNORECASE | re.DOTALL):
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


def _extract_mp_tables_per_row(html: str) -> list[dict]:
    """Extract MP rows when party section markers are unavailable."""
    mps: list[dict] = []
    for tr_match in re.finditer(r"<tr[^>]*>(.*?)</tr>", html, re.IGNORECASE | re.DOTALL):
        tr_content = tr_match.group(1)
        cells = re.findall(r"<td\b[^>]*>.*?</td>", tr_content, re.IGNORECASE | re.DOTALL)
        if len(cells) < 3:
            continue

        if len(cells) == 3:
            # Older fixtures and some simple tables use:
            # party, electorate/list, member.
            party_cell = cells[0]
            electorate_cell = cells[1]
            member_cell = cells[2]
        elif (
            len(cells) >= 5
            and extract_party_from_cell(cells[0])
            and normalize_party_label(cells[1]) not in set(PARTY_LABELS.values())
        ):
            # Some live Parsoid tables use:
            # colour swatch containing party metadata, member, electorate/list,
            # term number, roles.
            party_cell = cells[0]
            member_cell = cells[1]
            electorate_cell = cells[2]
        else:
            # Older live Parliament pages use:
            # colour swatch, party, member, electorate/list, term number.
            party_cell = cells[1]
            member_cell = cells[2]
            electorate_cell = cells[3]

        party = extract_party_from_cell(party_cell)
        if not party or any(skip == party for skip in ("Party", "Election", "Parliament")):
            continue

        member_link = re.search(
            r'<a\s+(?:[^>]*?\s)?href="(?:\./|/wiki/)([^"]+)"[^>]*>(.*?)</a>',
            member_cell,
            re.IGNORECASE | re.DOTALL,
        )
        if not member_link:
            continue

        wiki_slug = member_link.group(1).strip()
        name = clean_html_text(member_link.group(2))
        words = name.split()
        if len(words) < 2 or len(name) > 60 or len(name) < 4:
            continue
        if any(w in SKIP_WORDS for w in words[:2]):
            continue

        electorate = clean_html_text(electorate_cell)
        if not electorate or electorate in ("\u2014", "\u2013"):
            electorate = "List"
        if electorate.lower() in {"party list", "list"}:
            electorate = "List"

        mps.append(
            {
                "name": name,
                "party": party,
                "electorate": electorate,
                "wiki_slug": wiki_slug,
            }
        )
    return mps


def main():
    all_mps: dict[int, list[dict]] = {}
    source_articles: dict[str, dict[str, str]] = {}

    for parliament, article in PARLIAMENTS.items():
        print(f"\nFetching {parliament}th Parliament: {article}")
        html, source_article = fetch_article(article)
        source_articles[str(parliament)] = source_article
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
        "source_articles": source_articles,
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
