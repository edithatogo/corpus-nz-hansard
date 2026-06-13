# Evidence: Bills API Integration

## API Discovery (2026-06-12)

Confirmed accessible via direct HTTP POST with no authentication.

Sample response from /api/data/search with illTab: All:
- Total results: 3,513
- Parliaments covered: 44-54
- Bill types: Government, Member's, Private

Sample response from /api/data/Bill/{uuid}:
- Structured member data: Members[].PreferredFormOfAddress, DisplayName, SortedName
- Stage data: Stages[].StageName, StageDate, OutcomeName, StartDate, EndDate
- Linked to legislation.govt.nz: BillLegislationUrl field

Search request body documented in scripts/fetch_bills_api.py.

## Full Extraction Run (2026-06-13)

Script: `scripts/fetch_bills_api.py` (PID 2340, background subprocess via Python)

### Facets / Metadata
| Field | Value |
|---|---|
| Current Parliament | 54 |
| Parliaments covered | 43–54 (1990–Current) |
| Bill types | Government, Local, Member's, Private |
| Committees | 41 |
| Document stages | Committee of whole House, First Reading, Royal Assent, Second Reading, Select Committee, Terminated, Third Reading |
| Terminated reasons | Assented, Discharged, Divided, Lapsed, Not Agreed, Rejected, Terminated, Withdrawn |

### Extraction Results
| Metric | Count |
|---|---|
| Bill summaries fetched (paginated) | **3,513** |
| Bill details fetched (individual API calls) | **3,513** |
| Unique member names extracted | **351** |

### Output Files (`derived/bills_api/`)
| File | Size | Description |
|---|---|---|
| `facets.json` | 8.3 KB | Parliament list, committees, bill types, stages |
| `bills_summary_20260613T021002Z.json` | 519 KB | Paginated search results (all 3,513 bill summaries) |
| `bills_details_20260613T021002Z.json` | 513 KB | Individual bill detail records with member/sponsor data |
| `bills_members_20260613T021002Z.json` | 8.8 KB | Deduplicated member names (351 unique) |

### Member Name Samples
First 20 of 351 members extracted: Alastair Scott, Allan Peachey, Anahila Kanongata'a, Anahila Kanongata'a-Suisuiki, Andrew Bayly, Andy Foster, Angie Warren-Clark, Annabel Young, Arena Williams, Barbara Kuriger, Barbara Stewart, Belinda Vernon, Bob Simcock, Brendon Burns, Brett Hudson, Brian Neeson, Brooke van Velden, Cameron Luxton, Camilla Belich, Carl Bates.

Includes `Hon` and `Rt Hon` prefixes, Māori members, and MPs from Parliaments 43–54.

### Run Duration
Total wall-clock time: ~40 minutes (API rate limiting: 0.2s between detail fetches × 3,513 bills + 0.5s between paginated search pages).
