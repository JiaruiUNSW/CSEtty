from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from csetty import cli
from csetty.errors import UsageError
from csetty.paths import AppPaths


class _Runtime:
    def __init__(self) -> None:
        self.built: list[str] = []
        self.validated: list[Path] = []

    def build_image(self, profile: str) -> str:
        self.built.append(profile)
        return f"csetty/{profile}:dev"

    def validate_mipsy_oracle_source(self, source: Path) -> str:
        self.validated.append(source)
        return "61f96b38626c30c2ead7925486304f163ec56b2b"


class _VSCode:
    def __init__(self) -> None:
        self.prepared: list[str] = []

    def prepare(self, profile: str) -> dict[str, object]:
        self.prepared.append(profile)
        return {"code": {"version": "test"}}


def _components(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[AppPaths, _Runtime, _VSCode]:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = _Runtime()
    vscode = _VSCode()
    monkeypatch.setattr(cli, "_components", lambda: (paths, object(), runtime, vscode))
    return paths, runtime, vscode


def test_prepare_comp1521_uses_local_engine_without_upstream_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _paths, runtime, vscode = _components(tmp_path, monkeypatch)

    assert cli._prepare(argparse.Namespace(profile="comp1521", mipsy_source=None)) == 0
    record = json.loads((_paths.cache / "mipsy.json").read_text(encoding="utf-8"))
    assert record == {
        "course_engine": {"bundled": True, "name": "csetty-mips", "version": "0.1.2"},
        "schema_version": 2,
        "upstream_oracle": None,
    }
    assert runtime.built == ["comp1521"]
    assert runtime.validated == []
    assert vscode.prepared == ["comp1521"]


def test_prepare_can_record_an_optional_private_oracle_without_using_it_in_image(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths, runtime, vscode = _components(tmp_path, monkeypatch)
    source = tmp_path / "upstream-oracle"
    source.mkdir()

    assert cli._prepare(argparse.Namespace(profile="comp1521", mipsy_source=source)) == 0
    record = json.loads((paths.cache / "mipsy.json").read_text(encoding="utf-8"))
    assert record["course_engine"]["name"] == "csetty-mips"
    assert record["upstream_oracle"]["used_in_course_image"] is False
    assert record["upstream_oracle"]["purpose"] == "private-black-box-comparison-only"
    assert runtime.validated == [source.resolve()]
    assert runtime.built == ["comp1521"]
    assert vscode.prepared == ["comp1521"]


def test_prepare_rejects_an_oracle_source_for_comp1511_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _components(tmp_path, monkeypatch)
    with pytest.raises(UsageError, match="only valid when preparing COMP1521"):
        cli._prepare(argparse.Namespace(profile="comp1511", mipsy_source=tmp_path))
