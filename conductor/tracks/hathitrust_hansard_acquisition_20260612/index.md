# Track: HathiTrust Hansard Acquisition

Source: https://babel.hathitrust.org/cgi/mb?a=listis&c=71329709

Acquisition status: blocked. The collection-level inventory and access patterns are
documented for 510 full-view volumes covering NZ Parliamentary Debates 1854-1990,
but the repository does not yet contain the complete HathiTrust volume inventory,
bibliographic metadata, or OCR text.

## Coverage
- Parliaments 1-46 (pre-dates current DocumentsDB extract)
- All 510 collection items were identified as full view/public domain from the
  archived collection evidence.
- 100 sample HathiTrust volume IDs have been recovered from the Wayback page-1
  listing; the remaining 410 IDs still need hathifile, OAuth/API, or verified
  browser-backed enumeration.
- OCR text is expected to be available via the HathiTrust Data API only after
  OAuth/API access is obtained.

## Relevance
- Extends corpus backwards by ~150 years
- Fills gap before Parliament 47
- Enables historical member resolution

## Access
- Bibliographic metadata: HathiTrust Catalog API, currently not live-verified
  from this repo because simple HTTP access is Cloudflare-protected.
- Full text: HathiTrust Data API, blocked pending OAuth/access key approval.
- Fallback enumeration: monthly hathifile dump, blocked until the relevant
  hathifile is acquired and filtered.
