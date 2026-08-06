from __future__ import annotations

import argparse

from csetty.docker_runtime import DockerRuntime
from csetty.paths import AppPaths


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build and record local interactive/judge images without preparing VS Code"
    )
    parser.add_argument("--profile", choices=("comp1511", "comp1521"), required=True)
    arguments = parser.parse_args()

    paths = AppPaths.discover()
    paths.ensure()
    image = DockerRuntime(paths).build_image(arguments.profile)
    print(f"Prepared local source-built images for {arguments.profile}: {image}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
