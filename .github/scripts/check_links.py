#!/usr/bin/env python3
"""Check relative links and heading anchors in Markdown files.

Runs locally (`python3 .github/scripts/check_links.py`) and in CI. Exits 1 on
the first file with a problem so the log points at something actionable.

Rules kept deliberately strict:
  - a relative path must exist in the repository
  - a `#anchor` must match a heading in the target file, using GitHub's slug
    rules (lowercase, punctuation dropped, spaces to hyphens, duplicates get
    -1, -2, ...)
  - absolute URLs, mailto and bare anchors are not validated (see the note in
    docs/README.md about recording planned files as code, not links)
"""

from __future__ import annotations

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKIP_DIRS = {".git", "node_modules", ".terraform", ".next", "dist", "coverage", "tmp"}
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def walk_markdown() -> list[str]:
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if name.endswith(".md"):
                found.append(os.path.join(dirpath, name))
    return sorted(found)


def slugify(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"`", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"\s", "-", text)
    return text


def anchors_for(path: str) -> set[str]:
    anchors: set[str] = set()
    seen: dict[str, int] = {}
    with open(path, encoding="utf-8") as handle:
        in_fence = False
        for line in handle:
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            match = HEADING_RE.match(line)
            if not match:
                continue
            slug = slugify(match.group(2))
            if slug in seen:
                seen[slug] += 1
                anchors.add(f"{slug}-{seen[slug]}")
            else:
                seen[slug] = 0
                anchors.add(slug)
    return anchors


def main() -> int:
    problems: list[str] = []
    cache: dict[str, set[str]] = {}

    for doc in walk_markdown():
        rel_doc = os.path.relpath(doc, ROOT)
        with open(doc, encoding="utf-8") as handle:
            text = handle.read()

        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                continue

            path_part, _, anchor = target.partition("#")
            if path_part:
                resolved = os.path.normpath(os.path.join(os.path.dirname(doc), path_part))
            else:
                resolved = doc

            if not os.path.exists(resolved):
                problems.append(f"{rel_doc}: missing path -> {target}")
                continue

            if anchor and resolved.endswith(".md"):
                if resolved not in cache:
                    cache[resolved] = anchors_for(resolved)
                if anchor not in cache[resolved]:
                    problems.append(f"{rel_doc}: missing anchor -> {target}")

    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(f"  {problem}")
        return 1

    print(f"OK — {len(walk_markdown())} Markdown files, all relative links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
