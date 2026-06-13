# Track: Bills API Integration

Integrate the open REST API at ills.parliament.nz/api/ as an authority source.

## Discovered Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| /api/data/search | POST | Paginated bill listing (3,513 total) |
| /api/data/Bill/{uuid} | GET | Full bill detail with members, stages |
| /api/data/facet | POST | Parliament, committee, stage filters |
| /api/data/currentParliament | GET | Current parliament number (54) |
| /rss?set=Bills | GET | RSS feed of recent bills |

## Relevance

- Member sponsor names for identity resolution
- Bill stages and dates for parliamentary timeline
- Select committee assignments
- Links to legislation.govt.nz for cross-corpus referencing

## Script

- scripts/fetch_bills_api.py — fetches all bills, details, and member names
