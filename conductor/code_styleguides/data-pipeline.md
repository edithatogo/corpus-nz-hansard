# Data Pipeline Style Guide

## General

- Prefer deterministic scripts with explicit input and output paths.
- Keep source files immutable.
- Use clear command-line arguments or documented constants for source archive and generated-output locations.
- Fail loudly on unexpected schema changes.

## Python

- Use type hints for public functions.
- Keep file IO, parsing, normalization, and validation separable.
- Stream or chunk large CSV files instead of loading all data into memory.
- Write tests around small fixtures before running against full source extracts.

## Manifests and Validation

- Emit machine-readable JSON for manifests and validation reports.
- Include source file names, hashes, sizes, row counts, generated output paths, warnings, and tool versions when practical.
- Keep human-readable evidence summaries in the active Conductor track.
