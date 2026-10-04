#!/usr/bin/env python3
"""Check template structure and simple inline Markdown file links; stdlib only."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

REQUIRED_FILES = (
    "README.md",
    "AGENTS.md",
    "TEMPLATE_VERSION",
    "product/goals.md",
    "product/capabilities.md",
    "product/glossary.md",
    "specs/README.md",
    "architecture/overview.md",
    "architecture/decisions/README.md",
    "contracts/api/README.md",
    "contracts/schemas/README.md",
    "tests/acceptance/README.md",
    "templates/feature-spec.md",
    "templates/change-plan.md",
    "templates/adr.md",
    "docs/initialization.md",
    "docs/workflow.md",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/checks.yml",
    "scripts/check_project.py",
    "scripts/tests/test_check_project.py",
)
DOC_DIRS = ("product", "specs", "architecture", "contracts", "templates", "docs")
PLACEHOLDER = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
INLINE_LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(<[^>\n]+>|[^\s()]+)(?:\s+\"[^\"\n]*\")?\s*\)")


def prose_lines(text):
    """Ignore fenced blocks and single-line inline code in link checking."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, suffix = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence is None:
            yield number, re.sub(r"(`+).*?\1", "", line)


def local_link_errors(root, path, text):
    errors = []
    for number, line in prose_lines(text):
        for match in INLINE_LINK.finditer(line):
            href = match.group(1).strip("<>")
            if PLACEHOLDER.search(href):
                continue  # Blank templates are not actual links.
            try:
                url = urlsplit(href)
                if url.scheme or url.netloc or not url.path:
                    continue
                relative = unquote(url.path)
                # Leading '/' is interpreted as repository-root-relative.
                base = root if relative.startswith("/") else path.parent
                target = (base / relative.lstrip("/")).resolve()
                if not target.is_relative_to(root):
                    reason = "link escapes repository"
                elif not target.exists():
                    reason = "missing local link target"
                else:
                    continue
            except ValueError:
                reason = "invalid link target"
            errors.append(f"{path.relative_to(root)}:{number}: {reason}: {href}")
    return errors


def check(root, initialized=False):
    root = root.resolve()
    errors = []
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            errors.append(f"missing required file: {name}")
        elif not path.resolve().is_relative_to(root):
            errors.append(f"required file escapes repository: {name}")
        elif not path.read_text(encoding="utf-8").strip():
            errors.append(f"empty required file: {name}")

    paths = {root / "README.md", root / "AGENTS.md"}
    for name in DOC_DIRS:
        paths.update((root / name).rglob("*.md"))
    paths.update(root / name for name in REQUIRED_FILES if name.endswith(".md"))
    for path in sorted(paths):
        if not path.is_file():
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f"document escapes repository: {path.relative_to(root)}")
            continue
        text = path.read_text(encoding="utf-8")
        errors.extend(local_link_errors(root, path, text))
        relative = path.relative_to(root)
        if initialized and relative.parts[0] in {"product", "architecture", "specs"}:
            for number, line in enumerate(text.splitlines(), 1):
                if PLACEHOLDER.search(line):
                    errors.append(f"{relative}:{number}: unresolved project placeholder")

    owners = root / ".github/CODEOWNERS"
    if initialized and owners.is_file() and owners.resolve().is_relative_to(root):
        rules = [line.split() for line in owners.read_text(encoding="utf-8").splitlines()
                 if line.strip() and not line.lstrip().startswith("#")]
        if not any(len(rule) >= 2 and rule[1].startswith("@") for rule in rules):
            errors.append(".github/CODEOWNERS: add an active owner rule; verify access in GitHub")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--initialized", action="store_true",
                        help="also reject project placeholders and missing owner rules")
    args = parser.parse_args()
    try:
        errors = check(args.root, args.initialized)
    except (OSError, UnicodeError) as exc:
        print(f"FAIL: cannot read project files: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: template checks only (not business acceptance or platform permissions)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
