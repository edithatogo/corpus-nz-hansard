# Search and RAG Index MVP Evidence

## Phase 1

Status: complete.

Created:

- `tests/test_build_search_index.py`
- `docs/search-rag-index-contract.md`

### Red Phase

Command:

```powershell
python -m unittest discover tests
```

Result:

- Failed before implementation.
- Failure reason: `ModuleNotFoundError: No module named 'scripts.build_search_index'`.

## Phase 2

Status: complete.

Created:

- `scripts/build_search_index.py`
- `generated/search/hansard_search.sqlite`
- `manifests/search_index_validation.json`

### Green Phase

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest tests.test_build_search_index
```

Result:

- Passed.
- Test count: 2.
- Note: SQLite file creation required running outside the sandbox because sandboxed SQLite file locking raised `sqlite3.OperationalError: disk I/O error`.

### Full Index Build

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python scripts\build_search_index.py --parquet generated\parquet\hansard.parquet --database generated\search\hansard_search.sqlite --validation manifests\search_index_validation.json
```

Result:

- Database: `generated/search/hansard_search.sqlite`
- Validation: `manifests/search_index_validation.json`
- Source rows: 193,922
- Indexed documents: 193,922
- Indexed chunks: 1,018,955
- Index type: SQLite FTS5
- Embedding index: false

Sample query counts:

- `health`: 95,897
- `budget`: 77,683
- `education`: 76,241
- `housing`: 40,537
- `climate`: 24,388

Read-only SQLite verification:

- `chunks`: 1,018,955 rows
- `chunks_fts`: 1,018,955 rows
- Query `budget` returned citation-bearing Budget Debate hits.

## Phase 3

Status: complete.

Created:

- `docs/search-rag-index-report.md`

### Full Test Gate

Command:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; python -m unittest discover tests
```

Result:

- Passed.
- Test count: 19.

Final boundary:

- Local lexical search index only.
- No embeddings, vector database, hosted service, web publishing, or authoritative speaker attribution.
