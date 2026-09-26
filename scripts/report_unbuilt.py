#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from log_idea import LEDGER, parse_rows

UNBUILT = {"none", "", "tbd", "-"}


def main() -> int:
    if not LEDGER.exists():
        print("no ledger")
        return 1
    rows = parse_rows(LEDGER.read_text())
    open_rows = [
        r
        for r in rows
        if r["status"] in {"parked", "logging"} and r["repo"].lower() in UNBUILT
    ]
    print(f"unbuilt={len(open_rows)} ledger={len(rows)}")
    for r in open_rows:
        print(f"{r['id']}\t{r['title']}\t{r['status']}\tnext={r['next']}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
