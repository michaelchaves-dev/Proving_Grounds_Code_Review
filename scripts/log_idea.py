#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "ideas" / "LEDGER.md"
IDEAS = ROOT / "ideas"
STATUSES = {"parked", "logging", "sliced", "repo-exists", "killed"}
ROW = re.compile(
    r"^\| (?P<id>PG-\d+) \| (?P<date>\d{4}-\d{2}-\d{2}) \| (?P<title>[^|]+) \| (?P<status>[^|]+) \| (?P<repo>[^|]+) \| (?P<next>[^|]+) \|$"
)


def parse_rows(text: str) -> list[dict[str, str]]:
    rows = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if m:
            rows.append({k: v.strip() for k, v in m.groupdict().items()})
    return rows


def next_id(rows: list[dict[str, str]]) -> str:
    n = 0
    for r in rows:
        try:
            n = max(n, int(r["id"].split("-")[1]))
        except (IndexError, ValueError):
            continue
    return f"PG-{n + 1:03d}"


def slug(title: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:60] or "idea"


def find_title(rows: list[dict[str, str]], title: str) -> dict[str, str] | None:
    t = title.strip().lower()
    for r in rows:
        if r["title"].lower() == t:
            return r
    return None


def check(rows: list[dict[str, str]]) -> list[str]:
    errs: list[str] = []
    seen_id: set[str] = set()
    seen_title: set[str] = set()
    for r in rows:
        if r["id"] in seen_id:
            errs.append(f"dup id {r['id']}")
        seen_id.add(r["id"])
        key = r["title"].lower()
        if key in seen_title:
            errs.append(f"dup title {r['title']}")
        seen_title.add(key)
        if r["status"] not in STATUSES:
            errs.append(f"bad status {r['id']} {r['status']}")
    return errs


def append(title: str, status: str, repo: str, next_1pct: str) -> dict[str, str]:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    text = LEDGER.read_text() if LEDGER.exists() else ""
    rows = parse_rows(text)
    hit = find_title(rows, title)
    if hit:
        return hit
    pid = next_id(rows)
    today = date.today().isoformat()
    row = {
        "id": pid,
        "date": today,
        "title": title.strip(),
        "status": status,
        "repo": repo,
        "next": next_1pct,
    }
    line = f"| {pid} | {today} | {title.strip()} | {status} | {repo} | {next_1pct} |\n"
    if text and not text.endswith("\n"):
        text += "\n"
    if "| id |" not in text:
        text = (
            "# Idea ledger\n\n"
            "Status: parked | logging | sliced | repo-exists | killed\n\n"
            "| id | date | title | status | repo | next_1pct |\n"
            "|---|---|---|---|---|---|\n"
        )
    LEDGER.write_text(text + line)
    card = IDEAS / f"{today}_{slug(title)}.md"
    card.write_text(
        f"# {pid} {title.strip()}\n\n"
        f"- status: {status}\n"
        f"- repo: {repo}\n"
        f"- why: tbd\n"
        f"- next_1pct: {next_1pct}\n"
        f"- t0: no repo create from this card\n"
    )
    return row


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--title")
    p.add_argument("--status", default="parked", choices=sorted(STATUSES))
    p.add_argument("--repo", default="none")
    p.add_argument("--next", default="tbd")
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    text = LEDGER.read_text() if LEDGER.exists() else ""
    rows = parse_rows(text)
    if args.check:
        errs = check(rows)
        print(f"rows={len(rows)}")
        for e in errs:
            print("ERR", e)
        return 1 if errs else 0
    if not args.title:
        print("need --title or --check", file=sys.stderr)
        return 2
    row = append(args.title, args.status, args.repo, args.next)
    print(f"{row['id']}\t{row['title']}\t{row['status']}\t{row['repo']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
