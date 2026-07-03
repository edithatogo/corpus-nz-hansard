"""Fetch structured bill data from the NZ Parliament Bills API.

API endpoints (open, no auth):
  POST /api/data/search  - paginated bill listing
  GET  /api/data/Bill/{uuid} - full bill details
  POST /api/data/facet   - filter options
  GET  /api/data/currentParliament - current parliament number
  GET  /rss?set=Bills    - RSS feed

Output: derived/bills_api/
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

from scripts.http_retry import request_with_retries

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "derived" / "bills_api"

API_BASE = "https://bills.parliament.nz/api"
HEADERS = {
    "User-Agent": "corpus-nz-hansard/1.0 (research; +https://github.com/edithatogo/corpus-nz-hansard)",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

SEARCH_TEMPLATE = {
    "id": None,
    "documentPreset": 1,
    "keyword": None,
    "selectCommittee": None,
    "status": [],
    "documentTypes": [],
    "documentSubtypes": [],
    "beforeCommittee": None,
    "billStages": [],
    "billTab": "All",
    "billId": None,
    "includeBillStages": True,
    "subject": None,
    "person": None,
    "parliament": None,
    "dateFrom": None,
    "dateTo": None,
    "datePeriod": None,
    "restrictedFrom": None,
    "restrictedTo": None,
    "terminatedReason": None,
    "prettyTerminatedReason": None,
    "terminatedReasons": [],
    "column": 17,
    "direction": 1,
    "pageSize": 50,
    "page": 1,
}


def _json_artifact_text(payload: Any) -> str:
    """Serialize complete UTF-8 JSON text without truncating the payload."""
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def _write_json_artifact(path: Path, payload: Any) -> None:
    """Write complete UTF-8 JSON without truncating the payload."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_artifact_text(payload), encoding="utf-8")


def fetch_search(page: int = 1, parliament: int | None = None, page_size: int = 50) -> dict:
    body = dict(SEARCH_TEMPLATE)
    body["page"] = page
    body["pageSize"] = page_size
    if parliament:
        body["parliament"] = parliament
    resp = request_with_retries(
        "POST",
        f"{API_BASE}/data/search",
        json=body,
        headers=HEADERS,
        timeout=30,
    )
    return resp.json()


def fetch_bill_detail(bill_id: str) -> dict:
    resp = request_with_retries(
        "GET",
        f"{API_BASE}/data/Bill/{bill_id}",
        headers=HEADERS,
        timeout=30,
    )
    return resp.json()


def fetch_current_parliament() -> int:
    resp = request_with_retries(
        "GET",
        f"{API_BASE}/data/currentParliament",
        headers=HEADERS,
        timeout=10,
    )
    return int(resp.text)


def fetch_facets() -> dict:
    body = dict(SEARCH_TEMPLATE)
    body.pop("includeBillStages", None)
    resp = request_with_retries(
        "POST",
        f"{API_BASE}/data/facet",
        json=body,
        headers=HEADERS,
        timeout=30,
    )
    return resp.json()


def _member_names_from_detail(detail: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for member in detail.get("Members", []) or []:
        name = member.get("PreferredFormOfAddress", "") or member.get("DisplayName", "")
        if name:
            names.add(name)
    return names


def fetch_all_bills(*, page_size: int, page_sleep: float, detail_sleep: float) -> dict[str, Any]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Fetching current parliament...")
    current = fetch_current_parliament()
    print(f"  Current Parliament: {current}")

    print("\nFetching facets...")
    facets = fetch_facets()
    parliaments = [p["number"] for p in facets.get("parliaments", [])]
    committees = [c["name"] for c in facets.get("committees", [])]
    print(f"  Parliaments: {parliaments}")
    print(f"  Committees: {len(committees)}")
    print(f"  Bill types: {facets.get('documentSubTypes', [])}")
    _write_json_artifact(OUTPUT_DIR / "facets.json", facets)

    print("\nFetching all bills (paginated)...")
    all_bills: list[dict[str, Any]] = []
    total = None
    page = 1
    while True:
        data = fetch_search(page=page, page_size=page_size)
        results = data.get("results", [])
        if total is None:
            total = data.get("totalResults", 0)
            print(f"  Total bills: {total}")
        if not results:
            break
        all_bills.extend(results)
        print(f"  Page {page}: got {len(results)} bills (total so far: {len(all_bills)})")
        if len(all_bills) >= total:
            break
        page += 1
        time.sleep(page_sleep)

    print(f"\nFetched {len(all_bills)} bill summaries. Fetching details...")
    bill_details: list[dict[str, Any]] = []
    member_names: set[str] = set()
    errors: list[dict[str, str]] = []

    for i, bill in enumerate(all_bills):
        bid = bill.get("id", "")
        if not bid:
            continue
        try:
            detail = fetch_bill_detail(bid)
            bill_details.append(detail)
            member_names.update(_member_names_from_detail(detail))
            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(all_bills)} bills...")
            time.sleep(detail_sleep)
        except Exception as exc:  # noqa: BLE001 - recorded as extraction evidence
            errors.append({"bill_id": str(bid), "error": str(exc)})
            print(f"  Error fetching bill {bid}: {exc}")

    print(f"\nProcessed {len(bill_details)} bill details")
    print(f"Unique member names found: {len(member_names)}")
    if errors:
        print(f"Detail fetch errors: {len(errors)}")

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    summary_path = OUTPUT_DIR / f"bills_summary_{timestamp}.json"
    details_path = OUTPUT_DIR / f"bills_details_{timestamp}.json"
    members_path = OUTPUT_DIR / f"bills_members_{timestamp}.json"
    errors_path = OUTPUT_DIR / f"bills_errors_{timestamp}.json"

    _write_json_artifact(summary_path, all_bills)
    _write_json_artifact(details_path, bill_details)
    _write_json_artifact(
        members_path,
        {
            "source": "Bills API",
            "fetched_at": timestamp,
            "total_bills": len(all_bills),
            "total_details": len(bill_details),
            "unique_members": sorted(member_names),
            "member_count": len(member_names),
        },
    )
    if errors:
        _write_json_artifact(errors_path, errors)

    print(f"\nOutput saved to {OUTPUT_DIR}/")
    print(f"  Summary records: {len(all_bills)} -> {summary_path.name}")
    print(f"  Detail records: {len(bill_details)} -> {details_path.name}")
    print(f"  Member names: {len(member_names)} -> {members_path.name}")
    for name in sorted(member_names)[:20]:
        print(f"    - {name}")
    if len(member_names) > 20:
        print(f"    ... and {len(member_names) - 20} more")

    return {
        "timestamp": timestamp,
        "summary_path": summary_path,
        "details_path": details_path,
        "members_path": members_path,
        "errors": errors,
        "summary_count": len(all_bills),
        "details_count": len(bill_details),
        "member_count": len(member_names),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch complete NZ Parliament Bills API records.")
    parser.add_argument("--page-size", type=int, default=500)
    parser.add_argument("--page-sleep", type=float, default=0.1)
    parser.add_argument("--detail-sleep", type=float, default=0.05)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = fetch_all_bills(
        page_size=args.page_size,
        page_sleep=args.page_sleep,
        detail_sleep=args.detail_sleep,
    )
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
