"""
Simple Wikipedia crawler for Speer Technologies QA coding assessment.
Author: Faisal Yakubu
"""

import argparse
import csv
import json
import re
import sys
from collections import deque
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Constants
WIKI_BASE = "https://en.wikipedia.org"
WIKI_PATH_RE = re.compile(r"^/wiki/[^:#]+$")  # Valid /wiki/ links only; excludes anchors, files, special pages


def is_valid_wiki_url(url: str) -> bool:
    """
    Check if the provided URL is a valid Wikipedia article link.
    :param url: URL string to validate
    :return: Boolean indicating validity
    """
    parsed = urlparse(url)
    return (
        parsed.scheme in ("http", "https")
        and parsed.netloc.endswith("wikipedia.org")
        and WIKI_PATH_RE.match(parsed.path or "")
    )


def extract_wiki_links(html: str) -> list[str]:
    """
    Extract up to 10 unique Wikipedia article links from given HTML content.
    :param html: Raw HTML of the page
    :return: List of full Wikipedia links
    """
    soup = BeautifulSoup(html, "html.parser")
    links, seen = [], set()

    for a in soup.select("a[href]"):
        href = a["href"]
        if WIKI_PATH_RE.match(href) and href not in seen:
            links.append(urljoin(WIKI_BASE, href))  # Convert relative to full URL
            seen.add(href)
        if len(links) == 10:
            break
    return links


def crawl(seed_url: str, depth: int) -> list[str]:
    """
    Crawl Wikipedia links using breadth-first search up to a given depth.
    :param seed_url: Starting Wikipedia article URL
    :param depth: How many levels deep to crawl (1–3)
    :return: List of all discovered links
    """
    visited = set([seed_url])
    queue = deque([(seed_url, 0)])
    all_links = [seed_url]

    while queue:
        url, lvl = queue.popleft()
        if lvl == depth:
            continue  # Stop if maximum depth reached

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as exc:
            print(f"[WARN] Could not fetch {url}: {exc}", file=sys.stderr)
            continue

        for link in extract_wiki_links(resp.text):
            if link not in visited:
                visited.add(link)
                all_links.append(link)
                queue.append((link, lvl + 1))  # Add to queue for next level crawl
    return all_links


def write_csv(fname: str, links: list[str]) -> None:
    """
    Save results to a CSV file.
    :param fname: File name to write to
    :param links: List of URLs
    """
    with open(fname, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["index", "url"])  # Header
        for i, link in enumerate(links, 1):
            writer.writerow([i, link])


def write_json(fname: str, payload: dict) -> None:
    """
    Save results to a JSON file.
    :param fname: File name to write to
    :param payload: Dictionary containing crawl results
    """
    with open(fname, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2)


def main() -> None:
    """
    Main function to parse arguments and run crawler.
    """
    parser = argparse.ArgumentParser(description="Simple Wikipedia crawler (max depth 3).")
    parser.add_argument("url", help="Seed Wikipedia article URL")
    parser.add_argument("depth", type=int, help="Crawl depth (1–3)")
    parser.add_argument(
        "--out",
        choices=["csv", "json"],
        help="Optional output format; file written to current directory",
    )
    args = parser.parse_args()

    # Validate input
    if not is_valid_wiki_url(args.url):
        parser.error("URL must be a valid wikipedia.org/wiki/... link")

    if not 1 <= args.depth <= 3:
        parser.error("Depth must be an integer between 1 and 3")

    print(f"Starting crawl from: {args.url}")
    all_links = crawl(args.url, args.depth)
    unique_count = len(set(all_links))

    print(
        f"\nCrawl complete (depth {args.depth})"
        f"\nTotal links found : {len(all_links):>4}"
        f"\nUnique links      : {unique_count:>4}"
    )

    # Output results if --out option is used
    if args.out:
        if args.out == "csv":
            write_csv("results.csv", all_links)
            print("→ results.csv written")
        else:
            payload = {
                "seed": args.url,
                "depth": args.depth,
                "total_links_found": len(all_links),
                "unique_links": unique_count,
                "links": all_links,
            }
            write_json("results.json", payload)
            print("→ results.json written")


if __name__ == "__main__":
    main()
