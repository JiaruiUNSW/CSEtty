from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from csetty.docker_runtime import DockerRuntime
from csetty.paths import AppPaths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Stage a local Docker build context with pinned dependency source"
    )
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()

    with tempfile.TemporaryDirectory(prefix="csetty-build-state-") as state:
        paths = AppPaths.discover(Path(state))
        paths.ensure()
        digest = DockerRuntime(paths).stage_build_context(arguments.destination)
    print(f"Staged source-build context: {arguments.destination.expanduser().resolve()}")
    print(f"Context SHA-256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
