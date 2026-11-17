"""Fetch National Bank of Kazakhstan monthly 'Electronic banking services / payment cards' releases.

Saves raw HTML to data/raw/nbk/ and an index CSV (release id, version, publish date, url)
to data/raw/nbk/_index.csv. Re-running skips files already on disk.
"""
from __future__ import annotations

import csv
import re
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "nbk"
BASE = "https://www.nationalbank.kz"
INDEX = BASE + "/{lang}/news/elektronnye-bankovskie-uslugi"
HEADERS = {"User-Agent": "Mozilla/5.0 (research script; payments market analysis)"}


def get(url: str) -> str:
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, timeout=60)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:  # noqa: PERF203
            print(f"  retry {attempt + 1} {url}: {e}")
            time.sleep(3)
    raise RuntimeError(f"failed: {url}")


def list_releases(lang: str = "en", pages: int = 3) -> list[dict]:
    rows, seen = [], set()
    for p in range(1, pages + 1):
        url = INDEX.format(lang=lang) + (f"?page={p}" if p > 1 else "")
        html = get(url)
        (RAW / f"_index_{lang}_p{p}.html").write_text(html, encoding="utf-8")
        soup = BeautifulSoup(html, "lxml")
        for a in soup.find_all("a", href=re.compile(r"elektronnye-bankovskie-uslugi/\d+$")):
            href = a["href"]
            rid = href.rsplit("/", 1)[-1]
            if rid in seen:
                continue
            seen.add(rid)
            label = a.find_parent().find_parent().get_text(" ", strip=True)
            m = re.search(r"(\d{2}/\d{2}/\d{4})", label)
            v = re.search(r"(\d{3})\s*от", label.replace("¹", " "))
            rows.append({
                "release_id": rid,
                "version": v.group(1) if v else "",
                "published": m.group(1) if m else "",
                "url": BASE + href if href.startswith("/") else href,
            })
        time.sleep(1)
    return rows


def main() -> None:
    RAW.mkdir(parents=True, exist_ok=True)
    rows = list_releases("en", pages=3)
    with open(RAW / "_index.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} releases listed")
    for r in rows:
        out = RAW / f"release_{r['release_id']}.html"
        if out.exists():
            continue
        print("fetch", r["url"])
        out.write_text(get(r["url"]), encoding="utf-8")
        time.sleep(1)


if __name__ == "__main__":
    main()
