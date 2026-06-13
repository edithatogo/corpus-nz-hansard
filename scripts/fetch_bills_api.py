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

import json
import time
from datetime import UTC, datetime
from pathlib import Path

import requests

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


def fetch_search(page: int = 1, parliament: int | None = None) -> dict:
    body = dict(SEARCH_TEMPLATE)
    body["page"] = page
    if parliament:
        body["parliament"] = parliament
    resp = requests.post(f"{API_BASE}/data/search", json=body, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_bill_detail(bill_id: str) -> dict:
    resp = requests.get(f"{API_BASE}/data/Bill/{bill_id}", headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()


def fetch_current_parliament() -> int:
    resp = requests.get(f"{API_BASE}/data/currentParliament", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return int(resp.text)


def fetch_facets() -> dict:
    body = dict(SEARCH_TEMPLATE)
    body.pop("includeBillStages", None)
    resp = requests.post(f"{API_BASE}/data/facet", json=body, headers=HEADERS, timeout=15)
    resp.raise_for_status()
    return resp.json()


def main():
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

    # Save facets
    (OUTPUT_DIR / "facets.json").write_text(
        json.dumps(facets, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print("\nFetching all bills (paginated)...")
    all_bills = []
    total = None
    page = 1
    while True:
        data = fetch_search(page=page)
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
        time.sleep(0.5)

    print(f"\nFetched {len(all_bills)} bill summaries. Fetching details...")

    bill_details = []
    member_names: set[str] = set()

    for i, bill in enumerate(all_bills):
        bid = bill.get("id", "")
        if not bid:
            continue
        try:
            detail = fetch_bill_detail(bid)
            bill_details.append(detail)

            # Extract member names
            members = detail.get("Members", []) or []
            for m in members:
                name = m.get("PreferredFormOfAddress", "") or m.get("DisplayName", "")
                if name:
                    member_names.add(name)

            if (i + 1) % 50 == 0:
                print(f"  Processed {i + 1}/{len(all_bills)} bills...")
            time.sleep(0.2)
        except Exception as e:
            print(f"  Error fetching bill {bid}: {e}")

    print(f"\nProcessed {len(bill_details)} bill details")
    print(f"Unique member names found: {len(member_names)}")

    # Save outputs
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

    (OUTPUT_DIR / f"bills_summary_{timestamp}.json").write_text(
        json.dumps(all_bills, indent=2, ensure_ascii=False)[:500_000] + "\n... (truncated)",
        encoding="utf-8",
    )
    (OUTPUT_DIR / f"bills_details_{timestamp}.json").write_text(
        json.dumps(bill_details, indent=2, ensure_ascii=False)[:500_000] + "\n... (truncated)",
        encoding="utf-8",
    )

    # Save just the member names as a reference
    (OUTPUT_DIR / f"bills_members_{timestamp}.json").write_text(
        json.dumps(
            {
                "source": "Bills API",
                "fetched_at": timestamp,
                "total_bills": len(all_bills),
                "total_details": len(bill_details),
                "unique_members": sorted(member_names),
                "member_count": len(member_names),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"\nOutput saved to {OUTPUT_DIR}/")
    print(f"  Member names: {len(member_names)}")
    for name in sorted(member_names)[:20]:
        print(f"    - {name}")
    if len(member_names) > 20:
        print(f"    ... and {len(member_names) - 20} more")


if __name__ == "__main__":
    main()
