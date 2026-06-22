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
import hashlib
import json
import logging
import os
import re
import sys
import time
from collections.abc import Iterable
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
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INVENTORY_PATH = ROOT / "generated" / "hathitrust" / "volume_inventory.json"
DEFAULT_VALIDATION_PATH = ROOT / "manifests" / "hathitrust_inventory_validation.json"
HTID_PATTERN = re.compile(r"^[a-z0-9]+\.[a-z0-9.$_-]+$")

HATHIFILE_FIELDS = [
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

# Seeded from the track evidence captured from the 2023-10-03 Wayback listing.
# The live Wayback probe is useful when available, but it has returned transient
# 404s; this seed keeps the repository-side inventory deterministic.
KNOWN_WAYBACK_SAMPLE_IDS = (
    "uc1.a0001646314",
    "uc1.a0001745447",
    "uc1.a0001745553",
    "uc1.a0001745561",
    "uc1.a0001745579",
    "uc1.a0001745587",
    "uc1.a0001745595",
    "uc1.a0001745603",
    "uc1.a0001745611",
    "uc1.a0001745629",
    "uc1.a0001745637",
    "uc1.a0001757616",
    "uc1.a0001757772",
    "uc1.a0001757988",
    "uc1.a0001758010",
    "uc1.a0001800556",
    "uc1.a0001800861",
    "uc1.b2889853",
    "uc1.b2889879",
    "uc1.b2889888",
    "uc1.b2889951",
    "uc1.b2889953",
    "uc1.b2889962",
    "uc1.b2889969",
    "uc1.b2889971",
    "uc1.b2889974",
    "uc1.b2889976",
    "uc1.b2889978",
    "uc1.b2889983",
    "uc1.b2889989",
    "uc1.b2890198",
    "uc1.b2890228",
    "uc1.b2890240",
    "uc1.b2890245",
    "uc1.b2890262",
    "uc1.b2890264",
    "uc1.b2940052-81",
    "uc1.b2940127-59",
    "uc1.b2940162",
)

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
            page_ids = set(re.findall(r"/cgi/pt\\?id=([a-z0-9.$_-]+)", resp.text))
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
    open_func = gzip.open if hathifile_path.endswith(".gz") else open
    with open_func(hathifile_path, "rt", encoding="utf-8") as f:
        reader = csv.DictReader(f, fieldnames=HATHIFILE_FIELDS, delimiter="\t")
        for row in reader:
            htid = normalize_htid(row.get("htid", ""))
            source = row.get("source", "").lower()
            title = row.get("title", "").lower()
            author = row.get("author", "").lower()
            is_nz_hansard = (
                htid.startswith(f"{SOURCE_CODE}.")
                and source == SOURCE_CODE
                and "parliamentary debates" in title
                and ("new zealand" in title or "new zealand" in author)
            )
            if is_nz_hansard:
                row["htid"] = htid
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
    m = re.search(r"2027/([a-z0-9.$_-]+)", url)
    return m.group(1) if m else None


def parse_catalog_url(url: str) -> str | None:
    """Extract HT bib key from a catalog URL like https://catalog.hathitrust.org/Record/100034544"""
    m = re.search(r"/Record/([0-9]+)", url)
    return m.group(1) if m else None


# --- Offline inventory validation ---


def normalize_htid(value: str) -> str:
    """Normalize an HT volume ID for deterministic validation."""
    return value.strip().lower()


def _sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        msg = f"Expected JSON object in {path}"
        raise ValueError(msg)
    return data


def _sorted_unique(values: list[str]) -> list[str]:
    return sorted({normalize_htid(value) for value in values if normalize_htid(value)})


def extract_inventory_ids(inventory: dict[str, Any]) -> list[str]:
    """Extract HT IDs from supported inventory shapes."""
    raw_ids: list[str] = []
    enumerated_ids = inventory.get("enumerated_ids", [])
    if isinstance(enumerated_ids, list):
        raw_ids.extend(str(value) for value in enumerated_ids)

    volumes = inventory.get("volumes", [])
    if isinstance(volumes, list):
        for volume in volumes:
            if isinstance(volume, dict) and volume.get("htid"):
                raw_ids.append(str(volume["htid"]))

    rows = inventory.get("rows", [])
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and row.get("htid"):
                raw_ids.append(str(row["htid"]))

    return _sorted_unique(raw_ids)


def write_json(data: dict[str, Any], output_path: str | Path) -> Path:
    """Write stable JSON with parent directories created."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return path


def build_inventory_from_hathifile(
    hathifile_path: str | Path,
    output_dir: str | Path = "generated/hathitrust",
) -> Path:
    """Build a deterministic volume inventory from a local hathifile dump."""
    volumes = enumerate_volumes_from_hathifile(str(hathifile_path))
    ids = _sorted_unique([volume["htid"] for volume in volumes])
    inventory = {
        "collection_id": COLLECTION_ID,
        "collection_name": COLLECTION_NAME,
        "enumerated_count": len(ids),
        "enumerated_ids": ids,
        "expected_volumes": EXPECTED_VOLUMES,
        "pending_count": max(EXPECTED_VOLUMES - len(ids), 0),
        "source": "local_hathifile",
        "source_hathifile": {
            "path": str(Path(hathifile_path)),
            "sha256": _sha256_path(Path(hathifile_path)),
        },
    }
    return write_json(inventory, Path(output_dir) / "volume_inventory.json")


def build_inventory_validation(
    inventory_path: str | Path = DEFAULT_INVENTORY_PATH,
    *,
    access_key_present: bool = False,
    hathifile_path: str | Path | None = None,
) -> dict[str, Any]:
    """Validate local HathiTrust inventory evidence without live API claims."""
    inventory_path = Path(inventory_path)
    inventory = _load_json(inventory_path)
    ids = extract_inventory_ids(inventory)
    invalid_ids = [htid for htid in ids if not HTID_PATTERN.fullmatch(htid)]
    non_uc_ids = [htid for htid in ids if not htid.startswith(f"{SOURCE_CODE}.")]
    duplicate_count = max(len(inventory.get("enumerated_ids", [])) - len(ids), 0)
    pending_count = max(EXPECTED_VOLUMES - len(ids), 0)

    blockers = []
    if pending_count:
        blockers.append(
            {
                "blocker_id": "hathifile-or-browser-enumeration-required",
                "status": "external-input-required",
                "detail": (
                    "Local inventory does not enumerate all expected volumes; provide a "
                    "local hathifile dump or browser-derived listing before acquisition claims."
                ),
            },
        )
    if not access_key_present:
        blockers.append(
            {
                "blocker_id": "hathitrust-data-api-oauth-required",
                "status": "external-credential-required",
                "detail": (
                    "OCR and METS retrieval require a HathiTrust Data API access key; "
                    "no live full-text acquisition is validated by this manifest."
                ),
            },
        )
    if hathifile_path is None and inventory.get("source") != "local_hathifile":
        blockers.append(
            {
                "blocker_id": "local-hathifile-evidence-missing",
                "status": "external-file-required",
                "detail": (
                    "No local hathifile path was supplied for deterministic complete "
                    "metadata enumeration."
                ),
            },
        )

    status = (
        "validated-inventory" if not blockers and not invalid_ids and not non_uc_ids else "blocked"
    )
    return {
        "artifact_name": "hathitrust_inventory_validation",
        "collection": {
            "collection_id": COLLECTION_ID,
            "collection_name": COLLECTION_NAME,
            "expected_volumes": EXPECTED_VOLUMES,
            "source_code": SOURCE_CODE,
        },
        "inventory": {
            "enumerated_count": len(ids),
            "inventory_path": inventory_path.relative_to(ROOT).as_posix()
            if inventory_path.is_relative_to(ROOT)
            else str(inventory_path),
            "inventory_sha256": _sha256_path(inventory_path),
            "pending_count": pending_count,
            "source": inventory.get("source", "unknown"),
        },
        "checks": {
            "expected_volume_count": {
                "actual": len(ids),
                "expected": EXPECTED_VOLUMES,
                "status": "pass" if len(ids) == EXPECTED_VOLUMES else "blocked",
            },
            "htid_format": {
                "invalid_count": len(invalid_ids),
                "invalid_ids": invalid_ids[:25],
                "status": "pass" if not invalid_ids else "fail",
            },
            "source_prefix": {
                "non_matching_count": len(non_uc_ids),
                "non_matching_ids": non_uc_ids[:25],
                "required_prefix": f"{SOURCE_CODE}.",
                "status": "pass" if not non_uc_ids else "fail",
            },
            "unique_ids": {
                "duplicate_count": duplicate_count,
                "status": "pass" if duplicate_count == 0 else "fail",
            },
        },
        "blockers": blockers,
        "release_gate_status": status,
        "validated_volume_ids": ids,
    }


# --- CLI ---


def _dedupe_ids(ids: Iterable[str]) -> list[str]:
    return sorted({normalize_htid(item) for item in ids if normalize_htid(item)})


def build_volume_inventory(
    output_dir: str | Path = "generated/hathitrust",
    discovered_ids: Iterable[str] | None = None,
    *,
    live_probe_attempted: bool = True,
    output_file: str = "volume_inventory.json",
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

    if discovered_ids is None:
        # Enumerate from Wayback when available. This is a best-effort probe;
        # the committed seed below is the deterministic floor for CI and review.
        discovered_ids = enumerate_volumes_from_wayback()

    live_ids = _dedupe_ids(discovered_ids)
    seeded_ids = _dedupe_ids(KNOWN_WAYBACK_SAMPLE_IDS)
    enumerated_ids = _dedupe_ids([*seeded_ids, *live_ids])
    pending_count = max(EXPECTED_VOLUMES - len(enumerated_ids), 0)

    inventory = {
        "artifact_name": "hathitrust_hansard_acquisition_inventory",
        "track_id": "hathitrust_hansard_acquisition_20260612",
        "collection_id": COLLECTION_ID,
        "collection_name": COLLECTION_NAME,
        "expected_volumes": EXPECTED_VOLUMES,
        "enumerated_ids": enumerated_ids,
        "enumerated_count": len(enumerated_ids),
        "seeded_wayback_sample_count": len(seeded_ids),
        "live_wayback_discovered_count": len(live_ids),
        "live_probe_attempted": live_probe_attempted,
        "pending_count": pending_count,
        "acquisition_status": "blocked-pending-hathifile-or-oauth",
        "blockers": [
            "HathiTrust Data API OCR download requires an IP-restricted OAuth access key.",
            "Full 510-volume enumeration requires a hathifile dump or browser-authenticated collection listing.",
        ],
        "next_actions": [
            "Acquire the monthly hathi_full_YYYYMMDD.txt.gz hathifile and filter for collection candidates.",
            "Request a HathiTrust Data API access key before attempting OCR ZIP downloads.",
        ],
        "note": (
            f"{len(enumerated_ids)} IDs are enumerated from committed Wayback evidence and "
            f"best-effort live probes. Remaining {pending_count} volumes require hathifile "
            f"download, OAuth Data API access, or browser-based enumeration."
        ),
        "sources": [
            "wayback_machine_20231003_evidence_seed",
            "wayback_machine_live_probe" if live_probe_attempted else "test_fixture",
        ],
    }

    output_path = write_json(inventory, output_dir / output_file)
    log.info(
        "Inventory written to %s (%d of %d IDs)",
        output_path,
        len(enumerated_ids),
        EXPECTED_VOLUMES,
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
        "--validate-inventory",
        action="store_true",
        help="Validate local HathiTrust inventory evidence without live network access",
    )
    parser.add_argument(
        "--inventory",
        type=str,
        default=str(DEFAULT_INVENTORY_PATH),
        help="Path to local HathiTrust volume inventory JSON",
    )
    parser.add_argument(
        "--validation-output",
        type=str,
        default=str(DEFAULT_VALIDATION_PATH),
        help="Path to write HathiTrust inventory validation manifest",
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
        output_path = build_inventory_from_hathifile(args.from_hathifile, args.output)
        log.info("Hathifile inventory written to %s", output_path)
        if args.validate_inventory:
            validation = build_inventory_validation(
                output_path,
                access_key_present=bool(args.access_key),
                hathifile_path=args.from_hathifile,
            )
            validation_path = write_json(validation, args.validation_output)
            log.info("Validation manifest written to %s", validation_path)
        return

    if args.validate_inventory:
        validation = build_inventory_validation(
            args.inventory,
            access_key_present=bool(args.access_key),
        )
        validation_path = write_json(validation, args.validation_output)
        log.info("Validation manifest written to %s", validation_path)
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
