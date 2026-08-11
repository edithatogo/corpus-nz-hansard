"""Multi-format document parsing for select committee reports."""

from __future__ import annotations

import hashlib
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, ClassVar


SUPPORTED_FORMATS = frozenset({"pdf", "html", "docx"})


# ---------------------------------------------------------------------------
# Format detection
# ---------------------------------------------------------------------------


def detect_format(
    filename: str,
    content_type: str | None = None,
) -> str | None:
    """Detect the document format from filename and optional content-type.

    Parameters
    ----------
    filename:
        The document filename or URL path.
    content_type:
        Optional HTTP Content-Type header value.

    Returns
    -------
    str or None
        One of ``"pdf"``, ``"html"``, ``"docx"``, or ``None`` if unknown.
    """
    # content-type takes precedence
    if content_type:
        ct = content_type.lower().strip()
        if "pdf" in ct:
            return "pdf"
        if "html" in ct:
            return "html"
        if "wordprocessingml" in ct or "docx" in ct or "msword" in ct:
            return "docx"

    # Fallback to extension
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        return "pdf"
    if ext in (".html", ".htm"):
        return "html"
    if ext == ".docx":
        return "docx"

    return None


# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------

try:
    import pdfplumber
except ImportError:
    pdfplumber = None


def extract_text_from_pdf(
    path: Path | str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract text from a PDF document.

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
            with pdfplumber.open(str(path)) as pdf:
                pages_text = [page.extract_text() or "" for page in pdf.pages]
            text = "\n".join(pages_text).strip()
            if compute_hash:
                return {"text": text, "sha256": _hash(text)}
            return text
        except Exception:
            return {"text": "", "sha256": _hash("")} if compute_hash else ""

    # Fallback using PyMuPDF
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


# ---------------------------------------------------------------------------
# HTML text extraction
# ---------------------------------------------------------------------------


class _VisibleTextExtractor(HTMLParser):
    """Collect visible HTML text while dropping script and style content."""

    BLOCK_TAGS: ClassVar[set[str]] = {
        "p",
        "div",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "tr",
        "blockquote",
        "section",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._ignored_tag: str | None = None

    def handle_starttag(self, tag: str, _attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self._ignored_tag = tag
            return
        if self._ignored_tag is not None:
            return
        if tag == "br":
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if self._ignored_tag == tag:
            self._ignored_tag = None
            return
        if self._ignored_tag is not None:
            return
        if tag in self.BLOCK_TAGS:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignored_tag is None:
            self._chunks.append(data)

    def handle_comment(self, _data: str) -> None:
        return

    def text(self) -> str:
        return "".join(self._chunks)


def extract_text_from_html(
    html: str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract visible text from an HTML string.

    Parameters
    ----------
    html:
        Raw HTML content.
    compute_hash:
        If ``True``, return a dict with keys ``text`` and ``sha256``.

    Returns
    -------
    str or dict
        Plain text extracted from HTML, or empty string on failure.
    """
    if not html:
        return {"text": "", "sha256": _hash("")} if compute_hash else ""

    extractor = _VisibleTextExtractor()
    extractor.feed(html)
    extractor.close()
    text = extractor.text()

    # Collapse whitespace
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()
    if compute_hash:
        return {"text": text, "sha256": _hash(text)}
    return text


# ---------------------------------------------------------------------------
# DOCX text extraction
# ---------------------------------------------------------------------------

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None


def extract_text_from_docx(
    path: Path | str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract text from a Word DOCX document.

    Parameters
    ----------
    path:
        Path to the DOCX file.
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

    if DocxDocument is not None:
        try:
            doc = DocxDocument(str(path))
            paragraphs = [p.text for p in doc.paragraphs]
            text = "\n".join(paragraphs).strip()
            if compute_hash:
                return {"text": text, "sha256": _hash(text)}
            return text
        except Exception:
            return {"text": "", "sha256": _hash("")} if compute_hash else ""

    return {"text": "", "sha256": _hash("")} if compute_hash else ""


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def extract_text(
    source: str | Path,
    fmt: str,
    compute_hash: bool = False,
) -> str | dict[str, str]:
    """Extract text from a document in any supported format.

    Parameters
    ----------
    source:
        For PDF/DOCX: file path. For HTML: raw HTML string.
    fmt:
        One of ``"pdf"``, ``"html"``, ``"docx"``.
    compute_hash:
        If ``True``, return a dict with ``text`` and ``sha256``.

    Returns
    -------
    str or dict
        Extracted text content, or empty string on failure.
    """
    if fmt == "pdf":
        return extract_text_from_pdf(source, compute_hash=compute_hash)
    if fmt == "html":
        return extract_text_from_html(str(source), compute_hash=compute_hash)
    if fmt == "docx":
        return extract_text_from_docx(source, compute_hash=compute_hash)
    return {"text": "", "sha256": _hash("")} if compute_hash else ""


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
