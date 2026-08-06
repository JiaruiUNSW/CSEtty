from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from setuptools import setup

ROOT = Path(__file__).resolve().parent


def runtime_data_files() -> list[tuple[str, list[str]]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    for filename in (
        "compose.yaml",
        "toolchains.lock",
        "checksums.lock",
        "THIRD_PARTY_NOTICES.md",
        "LICENSE",
        "NOTICE",
        "LICENSES.md",
        "ASSESSMENT_MATERIALS_LICENSE.md",
        "TRADEMARKS.md",
    ):
        grouped["share/csetty"].append(filename)
    for source_name in ("docker", "packs", "question_bank"):
        source_root = ROOT / source_name
        for source in sorted(source_root.rglob("*")):
            if not source.is_file() or source.is_symlink():
                continue
            relative_directory = source.parent.relative_to(source_root)
            destination = (Path("share/csetty") / source_name / relative_directory).as_posix()
            grouped[destination].append(source.relative_to(ROOT).as_posix())
    return [(destination, files) for destination, files in sorted(grouped.items())]


setup(data_files=runtime_data_files())
