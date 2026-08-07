from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import venv
import zipfile
from email.parser import BytesParser
from email.policy import default
from pathlib import Path


def run(argv: list[str], *, cwd: Path, environment: dict[str, str]) -> str:
    completed = subprocess.run(
        argv,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )
    if completed.returncode != 0:
        raise SystemExit(
            f"command failed ({completed.returncode}): {argv!r}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed.stdout


def resolve_wheel(argument: str) -> tuple[Path, str]:
    candidate = Path(argument).expanduser().resolve(strict=True)
    if candidate.is_dir():
        wheels = sorted(candidate.glob("cseexamtty-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(
                f"expected exactly one cseexamtty wheel in {candidate}, found {len(wheels)}"
            )
        candidate = wheels[0]
    if not candidate.is_file() or candidate.suffix != ".whl":
        raise SystemExit(f"not a wheel: {candidate}")
    with zipfile.ZipFile(candidate) as archive:
        metadata_names = [
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        ]
        if len(metadata_names) != 1:
            raise SystemExit(
                f"expected exactly one wheel METADATA file, found {len(metadata_names)}"
            )
        metadata = BytesParser(policy=default).parsebytes(archive.read(metadata_names[0]))
    version = metadata.get("Version")
    if not version:
        raise SystemExit("wheel metadata does not declare Version")
    return candidate, version


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: smoke_wheel.py PATH_TO_WHEEL_OR_DIST_DIRECTORY")
    wheel, expected_version = resolve_wheel(sys.argv[1])
    with tempfile.TemporaryDirectory(prefix="csetty-wheel-smoke-") as temporary:
        root = Path(temporary)
        environment = os.environ.copy()
        environment["CSETTY_STATE_DIR"] = str(root / "state")
        virtualenv = root / "venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(virtualenv)
        scripts = virtualenv / ("Scripts" if os.name == "nt" else "bin")
        python = scripts / ("python.exe" if os.name == "nt" else "python")
        csetty = scripts / ("csetty.exe" if os.name == "nt" else "csetty")

        run(
            [str(python), "-m", "pip", "install", "--disable-pip-version-check", str(wheel)],
            cwd=root,
            environment=environment,
        )
        version = run([str(csetty), "--version"], cwd=root, environment=environment)
        packs = run([str(csetty), "packs", "list"], cwd=root, environment=environment)
        assets = run(
            [
                str(python),
                "-c",
                """
from pathlib import Path
from importlib import resources

from csetty.assets import assets_root
from csetty.pack import PackRepository, snapshot_author_materials, snapshot_pack

r = assets_root()
assert resources.files('csetty').joinpath('py.typed').is_file()
assert (r / 'compose.yaml').is_file()
assert (r / 'checksums.lock').is_file()
assert (r / 'docker' / 'Dockerfile.interactive').is_file()
assert (r / 'docker' / 'Dockerfile.judge').is_file()
assert (r / 'docker' / 'build-dcc.sh').is_file()
assert (r / 'docker' / 'dcc-command').is_file()
assert (r / 'docker' / 'exam-command').is_file()
assert (r / 'docker' / 'mipsy-command').is_file()
assert (r / 'THIRD_PARTY_NOTICES.md').is_file()
assert (r / 'LICENSES.md').is_file()
assert (r / 'ASSESSMENT_MATERIALS_LICENSE.md').is_file()
assert (r / 'TRADEMARKS.md').is_file()
assert (r / 'NOTICE').is_file()

pack = PackRepository().get('comp1511-original-a')
assert (pack.root / 'solutions' / 'explanations').is_dir()
assert (pack.root / 'solutions' / 'reference').is_dir()
student_pack = snapshot_pack(pack, Path.cwd() / 'student-pack')
assert not (student_pack.root / 'solutions').exists()
author_root = Path.cwd() / 'author'
snapshot_author_materials(pack, author_root)
assert (author_root / 'solutions' / 'explanations').is_dir()
assert (author_root / 'solutions' / 'reference').is_dir()
print(r)
""",
            ],
            cwd=root,
            environment=environment,
        )
        staged = run(
            [
                str(python),
                "-c",
                """
from csetty.docker_runtime import DockerRuntime
from csetty.paths import AppPaths

paths = AppPaths.discover()
paths.ensure()
runtime = DockerRuntime(paths)
with runtime._staged_build_context() as context:
    assert (context / 'compose.yaml').is_file()
    assert (context / 'checksums.lock').is_file()
    assert (context / 'docker' / 'Dockerfile.interactive').is_file()
    assert (context / 'docker' / 'Dockerfile.judge').is_file()
    assert (context / 'docker' / 'build-dcc.sh').is_file()
    assert (context / 'docker' / 'dcc-command').is_file()
    assert (context / 'docker' / 'exam-command').is_file()
    assert (context / 'docker' / 'mipsy-command').is_file()
    assert (context / 'THIRD_PARTY_NOTICES.md').is_file()
    assert (context / 'LICENSE').is_file()
    assert (context / 'NOTICE').is_file()
    assert (context / 'src' / 'csetty' / 'judge.py').is_file()
    assert (context / 'build-inputs' / 'csetty-mips' / 'csetty_mips' / 'machine.py').is_file()
    assert (context / 'build-inputs' / 'csetty-mips' / 'LICENSE').is_file()
    assert (context / 'build-inputs' / 'csetty-mips' / 'NOTICE').is_file()
    assert not (context / 'packs').exists()
print('wheel-installed Docker build context: PASS')
""",
            ],
            cwd=root,
            environment=environment,
        )
        if f"csetty {expected_version}" not in version:
            raise SystemExit(f"unexpected version output: {version!r}")
        for pack_id in ("comp1511-original-a", "comp1521-original-a"):
            if pack_id not in packs:
                raise SystemExit(f"installed wheel did not expose {pack_id}")
        print(version.strip())
        print(packs.strip())
        print(f"assets: {assets.strip()}")
        print("host author assets/student-pack isolation: PASS")
        print(staged.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
