# Proving Grounds Code Review

Cursor / Codex lane for Subtract Architect. Ideas land here as ledger rows before they become repos.

Owner is T0. Agents propose and prove. Merge, main, live money, mail, DNS, RAG ingest, bot create, and routine-save wait for an explicit owner prompt (`T0 yes` / `merge` / `lock` / `skip`).

## Commands

In Cursor: `/log-idea` (see `.cursor/commands/log-idea.md`).

In any chat: say `log-idea` plus title. Agent appends `ideas/YYYY-MM-DD_slug.md` and a row in `ideas/LEDGER.md`. Duplicate titles reuse the existing row.

## Layout

- `T0.md` — irreversible gates
- `AGENTS.md` — Cursor/agent contract
- `ideas/` — parked and unbuilt work
- `scripts/log_idea.py` — append + validate
- `scripts/report_unbuilt.py` — ideas with no matching repo

## Unbuilt report

```bash
python3 scripts/report_unbuilt.py
```

Prints ledger rows whose `repo` is empty or `none`. That list is the bot duty input. The bot reports. It does not create repos.

## 1% rule

One slice per change. Proof in the PR (script output or test). No comment-as-fix. No second OS.

<!-- SAS-IP-FOOTER-v1 -->
---
**Subtract Architect Studios™**  
Copyright © 2026 Michael F. Chaves. All rights reserved in original Subtract Architect Studios materials except as expressly licensed. See [IP_NOTICE.md](./IP_NOTICE.md). Existing open-source and third-party licenses remain controlling for materials they cover.
