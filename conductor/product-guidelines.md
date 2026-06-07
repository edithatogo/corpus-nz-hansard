# Product Guidelines

This document outlines the design, documentation, and data quality guidelines for the `corpus-nz-hansard` workspace.

## 1. Documentation & Reproducibility Standards

- **Self-Documenting Code:** All Python parsing, normalization, and validation scripts must feature clear inline comments and function docstrings explaining the parsing logic, especially when dealing with anomalies or custom text-cleaning rules in the CSVs.
- **Run Records & Auditability:** Every processing run or stage must output a markdown file or log capturing the environment configuration, command line parameters, and overall processing context to ensure anyone can reproduce the corpus generation from the raw ZIP archive.

## 2. Naming Conventions & Schema Standards

- **Alignment with Official Terminology:** Dataset schemas, column names, and intermediate variables must align with the official terminology used by the New Zealand Parliament (e.g., `Speaker`, `Party`, `SittingDate`, `DebateTitle`, `Volume`). Avoid generic names like `col1` or `data_field`.
- **Case and Formatting Consistency:** Schema fields must use a consistent casing convention (e.g., snake_case or PascalCase) across all normalized outputs to simplify downstream SQL querying and NLP integration.

## 3. Data Provenance & Manifest Integrity

- **Provenance Tracking:** Normalized data outputs must be accompanied by a machine-readable JSON or YAML manifest recording the MD5/SHA-256 hash, file size, and row count of both the input archive and the resulting outputs.
- **Log Automation:** Normalization pipelines must automatically direct stdout/stderr to standard log locations. Warnings related to mismatched schemas, invalid dates, or unknown speakers must be explicitly logged without halting the entire pipeline unless a fatal error occurs.
