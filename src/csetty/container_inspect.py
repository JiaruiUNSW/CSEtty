from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path, PurePosixPath


def _safe(root: Path, value: str) -> Path:
    relative = PurePosixPath(value)
    if (
        not value
        or "\x00" in value
        or relative.is_absolute()
        or any(part in {"", ".", ".."} for part in relative.parts)
    ):
        raise ValueError(f"unsafe workspace path: {value!r}")
    candidate = root
    for part in relative.parts:
        candidate /= part
        if candidate.is_symlink():
            raise ValueError(f"submission path contains a symlink: {value}")
    if not candidate.is_file():
        raise ValueError(f"submission path is not a regular file: {value}")
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"submission path escapes workspace: {value}")
    return resolved


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/home/student/exam")
    parser.add_argument("paths", nargs="+")
    args = parser.parse_args(argv)
    root = Path(args.root)
    try:
        files = []
        for value in args.paths:
            path = _safe(root, value)
            data = path.read_bytes()
            if len(data) > 4 * 1024 * 1024:
                raise ValueError(f"submission file exceeds 4 MiB: {value}")
            files.append(
                {"path": value, "size": len(data), "content": base64.b64encode(data).decode()}
            )
        print(json.dumps({"ok": True, "files": files}, sort_keys=True))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
