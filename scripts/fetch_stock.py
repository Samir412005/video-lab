#!/usr/bin/env python3
"""Fetch free stock images / audio from Openverse — no API key needed.

Openverse (api.openverse.org) aggregates 800M+ openly licensed works
(Flickr, Wikimedia, ...). This script filters to CC0 / public-domain works
by default so the files can be used freely in videos with no attribution.

Usage:
  python3 fetch_stock.py --query "man portrait" --kind image --count 5
  python3 fetch_stock.py --query "rain ambience" --kind audio --count 3 --out assets/stock

Output: files in <out>/ + manifest.json with title / license / source URL
for every downloaded file.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request

API_BASE = "https://api.openverse.org/v1"


def search(query, kind, license_filter, count):
    endpoint = "images" if kind == "image" else "audio"
    params = {
        "q": query,
        "license": license_filter,
        "page_size": max(1, min(count, 50)),
        "fields": "title,url,license,foreign_landing_url",
    }
    url = f"{API_BASE}/{endpoint}/?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "video-lab/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.load(resp).get("results", [])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--query", required=True, help="search words")
    p.add_argument("--kind", choices=["image", "audio"], default="image")
    p.add_argument("--license", default="cc0",
                   help="license filter, e.g. cc0 or cc0,pdm (default: cc0)")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--out", default="assets/stock")
    args = p.parse_args()

    os.makedirs(args.out, exist_ok=True)
    results = search(args.query, args.kind, args.license, args.count)
    if not results:
        print(f"No results for {args.query!r} ({args.kind}, license={args.license})")
        return 1

    manifest = []
    for i, r in enumerate(results, 1):
        url = r.get("url") or ""
        if not url:
            continue
        ext = os.path.splitext(urllib.parse.urlparse(url).path)[1] or (
            ".jpg" if args.kind == "image" else ".mp3")
        ext = ext.split("?")[0][:6]
        name = f"{i:02d}{ext}"
        path = os.path.join(args.out, name)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "video-lab/1.0"})
            with urllib.request.urlopen(req, timeout=120) as resp, open(path, "wb") as f:
                f.write(resp.read())
            size = os.path.getsize(path)
            print(f"[{i}] {name} ({size} bytes) license={r.get('license')} :: "
                  f"{(r.get('title') or '')[:60]}")
            manifest.append({
                "file": name, "title": r.get("title"), "license": r.get("license"),
                "source_url": url, "landing": r.get("foreign_landing_url"),
            })
        except Exception as e:  # noqa: BLE001 - report and continue with the next file
            print(f"[{i}] FAILED {url[:80]}: {e}", file=sys.stderr)

    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(manifest)} file(s) to {args.out}/ + manifest.json")
    return 0 if manifest else 1


if __name__ == "__main__":
    raise SystemExit(main())
