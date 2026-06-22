# Plan: HathiTrust Hansard Acquisition

- [x] Task: Identify collection and verify 510 full-view items
- [x] Task: Investigate HathiTrust API endpoints (documented in evidence.md)
- [x] Task: Build deterministic inventory manifest from committed Wayback sample
- [!] Task: Register for HathiTrust Data API key (OAuth) or acquire hathifile
- [!] Task: Enumerate all 510 volume IDs (100 sample IDs recovered; remaining 410 need OAuth/API, hathifile, or verified browser-backed access)
- [!] Task: Download bibliographic metadata for each volume (blocked until complete IDs and live access path exist)
- [!] Task: Download OCR text for each volume via Data API (blocked pending OAuth/access key)
- [ ] Task: Convert to corpus-compatible format
- [ ] Task: Reconcile against official sitting calendar

## Current Reconciliation (2026-06-22)

Completed evidence-backed work is limited to source identification, archived
collection review, API/access-path documentation, and a 100-ID sample inventory
from Wayback page 1. This track has not acquired the complete HathiTrust corpus:
the complete 510-volume identifier list, bibliographic metadata, OCR downloads,
corpus conversion, and sitting-calendar reconciliation remain outstanding.

The track is therefore blocked rather than planned or complete. The next
unblocking step is one of:

1. Obtain a HathiTrust Data API OAuth/access key.
2. Acquire the relevant monthly hathifile dump and filter it for the collection.
3. Use a verified browser-backed collection enumeration path and document the
   resulting evidence.

## API Investigation Results (2026-06-13)

### Endpoints Verified
- **Collection page**: `https://babel.hathitrust.org/cgi/mb?a=listis&c=71329709` (via Wayback Machine)
- **Volume viewer**: `/cgi/pt?id={ht_id}` -- HT IDs use `uc1.` prefix (UC source)
- **Catalog API**: `/api/volumes/brief/json/{id}` -- documented but Cloudflare-protected
- **Data API**: `/cgi/htd/volume/{ht_id}/...` -- requires OAuth key from `/cgi/kgs/request`
- **Hathifiles**: Full collection metadata in 37-column TSV (~1GB/monthly dump)
- **OAI-PMH**: `/cgi/oai2` -- Cloudflare-protected

### Key Findings
1. All `*.hathitrust.org` domains are behind **Cloudflare** -- simple HTTP clients get 403
2. 100 sample HT volume IDs extracted from Wayback Machine page 1 snapshot
3. Remaining 410 volumes need enumeration via hathifile or browser automation
4. Volume IDs follow pattern: `{source_code}.{local_id}` (e.g., `uc1.b2889853`)
5. The Data API requires an IP-restricted access key for OCR retrieval

### Access Strategy Recommendations
1. **Primary**: Request OAuth key from `/cgi/kgs/request` (enables all Data API features)
2. **Fallback**: Download hathifile `hathi_full_*.txt.gz` and filter for UC source
3. **Last resort**: Browser automation (Playwright) to resolve Cloudflare and scrape listings
