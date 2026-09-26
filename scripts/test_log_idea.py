#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import log_idea

SAMPLE = """# Idea ledger

| id | date | title | status | repo | next_1pct |
|---|---|---|---|---|---|
| PG-001 | 2026-09-26 | Alpha | parked | none | tbd |
| PG-002 | 2026-09-26 | Beta | sliced | SomeRepo | gate |
"""


class LogIdeaTests(unittest.TestCase):
    def test_parse_and_next(self) -> None:
        rows = log_idea.parse_rows(SAMPLE)
        self.assertEqual(len(rows), 2)
        self.assertEqual(log_idea.next_id(rows), "PG-003")

    def test_check_ok(self) -> None:
        self.assertEqual(log_idea.check(log_idea.parse_rows(SAMPLE)), [])

    def test_check_dup(self) -> None:
        bad = SAMPLE + "| PG-001 | 2026-09-26 | Alpha | parked | none | tbd |\n"
        errs = log_idea.check(log_idea.parse_rows(bad))
        self.assertTrue(any("dup" in e for e in errs))

    def test_reuse_title(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ideas = root / "ideas"
            ideas.mkdir()
            ledger = ideas / "LEDGER.md"
            ledger.write_text(SAMPLE)
            with mock.patch.object(log_idea, "ROOT", root), mock.patch.object(
                log_idea, "LEDGER", ledger
            ), mock.patch.object(log_idea, "IDEAS", ideas):
                row = log_idea.append("Alpha", "parked", "none", "tbd")
                self.assertEqual(row["id"], "PG-001")
                self.assertEqual(len(log_idea.parse_rows(ledger.read_text())), 2)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
