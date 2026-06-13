import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "derived" / "wikidata_nz_mps.json"
SPARQL_URL = "https://query.wikidata.org/sparql"

# Provenance note on Wikidata as a secondary source:
# Wikidata is an aggregator, not a primary authority. Each statement in Wikidata
# carries references citing the primary source(s) used. The queries below capture
# those references to provide full provenance chains:
#
#   Wikidata → reference URL (P854) → primary source (e.g. parliament.nz page)
#   Wikidata → described at URL (P973) → official biography page
#   Wikidata → imported from (P143) → Wikipedia, Wikimedia project
#   Wikidata → stated in (P248) → official publication/database
#
# By capturing these, consumers can trace each identity assertion back to its
# primary authority source.

# Primary query: MPs with P39 for Member of NZ Parliament,
# including provenance references showing which primary sources Wikidata used.
QUERY_P39 = """
SELECT ?item ?itemLabel ?parliamentId ?givenName ?familyName
       ?startDate ?endDate ?partyLabel ?parliamentLabel ?parliamentNumber
       ?describedAtUrl
       (GROUP_CONCAT(DISTINCT ?refUrl; SEPARATOR=" | ") AS ?referenceUrls)
       (GROUP_CONCAT(DISTINCT ?alias; SEPARATOR=" | ") AS ?aliases)
WHERE {
  ?item p:P39 ?ps . ?ps ps:P39 wd:Q18145518 .
  OPTIONAL { ?item wdt:P6262 ?parliamentId . }
  OPTIONAL { ?item wdt:P735 ?gn . ?gn rdfs:label ?givenName . FILTER(LANG(?givenName) = "en") }
  OPTIONAL { ?item wdt:P734 ?fn . ?fn rdfs:label ?familyName . FILTER(LANG(?familyName) = "en") }
  OPTIONAL { ?ps pq:P580 ?startDate . }
  OPTIONAL { ?ps pq:P582 ?endDate . }
  OPTIONAL { ?item wdt:P102 ?p . ?p rdfs:label ?partyLabel . FILTER(LANG(?partyLabel) = "en") }
  OPTIONAL { ?ps pq:P2937 ?parl . ?parl rdfs:label ?parliamentLabel . FILTER(LANG(?parliamentLabel) = "en") OPTIONAL { ?parl wdt:P1545 ?parliamentNumber . } }
  OPTIONAL { ?item skos:altLabel ?alias . FILTER(LANG(?alias) = "en") }
  # Provenance: described at URL (P973) — the primary source URL describing the item
  OPTIONAL { ?item wdt:P973 ?describedAtUrl . }
  # Provenance: reference URLs on the P39 statement — the sources Wikidata used
  OPTIONAL { ?ps prov:wasDerivedFrom ?ref . ?ref pr:P854 ?refUrl . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?item ?itemLabel ?parliamentId ?givenName ?familyName
         ?startDate ?endDate ?partyLabel ?parliamentLabel ?parliamentNumber
         ?describedAtUrl
ORDER BY ?itemLabel
"""

# Fallback query: MPs without the P39 position property but linked to
# New Zealand Parliament via membership (P463 = member of) or
# parliamentary group (P4100 = parliamentary group).
# This catches recent MPs whose Wikidata items lack the position statement
# (e.g. many 54th Parliament MPs elected 2023).
QUERY_MEMBER_OF = """
SELECT ?item ?itemLabel ?parliamentId ?givenName ?familyName
       ?partyLabel ?describedAtUrl
       (GROUP_CONCAT(DISTINCT ?refUrl; SEPARATOR=" | ") AS ?referenceUrls)
       (GROUP_CONCAT(DISTINCT ?alias; SEPARATOR=" | ") AS ?aliases)
WHERE {
  ?item wdt:P463 wd:Q38943 .     # member of: New Zealand House of Representatives
  FILTER NOT EXISTS { ?item p:P39 ?st . ?st ps:P39 wd:Q18145518 . }
  OPTIONAL { ?item wdt:P6262 ?parliamentId . }
  OPTIONAL { ?item wdt:P735 ?gn . ?gn rdfs:label ?givenName . FILTER(LANG(?givenName) = "en") }
  OPTIONAL { ?item wdt:P734 ?fn . ?fn rdfs:label ?familyName . FILTER(LANG(?familyName) = "en") }
  OPTIONAL { ?item wdt:P102 ?p . ?p rdfs:label ?partyLabel . FILTER(LANG(?partyLabel) = "en") }
  OPTIONAL { ?item skos:altLabel ?alias . FILTER(LANG(?alias) = "en") }
  OPTIONAL { ?item wdt:P973 ?describedAtUrl . }
  OPTIONAL { ?item prov:wasDerivedFrom ?ref . ?ref pr:P854 ?refUrl . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
GROUP BY ?item ?itemLabel ?parliamentId ?givenName ?familyName
         ?partyLabel ?describedAtUrl
ORDER BY ?itemLabel
"""

QUERIES = [
    ("p39-members-of-parliament", QUERY_P39),
    ("member-of-nz-house", QUERY_MEMBER_OF),
]


def fetch_wikidata(query, max_retries=3):
    """Fetch results from Wikidata SPARQL endpoint with retry."""
    params = {"format": "json", "query": query}
    headers = {
        "User-Agent": "corpus-nz-hansard/1.0 (research)",
        "Accept": "application/sparql-results+json",
    }
    for attempt in range(max_retries):
        try:
            resp = requests.get(SPARQL_URL, params=params, headers=headers, timeout=300)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.Timeout:
            print(f"  Timeout attempt {attempt + 1}/{max_retries}")
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP {e.response.status_code}")
            if e.response.status_code == 429:
                time.sleep(5 * (attempt + 1))
                continue
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"  Connection: {e}")
        if attempt < max_retries - 1:
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(f"Failed after {max_retries} attempts")


def transform_records(data):
    """Transform SPARQL JSON into clean MP records, deduplicated by item."""
    records = []
    seen = set()
    for b in data["results"]["bindings"]:
        iid = b.get("item", {}).get("value", "").split("/")[-1]
        if iid in seen:
            continue
        seen.add(iid)
        raw_aliases = b.get("aliases", {}).get("value", "")
        aliases = [a.strip() for a in raw_aliases.split("|") if a.strip()] if raw_aliases else []
        raw_refs = b.get("referenceUrls", {}).get("value", "")
        ref_urls = [u.strip() for u in raw_refs.split("|") if u.strip()] if raw_refs else []
        described_url = b.get("describedAtUrl", {}).get("value", "")
        records.append(
            {
                "wikidata_id": iid,
                "label": b.get("itemLabel", {}).get("value", ""),
                "parliament_nz_id": b.get("parliamentId", {}).get("value", ""),
                "given_name": b.get("givenName", {}).get("value", ""),
                "family_name": b.get("familyName", {}).get("value", ""),
                "start_date": b.get("startDate", {}).get("value", ""),
                "end_date": b.get("endDate", {}).get("value", ""),
                "party": b.get("partyLabel", {}).get("value", ""),
                "parliament_label": b.get("parliamentLabel", {}).get("value", ""),
                "parliament_number": b.get("parliamentNumber", {}).get("value", ""),
                "aliases": aliases,
                # Provenance: the primary sources Wikidata used for this item
                "provenance": {
                    "described_at_url": described_url,
                    "reference_urls": ref_urls,
                    "wikidata_item_url": f"https://www.wikidata.org/wiki/{iid}",
                },
            }
        )
    return records


def merge_results(results_by_source):
    """Merge results from multiple queries, deduplicating by wikidata_id."""
    seen = set()
    merged = []
    source_counts = {}
    for source_name, records in results_by_source:
        source_counts[source_name] = len(records)
        for rec in records:
            wid = rec["wikidata_id"]
            if wid not in seen:
                seen.add(wid)
                rec["matched_by_query"] = source_name
                merged.append(rec)
    return merged, source_counts


def main():
    print("Fetching NZ MP data from Wikidata SPARQL endpoint...")
    all_results = []
    for source_name, query in QUERIES:
        print(f"  Query: {source_name}")
        try:
            data = fetch_wikidata(query)
            records = transform_records(data)
            all_results.append((source_name, records))
            print(f"    Got {len(records)} unique items")
        except Exception as e:
            print(f"    Failed: {e}")
            all_results.append((source_name, []))

    merged_records, source_counts = merge_results(all_results)
    n = len(merged_records)
    raw_n = sum(sc for sc in source_counts.values())
    with_pid = sum(1 for r in merged_records if r["parliament_nz_id"])
    with_party = sum(1 for r in merged_records if r["party"])
    with_dates = sum(1 for r in merged_records if r["start_date"])
    with_described_url = sum(1 for r in merged_records if r.get("provenance", {}).get("described_at_url"))
    with_ref_urls = sum(1 for r in merged_records if r.get("provenance", {}).get("reference_urls"))
    print(f"\n  Source counts: {source_counts}")
    print(f"  Total raw bindings: {raw_n}")
    print(f"  Unique MP items: {n}")
    print(f"  With Parliament.nz ID: {with_pid}")
    print(f"  With party: {with_party}")
    print(f"  With start/end dates: {with_dates}")
    print(f"  Provenance — described_at_url: {with_described_url}")
    print(f"  Provenance — reference_urls: {with_ref_urls}")
    output = {
        "source": "wikidata-sparql",
        "endpoint": SPARQL_URL,
        "retrieved_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "queries_used": [name for name, _ in QUERIES],
        "n_raw_bindings_by_source": source_counts,
        "n_unique_mp_items": n,
        "member_records": merged_records,
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {OUTPUT_PATH}")
    print(f"  {n} MP records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())