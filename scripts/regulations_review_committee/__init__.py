"""Regulations Review Committee proceedings ingestion pipeline.

Modules
-------
metadata
    Metadata extraction from committee proceeding documents.
pdf_parser
    PDF/HTML text extraction for proceeding documents.
scraper
    Scraper connectors for the Parliament API.
complaint_parser
    Complaint parsing and structured extraction from proceeding text.
regulation_cross_reference
    Cross-referencing complaints to NZ secondary legislation keys.
"""
from __future__ import annotations
