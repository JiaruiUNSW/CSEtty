from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) == 2 else "dist").resolve(strict=True)
    output = root / "SHA256SUMS"
    files = sorted(
        path
        for path in root.iterdir()
        if path.is_file() and path != output and not path.name.startswith(".")
    )
    output.write_text(
        "".join(f"{digest(path)}  {path.name}\n" for path in files),
        encoding="utf-8",
    )
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
