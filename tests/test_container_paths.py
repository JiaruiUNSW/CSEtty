from __future__ import annotations

import os
from pathlib import Path

import pytest

from csetty.container_inspect import _safe
from csetty.container_write import write_file

pytestmark = pytest.mark.skipif(
    os.name != "posix", reason="container path helpers execute only inside the Linux image"
)


def test_container_write_is_atomic_and_respects_overwrite(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    root.mkdir()
    assert write_file(root, "nested/q.c", b"first", overwrite=False) == "restored"
    assert write_file(root, "nested/q.c", b"ignored", overwrite=False) == "kept"
    assert (root / "nested" / "q.c").read_bytes() == b"first"
    assert write_file(root, "nested/q.c", b"second", overwrite=True) == "restored"
    assert (root / "nested" / "q.c").read_bytes() == b"second"


def test_container_write_rejects_parent_and_final_symlinks(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        write_file(root, "linked/q.c", b"unsafe", overwrite=True)
    assert not (outside / "q.c").exists()

    (root / "q.c").symlink_to(outside / "target.c")
    with pytest.raises(ValueError, match="symlink"):
        write_file(root, "q.c", b"unsafe", overwrite=True)


def test_container_inspect_rejects_any_symlink_component(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (outside / "answer.c").write_text("secret", encoding="utf-8")
    (root / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        _safe(root, "linked/answer.c")
