#!/usr/bin/env python3
"""Drift guard: keep the copied rule region in rules-zh.md identical to docs/rules.md.

`docs/rules.md` is the single source of truth. `skills/sha-plain-docs/references/rules-zh.md`
copies it verbatim between two markers so the skill stays self-contained after install. This
script fails when the two diverge (design D6 / task 8.1).

Usage:
    python3 scripts/check_rules_drift.py [--json]

Exit codes:
    0 = in sync, 1 = drift detected, 2 = usage/environment error.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

BEGIN = "<!-- BEGIN COPY OF docs/rules.md -->"
END = "<!-- END COPY OF docs/rules.md -->"
SOURCE_REL = Path("docs/rules.md")
COPY_REL = Path("skills/sha-plain-docs/references/rules-zh.md")


def comparable_lines(text: str) -> list[str]:
    lines = [line.rstrip() for line in text.replace("\r\n", "\n").split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return lines


def extract_copy_region(provider_text: str) -> list[str] | None:
    if BEGIN not in provider_text or END not in provider_text:
        return None
    region = provider_text.split(BEGIN, 1)[1].split(END, 1)[0]
    return comparable_lines(region)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check docs/rules.md ↔ rules-zh.md copy drift.")
    parser.add_argument("--json", action="store_true", help="emit a JSON report on stdout")
    parser.add_argument("--root", default=None, help="repo root (default: parent of this script's dir)")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parent.parent
    source_path = root / SOURCE_REL
    copy_path = root / COPY_REL

    for path in (source_path, copy_path):
        if not path.is_file():
            message = f"missing file: {path}"
            print(json.dumps({"error": message}) if args.json else f"ERROR: {message}", file=sys.stderr)
            return 2

    source_lines = comparable_lines(source_path.read_text(encoding="utf-8"))
    region = extract_copy_region(copy_path.read_text(encoding="utf-8"))
    if region is None:
        message = f"{COPY_REL} is missing the {BEGIN} / {END} markers"
        print(json.dumps({"error": message}) if args.json else f"ERROR: {message}", file=sys.stderr)
        return 2

    if source_lines == region:
        if args.json:
            print(json.dumps({"status": "in_sync", "source": str(SOURCE_REL), "copy": str(COPY_REL)}))
        else:
            print(f"in sync: {SOURCE_REL} == copy region of {COPY_REL} ({len(source_lines)} lines)")
        return 0

    diff = list(
        difflib.unified_diff(
            source_lines, region, fromfile=str(SOURCE_REL), tofile=f"{COPY_REL} (copy region)", lineterm=""
        )
    )
    if args.json:
        print(
            json.dumps(
                {
                    "status": "drift",
                    "source": str(SOURCE_REL),
                    "copy": str(COPY_REL),
                    "source_lines": len(source_lines),
                    "copy_lines": len(region),
                    "diff": diff,
                },
                ensure_ascii=False,
            )
        )
    else:
        print(f"DRIFT: {SOURCE_REL} and the copy region of {COPY_REL} differ.")
        print(f"Fix: re-copy {SOURCE_REL} into the region between the BEGIN/END markers.")
        print("\n".join(diff))
    return 1


if __name__ == "__main__":
    sys.exit(main())
