from __future__ import annotations

import hashlib
import os
import sys
import tempfile
from pathlib import Path


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def release_files(root: Path) -> tuple[Path, Path, Path]:
    wheels = sorted(root.glob("cseexamtty-*.whl"))
    sdists = sorted(root.glob("cseexamtty-*.tar.gz"))
    sbom = root / "cseexamtty-python.cdx.json"
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one cseexamtty wheel, found {len(wheels)}")
    if len(sdists) != 1:
        raise SystemExit(f"expected exactly one cseexamtty sdist, found {len(sdists)}")
    if not sbom.is_file():
        raise SystemExit(f"missing release SBOM: {sbom}")
    return wheels[0], sdists[0], sbom


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) == 2 else "dist").resolve(strict=True)
    output = root / "SHA256SUMS"
    files = release_files(root)
    contents = "".join(f"{digest(path)}  {path.name}\n" for path in files)
    temporary_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=root,
            prefix=".SHA256SUMS.",
            delete=False,
        ) as stream:
            temporary_name = stream.name
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
        Path(temporary_name).replace(output)
    finally:
        if temporary_name is not None:
            Path(temporary_name).unlink(missing_ok=True)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
