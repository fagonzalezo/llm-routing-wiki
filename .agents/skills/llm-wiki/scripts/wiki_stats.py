#!/usr/bin/env python3
"""
wiki_stats.py — Quick summary of wiki size, shape, and link density.

Useful for deciding when to shard the index or split pages.

Usage:
    python3 wiki_stats.py [<wiki-dir>]

Example:
    python3 wiki_stats.py wiki/
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


SKIP_TOP_LEVEL_FILES = {"SCHEMA.md", "log.md", "README.md"}
SKIP_TOP_LEVEL_DIRS = {"indexes", "graph"}

# Frontmatter list fields whose values are bare slug references to other pages.
# Counted toward the hub tally alongside body [[wikilinks]] (see page-conventions.md).
FRONTMATTER_REF_FIELDS = ("sources", "entities", "concepts")


def parse_type(text: str) -> str | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    fm = m.group(1)
    for line in fm.split("\n"):
        kv = re.match(r"^type:\s*(.*)$", line)
        if kv:
            return kv.group(1).strip().strip('"').strip("'")
    return None


def parse_frontmatter_refs(text: str) -> list[str]:
    """Flatten slug references from frontmatter ref fields (inline or block lists)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []
    refs = []
    current = None
    for line in m.group(1).split("\n"):
        if not line.strip():
            continue
        kv = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            current = None
            if key not in FRONTMATTER_REF_FIELDS:
                continue
            if value.startswith("[") and value.endswith("]"):
                refs.extend(x.strip().strip('"').strip("'") for x in value[1:-1].split(",") if x.strip())
            elif value:
                refs.append(value.strip('"').strip("'"))
            else:
                current = key
        elif line.startswith("  - ") and current:
            item = line[4:].strip().strip('"').strip("'")
            if item:
                refs.append(item)
    return refs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("wiki", nargs="?", type=Path, default=Path("wiki"))
    args = parser.parse_args()

    if not args.wiki.exists():
        print(f"Wiki directory not found: {args.wiki}", file=sys.stderr)
        sys.exit(1)

    total_pages = 0
    total_lines = 0
    total_words = 0
    total_links = 0
    pages_by_type = Counter()
    pages_by_dir = Counter()
    largest = []
    most_linked_in = Counter()
    index_lines = 0

    for md_path in args.wiki.rglob("*.md"):
        rel = md_path.relative_to(args.wiki)
        try:
            text = md_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if rel.name == "index.md" and len(rel.parts) == 1:
            index_lines = text.count("\n") + 1
            continue
        if rel.parts[0] in SKIP_TOP_LEVEL_FILES:
            continue
        if rel.parts[0] in SKIP_TOP_LEVEL_DIRS:
            continue
        if rel.name.startswith("."):
            continue

        total_pages += 1
        line_count = text.count("\n") + 1
        word_count = len(text.split())
        total_lines += line_count
        total_words += word_count
        # Strip frontmatter before counting wikilinks; frontmatter uses bare slugs.
        body = FRONTMATTER_RE.sub("", text, count=1) if text.startswith("---") else text
        links = WIKILINK_RE.findall(body)
        total_links += len(links)
        for link in links:
            target = link.split("|")[0].strip()
            most_linked_in[target] += 1
        # Frontmatter sources/entities/concepts count toward the hub tally too,
        # so source pages (cited via frontmatter, not body links) surface as hubs.
        for ref in parse_frontmatter_refs(text):
            most_linked_in[ref] += 1
        page_type = parse_type(text) or "(none)"
        pages_by_type[page_type] += 1
        if len(rel.parts) > 1:
            pages_by_dir[rel.parts[0]] += 1
        else:
            pages_by_dir["(root)"] += 1
        largest.append((line_count, str(rel)))

    largest.sort(reverse=True)

    print("=" * 60)
    print(f"Wiki Stats: {args.wiki}")
    print("=" * 60)
    print(f"Pages:         {total_pages}")
    print(f"Total lines:   {total_lines:,}")
    print(f"Total words:   {total_words:,}")
    print(f"Total links:   {total_links:,}")
    if total_pages:
        print(f"Avg page:      {total_lines // total_pages} lines / {total_words // total_pages} words")
        print(f"Link density:  {total_links / total_pages:.1f} links per page")
    print(f"index.md:      {index_lines} lines" + ("  ← shard recommended (>300)" if index_lines > 300 else ""))
    print()

    print("Pages by type:")
    for t, n in pages_by_type.most_common():
        print(f"  {t:15s} {n}")
    print()

    print("Pages by directory:")
    for d, n in pages_by_dir.most_common():
        print(f"  {d:15s} {n}")
    print()

    if largest:
        print("Largest pages:")
        for lines, path in largest[:10]:
            warn = ""
            if lines > 800:
                warn = "  ← OVER HARD CAP"
            elif lines > 400:
                warn = "  ← over soft cap"
            print(f"  {lines:5d}  {path}{warn}")
        print()

    if most_linked_in:
        print("Most-linked-to pages (hubs):")
        for slug, count in most_linked_in.most_common(10):
            print(f"  {count:4d}  [[{slug}]]")
        print()

    # Scaling recommendations
    print("Scaling thresholds:")
    if total_pages < 50:
        print("  → Below first threshold. Flat structure is fine.")
    elif total_pages < 150 and index_lines < 300:
        print("  → Below shard threshold. Continue with single index.md.")
    elif (total_pages >= 150 or index_lines >= 300) and not (args.wiki / "indexes").exists():
        print("  → AT SHARD THRESHOLD. Consider sharding index.md into wiki/indexes/<type>.md.")
        print("    See references/scaling-playbook.md.")
    elif total_pages >= 300:
        print("  → Past 300 pages. Use scripts/wiki_search.py as a routine fallback.")
    if total_pages >= 500:
        print("  → Past 500 pages. Run lint weekly or per-N-ingests.")


if __name__ == "__main__":
    main()
