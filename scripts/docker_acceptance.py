from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
import uuid
from datetime import UTC, datetime
from pathlib import Path

from csetty.docker_runtime import DockerRuntime
from csetty.models import Attempt, AttemptMode, AttemptState, WorkspaceKind
from csetty.paths import AppPaths


def run(
    argv: list[str],
    *,
    check: bool = True,
    timeout: float = 30,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
    )
    if check and completed.returncode != 0:
        raise SystemExit(
            f"command failed ({completed.returncode}): {argv!r}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed


def _attempt(container_name: str, profile: str, image: str) -> Attempt:
    now = datetime.now(UTC)
    return Attempt(
        id=f"acceptance-{uuid.uuid4().hex}",
        pack_id="acceptance",
        pack_version="0",
        pack_path="/private/acceptance",
        pack_digest="0" * 64,
        course=profile.upper(),
        profile=profile,
        mode=AttemptMode.EXAM,
        state=AttemptState.WORKING,
        timed=True,
        created_at=now,
        reading_started_at=now,
        working_started_at=now,
        deadline_at=now,
        finished_at=None,
        finish_reason=None,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="acceptance",
        image=image,
        provenance={},
        container_name=container_name,
        session_token="acceptance",
        network="none",
        editor="terminal",
        candidate_id="z0000000",
    )


def _assert_inspect_boundary(container_name: str, profile: str) -> None:
    inspected = run(["docker", "inspect", container_name])
    record = json.loads(inspected.stdout)[0]
    config = record["Config"]
    host = record["HostConfig"]
    if config["User"] not in {"student", "1000", "1000:1000"}:
        raise SystemExit(f"container is not configured as the student user: {config['User']!r}")
    expected = {
        "ReadonlyRootfs": True,
        "Privileged": False,
        "NetworkMode": "none",
    }
    for key, value in expected.items():
        if host.get(key) != value:
            raise SystemExit(f"unexpected Docker boundary {key}: {host.get(key)!r}")
    if "ALL" not in (host.get("CapDrop") or []):
        raise SystemExit("container does not drop all Linux capabilities")
    if "no-new-privileges" not in (host.get("SecurityOpt") or []):
        raise SystemExit("container does not set no-new-privileges")
    if int(host.get("PidsLimit") or 0) <= 0:
        raise SystemExit("container does not have a PID limit")
    if int(host.get("Memory") or 0) <= 0 or int(host.get("NanoCpus") or 0) <= 0:
        raise SystemExit("container does not have memory and CPU limits")
    if host.get("Binds"):
        raise SystemExit(f"acceptance container unexpectedly has bind mounts: {host['Binds']!r}")
    if any(mount.get("Type") == "bind" for mount in record.get("Mounts", [])):
        raise SystemExit("acceptance container unexpectedly exposes a host bind mount")
    if profile == "comp1521":
        labels = config.get("Labels") or {}
        expected_labels = {
            "io.csetty.mips.engine": "csetty-mips",
            "io.csetty.mips.version": "0.1.2",
            "io.csetty.mips.license": "MPL-2.0",
        }
        for key, value in expected_labels.items():
            if labels.get(key) != value:
                raise SystemExit(f"COMP1521 image has wrong {key} label: {labels.get(key)!r}")


def _run_security_probes(container_name: str, profile: str) -> None:
    probe = r"""
import hashlib
import os
import shutil
import socket
from pathlib import Path

assert os.getuid() == 1000, os.getuid()
assert not Path('/var/run/docker.sock').exists()
assert not Path('/run/docker.sock').exists()
for command in ('exam', '1511', '1521', 'autotest', 'submit', 'check'):
    assert shutil.which(command), command
assert shutil.which('give') is None

status = Path('/proc/self/status').read_text()
cap_eff = next(line.split()[1] for line in status.splitlines() if line.startswith('CapEff:'))
assert int(cap_eff, 16) == 0, cap_eff

try:
    Path('/home/student/csetty-rootfs-probe').write_text('unexpected')
except OSError:
    pass
else:
    raise AssertionError('read-only root filesystem accepted a write')

network = socket.socket()
network.settimeout(1)
try:
    network.connect(('1.1.1.1', 53))
except OSError:
    pass
else:
    raise AssertionError('network-none container reached an external address')
finally:
    network.close()

license_path = Path('/usr/share/doc/dcc/LICENSE')
assert license_path.is_file() and license_path.stat().st_size > 1000
assert hashlib.sha256(license_path.read_bytes()).hexdigest() == (
    '3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986'
)
source = Path('/usr/share/doc/dcc/SOURCE').read_text()
assert '0a888fdb2bfe130c611fb84514fdbf52d3efe149' in source
assert Path('/usr/share/doc/csetty/THIRD_PARTY_NOTICES.md').is_file()
assert Path('/usr/share/doc/csetty/NOTICE').is_file()
print('security boundary and legal payload: PASS')
"""
    result = run(["docker", "exec", container_name, "python3", "-c", probe], timeout=20)
    print(f"{profile}: {result.stdout.strip()}")

    if profile == "comp1521":
        mips_probe = r"""
from pathlib import Path
import csetty_mips

assert csetty_mips.__version__ == '0.1.2'
assert str(Path(csetty_mips.__file__).resolve()).startswith('/opt/csetty/csetty_mips/')
assert Path('/usr/share/doc/csetty-mips/NOTICE').is_file()
assert Path('/usr/share/doc/csetty-mips/LICENSE').is_file()
launcher = Path('/usr/local/bin/mipsy').read_text()
assert 'from csetty_mips.cli import main' in launcher
print('local csetty-mips payload and provenance: PASS')
"""
        result = run(
            ["docker", "exec", container_name, "python3", "-c", mips_probe], timeout=20
        )
        print(f"{profile}: {result.stdout.strip()}")

    crash = run(
        ["docker", "exec", container_name, "python3", "-c", "import os; os.abort()"],
        check=False,
        timeout=10,
    )
    if crash.returncode == 0:
        raise SystemExit("crashing student process unexpectedly returned success")
    running = run(["docker", "inspect", "--format", "{{.State.Running}}", container_name])
    if running.stdout.strip() != "true":
        raise SystemExit("a crashing student process stopped the interactive container")
    print(f"{profile}: crashing child process containment: PASS")


def _run_pid_limit_probe(container_name: str, profile: str) -> None:
    probe = r"""
import os
import signal
import time

children = []
limited = False
try:
    while len(children) < 256:
        pid = os.fork()
        if pid == 0:
            time.sleep(10)
            os._exit(0)
        children.append(pid)
except OSError:
    limited = True
finally:
    for pid in children:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    for pid in children:
        try:
            os.waitpid(pid, 0)
        except ChildProcessError:
            pass
assert limited, f'PID limit did not stop {len(children)} forks'
print(f'PID limit stopped fork growth after {len(children)} children')
"""
    result = run(["docker", "exec", container_name, "python3", "-c", probe], timeout=20)
    print(f"{profile}: {result.stdout.strip()}: PASS")


def _run_toolchain_probe(container_name: str, profile: str) -> None:
    commands = [
        ["python3", "--version"],
        ["gcc", "--version"],
        ["clang", "--version"],
        ["dcc", "--version"],
        ["make", "--version"],
        ["gdb", "--version"],
        ["valgrind", "--version"],
    ]
    if profile == "comp1521":
        commands.append(["mipsy", "--version"])
    for command in commands:
        result = run(["docker", "exec", container_name, *command], timeout=20)
        first_line = (result.stdout or result.stderr).strip().splitlines()[0]
        print(f"{profile}: {' '.join(command)} -> {first_line}")


def _run_broadcast_probe(
    runtime: DockerRuntime,
    attempt: Attempt,
) -> None:
    listener = subprocess.Popen(
        [
            "docker",
            "exec",
            "--tty",
            "--user",
            "student",
            attempt.container_name,
            "sh",
            "-c",
            "printf 'TTY_READY\\n'; sleep 3",
        ],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        time.sleep(0.5)
        message = "*** CSEExamTTY ACCEPTANCE TIME WARNING: 5 minutes remaining ***"
        written = runtime.broadcast_terminal(attempt, message)
        output, _ = listener.communicate(timeout=6)
    finally:
        if listener.poll() is None:
            listener.terminate()
            listener.wait(timeout=3)
    if written < 1 or message not in output:
        raise SystemExit(
            f"terminal broadcast was not observed (written={written}, output={output!r})"
        )
    print("comp1511: live pseudo-terminal deadline broadcast: PASS")


def verify_profile(
    runtime: DockerRuntime,
    profile: str,
    *,
    broadcast: bool,
    image: str | None = None,
) -> None:
    image = image or f"csetty/{profile}:dev"
    container_name = f"csetty-acceptance-{profile}-{uuid.uuid4().hex[:10]}"
    attempt = _attempt(container_name, profile, image)
    arguments = [
        "docker",
        "run",
        "--detach",
        "--name",
        container_name,
        "--network",
        "none",
        "--cpus",
        "1.0",
        "--memory",
        "256m",
        "--pids-limit",
        "32",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--read-only",
        "--tmpfs",
        "/tmp:rw,nosuid,nodev,exec,size=64m",
        "--user",
        "student",
        image,
        "sleep",
        "infinity",
    ]
    run(arguments, timeout=30)
    try:
        _assert_inspect_boundary(container_name, profile)
        _run_security_probes(container_name, profile)
        _run_pid_limit_probe(container_name, profile)
        _run_toolchain_probe(container_name, profile)
        if broadcast:
            _run_broadcast_probe(runtime, attempt)
    finally:
        run(["docker", "rm", "--force", container_name], check=False, timeout=20)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run live, destructive-only-to-temporary-container Docker acceptance probes"
    )
    parser.add_argument(
        "--profile",
        choices=("comp1511", "comp1521", "all"),
        default="all",
    )
    parser.add_argument(
        "--image",
        help="validate this image tag (requires one explicit profile)",
    )
    parser.add_argument("--skip-broadcast", action="store_true")
    arguments = parser.parse_args()
    if arguments.image is not None and arguments.profile == "all":
        parser.error("--image requires --profile comp1511 or --profile comp1521")
    profiles = ("comp1511", "comp1521") if arguments.profile == "all" else (arguments.profile,)

    with tempfile.TemporaryDirectory(prefix="csetty-docker-acceptance-") as temporary:
        paths = AppPaths.discover(Path(temporary) / "state")
        paths.ensure()
        runtime = DockerRuntime(paths)
        doctor = runtime.doctor()
        if not doctor["daemon"]:
            raise SystemExit(f"Docker daemon is unavailable: {doctor['error']}")
        for profile in profiles:
            image = arguments.image or f"csetty/{profile}:dev"
            if not runtime.image_exists(image):
                raise SystemExit(f"missing image {image}")
            verify_profile(
                runtime,
                profile,
                broadcast=profile == "comp1511" and not arguments.skip_broadcast,
                image=image,
            )
    print("DOCKER ACCEPTANCE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
