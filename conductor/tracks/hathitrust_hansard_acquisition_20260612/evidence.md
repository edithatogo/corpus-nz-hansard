# Evidence: HathiTrust Hansard Acquisition

## Collection Identification (2026-06-12)

- **Collection URL**: https://babel.hathitrust.org/cgi/mb?a=listis&c=71329709
- **Collection ID**: `71329709`
- **Name**: NZ Parliamentary Debates (Hansard)
- **Total items**: 510 (all Full View / public domain)
- **Coverage**: 1854 to ~1990
- **Contributing library**: University of California (source code: `uc1`)
- **Persistent handle**: `https://hdl.handle.net/2027/{ht_id}`

### Confirmed via Wayback Machine (2023-10-03)

- All 510 items are **Full View** (public domain)
- Source institution code: `uc1` (University of California)
- Author: New Zealand. Parliament.
- Format: Journal/Serial
- Language: English
- Place of publication: New Zealand

### Date Distribution

| Period | Volumes |
|--------|---------|
| 1850-1859 | 56 |
| 1860-1869 | 10 |
| 1870-1879 | 28 |
| 1880-1889 | 32 |
| 1890-1899 | 42 |
| 1900-1909 | 36 |
| 1910-1919 | 37 |
| 1920-1929 | 38 |
| 1930-1939 | 33 |
| 1940-1949 | 23 |
| 1960-1969 | 29 |
| 1970-1979 | 64 |
| 1980-1989 | 78 |
| 1854 (single year) | 54 |
| **Total** | **~510** |

### 100 Sample Volume IDs (from page 1)

```
uc1.a0001646314  uc1.a0001745447  uc1.a0001745553  uc1.a0001745561
uc1.a0001745579  uc1.a0001745587  uc1.a0001745595  uc1.a0001745603
uc1.a0001745611  uc1.a0001745629  uc1.a0001745637  uc1.a0001757616
uc1.a0001757772  uc1.a0001757988  uc1.a0001758010  uc1.a0001800556
uc1.a0001800861  uc1.b2889853     uc1.b2889879     uc1.b2889888
uc1.b2889951     uc1.b2889953     uc1.b2889962     uc1.b2889969
uc1.b2889971     uc1.b2889974     uc1.b2889976     uc1.b2889978
uc1.b2889983     uc1.b2889989     uc1.b2890198     uc1.b2890228
uc1.b2890240     uc1.b2890245     uc1.b2890262     uc1.b2890264
uc1.b2940052-81  uc1.b2940127-59  uc1.b2940162
```
(100 IDs from page 1; 410 more across pages 2-6 pending enumeration)

## API Endpoint Patterns

### 1. Collection Enumeration

| Pattern | URL | Notes |
|---------|-----|-------|
| Collection listing | `GET /cgi/mb?a=listis&c={id}` | Paginated HTML, 100 items/page |
| Page N | `GET /cgi/mb?a=listis;c={id};pn={N};sort=title_a` | Use `;pn=1..6` |
| Search | `GET /cgi/mb?a=listsrch;c={id};q1=*&facet=...` | Facet filtering |

### 2. Catalog (Bibliographic) API

Base: `https://catalog.hathitrust.org/api/volumes/`

| Endpoint | Description |
|----------|-------------|
| `GET /brief/json/{identifier}` | Brief JSON record |
| `GET /full/json/{identifier}` | Full MARC-in-JSON |
| `GET /Record/{ht_bib_key}` | HTML catalog page |

**Identifiers**: HT Record#, HT Item ID, OCLC#, ISBN, ISSN, LCCN.

### 3. Data API (OAuth Required)

**Auth**: Key from `https://babel.hathitrust.org/cgi/kgs/request`
- Pass as `?access_key={key}` parameter

Base: `https://babel.hathitrust.org/cgi/htd/`

| Endpoint | Description |
|----------|-------------|
| `GET /volume/{ht_id}/mets` | METS metadata |
| `GET /volume/{ht_id}/page/{n}/image` | Page image |
| `GET /volume/{ht_id}/page/{n}/ocr` | Page OCR |
| `GET /volume/{ht_id}/zip/ocr` | All OCR (zip) |
| `GET /volume/{ht_id}/zip/image` | All images (zip) |

### 4. Hathifiles (Bulk Metadata)

- **Downloads**: `https://www.hathitrust.org/hathifiles`
- **Full dump**: `hathi_full_YYYYMMDD.txt.gz` (~1.05 GB)
- **Updates**: `hathi_upd_YYYYMMDD.txt.gz`
- **37-column TSV format** (key columns: `htid`, `access`, `rights`, `ht_bib_key`, `description`, `title`, `imprint`, `oclc_num`, `isbn`, `issn`, `lccn`, `lang`, `bib_fmt`, `author`)

### 5. OAI-PMH

- **URL**: `https://babel.hathitrust.org/cgi/oai2`
- **Verbs**: `Identify`, `ListSets`, `ListRecords`
- **Formats**: `marc21`, `oai_dc`

### 6. Volume Viewer

- **Viewer**: `https://babel.hathitrust.org/cgi/pt?id={ht_id}`
- **Handle**: `https://hdl.handle.net/2027/{ht_id}`

## Access Limitations

All HathiTrust domains (`babel.*`, `catalog.*`, `www.*`, `quod.lib.umich.edu`) are behind **Cloudflare** anti-bot protection. Simple HTTP clients get 403.

### Access Strategies

1. **OAuth key** from `/cgi/kgs/request` -- enables Data API
2. **Hathifiles** -- bulk metadata via external mirrors
3. **HTRC platform** -- text analysis with direct access
4. **Browser automation** -- selenium/playwright for Cloudflare bypass

## Next Steps

1. [ ] Register for HathiTrust Data API key
2. [ ] Enumerate all 510 volume IDs
3. [ ] Fetch bibliographic metadata
4. [ ] Download OCR text
5. [ ] Convert to corpus-compatible format
