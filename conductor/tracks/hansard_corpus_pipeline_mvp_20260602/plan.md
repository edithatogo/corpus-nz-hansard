# Plan: Hansard Corpus Pipeline MVP

## Phase 1: Source Inventory and Storage Policy

- [x] Task: Define generated-output directory and ignore/regeneration policy.
    - [x] Add or update project-local ignore rules for generated multi-GB outputs.
    - [x] Document which lightweight manifests are tracked and which outputs are regenerated.
- [x] Task: Build source archive inventory.
    - [x] Create a script that records source ZIP path, size, timestamp, hash, contained file names, compressed sizes, uncompressed sizes, and contained timestamps.
    - [x] Write machine-readable inventory output.
    - [x] Record command output and summary in track evidence.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Source Inventory and Storage Policy' (Protocol in workflow.md)

## Phase 2: CSV Schema Discovery

- [x] Task: Build schema discovery tooling.
    - [x] Inspect each contained CSV without extracting all data into the repo root.
    - [x] Detect encoding, delimiter, headers, sample rows, null patterns, and obvious date/text fields.
    - [x] Record schema drift across `Hansard-47.csv` through `Hansard-54.csv`.
- [x] Task: Produce schema discovery report.
    - [x] Include row counts where practical.
    - [x] Identify candidate normalized fields for parliamentary term, sitting date, speaker, party, debate/topic, and text.
    - [x] Record limitations and uncertain fields.
- [x] Task: Conductor - User Manual Verification 'Phase 2: CSV Schema Discovery' (Protocol in workflow.md)

## Phase 3: Normalization Pipeline MVP

- [x] Task: Design normalization contract.
    - [x] Define normalized table or dataset shape.
    - [x] Document field mappings, coercions, and rejection/warning behavior.
    - [x] Add small fixture-based tests before full-source processing.
- [x] Task: Implement repeatable normalization.
    - [x] Stream or chunk source CSV records.
    - [x] Write normalized Parquet outputs under the generated-output directory.
    - [x] Emit manifest and validation JSON.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Normalization Pipeline MVP' (Protocol in workflow.md)

## Phase 4: DuckDB Analysis Surface

- [x] Task: Build DuckDB output or reproducible DuckDB build script.
    - [x] Load or query normalized Parquet outputs.
    - [x] Provide basic verification queries for counts and representative fields.
    - [x] Document local query examples.
- [x] Task: Validate generated analytical outputs.
    - [x] Compare source row counts to normalized output counts.
    - [x] Record warnings, skipped records, and validation failures.
    - [x] Separate research-readiness, public-dataset-readiness, and reporting-readiness notes.
- [x] Task: Conductor - User Manual Verification 'Phase 4: DuckDB Analysis Surface' (Protocol in workflow.md)

## Phase 5: Handoff and Readiness

- [x] Task: Produce pipeline handoff documentation.
    - [x] Document setup commands, regeneration commands, expected outputs, and known limitations.
    - [x] Identify next tracks for public dataset publication, reporting/Power BI, or search/RAG indexing.
- [x] Task: Final readiness review.
    - [x] Confirm all generated outputs are reproducible.
    - [x] Confirm evidence is sufficient to audit each major claim.
    - [x] Update `conductor/tracks.md` only when acceptance criteria are met.
- [x] Task: Conductor - User Manual Verification 'Phase 5: Handoff and Readiness' (Protocol in workflow.md)
