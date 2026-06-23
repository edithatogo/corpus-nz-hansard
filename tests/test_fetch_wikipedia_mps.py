from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.fetch_wikipedia_mps import extract_mp_tables, extract_party_from_cell


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "wikipedia_mps"


def read_fixture(name: str) -> str:
    return (FIXTURE_DIR / name).read_text(encoding="utf-8")


class FetchWikipediaMpsTests(unittest.TestCase):
    def test_extracts_modern_party_header_tables(self) -> None:
        html = read_fixture("modern_party_header_table.html")

        self.assertEqual(
            extract_mp_tables(html),
            [
                {
                    "name": "Jacinda Ardern",
                    "party": "Labour",
                    "electorate": "Mount Albert",
                    "wiki_slug": "Jacinda_Ardern",
                },
                {
                    "name": "Grant Robertson",
                    "party": "Labour",
                    "electorate": "List",
                    "wiki_slug": "Grant_Robertson",
                },
                {
                    "name": "Chloe Swarbrick",
                    "party": "Green",
                    "electorate": "Auckland Central",
                    "wiki_slug": "Chloe_Swarbrick",
                },
            ],
        )

    def test_extracts_older_per_row_party_electorate_member_tables(self) -> None:
        html = read_fixture("older_per_row_party_electorate_member_table.html")

        self.assertEqual(
            extract_mp_tables(html),
            [
                {
                    "name": "Helen Clark",
                    "party": "Labour",
                    "electorate": "Mount Albert",
                    "wiki_slug": "Helen_Clark",
                },
                {
                    "name": "Simon Bridges",
                    "party": "National",
                    "electorate": "Tauranga",
                    "wiki_slug": "Simon_Bridges",
                },
                {
                    "name": "Rodney Hide",
                    "party": "ACT",
                    "electorate": "List",
                    "wiki_slug": "Rodney_Hide",
                },
            ],
        )

    def test_extracts_color_cell_party_member_electorate_tables(self) -> None:
        html = read_fixture("color_cell_party_member_electorate_table.html")

        self.assertEqual(
            extract_mp_tables(html),
            [
                {
                    "name": "Ruth Dyson",
                    "party": "Labour",
                    "electorate": "Port Hills",
                    "wiki_slug": "Ruth_Dyson",
                },
                {
                    "name": "Metiria Turei",
                    "party": "Green",
                    "electorate": "List",
                    "wiki_slug": "Metiria_Turei",
                },
                {
                    "name": "David Bennett",
                    "party": "National",
                    "electorate": "Hamilton East",
                    "wiki_slug": "David_Bennett_(New_Zealand_politician)",
                },
            ],
        )


    def test_party_metadata_does_not_use_unrelated_substrings(self) -> None:
        cell_html = '<td data-mw="{&quot;action&quot;:&quot;view&quot;}">&nbsp;</td>'

        self.assertEqual(extract_party_from_cell(cell_html), "")


if __name__ == "__main__":
    unittest.main()
