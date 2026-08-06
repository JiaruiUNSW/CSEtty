from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import ValidationError


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def safe_relative_path(value: str, *, label: str = "path") -> PurePosixPath:
    if not value or "\x00" in value:
        raise ValidationError(f"{label} must be a non-empty relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValidationError(f"unsafe {label}: {value!r}")
    return path


def resolve_under(root: Path, relative: str, *, must_exist: bool = True) -> Path:
    safe = safe_relative_path(relative)
    candidate = root.joinpath(*safe.parts)
    resolved_root = root.resolve()
    if must_exist:
        resolved = candidate.resolve(strict=True)
    else:
        resolved = candidate.parent.resolve(strict=True) / candidate.name
    if not resolved.is_relative_to(resolved_root):
        raise ValidationError(f"path escapes declared root: {relative}")
    return resolved


def atomic_write(path: Path, data: bytes, *, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temp_path = Path(temporary)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temp_path, mode)
        os.replace(temp_path, path)
    finally:
        temp_path.unlink(missing_ok=True)
