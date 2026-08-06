from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from csetty.docker_runtime import DockerRuntime
from csetty.errors import ValidationError
from csetty.pack import PackRepository, load_pack, snapshot_author_materials, snapshot_pack
from csetty.paths import AppPaths


def make_pack(root: Path, *, extra: str = "") -> Path:
    (root / "paper").mkdir(parents=True)
    (root / "starter").mkdir()
    (root / "paper" / "index.md").write_text("# Original paper\n", encoding="utf-8")
    (root / "starter" / "q1.c").write_text("int main(void) { return 0; }\n", encoding="utf-8")
    (root / "pack.toml").write_text(
        """
schema_version = 1
id = "test-pack"
version = "1.0.0"
title = "Test pack"
course = "COMP1511"
profile = "comp1511"
author = "Tests"
license = "CC BY-NC-ND 4.0"
paper = "paper/index.md"
reading_time_seconds = 0
working_time_seconds = 60

[environment]
image = "csetty/comp1511:dev"
network = "none"
cpus = 1
memory_mb = 256
pids = 32
output_limit_kb = 64

[[questions]]
id = "q1"
title = "Return success"
kind = "c_program"
points = 10
pass_points = 5
starter_files = ["starter/q1.c"]
submission_files = ["q1.c"]

[questions.build]
argv = ["dcc", "q1.c", "-o", "q1"]

[[questions.test_groups]]
id = "public"
visibility = "public"
points = 5

[[questions.test_groups.tests]]
id = "basic"
argv = ["./q1"]
expected_stdout = ""
expected_stderr = ""
expected_exit = 0

[[questions.test_groups]]
id = "marking"
visibility = "after_finish"
points = 5

[[questions.test_groups.tests]]
id = "hidden"
argv = ["./q1"]
expected_stdout = ""
expected_stderr = ""
expected_exit = 0
"""
        + extra,
        encoding="utf-8",
    )
    return root


def test_load_pack_and_digest(tmp_path: Path) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    assert pack.id == "test-pack"
    assert pack.total_points == 10
    assert pack.question("q1").automatic_points == 10
    assert len(pack.digest) == 64
    assert pack.starter_target("starter/q1.c").as_posix() == "q1.c"


def test_digest_ignores_reference_solutions(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "solutions").mkdir()
    solution = root / "solutions" / "answer.c"
    solution.write_text("first", encoding="utf-8")
    first = load_pack(root).digest
    solution.write_text("second", encoding="utf-8")
    assert load_pack(root).digest == first


def test_judge_pack_excludes_reference_solutions(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "solutions").mkdir()
    (root / "solutions" / "q1.c").write_text("secret", encoding="utf-8")
    pack = load_pack(root)
    destination = tmp_path / "judge-pack"
    DockerRuntime(AppPaths.discover(tmp_path / "state"))._copy_judge_pack(pack, destination)
    assert (destination / "pack.toml").is_file()
    assert not (destination / "solutions").exists()


def test_attempt_pack_snapshot_is_independent_and_excludes_solutions(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "solutions").mkdir()
    (root / "solutions" / "q1.c").write_text("secret", encoding="utf-8")
    source = load_pack(root)

    frozen = snapshot_pack(source, tmp_path / "attempt" / "pack")
    assert frozen.digest == source.digest
    assert not (frozen.root / "solutions").exists()
    assert (frozen.root / "starter" / "q1.c").stat().st_mode & 0o222 == 0

    (root / "starter" / "q1.c").write_text("changed\n", encoding="utf-8")
    assert (frozen.root / "starter" / "q1.c").read_text(encoding="utf-8") != "changed\n"
    assert load_pack(root).digest != frozen.digest


def test_author_material_snapshot_is_separate_and_stable(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "solutions" / "explanations").mkdir(parents=True)
    (root / "solutions" / "explanations" / "q1.md").write_text(
        "# Explanation\n", encoding="utf-8"
    )
    pack = load_pack(root)
    destination = tmp_path / "attempt" / "author"
    digest = snapshot_author_materials(pack, destination)
    assert len(digest) == 64
    assert (destination / "solutions" / "explanations" / "q1.md").is_file()
    assert snapshot_author_materials(pack, destination) == digest


def test_bundled_packs_have_detailed_prompts_and_author_solutions() -> None:
    repository = Path(__file__).resolve().parents[1]
    expected_counts = {"comp1511-original-a": 11, "comp1521-original-a": 10}
    for pack_name, expected_count in expected_counts.items():
        pack = load_pack(repository / "packs" / pack_name)
        assert len(pack.questions) == expected_count
        for question in pack.questions:
            prompt = pack.question_prompt(question)
            assert "## Background" in prompt
            assert "## Examples" in prompt
            assert "## Implementation notes" in prompt
            assert "## Requirements" in prompt or "## Program requirements" in prompt
            explanation = (
                pack.root / "solutions" / "explanations" / f"{question.id}.md"
            ).read_text(encoding="utf-8")
            for heading in (
                "## Approach",
                "## Correctness",
                "## Complexity",
                "## Common pitfalls",
            ):
                assert heading in explanation
            for submission_file in question.submission_files:
                assert (pack.root / "solutions" / "reference" / submission_file).is_file()


def test_pack_snapshot_materializes_safe_file_symlinks(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    (root / "paper-copy.md").symlink_to("paper/index.md")
    source = load_pack(root)
    frozen = snapshot_pack(source, tmp_path / "attempt" / "pack")
    copied = frozen.root / "paper-copy.md"
    assert copied.is_file()
    assert not copied.is_symlink()
    assert copied.read_text(encoding="utf-8") == "# Original paper\n"
    assert frozen.digest == source.digest


def test_pack_rejects_escaping_symlink(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    (root / "escape.txt").symlink_to(outside)
    with pytest.raises(ValidationError, match="symlink escapes"):
        load_pack(root)


def test_repository_deduplicates_identical_pack_copies_but_rejects_conflicts(
    tmp_path: Path,
) -> None:
    first = make_pack(tmp_path / "first")
    second = tmp_path / "second"
    shutil.copytree(first, second)
    repository = PackRepository((first, second))
    assert len(repository.list()) == 1

    (second / "starter" / "q1.c").write_text("changed\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="conflicting installed pack identity"):
        repository.list()


def test_rejects_path_traversal(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            'submission_files = ["q1.c"]', 'submission_files = ["../q1.c"]'
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="unsafe"):
        load_pack(root)


def test_rejects_points_above_question_total(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            "points = 5\n\n[[questions.test_groups.tests]]",
            "points = 8\n\n[[questions.test_groups.tests]]",
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="exceed question points"):
        load_pack(root)


def test_rejects_resource_values_outside_application_ceiling(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace("pids = 32", "pids = 10000"),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="environment.pids"):
        load_pack(root)


def test_rejects_unbounded_test_timeout(tmp_path: Path) -> None:
    root = make_pack(tmp_path / "pack")
    manifest = root / "pack.toml"
    manifest.write_text(
        manifest.read_text(encoding="utf-8").replace(
            'id = "basic"\nargv = ["./q1"]',
            'id = "basic"\nargv = ["./q1"]\ntimeout_ms = 60001',
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValidationError, match="timeout_ms"):
        load_pack(root)
