#!/usr/bin/env python3
"""Reader for the decision log (artifact/decisions.md).

An entry starts at a line beginning with "## " and runs to the next one.

Usage:
    script/decision-log.py <path-to-log> -r [N]
    script/decision-log.py <path-to-log> -l
    script/decision-log.py <path-to-log> -t WORDS
    script/decision-log.py <path-to-log> -g PATTERN
"""

import argparse
import re
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="Read decision log entries.")
    parser.add_argument("path", type=Path, help="Path to the decision log")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r",
        "--read",
        type=int,
        nargs="?",
        const=5,
        metavar="N",
        help="Print the last N entries (default: 5)",
    )
    group.add_argument("-l", "--list", action="store_true", help="List titles")
    group.add_argument(
        "-t", "--title", metavar="WORDS", help="Print entries whose title contains WORDS"
    )
    group.add_argument(
        "-g",
        "--grep",
        metavar="PATTERN",
        help="List titles of entries matching a regular expression, with hit counts",
    )
    return parser.parse_args()


def read_entries(log_path: Path):
    entries = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            entries.append([line])
        elif entries:
            entries[-1].append(line)
    return ["\n".join(lines).strip() for lines in entries]


def title(entry: str):
    return entry.splitlines()[0][3:]


def print_or_no_match(blocks, sep="\n\n"):
    print(sep.join(blocks) if blocks else "No match.")


def main():
    args = parse_args()
    entries = read_entries(args.path)
    if args.read is not None:
        print("\n\n".join(entries[-args.read :]))
    elif args.list:
        print("\n".join(title(e) for e in entries))
    elif args.title is not None:
        print_or_no_match([e for e in entries if args.title.lower() in title(e).lower()])
    else:
        pattern = re.compile(args.grep, re.IGNORECASE)
        hits = [(e, sum(bool(pattern.search(l)) for l in e.splitlines())) for e in entries]
        print_or_no_match([f"{title(e)}  ({k} hits)" for e, k in hits if k], sep="\n")


if __name__ == "__main__":
    main()
