#!/usr/bin/env python3
"""Remove authoring boilerplate and clarify the original 150 bank prompts.

The expansion catalogue has its own generator.  This script handles the older
COMP1511 core/advanced and COMP1521 low-level/files/concurrency questions whose
committed prompts pre-date the student-facing writing standard.
"""

from __future__ import annotations

import json
import re
import shlex
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUESTION_ROOT = ROOT / "question_bank"
LEGACY_GLOBS = (
    "comp1511/questions/c1511-core-*/prompt.md",
    "comp1511/questions/c1511-adv-*/prompt.md",
    "comp1521/questions/c1521-low-*/prompt.md",
    "comp1521/questions/c1521-fs-*/prompt.md",
    "comp1521/questions/c1521-conc-*/prompt.md",
)

REMOVALS = (
    "This is an original C programming task for the local CSEExamTTY simulator.\n\n",
    "This original exercise practises a small, precisely specified linked-list "
    "transformation or analysis. ",
    "This original exercise focuses on safe pointer-based processing of "
    "dynamically allocated arrays. ",
    "This original short exercise isolates one core C skill behind a complete "
    "command-line harness. ",
    "This original medium exercise combines several C concepts in one self-contained "
    "linked or dynamically allocated data task. ",
    "This is an original whole-program exercise. ",
    " Inputs are supplied as documented so the target behaviour can be reproduced directly.",
    " The supplied harness constructs all input state and retains the ownership "
    "rules described below.",
    " Build commands are argument arrays and do not invoke a shell.",
    " Your submitted file must compile cleanly with `dcc -Werror`.",
    " Build and submit the unique source file using the shell-free `dcc -Werror` "
    "command supplied by the pack.",
    " The build uses the shell-free argument array `dcc -Werror <file> -o <program>`.",
    ", compiled using the supplied shell-free `dcc -Werror` argument array",
    ", and compile the unique submission file with `dcc -Werror`",
    " rather than printing sample-specific answers",
    "\n\nDo not special-case the shown values or embed a table of test answers. Your\n"
    "algorithm must work for every value permitted by the constraints.",
    "\n\nThe public examples illustrate the interface only; marking also uses distinct\n"
    "boundary and mixed-value cases.",
)

REPLACEMENTS = (
    ("The supplied command-line harness", "The supplied `main`"),
    ("the supplied command-line harness", "the supplied `main`"),
    ("The supplied harness", "The supplied `main`"),
    ("the supplied harness", "the supplied `main`"),
    ("The harness", "The supplied `main`"),
    ("the harness", "the supplied `main`"),
    ("starter harness", "starter program"),
    ("harness code", "starter code"),
    ("provided harness", "provided starter program"),
)

LOW_PROVENANCE = re.compile(
    r"\n\nThis is an original local practice task\. It exercises the `[^`]+`\n"
    r"part of COMP1521 without relying on any UNSW assessment text\."
)

OUTPUT_RULES = {
    "c1521-conc-006": (
        "Print one line per worker as `worker I lines=L bytes=B words=W`, then print "
        "`total lines=L bytes=B words=W`."
    ),
    "c1521-conc-015": "Print each task as `INDEX value=V square=S cube=C`.",
    "c1521-conc-017": (
        "Print each result as `INDEX square=S`, then print the final line `total=T`."
    ),
    "c1521-conc-020": (
        "Print exactly one line as `count=N even=E even_sum=ES odd=O odd_sum=OS min=MIN max=MAX`."
    ),
}

MANIFEST_EXAMPLE_PREFIXES = ("c1511-adv-", "c1521-fs-", "c1521-conc-")


def _as_bullets(section: str) -> str:
    stripped = section.strip()
    if stripped.startswith("- "):
        return stripped
    flat = " ".join(line.strip() for line in stripped.splitlines())
    sentences = re.split(r"(?<=[.!?])\s+(?=(?:[A-Z`]|\*))", flat)
    return "\n".join(f"- {sentence.strip()}" for sentence in sentences if sentence.strip())


def _replace_section(text: str, heading: str, following: str, body: str) -> str:
    pattern = re.compile(
        rf"({re.escape(heading)}\n\n).*?(\n\n{re.escape(following)})",
        re.DOTALL,
    )
    updated, count = pattern.subn(
        lambda match: f"{match.group(1)}{body.rstrip()}{match.group(2)}",
        text,
        count=1,
    )
    if count != 1:
        raise ValueError(f"could not find {heading} before {following}")
    return updated


def _code_block(label: str, content: str) -> str:
    rendered = content.rstrip("\n")
    return f"{label}:\n\n```text\n{rendered}\n```"


def _fixture_description(question_root: Path, fixture: dict[str, Any]) -> str:
    target = fixture["path"]
    content = (question_root / fixture["source"]).read_bytes()
    if not content:
        return f"- `{target}` is empty."
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        decoded = ""
    if decoded and all(character.isprintable() or character in "\n\r\t" for character in decoded):
        indented = "\n".join(f"  {line}" for line in decoded.rstrip("\n").split("\n"))
        return f"- `{target}` ({len(content)} bytes) contains:\n\n  ```text\n{indented}\n  ```"
    return f"- `{target}` contains `{content.hex()}` (hexadecimal bytes)."


def _manifest_example(path: Path) -> str:
    question_root = path.parent
    raw = json.loads((question_root / "question.json").read_text(encoding="utf-8"))
    public = next(group for group in raw["test_groups"] if group["visibility"] == "public")
    test = public["tests"][0]
    sections = [_code_block("Command", shlex.join(test["argv"]))]
    fixtures = test.get("fixtures", [])
    if fixtures:
        descriptions = "\n".join(
            _fixture_description(question_root, fixture) for fixture in fixtures
        )
        sections.append(f"Files provided for this example:\n\n{descriptions}")
    if test.get("stdin"):
        sections.append(_code_block("Input", test["stdin"]))
    stdout = test.get("expected_stdout")
    if stdout:
        sections.append(_code_block("Output", stdout))
    else:
        sections.append("Output: no text is written to standard output.")
    stderr = test.get("expected_stderr")
    if stderr:
        sections.append(_code_block("Standard error", stderr))
    expected_exit = test.get("expected_exit", 0)
    if expected_exit != 0:
        sections.append(f"Exit status: `{expected_exit}`")
    return "\n\n".join(sections)


def _polish(path: Path) -> bool:
    question_id = path.parent.name
    text = path.read_text(encoding="utf-8")
    updated = LOW_PROVENANCE.sub("", text)
    for phrase in REMOVALS:
        updated = updated.replace(phrase, "")
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)

    if question_id.startswith(("c1521-fs-", "c1521-conc-")):
        match = re.search(r"## Requirements\n\n(.*?)\n\n## Examples", updated, re.DOTALL)
        if match is None:
            raise ValueError(f"missing Requirements section in {path}")
        requirements = match.group(1).strip()
        output_rule = OUTPUT_RULES.get(question_id)
        if output_rule and output_rule not in requirements:
            requirements = f"{requirements} {output_rule}"
        updated = _replace_section(
            updated,
            "## Requirements",
            "## Examples",
            _as_bullets(requirements),
        )

    if question_id.startswith(MANIFEST_EXAMPLE_PREFIXES):
        example = _manifest_example(path)
        updated = _replace_section(updated, "## Examples", "## Implementation notes", example)

    updated = re.sub(r"\n{3,}", "\n\n", updated).rstrip() + "\n"
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    paths = sorted(path for pattern in LEGACY_GLOBS for path in QUESTION_ROOT.glob(pattern))
    if len(paths) != 150:
        raise RuntimeError(f"expected 150 legacy prompts, found {len(paths)}")
    changed = sum(_polish(path) for path in paths)
    print(f"polished {changed} of {len(paths)} legacy prompts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
