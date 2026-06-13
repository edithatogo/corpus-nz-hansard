"""
fetch_hathitrust.py - HathiTrust NZ Parliamentary Debates Acquisition

Acquires 510 full-view volumes (1854-1990) from HathiTrust collection 71329709.

API Documentation:
- Collection: https://babel.hathitrust.org/cgi/mb?a=listis&c=71329709
- Catalog API: https://catalog.hathitrust.org/api/volumes/
- Data API: https://babel.hathitrust.org/cgi/htd/  (requires OAuth key)
- Hathifiles: https://www.hathitrust.org/hathifiles  (bulk metadata TSV)

Usage:
  python scripts/fetch_hathitrust.py --list-volumes
  python scripts/fetch_hathitrust.py --fetch-metadata --output metadata/
  python scripts/fetch_hathitrust.py --fetch-ocr --output ocr/ --access-key KEY
  python scripts/fetch_hathitrust.py --from-hathifile hathi_full_20230301.txt.gz

Note: All babel.hathitrust.org and catalog.hathitrust.org endpoints are behind
Cloudflare anti-bot protection. This script currently documents the API patterns;
actual acquisition will require either an OAuth API key or browser automation.
"""

import argparse
import csv
import gzip
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import requests

# --- Constants ---

COLLECTION_ID = "71329709"
COLLECTION_NAME = "NZ Parliamentary Debates (Hansard)"
EXPECTED_VOLUMES = 510
DATE_RANGE = (1854, 1990)

COLLECTION_BASE = "https://babel.hathitrust.org/cgi/mb"
CATALOG_API = "https://catalog.hathitrust.org/api/volumes"
DATA_API = "https://babel.hathitrust.org/cgi/htd"
VIEWER_URL = "https://babel.hathitrust.org/cgi/pt"

SOURCE_CODE = "uc1"  # University of California

# --- Logging ---

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# --- Volume Enumeration ---


def enumerate_volumes_from_wayback(
    capture_date: str = "20231003073233",
) -> list[str]:
    """
    Extract HT volume IDs from Wayback Machine captures of the collection listing.

    The live collection page is Cloudflare-protected, so we use archived captures.
    Only page 1 (100 items) is currently available via Wayback.
    Remaining 410 volumes (pages 2-6) need alternative enumeration strategies.

    URL pattern:
      https://web.archive.org/web/{capture_date}id_/https://babel.hathitrust.org/cgi/mb?a=listis;c={COLLECTION_ID};pn={N};sort=title_a
    """
    ids: list[str] = []
    for page in range(1, 7):
        url = (
            f"https://web.archive.org/web/{capture_date}id_/"
            f"https://babel.hathitrust.org/cgi/mb"
            f"?a=listis;c={COLLECTION_ID};pn={page};sort=title_a"
        )
        try:
            resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=60)
            if resp.status_code != 200:
                log.warning("Page %d: HTTP %d", page, resp.status_code)
                continue
            page_ids = set(re.findall(r"/cgi/pt\\?id=([a-z0-9.$_]+)", resp.text))
            log.info("Page %d: found %d volume IDs", page, len(page_ids))
            ids.extend(sorted(page_ids))
        except requests.RequestException as exc:
            log.warning("Page %d request failed: %s", page, exc)
    return ids


def enumerate_volumes_from_hathifile(hathifile_path: str) -> list[dict[str, str]]:
    """
    Extract volume metadata from a hathifile (37-column TSV) dump.

    The hathifile covers the entire HathiTrust collection. Filter by:
    - source == "uc1" (University of California)
    - title contains "Parliamentary debates"
    - OR by ht_bib_key matching the parent serial record
    """
    volumes: list[dict[str, str]] = []
    field_names = [
        "htid",
        "access",
        "rights",
        "ht_bib_key",
        "description",
        "source",
        "source_bib_num",
        "oclc_num",
        "isbn",
        "issn",
        "lccn",
        "title",
        "imprint",
        "rights_reason_code",
        "rights_timestamp",
        "us_gov_doc_flag",
        "rights_date_used",
        "pub_place",
        "lang",
        "bib_fmt",
        "collection_code",
        "content_provider_code",
        "responsible_entity_code",
        "digitization_agent_code",
        "access_profile_code",
        "author",
    ]

    open_func = gzip.open if hathifile_path.endswith(".gz") else open
    with open_func(hathifile_path, "rt", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=field_names, delimiter="\t")
        for row in reader:
            title = row.get("title", "")
            source = row.get("source", "")
            if "parliamentary debates" in title.lower() or source == "uc1":
                volumes.append(row)

    log.info("Extracted %d potential volumes from hathifile", len(volumes))
    return volumes


def build_collection_search_urls() -> list[str]:
    """
    Build search URLs to enumerate volumes by date range facets.

    The collection listing is paginated at 100 items/page.
    Date-range facet searches may return more complete results.
    """
    date_ranges = [
        "1854",
        "1850-1859",
        "1860-1869",
        "1870-1879",
        "1880-1889",
        "1890-1899",
        "1900-1909",
        "1910-1919",
        "1920-1929",
        "1930-1939",
        "1940-1949",
        "1960-1969",
        "1970-1979",
        "1980-1989",
    ]
    urls = []
    for dr in date_ranges:
        url = (
            f"{COLLECTION_BASE}?a=listsrch"
            f";c={COLLECTION_ID}"
            f";sort=title_a"
            f";q1=%2A"
            f"&facet=bothPublishDateRange:%22{dr}%22"
        )
        urls.append(url)
    return urls


# --- Metadata Retrieval ---


def fetch_brief_metadata(
    identifier: str,
    session: requests.Session | None = None,
) -> dict[str, Any] | None:
    """
    Fetch brief bibliographic JSON from the HathiTrust Catalog API.

    Supported identifiers:
    - HT item ID: "uc1.b2889853"
    - HT bib key: "100034544"
    - OCLC number
    - ISBN, ISSN, LCCN

    API: GET https://catalog.hathitrust.org/api/volumes/brief/json/{identifier}

    Note: Cloudflare-protected; may return 403.
    """
    if session is None:
        session = requests.Session()
    url = f"{CATALOG_API}/brief/json/{identifier}"
    try:
        resp = session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        log.warning("Catalog API returned %d for %s", resp.status_code, identifier)
        return None
    except requests.RequestException as exc:
        log.error("Catalog API request failed for %s: %s", identifier, exc)
        return None


def fetch_full_metadata(
    identifier: str,
    session: requests.Session | None = None,
) -> dict[str, Any] | None:
    """
    Fetch full MARC JSON from the HathiTrust Catalog API.

    API: GET https://catalog.hathitrust.org/api/volumes/full/json/{identifier}
    """
    if session is None:
        session = requests.Session()
    url = f"{CATALOG_API}/full/json/{identifier}"
    try:
        resp = session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30,
        )
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.RequestException:
        return None


# --- OCR / Full Text Access ---


def fetch_page_ocr(
    ht_id: str,
    page_num: int,
    access_key: str,
    session: requests.Session | None = None,
) -> str | None:
    """
    Fetch OCR text for a single page via the HathiTrust Data API.

    API: GET https://babel.hathitrust.org/cgi/htd/volume/{ht_id}/page/{page_num}/ocr
    Auth: ?access_key={key}

    Returns plain text or None on failure.
    """
    if session is None:
        session = requests.Session()
    url = f"{DATA_API}/volume/{ht_id}/page/{page_num}/ocr"
    params = {"access_key": access_key}
    try:
        resp = session.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.text
        log.warning("Data API returned %d for %s page %d", resp.status_code, ht_id, page_num)
        return None
    except requests.RequestException as exc:
        log.error("Data API request failed: %s", exc)
        return None


def fetch_volume_ocr_zip(
    ht_id: str,
    access_key: str,
    output_path: str | Path,
) -> bool:
    """
    Download all OCR text for a volume as a ZIP archive.

    API: GET https://babel.hathitrust.org/cgi/htd/volume/{ht_id}/zip/ocr
    Auth: ?access_key={key}
    """
    url = f"{DATA_API}/volume/{ht_id}/zip/ocr"
    params = {"access_key": access_key}
    try:
        resp = requests.get(url, params=params, stream=True, timeout=300)
        if resp.status_code == 200:
            with Path(output_path).open("wb") as f:
                f.writelines(resp.iter_content(chunk_size=8192))
            log.info("Downloaded OCR zip for %s to %s", ht_id, output_path)
            return True
        log.warning("OCR zip returned %d for %s", resp.status_code, ht_id)
        return False
    except requests.RequestException as exc:
        log.error("OCR zip download failed: %s", exc)
        return False


def fetch_mets_metadata(
    ht_id: str,
    access_key: str,
) -> str | None:
    """
    Fetch METS XML metadata for a volume.

    API: GET https://babel.hathitrust.org/cgi/htd/volume/{ht_id}/mets
    Auth: ?access_key={key}
    """
    url = f"{DATA_API}/volume/{ht_id}/mets"
    params = {"access_key": access_key}
    try:
        resp = requests.get(url, params=params, timeout=60)
        if resp.status_code == 200:
            return resp.text
        return None
    except requests.RequestException:
        return None


# --- Volume ID Parsing ---


def parse_handle_url(url: str) -> str | None:
    """Extract HT ID from a handle URL like https://hdl.handle.net/2027/uc1.b2889853"""
    m = re.search(r"2027/([a-z0-9.$_]+)", url)
    return m.group(1) if m else None


def parse_catalog_url(url: str) -> str | None:
    """Extract HT bib key from a catalog URL like https://catalog.hathitrust.org/Record/100034544"""
    m = re.search(r"/Record/([0-9]+)", url)
    return m.group(1) if m else None


# --- CLI ---


def build_volume_inventory(
    output_dir: str | Path = "generated/hathitrust",
) -> Path:
    """
    Build a JSON inventory of all volumes in the collection.

    Combines enumeration strategies:
    1. Wayback Machine captures (page 1 only)
    2. Hathifile extraction (when available)
    3. Collection search facet URLs (documented for future use)
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Enumerate from Wayback (page 1 only, ~100 IDs)
    wayback_ids = enumerate_volumes_from_wayback()

    inventory = {
        "collection_id": COLLECTION_ID,
        "collection_name": COLLECTION_NAME,
        "expected_volumes": EXPECTED_VOLUMES,
        "enumerated_ids": wayback_ids,
        "enumerated_count": len(wayback_ids),
        "pending_count": EXPECTED_VOLUMES - len(wayback_ids),
        "note": (
            f"Only {len(wayback_ids)} IDs recovered from Wayback page 1. "
            f"Remaining {EXPECTED_VOLUMES - len(wayback_ids)} volumes "
            f"require hathifile download or browser-based enumeration."
        ),
        "source": "wayback_machine_20231003",
    }

    output_path = output_dir / "volume_inventory.json"
    with Path(output_path).open("w") as f:
        json.dump(inventory, f, indent=2)
    log.info(
        "Inventory written to %s (%d of %d IDs)", output_path, len(wayback_ids), EXPECTED_VOLUMES
    )
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Acquire NZ Parliamentary Debates from HathiTrust collection 71329709",
    )
    parser.add_argument(
        "--list-volumes",
        action="store_true",
        help="Enumerate volumes and build inventory",
    )
    parser.add_argument(
        "--fetch-metadata",
        action="store_true",
        help="Fetch bibliographic metadata for each volume",
    )
    parser.add_argument(
        "--fetch-ocr",
        action="store_true",
        help="Download OCR text for volumes",
    )
    parser.add_argument(
        "--from-hathifile",
        type=str,
        help="Path to hathifile TSV (hathi_full_*.txt.gz) for volume enumeration",
    )
    parser.add_argument(
        "--access-key",
        type=str,
        help="HathiTrust Data API access key",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="generated/hathitrust",
        help="Output directory",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.list_volumes:
        build_volume_inventory(args.output)
        return

    if args.from_hathifile:
        volumes = enumerate_volumes_from_hathifile(args.from_hathifile)
        output_path = Path(args.output) / "hathifile_volumes.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with Path(output_path).open("w") as f:
            json.dump(volumes, f, indent=2, default=str)
        log.info("Extracted %d volumes to %s", len(volumes), output_path)
        return

    if args.fetch_metadata:
        log.warning("Metadata fetching requires Cloudflare bypass or API key")
        log.info("See evidence.md for API patterns")
        # TODO: Implement batch metadata fetching
        return

    if args.fetch_ocr:
        if not args.access_key:
            log.error("--access-key is required for OCR fetching")
            sys.exit(1)
        log.warning("OCR fetching requires live API access (Cloudflare bypass)")
        # TODO: Implement OCR downloading
        return

    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
