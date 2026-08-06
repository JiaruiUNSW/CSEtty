from __future__ import annotations

import base64
import errno
import json
import os
import stat
import sys
import uuid
from contextlib import suppress
from pathlib import Path, PurePosixPath

_MAX_INPUT_BYTES = 6 * 1024 * 1024


def _required_os_flag(name: str) -> int:
    value = getattr(os, name, None)
    if not isinstance(value, int):
        raise OSError(errno.ENOSYS, f"container writer requires POSIX flag {name}")
    return value


def _relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        not value
        or "\x00" in value
        or path.is_absolute()
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError(f"unsafe workspace path: {value!r}")
    return path


def _open_parent(root: Path, parts: tuple[str, ...]) -> int:
    flags = os.O_RDONLY | _required_os_flag("O_DIRECTORY") | _required_os_flag("O_NOFOLLOW")
    directory_fd = os.open(root, flags)
    try:
        for part in parts:
            with suppress(FileExistsError):
                os.mkdir(part, 0o700, dir_fd=directory_fd)
            next_fd = os.open(part, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        return directory_fd
    except OSError as exc:
        os.close(directory_fd)
        if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise ValueError(
                "workspace path contains a symlink or non-directory component"
            ) from exc
        raise
    except Exception:
        os.close(directory_fd)
        raise


def _existing_kind(directory_fd: int, name: str) -> str | None:
    try:
        mode = os.stat(name, dir_fd=directory_fd, follow_symlinks=False).st_mode
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(mode):
        return "symlink"
    if stat.S_ISREG(mode):
        return "file"
    return "non-regular path"


def write_file(root: Path, relative: str, content: bytes, *, overwrite: bool) -> str:
    path = _relative(relative)
    directory_fd = _open_parent(root, tuple(path.parts[:-1]))
    name = path.name
    temporary = f".csetty-{uuid.uuid4().hex}.tmp"
    temporary_fd: int | None = None
    try:
        existing = _existing_kind(directory_fd, name)
        if existing == "symlink":
            raise ValueError(f"refusing to replace symlink: {relative}")
        if existing not in {None, "file"}:
            raise ValueError(f"workspace target is not a regular file: {relative}")
        if existing == "file" and not overwrite:
            return "kept"
        temporary_fd = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | _required_os_flag("O_NOFOLLOW"),
            0o600,
            dir_fd=directory_fd,
        )
        view = memoryview(content)
        while view:
            written = os.write(temporary_fd, view)
            view = view[written:]
        os.fsync(temporary_fd)
        os.close(temporary_fd)
        temporary_fd = None
        if overwrite:
            os.replace(temporary, name, src_dir_fd=directory_fd, dst_dir_fd=directory_fd)
        else:
            try:
                os.link(
                    temporary,
                    name,
                    src_dir_fd=directory_fd,
                    dst_dir_fd=directory_fd,
                    follow_symlinks=False,
                )
            except FileExistsError:
                existing = _existing_kind(directory_fd, name)
                if existing != "file":
                    raise ValueError(f"refusing unsafe existing path: {relative}") from None
                return "kept"
        os.fsync(directory_fd)
        return "restored"
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.ENOTDIR}:
            raise ValueError(f"workspace path contains a symlink: {relative}") from exc
        raise
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        with suppress(FileNotFoundError):
            os.unlink(temporary, dir_fd=directory_fd)
        os.close(directory_fd)


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    if len(arguments) != 1:
        print(json.dumps({"ok": False, "error": "one workspace path is required"}))
        return 2
    raw = sys.stdin.buffer.read(_MAX_INPUT_BYTES + 1)
    if len(raw) > _MAX_INPUT_BYTES:
        print(json.dumps({"ok": False, "error": "write request is too large"}))
        return 2
    try:
        payload = json.loads(raw)
        if not isinstance(payload, dict) or not isinstance(payload.get("content"), str):
            raise ValueError("write request is invalid")
        content = base64.b64decode(payload["content"], validate=True)
        status = write_file(
            Path("/home/student/exam"),
            arguments[0],
            content,
            overwrite=bool(payload.get("overwrite", False)),
        )
        print(json.dumps({"ok": True, "status": status}, sort_keys=True))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
