"""Build a browser-discovered index for the weekly journals archive."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_PATH = (
    ROOT / "derived/historical_sitting_official_exports/weekly_journals_archive_index.json"
)
DEFAULT_PAGE_NUMBERS = [23, 22, 20, 16, 14]
DEFAULT_CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ARTICLE_RE = re.compile(r"/weekly-journals-archive/document/")


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _extract_year(title: str) -> str | None:
    match = re.search(r"(19|20)\d{2}", title)
    return match.group(0) if match else None


def _summarize_articles(articles: list[dict[str, str]]) -> dict[str, Any]:
    years = sorted({year for year in (_extract_year(item["title"]) for item in articles) if year})
    return {
        "article_count": len(articles),
        "pdf_href_count": sum(1 for item in articles if item.get("pdf_href")),
        "years": years,
        "first_title": articles[0]["title"] if articles else None,
        "last_title": articles[-1]["title"] if articles else None,
    }


def build_historical_sitting_weekly_archive_index(
    *,
    page_reports: list[dict[str, Any]],
    output_path: Path = DEFAULT_OUTPUT_PATH,
    generated_at: str | None = None,
) -> dict[str, Any]:
    page_numbers = [report.get("page_number", report.get("page")) for report in page_reports]
    normalized_pages: list[dict[str, Any]] = []
    articles: list[dict[str, str]] = []
    for report in page_reports:
        page_number = report.get("page_number", report.get("page"))
        normalized_articles: list[dict[str, str]] = []
        for article in list(report.get("articles") or report.get("results") or []):
            normalized_articles.append(
                {
                    "article_url": article.get("article_url") or article.get("articleUrl") or article.get("url"),
                    "title": article["title"],
                    "pdf_href": article.get("pdf_href") or article.get("pdf"),
                }
            )
        articles.extend(normalized_articles)
        normalized_pages.append(
            {
                "page_number": page_number,
                "articles": normalized_articles,
                **_summarize_articles(normalized_articles),
            }
        )

    unique_articles: list[dict[str, str]] = []
    seen: set[str] = set()
    for article in articles:
        key = article["article_url"]
        if key in seen:
            continue
        seen.add(key)
        unique_articles.append(article)

    payload = {
        "artifact_name": "historical_sitting_weekly_archive_index",
        "artifact_version": "0.1.0",
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "page_numbers": page_numbers,
        "pages": normalized_pages,
        "summary": {
            "pages_crawled": len(page_reports),
            "article_count": len(unique_articles),
            "pdf_href_count": sum(1 for item in unique_articles if item.get("pdf_href")),
            "year_coverage": sorted(
                {year for year in (_extract_year(item["title"]) for item in unique_articles) if year}
            ),
        },
        "notes": [
            "This browser-discovered index records weekly journal archive article and PDF hrefs.",
            "It does not download or validate the PDF payload bytes.",
            "It is intended to feed cached comparison inputs for historical reconciliation.",
        ],
    }
    _write_json(payload, output_path)
    return payload


async def _crawl_page(page, page_number: int, browser) -> dict[str, Any]:
    url = (
        "https://www3.parliament.nz/en/pb/journals-of-the-house/weekly-journals-archive/"
        f"?Criteria.PageNumber={page_number}"
    )
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    await page.wait_for_selector('a[href*="/weekly-journals-archive/document/"]', timeout=30000)
    links = await page.locator('a[href*="/weekly-journals-archive/document/"]').evaluate_all(
        """
        nodes => Array.from(new Map(nodes.map(a => [a.href, {
            title: (a.textContent || '').trim(),
            url: a.href
        }])).values()).filter(x => x.title && x.url)
        """
    )
    articles: list[dict[str, str]] = []
    for link in links:
        article_page = await browser.new_page()
        await article_page.goto(link["url"], wait_until="networkidle", timeout=60000)
        await article_page.wait_for_timeout(2000)
        title = _normalize(await article_page.locator("h1").first.text_content() or link["title"])
        pdf_href = ""
        try:
            pdf_href = await article_page.locator("text=/PDF/i").first.evaluate("el => el.href")
        except Exception:
            pdf_href = ""
        articles.append(
            {
                "article_url": link["url"],
                "title": title,
                "pdf_href": pdf_href,
            }
        )
        await article_page.close()
    return {
        "page_number": page_number,
        "article_count": len(articles),
        "articles": articles,
        **_summarize_articles(articles),
    }


async def _crawl_weekly_archive(
    *,
    page_numbers: list[int],
    executable_path: str = DEFAULT_CHROME,
) -> list[dict[str, Any]]:
    from playwright.async_api import async_playwright

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            executable_path=executable_path,
        )
        page = await browser.new_page()
        reports: list[dict[str, Any]] = []
        for page_number in page_numbers:
            reports.append(await _crawl_page(page, page_number, browser))
        await browser.close()
        return reports


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a weekly journals archive index.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--chrome", default=DEFAULT_CHROME)
    parser.add_argument("--page", type=int, action="append", dest="pages")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    page_numbers = args.pages or DEFAULT_PAGE_NUMBERS
    page_reports = asyncio.run(_crawl_weekly_archive(page_numbers=page_numbers, executable_path=args.chrome))
    result = build_historical_sitting_weekly_archive_index(
        page_reports=page_reports,
        output_path=args.output,
    )
    print(f"Wrote {args.output}")
    print(f"Pages crawled: {result['summary']['pages_crawled']}")
    print(f"Articles indexed: {result['summary']['article_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
