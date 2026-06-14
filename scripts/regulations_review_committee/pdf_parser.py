"""PDF/HTML text extraction for Regulations Review Committee proceedings."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_proceeding_text(
    path: Path | str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract text from a proceeding PDF document.

    Parameters
    ----------
    path:
        Path to the PDF file.
    compute_hash:
        If ``True``, return a dict with keys ``text`` and ``sha256``.

    Returns
    -------
    str or dict
        Extracted text content, or empty string on failure.
    """
    path = Path(path)
    if not path.exists():
        return {"text": "", "sha256": _hash("")} if compute_hash else ""

    if pdfplumber is not None:
        try:
            return _extract_with_pdfplumber(path, compute_hash)
        except Exception:
            return {"text": "", "sha256": _hash("")} if compute_hash else ""

    return _extract_fallback(path, compute_hash)


def extract_proceeding_metadata(path: Path | str) -> dict:
    """Extract basic metadata from a proceeding PDF.

    Returns a dict with ``page_count`` and available PDF metadata fields.
    Returns ``{"page_count": 0, "error": "file_not_found"}`` for missing files.
    """
    path = Path(path)
    if not path.exists():
        return {"page_count": 0, "error": "file_not_found"}

    if pdfplumber is not None:
        try:
            with pdfplumber.open(str(path)) as pdf:
                meta = dict(pdf.metadata) if pdf.metadata else {}
                meta["page_count"] = len(pdf.pages)
                return meta
        except Exception as e:
            return {"page_count": 0, "error": str(e)}

    return _metadata_fallback(path)


def extract_agenda_items(text: str) -> list[str]:
    """Extract agenda item titles from proceeding text."""
    if not text:
        return []
    items: list[str] = []
    # Match numbered agenda items
    in_agenda = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.search(r"\bagenda\b", stripped, re.IGNORECASE):
            in_agenda = True
            continue
        if in_agenda:
            m = re.match(r"^\d+[\.\)]\s*(.+)", stripped)
            if m:
                items.append(m.group(1).strip())
            elif stripped and not stripped.startswith(("The committee", "The meeting")):
                # Check if we've left the agenda section
                if re.match(r"^[A-Z][a-z]", stripped) and not re.match(
                    r"^\d+", stripped
                ):
                    if items:  # Only stop if we found at least one item
                        break
    return items


def extract_committee_members(text: str) -> list[str]:
    """Extract committee member names from proceeding text."""
    if not text:
        return []
    members: list[str] = []
    patterns = [
        re.compile(r"Present:\s*(.+)", re.IGNORECASE),
        re.compile(r"Members\s+(?:Present|attending):\s*(.+)", re.IGNORECASE),
        re.compile(r"Committee\s+(?:Members|members):\s*(.+)", re.IGNORECASE),
    ]
    for pat in patterns:
        m = pat.search(text)
        if m:
            raw = m.group(1)
            # Remove parenthetical role qualifiers like (Chair)
            raw = re.sub(r"\s*\([^)]*\)\s*", " ", raw)
            # Split by comma or "and"
            parts = re.split(r",\s*|\s+and\s+", raw)
            for part in parts:
                name = part.strip().strip(".,;:")
                if name and len(name) > 2:
                    members.append(name)
            break
    return members


def _extract_with_pdfplumber(path: Path, compute_hash: bool) -> str | dict:
    """Extract text using pdfplumber."""
    with pdfplumber.open(str(path)) as pdf:
        pages_text = [page.extract_text() or "" for page in pdf.pages]
    text = "\n".join(pages_text).strip()
    if compute_hash:
        return {"text": text, "sha256": _hash(text)}
    return text


def _extract_fallback(path: Path, compute_hash: bool = False) -> str | dict:
    """Fallback extraction using PyMuPDF (fitz)."""
    try:
        import fitz  # type: ignore[import-untyped]
    except ImportError:
        return {"text": "", "sha256": _hash("")} if compute_hash else ""

    try:
        doc = fitz.open(str(path))
        pages = [doc[i].get_text() for i in range(len(doc))]
        text = "\n".join(pages).strip()
        doc.close()
    except Exception:
        text = ""

    if compute_hash:
        return {"text": text, "sha256": _hash(text)}
    return text


def _metadata_fallback(path: Path) -> dict:
    """Fallback metadata extraction using PyMuPDF."""
    try:
        import fitz  # type: ignore[import-untyped]
    except ImportError:
        return {"page_count": 0, "error": "no_pdf_library"}

    try:
        doc = fitz.open(str(path))
        meta = {"page_count": len(doc)}
        if doc.metadata:
            meta.update(doc.metadata)
        doc.close()
        return meta
    except Exception as e:
        return {"page_count": 0, "error": str(e)}


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

