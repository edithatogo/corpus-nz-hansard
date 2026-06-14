"""PDF text extraction for submission documents using pdfplumber."""

from __future__ import annotations

import hashlib
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_pdf_text(
    path: Path | str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract text from a PDF file using pdfplumber.

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

    # Fallback via PyMuPDF
    return _extract_fallback(path, compute_hash)


def extract_pdf_metadata(path: Path | str) -> dict:
    """Extract basic metadata from a PDF file.

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

    # Fallback via PyMuPDF
    return _metadata_fallback(path)


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

