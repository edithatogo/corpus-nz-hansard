"""Parliament submissions ingestion pipeline.

Modules:
    pdf_parser  — PDF text extraction using pdfplumber
    download    — Document download with verification
    scraper     — NZ Parliament select committee submissions scraper
    metadata    — Metadata extraction from submission documents
"""

from __future__ import annotations


