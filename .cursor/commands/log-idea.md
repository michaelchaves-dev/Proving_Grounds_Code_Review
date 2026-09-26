# /log-idea

Log a conceived project so it is not forgotten.

## Do

1. Take the title from the user. One line.
2. If `ideas/LEDGER.md` already has that title (case-insensitive), reuse the row. Do not duplicate.
3. Else run:

```bash
python3 scripts/log_idea.py --title "TITLE" --status parked --repo none
```

4. Fill `why` and `next_1pct` only if the user named them. Otherwise leave `tbd`.
5. Show the new or reused row. Stop.
6. Do not create a GitHub repo. Do not create a bot. Do not merge.

## Status enum

`parked` | `logging` | `sliced` | `repo-exists` | `killed`
