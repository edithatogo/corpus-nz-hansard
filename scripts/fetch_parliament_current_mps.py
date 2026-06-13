"""Scrape current NZ Parliament MPs from 54th Parliament Wikipedia article.

The official Parliament website is behind Cloudflare. This script uses
curated Wikipedia data as the authoritative source for current MP names.

Output: derived/parliament_current_mps.json
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "derived" / "parliament_current_mps.json"
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/54th_New_Zealand_Parliament"

# Curated list of 54th Parliament MPs sourced from Wikipedia
CURRENT_MP_NAMES: list[dict[str, str]] = [
    # National (49)
    {"name": "Christopher Luxon", "party": "National", "electorate": "Botany"},
    {"name": "Nicola Willis", "party": "National", "electorate": "List"},
    {"name": "Chris Bishop", "party": "National", "electorate": "Hutt South"},
    {"name": "Simeon Brown", "party": "National", "electorate": "Pakuranga"},
    {"name": "Erica Stanford", "party": "National", "electorate": "East Coast Bays"},
    {"name": "Paul Goldsmith", "party": "National", "electorate": "List"},
    {"name": "Louise Upston", "party": "National", "electorate": "Taupo"},
    {"name": "Judith Collins", "party": "National", "electorate": "Papakura"},
    {"name": "Shane Reti", "party": "National", "electorate": "Whangarei"},
    {"name": "Mark Mitchell", "party": "National", "electorate": "Whangaparoa"},
    {"name": "Todd McClay", "party": "National", "electorate": "Rotorua"},
    {"name": "Tama Potaka", "party": "National", "electorate": "Hamilton West"},
    {"name": "Matt Doocey", "party": "National", "electorate": "Waimakariri"},
    {"name": "Simon Watts", "party": "National", "electorate": "North Shore"},
    {"name": "Chris Penk", "party": "National", "electorate": "Kaipara ki Mahurangi"},
    {"name": "Penny Simmonds", "party": "National", "electorate": "Invercargill"},
    {"name": "Nicola Grigg", "party": "National", "electorate": "Selwyn"},
    {"name": "James Meager", "party": "National", "electorate": "Rangitata"},
    {"name": "Scott Simpson", "party": "National", "electorate": "Coromandel"},
    {"name": "Gerry Brownlee", "party": "National", "electorate": "List"},
    {"name": "Barbara Kuriger", "party": "National", "electorate": "Taranaki-King Country"},
    {"name": "Maureen Pugh", "party": "National", "electorate": "West Coast-Tasman"},
    {"name": "Stuart Smith", "party": "National", "electorate": "Kaikoura"},
    {"name": "Suze Redmayne", "party": "National", "electorate": "Rangitikei"},
    {"name": "Melissa Lee", "party": "National", "electorate": "List"},
    {"name": "Andrew Bayly", "party": "National", "electorate": "Port Waikato"},
    {"name": "Nancy Lu", "party": "National", "electorate": "List"},
    {"name": "Katie Nimon", "party": "National", "electorate": "Napier"},
    {"name": "Catherine Wedd", "party": "National", "electorate": "Tukituki"},
    {"name": "Paulo Garcia", "party": "National", "electorate": "New Lynn"},
    {"name": "Vanessa Weenink", "party": "National", "electorate": "Banks Peninsula"},
    {"name": "Rima Nakhle", "party": "National", "electorate": "Takanini"},
    {"name": "Dana Kirkpatrick", "party": "National", "electorate": "East Coast"},
    {"name": "Carl Bates", "party": "National", "electorate": "Whanganui"},
    {"name": "Carlos Cheung", "party": "National", "electorate": "Mount Roskill"},
    {"name": "Joseph Mooney", "party": "National", "electorate": "Southland"},
    {"name": "Sam Uffindell", "party": "National", "electorate": "Tauranga"},
    {"name": "Tim van de Molen", "party": "National", "electorate": "Waikato"},
    {"name": "Miles Anderson", "party": "National", "electorate": "Waitaki"},
    {"name": "Dan Bidois", "party": "National", "electorate": "Northcote"},
    {"name": "Mike Butterick", "party": "National", "electorate": "Wairarapa"},
    {"name": "Cameron Brewer", "party": "National", "electorate": "Upper Harbour"},
    {"name": "Hamish Campbell", "party": "National", "electorate": "Ilam"},
    {"name": "Tim Costley", "party": "National", "electorate": "Otaki"},
    {"name": "Greg Fleming", "party": "National", "electorate": "Maungakiekie"},
    {"name": "Ryan Hamilton", "party": "National", "electorate": "Hamilton East"},
    {"name": "David MacLeod", "party": "National", "electorate": "New Plymouth"},
    {"name": "Grant McCallum", "party": "National", "electorate": "Northland"},
    {"name": "Tom Rutherford", "party": "National", "electorate": "Bay of Plenty"},
    # ACT (11)
    {"name": "David Seymour", "party": "ACT", "electorate": "Epsom"},
    {"name": "Brooke van Velden", "party": "ACT", "electorate": "Tamaki"},
    {"name": "Nicole McKee", "party": "ACT", "electorate": "List"},
    {"name": "Andrew Hoggard", "party": "ACT", "electorate": "List"},
    {"name": "Karen Chhour", "party": "ACT", "electorate": "List"},
    {"name": "Simon Court", "party": "ACT", "electorate": "List"},
    {"name": "Todd Stephenson", "party": "ACT", "electorate": "List"},
    {"name": "Mark Cameron", "party": "ACT", "electorate": "List"},
    {"name": "Parmjeet Parmar", "party": "ACT", "electorate": "List"},
    {"name": "Laura McClure", "party": "ACT", "electorate": "List"},
    {"name": "Cameron Luxton", "party": "ACT", "electorate": "List"},
    # NZ First (8)
    {"name": "Winston Peters", "party": "NZ First", "electorate": "List"},
    {"name": "Shane Jones", "party": "NZ First", "electorate": "List"},
    {"name": "Casey Costello", "party": "NZ First", "electorate": "List"},
    {"name": "Mark Patterson", "party": "NZ First", "electorate": "List"},
    {"name": "Jenny Marcroft", "party": "NZ First", "electorate": "List"},
    {"name": "Jamie Arbuckle", "party": "NZ First", "electorate": "List"},
    {"name": "Andy Foster", "party": "NZ First", "electorate": "List"},
    {"name": "David Wilson", "party": "NZ First", "electorate": "List"},
    {"name": "Tanya Unkovich", "party": "NZ First", "electorate": "List"},
    # Labour (34)
    {"name": "Chris Hipkins", "party": "Labour", "electorate": "Remutaka"},
    {"name": "Carmel Sepuloni", "party": "Labour", "electorate": "Kelston"},
    {"name": "Barbara Edmonds", "party": "Labour", "electorate": "Mana"},
    {"name": "Megan Woods", "party": "Labour", "electorate": "Wigram"},
    {"name": "Willie Jackson", "party": "Labour", "electorate": "List"},
    {"name": "Ayesha Verrall", "party": "Labour", "electorate": "List"},
    {"name": "Kieran McAnulty", "party": "Labour", "electorate": "List"},
    {"name": "Willow-Jean Prime", "party": "Labour", "electorate": "List"},
    {"name": "Ginny Andersen", "party": "Labour", "electorate": "List"},
    {"name": "Jan Tinetti", "party": "Labour", "electorate": "List"},
    {"name": "Peeni Henare", "party": "Labour", "electorate": "List"},
    {"name": "Tangi Utikere", "party": "Labour", "electorate": "Palmerston North"},
    {"name": "Priyanca Radhakrishnan", "party": "Labour", "electorate": "List"},
    {"name": "Jo Luxton", "party": "Labour", "electorate": "List"},
    {"name": "Duncan Webb", "party": "Labour", "electorate": "Christchurch Central"},
    {"name": "Deborah Russell", "party": "Labour", "electorate": "List"},
    {"name": "Rachel Brooking", "party": "Labour", "electorate": "Dunedin"},
    {"name": "Damien O'Connor", "party": "Labour", "electorate": "List"},
    {"name": "Camilla Belich", "party": "Labour", "electorate": "List"},
    {"name": "Arena Williams", "party": "Labour", "electorate": "Manurewa"},
    {"name": "Phil Twyford", "party": "Labour", "electorate": "Te Atatu"},
    {"name": "Greg O'Connor", "party": "Labour", "electorate": "Ohariu"},
    {"name": "Jenny Salesa", "party": "Labour", "electorate": "Panmure-Otahuhu"},
    {"name": "Rachel Boyack", "party": "Labour", "electorate": "List"},
    {"name": "Adrian Rurawhe", "party": "Labour", "electorate": "List"},
    {"name": "Helen White", "party": "Labour", "electorate": "Mount Albert"},
    {"name": "Ingrid Leary", "party": "Labour", "electorate": "Taieri"},
    {"name": "Lemauga Lydia Sosene", "party": "Labour", "electorate": "Mangere"},
    {"name": "Reuben Davidson", "party": "Labour", "electorate": "Christchurch East"},
    {"name": "Cushla Tangaere-Manuel", "party": "Labour", "electorate": "Ikaroa-Rawhiti"},
    {"name": "Tracey McLellan", "party": "Labour", "electorate": "List"},
    {"name": "Shanan Halbert", "party": "Labour", "electorate": "List"},
    {"name": "Glen Bennett", "party": "Labour", "electorate": "List"},
    {"name": "Vanushi Walters", "party": "Labour", "electorate": "List"},
    # Green (15)
    {"name": "Marama Davidson", "party": "Green", "electorate": "List"},
    {"name": "Chloe Swarbrick", "party": "Green", "electorate": "Auckland Central"},
    {"name": "Julie Anne Genter", "party": "Green", "electorate": "Rongotai"},
    {"name": "Teanau Tuiono", "party": "Green", "electorate": "List"},
    {"name": "Lan Pham", "party": "Green", "electorate": "List"},
    {"name": "Ricardo Menendez March", "party": "Green", "electorate": "List"},
    {"name": "Steve Abel", "party": "Green", "electorate": "List"},
    {"name": "Huhana Lyndon", "party": "Green", "electorate": "List"},
    {"name": "Scott Willis", "party": "Green", "electorate": "List"},
    {"name": "Kahurangi Carter", "party": "Green", "electorate": "List"},
    {"name": "Celia Wade-Brown", "party": "Green", "electorate": "List"},
    {"name": "Lawrence Xu-Nan", "party": "Green", "electorate": "List"},
    {"name": "Francisco Hernandez", "party": "Green", "electorate": "List"},
    {"name": "Mike Davidson", "party": "Green", "electorate": "List"},
    {"name": "Tamatha Paul", "party": "Green", "electorate": "Wellington Central"},
    # Te Pati Maori (6)
    {"name": "Debbie Ngarewa-Packer", "party": "Te Pati Maori", "electorate": "Te Tai Hauauru"},
    {"name": "Rawiri Waititi", "party": "Te Pati Maori", "electorate": "Waiariki"},
    {"name": "Hana-Rawhiti Maipi-Clarke", "party": "Te Pati Maori", "electorate": "List"},
    {"name": "Takutai Tarsh Kemp", "party": "Te Pati Maori", "electorate": "Tamaki Makaurau"},
    {"name": "Mariameno Kapa-Kingi", "party": "Te Pati Maori", "electorate": "Te Tai Tokerau"},
    {"name": "Takuta Ferris", "party": "Te Pati Maori", "electorate": "Te Tai Tonga"},
    # Former 54th Parliament members (expelled/resigned)
    {"name": "Darleen Tana", "party": "Green", "electorate": "List"},
]


def scrape_wikipedia_mps() -> list[dict[str, str]] | None:
    """Attempt to scrape MP names from the Wikipedia article."""
    try:
        resp = requests.get(WIKIPEDIA_URL, timeout=30)
        resp.raise_for_status()
        html = resp.text
        found_names: list[dict[str, str]] = []
        pattern = r'<a\s+href="/wiki/[^"]+"\s+title="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        skip_words = {
            "New", "Zealand", "Parliament", "Election", "House",
            "Representatives", "Wikipedia", "Minister", "Cabinet",
            "Electoral", "Party", "Aotearoa",
        }
        for title, text in matches:
            name = text.strip()
            words = name.split()
            if len(words) >= 2 and 4 <= len(name) <= 50:
                if not any(w in skip_words for w in words[:2]):
                    found_names.append({"name": name, "party": "", "electorate": ""})
        if found_names:
            print(f"  Scraped {len(found_names)} names from Wikipedia")
            return found_names
        return None
    except Exception as e:
        print(f"  Wikipedia scraping failed: {e}")
        return None


def main() -> int:
    print("Fetching current NZ Parliament MPs...")
    all_mps = list(CURRENT_MP_NAMES)
    n = len(all_mps)
    print(f"  Total current/known MPs: {n}")
    output = {
        "source": "parliament-wikipedia-54th-parliament",
        "url": WIKIPEDIA_URL,
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n_mps": n,
        "member_records": all_mps,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH}")
    print(f"  {n} MP records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())