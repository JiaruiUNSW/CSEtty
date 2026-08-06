from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import tempfile
import tomllib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

_CHUNK_SIZE = 1024 * 1024


def _digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_CHUNK_SIZE), b""):
            result.update(chunk)
    return result.hexdigest()


def _dcc_lock(project_root: Path) -> dict[str, Any]:
    lock = tomllib.loads((project_root / "toolchains.lock").read_text(encoding="utf-8"))
    dcc = lock.get("dcc")
    if not isinstance(dcc, dict):
        raise SystemExit("toolchains.lock does not contain a [dcc] table")
    return dcc


def fetch(destination: Path, *, project_root: Path) -> Path:
    dcc = _dcc_lock(project_root)
    version = str(dcc.get("version", ""))
    url = str(dcc.get("source_url", ""))
    expected = str(dcc.get("source_sha256", ""))
    if not version or not url or len(expected) != 64:
        raise SystemExit("DCC source provenance is incomplete in toolchains.lock")

    destination.mkdir(parents=True, exist_ok=True)
    target = destination / f"dcc-{version}-source.tar.gz"
    if target.is_file() and _digest(target) == expected:
        print(f"Verified existing {target}")
        return target

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            prefix=f".{target.name}.", suffix=".tmp", dir=destination, delete=False
        ) as temporary:
            temporary_path = Path(temporary.name)
        curl = shutil.which("curl")
        if curl:
            completed = subprocess.run(
                [
                    curl,
                    "--fail",
                    "--location",
                    "--silent",
                    "--show-error",
                    "--output",
                    str(temporary_path),
                    url,
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=120,
            )
            if completed.returncode != 0:
                detail = completed.stderr.strip() or f"curl exited {completed.returncode}"
                raise SystemExit(f"could not download DCC corresponding source: {detail}")
        else:
            request = urllib.request.Request(
                url,
                headers={"User-Agent": "CSEExamTTY-source-fetch/0.1"},
            )
            try:
                with (
                    urllib.request.urlopen(request, timeout=60) as response,  # noqa: S310
                    temporary_path.open("wb") as output,
                ):
                    while chunk := response.read(_CHUNK_SIZE):
                        output.write(chunk)
                    output.flush()
                    os.fsync(output.fileno())
            except (OSError, urllib.error.URLError) as exc:
                raise SystemExit(f"could not download DCC corresponding source: {exc}") from exc

        actual = _digest(temporary_path)
        if actual != expected:
            raise SystemExit(
                "DCC source archive digest mismatch: "
                f"expected {expected}, received {actual}"
            )
        os.chmod(temporary_path, 0o644)
        temporary_path.replace(target)
        temporary_path = None
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

    print(f"Downloaded and verified {target}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch the exact DCC corresponding-source archive for a release artifact"
    )
    parser.add_argument("destination", nargs="?", type=Path, default=Path("dist"))
    arguments = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    fetch(arguments.destination.expanduser().resolve(), project_root=project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
