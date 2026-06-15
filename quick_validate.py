#!/usr/bin/env python3
"""Basic validation for this Codex skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ALLOWED_FIELDS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
TRIGGER_WORDS = ("use when", "trigger", "use this skill")
PURPOSE_WORDS = ("interpret", "interpretation", "reading", "synthesize", "synthesis")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    if not lines or lines[0] != "---":
        fail("SKILL.md must start with YAML frontmatter delimited by ---")

    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail("SKILL.md frontmatter must end with ---")

    metadata: dict[str, str] = {}
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"frontmatter line {line_number} must be a key: value pair")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            fail(f"frontmatter line {line_number} has an empty key")
        if key in metadata:
            fail(f"frontmatter field {key!r} is duplicated")
        metadata[key] = value

    return metadata


def validate_metadata(metadata: dict[str, str]) -> None:
    fields = set(metadata)
    extra_fields = fields - ALLOWED_FIELDS
    missing_fields = ALLOWED_FIELDS - fields

    if extra_fields:
        fail(f"frontmatter contains unsupported fields: {', '.join(sorted(extra_fields))}")
    if missing_fields:
        fail(f"frontmatter is missing required fields: {', '.join(sorted(missing_fields))}")

    name = metadata["name"]
    if not NAME_RE.fullmatch(name):
        fail("skill name must use lowercase hyphen-case")

    description = metadata["description"]
    if len(description) < 80:
        fail("description must clearly describe the skill and when it should trigger")

    normalized_description = description.lower()
    if not any(word in normalized_description for word in PURPOSE_WORDS):
        fail("description must state what the skill does")
    if not any(word in normalized_description for word in TRIGGER_WORDS):
        fail("description must state when the skill should trigger")


def main() -> None:
    skill_path = Path(__file__).with_name("SKILL.md")
    if not skill_path.exists():
        fail("SKILL.md not found")

    metadata = parse_frontmatter(skill_path)
    validate_metadata(metadata)
    print("PASS: SKILL.md metadata is valid")


if __name__ == "__main__":
    main()
