from __future__ import annotations

import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "publish-pypi.yml"


def _load_script(name: str) -> ModuleType:
    spec = spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load script module {name}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release_gate = _load_script("release_gate")
write_checksums_module = _load_script("write_checksums")
_TRUSTED_PUBLISH_ACTION = release_gate._TRUSTED_PUBLISH_ACTION
_verify_private_workflows = release_gate._verify_private_workflows
write_checksums = write_checksums_module.main


def _workflow_root(tmp_path: Path, text: str | None = None) -> Path:
    workflows = tmp_path / ".github" / "workflows"
    workflows.mkdir(parents=True)
    (workflows / "publish-pypi.yml").write_text(
        WORKFLOW.read_text(encoding="utf-8") if text is None else text,
        encoding="utf-8",
    )
    return tmp_path


def test_trusted_publish_workflow_is_the_only_allowed_package_publisher(
    tmp_path: Path,
) -> None:
    project_root = _workflow_root(tmp_path)
    _verify_private_workflows(project_root)

    untrusted = project_root / ".github" / "workflows" / "untrusted.yml"
    untrusted.write_text(
        f"name: untrusted\nsteps:\n  - uses: {_TRUSTED_PUBLISH_ACTION}\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="publishing command"):
        _verify_private_workflows(project_root)


@pytest.mark.parametrize(
    "old,new,expected_message",
    (
        (
            _TRUSTED_PUBLISH_ACTION,
            "pypa/gh-action-pypi-publish@release/v1",
            "full-SHA-pinned",
        ),
        (
            "GH_TOKEN: ${{ github.token }}",
            "GH_TOKEN: ${{ github.token }}\n          PYPI_TOKEN: ${{ secrets.PYPI_API_TOKEN }}",
            "forbidden trigger",
        ),
        (
            "types: [published]",
            "types: [published]\n  workflow_dispatch:",
            "forbidden trigger",
        ),
    ),
)
def test_trusted_publish_workflow_rejects_weakened_controls(
    tmp_path: Path,
    old: str,
    new: str,
    expected_message: str,
) -> None:
    workflow = WORKFLOW.read_text(encoding="utf-8")
    project_root = _workflow_root(tmp_path, workflow.replace(old, new))
    with pytest.raises(SystemExit, match=expected_message):
        _verify_private_workflows(project_root)


def test_release_checksums_include_only_public_release_payloads(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = {
        "cseexamtty-1.2.3-py3-none-any.whl": b"wheel",
        "cseexamtty-1.2.3.tar.gz": b"sdist",
        "cseexamtty-python.cdx.json": b"sbom",
    }
    for filename, contents in expected.items():
        (tmp_path / filename).write_bytes(contents)
    (tmp_path / "dcc-2.37-source.tar.gz").write_bytes(b"local verification only")

    monkeypatch.setattr(sys, "argv", ["write_checksums.py", str(tmp_path)])
    assert write_checksums() == 0

    checksum_names = {
        line.split("  ", maxsplit=1)[1]
        for line in (tmp_path / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    }
    assert checksum_names == set(expected)
    assert not list(tmp_path.glob(".SHA256SUMS.*"))


def test_release_checksums_fail_when_dist_contains_multiple_wheels(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for filename in (
        "cseexamtty-1.2.3-py3-none-any.whl",
        "cseexamtty-1.2.4-py3-none-any.whl",
        "cseexamtty-1.2.3.tar.gz",
        "cseexamtty-python.cdx.json",
    ):
        (tmp_path / filename).write_bytes(b"payload")

    monkeypatch.setattr(sys, "argv", ["write_checksums.py", str(tmp_path)])
    with pytest.raises(SystemExit, match="exactly one cseexamtty wheel"):
        write_checksums()
