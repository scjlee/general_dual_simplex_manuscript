#!/usr/bin/env python3
"""Turn a self-contained R Markdown HTML report into text an agent can read.

Figures are downscaled by default to save vision tokens.

    <out>/report.md          headings, prose, printed output, tables, figure links
    <out>/fig/NN_<sec>.png   embedded figures, numbered in document order
"""

import argparse
import base64
import html.parser
import io
import os
import re
import shutil
import struct
from pathlib import Path

from PIL import Image

VOID = {"img", "br", "hr", "meta", "link", "input", "col", "source", "wbr"}
BLOCKS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower())[:40].strip("-") or "top"


class Report(html.parser.HTMLParser):
    def __init__(self, out, with_source, fig_scale):
        super().__init__(convert_charrefs=True)
        self.out, self.with_source, self.fig_scale = out, with_source, fig_scale
        self.stack, self.skip_at = [], None
        self.block, self.buf, self.pre_class = None, [], ""
        self.table, self.row = None, None
        self.lists = []  # open <ul>/<ol>: [next number or None, indent, width of last marker]
        self.lines, self.figs, self.section = [], [], "top"

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if self.skip_at is not None:
            return
        if tag in ("script", "style", "head") or a.get("id") == "TOC":
            self.skip_at = len(self.stack)
        elif tag == "img" and (a.get("src") or "").startswith("data:image/png;base64,"):
            self.save_figure(a)
        elif tag == "table":
            self.table = []
        elif tag == "tr" and self.table is not None:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.buf = []
        elif tag in ("ul", "ol"):
            self.open_list(tag, a)
        elif tag in BLOCKS and self.block is None:
            self.block, self.buf, self.pre_class = tag, [], a.get("class") or ""

    def handle_endtag(self, tag):
        if tag in VOID or tag not in self.stack:
            return
        while self.stack and self.stack.pop() != tag:
            pass
        if self.skip_at is not None:
            if len(self.stack) < self.skip_at:
                self.skip_at = None
            return
        text = "".join(self.buf)
        if tag in ("td", "th") and self.row is not None:
            self.row.append(" ".join(text.split()))
        elif tag == "tr" and self.table is not None and self.row is not None:
            self.table.append(self.row)
            self.row = None
        elif tag == "table" and self.table is not None:
            self.emit_table()
        elif tag in ("ul", "ol") and self.lists:
            self.lists.pop()
            if not self.lists:
                self.lines.append("")
        elif tag == self.block:
            self.emit_block(tag, text)
            self.block = None

    def handle_data(self, data):
        if self.skip_at is None:
            self.buf.append(data)

    def emit_block(self, tag, text):
        if tag == "pre":
            if "r" in self.pre_class.split() and not self.with_source:
                return
            self.lines += ["```", text.rstrip("\n"), "```", ""]
            return
        text = " ".join(text.split())
        if not text:
            return
        if tag[0] == "h":
            self.section = slug(text)
            self.lines += ["#" * int(tag[1]) + " " + text, ""]
        elif tag == "li":
            lst = self.lists[-1] if self.lists else [None, "", 2]
            marker = "-" if lst[0] is None else f"{lst[0]}."
            if lst[0] is not None:
                lst[0] += 1
            lst[2] = len(marker) + 1
            self.lines.append(f"{lst[1]}{marker} {text}")
        else:
            self.lines += [text, ""]

    def open_list(self, tag, a):
        if self.block == "li":  # the parent item's own text comes before its sublist
            self.emit_block("li", "".join(self.buf))
            self.block = None
        parent = self.lists[-1] if self.lists else None
        indent = parent[1] + " " * parent[2] if parent else ""
        self.lists.append([int(a.get("start") or 1) if tag == "ol" else None, indent, 2])

    def emit_table(self):
        rows, self.table = self.table, None
        if not rows:
            return
        width = max(map(len, rows))
        rows = [r + [""] * (width - len(r)) for r in rows]
        self.lines += ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * width]
        self.lines += ["| " + " | ".join(r) + " |" for r in rows[1:]] + [""]

    def save_figure(self, a):
        raw = base64.b64decode(a["src"].split(",", 1)[1])
        w, h = struct.unpack(">II", raw[16:24])
        w, h = round(w * self.fig_scale), round(h * self.fig_scale)
        n = len(self.figs) + 1
        name = f"fig/{n:02d}_{self.section}.png"
        path = self.out / name
        if self.fig_scale == 1:
            path.write_bytes(raw)
        else:
            with Image.open(io.BytesIO(raw)) as im:
                im.resize((w, h), Image.LANCZOS).save(path)
        alt = a.get("alt") or ""
        self.figs.append((n, self.section, alt, w, h, name))
        self.lines += [f"![fig {n:02d} | {self.section} {alt}".rstrip() + f"]({name})", ""]

    def markdown(self, src):
        index = ["## Figure index", "", "| # | section | alt | size | file |", "|---|---|---|---|---|"]
        index += [f"| {n:02d} | {s} | {alt} | {w}x{h} | {f} |" for n, s, alt, w, h, f in self.figs]
        return "\n".join([f"<!-- extracted from {src} -->", ""] + self.lines + index) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html", type=Path, help="self-contained HTML report")
    parser.add_argument("-o", "--out", type=Path,
                        help="output directory (default: $TMPDIR/extract-report/<stem>)")
    parser.add_argument("--fig-scale", type=float, default=0.3,
                        help="scale factor for embedded figures (default: 0.3; 1 writes original bytes)")
    parser.add_argument("--with-source", action="store_true",
                        help="include R source chunks (omitted by default; read the Rmd)")
    args = parser.parse_args()

    out = args.out or Path(os.environ.get("TMPDIR", "/tmp")) / "extract-report" / args.html.stem
    shutil.rmtree(out / "fig", ignore_errors=True)
    (out / "fig").mkdir(parents=True)

    report = Report(out, args.with_source, args.fig_scale)
    report.feed(args.html.read_text(encoding="utf-8"))
    (out / "report.md").write_text(report.markdown(args.html))
    print(f"{out / 'report.md'}  ({len(report.figs)} figures)")


if __name__ == "__main__":
    main()
