from __future__ import annotations

import json
import os
import stat
from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path

import pytest
from test_pack import make_pack

import csetty.docker_runtime as docker_runtime_module
from csetty.docker_runtime import CommandResult, DockerRuntime
from csetty.errors import ToolUnavailableError
from csetty.models import Attempt, AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack
from csetty.paths import AppPaths


def _attempt() -> Attempt:
    now = datetime(2026, 8, 5, tzinfo=UTC)
    return Attempt(
        id="attempt",
        pack_id="pack",
        pack_version="1.0.0",
        pack_path="/pack",
        pack_digest="a" * 64,
        course="COMP1511",
        profile="comp1511",
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
        workspace_ref="volume",
        image="csetty/comp1511:dev",
        provenance={},
        container_name="csetty-attempt",
        session_token="token",
        network="none",
        editor="terminal",
    )


def test_terminal_broadcast_embedded_script_is_valid_python(monkeypatch, tmp_path: Path) -> None:
    runtime = DockerRuntime(AppPaths.discover(tmp_path / "state"))

    def fake_run(arguments, **_kwargs):
        script = arguments[arguments.index("-c") + 1]
        compile(script, "<terminal-broadcast>", "exec")
        return CommandResult(tuple(arguments), 0, "2\n", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    assert runtime.broadcast_terminal(_attempt(), "time warning") == 2


def test_attempt_prefers_recorded_image_id(monkeypatch, tmp_path: Path) -> None:
    runtime = DockerRuntime(AppPaths.discover(tmp_path / "state"))
    attempt = replace(_attempt(), provenance={"image": {"id": "sha256:fixed"}})
    monkeypatch.setattr(runtime, "image_exists", lambda image: image == "sha256:fixed")
    assert runtime.pinned_attempt_image(attempt) == "sha256:fixed"


def test_prepare_vscode_recreates_container_when_course_image_changed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    commands: list[list[str]] = []

    monkeypatch.setattr(runtime, "image_exists", lambda _image: True)
    monkeypatch.setattr(runtime, "_ensure_owned_volume", lambda *_args: False)
    monkeypatch.setattr(runtime, "_container_exists", lambda _name: True)
    monkeypatch.setattr(runtime, "_container_image_id", lambda _name: "sha256:old")
    monkeypatch.setattr(runtime, "_image_id", lambda _image: "sha256:new")

    def fake_run(arguments, **_kwargs):
        commands.append(list(arguments))
        return CommandResult(tuple(arguments), 0, "", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    assert runtime.prepare_vscode_container("comp1511") == "csetty-vscode-prep-comp1511"
    assert ["container", "rm", "--force", "csetty-vscode-prep-comp1511"] in commands
    create = commands[-1]
    assert create[0] == "run"
    assert create[-3:] == ["csetty/comp1511:dev", "sleep", "infinity"]


def test_vscode_cache_check_receives_exact_server_commit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    runtime = DockerRuntime(AppPaths.discover(tmp_path / "state"))
    captured: list[str] = []

    def fake_run(arguments, **_kwargs):
        if arguments[0] == "run":
            script = arguments[arguments.index("-c") + 1]
            compile(script, "<vscode-cache-check>", "exec")
            captured.extend(arguments)
        return CommandResult(tuple(arguments), 0, "", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    commit = "e" * 40
    assert runtime.vscode_cache_ready("comp1511", ("ms-vscode.cpptools",), commit)
    assert captured[captured.index("-c") + 2] == commit


def test_vscode_server_check_requires_exact_running_commit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    runtime = DockerRuntime(AppPaths.discover(tmp_path / "state"))
    captured: list[str] = []
    monkeypatch.setattr(runtime, "_container_running", lambda _name: True)

    def fake_run(arguments, **_kwargs):
        script = arguments[arguments.index("-c") + 1]
        compile(script, "<vscode-server-check>", "exec")
        captured.extend(arguments)
        return CommandResult(tuple(arguments), 0, "", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    commit = "e" * 40
    assert runtime.vscode_server_ready("csetty-attempt", commit)
    assert captured[-1] == commit


def test_vscode_server_check_rejects_stopped_container(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    runtime = DockerRuntime(AppPaths.discover(tmp_path / "state"))
    monkeypatch.setattr(runtime, "_container_running", lambda _name: False)
    monkeypatch.setattr(
        runtime,
        "_run",
        lambda *_args, **_kwargs: pytest.fail("docker exec should not run"),
    )
    assert not runtime.vscode_server_ready("csetty-attempt", "e" * 40)


def test_staged_image_context_contains_only_required_runtime_inputs(tmp_path: Path) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    with runtime._staged_build_context() as context:
        assert (context / "compose.yaml").is_file()
        assert (context / "checksums.lock").is_file()
        assert (context / "docker" / "Dockerfile.interactive").is_file()
        assert (context / "docker" / "Dockerfile.judge").is_file()
        assert (context / "docker" / "build-dcc.sh").is_file()
        assert (context / "docker" / "exam-command").is_file()
        assert (context / "docker" / "mipsy-command").is_file()
        assert (context / "THIRD_PARTY_NOTICES.md").is_file()
        assert (context / "LICENSE").is_file()
        assert (context / "src" / "csetty" / "judge.py").is_file()
        mips = context / "build-inputs" / "csetty-mips"
        assert (mips / "csetty_mips" / "machine.py").is_file()
        assert (mips / "LICENSE").is_file()
        assert (mips / "NOTICE").is_file()
        assert not list(context.rglob("__pycache__"))
        assert not any(" " in path.name for path in mips.rglob("*.py"))
        assert not (context / "packs").exists()


def test_staged_image_context_rejects_changed_mips_package(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        docker_runtime_module,
        "CSETTY_MIPS_PACKAGE_TREE_SHA256",
        "0" * 64,
    )
    with pytest.raises(ToolUnavailableError, match="package content digest mismatch"):
        DockerRuntime._csetty_mips_distribution_files()


def test_comp1521_image_build_uses_the_pinned_dependency_without_an_upstream_context(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    captured: list[list[str]] = []

    def fake_run(arguments, **_kwargs):
        captured.append(list(arguments))
        if arguments[:3] == ["image", "inspect", "--format"]:
            reference = arguments[-1]
            if arguments[3] == "{{.Id}}":
                return CommandResult(tuple(arguments), 0, f"sha256:{reference}\n", "")
            role = "judge" if "-judge:" in reference else "interactive"
            labels = json.dumps(
                {"io.csetty.profile": "comp1521", "io.csetty.image.role": role}
            )
            return CommandResult(tuple(arguments), 0, labels, "")
        return CommandResult(tuple(arguments), 0, "", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    assert runtime.build_image("comp1521") == "csetty/comp1521:dev"
    compose = captured[0]
    assert compose[0] == "compose"
    assert compose[-3:] == ["build", "comp1521-interactive", "comp1521-judge"]
    assert "--build-context" not in compose
    receipt = json.loads(runtime._image_receipt_path("comp1521").read_text(encoding="utf-8"))
    assert receipt["images"]["interactive"]["reference"] == "csetty/comp1521:dev"
    assert receipt["images"]["judge"]["reference"] == "csetty/comp1521-judge:dev"


def test_prepared_image_receipt_rejects_retagged_judge_image(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    with runtime._staged_build_context() as context:
        context_digest = runtime._build_context_digest(context)
    receipt = {
        "schema_version": 1,
        "profile": "comp1511",
        "build_context_sha256": context_digest,
        "images": {
            "interactive": {"id": "sha256:interactive"},
            "judge": {"id": "sha256:judge"},
        },
    }
    path = runtime._image_receipt_path("comp1511")
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(receipt), encoding="utf-8")

    image_ids = {
        "csetty/comp1511:dev": "sha256:interactive",
        "csetty/comp1511-judge:dev": "sha256:judge",
    }
    monkeypatch.setattr(runtime, "_image_id", lambda image: image_ids[image])
    runtime.ensure_profile_ready("comp1511")

    image_ids["csetty/comp1511-judge:dev"] = "sha256:replaced"
    with pytest.raises(ToolUnavailableError, match="judge image no longer matches"):
        runtime.ensure_profile_ready("comp1511")


def test_prepared_image_receipt_rejects_changed_source_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    receipt = {
        "schema_version": 1,
        "profile": "comp1511",
        "build_context_sha256": "0" * 64,
        "images": {},
    }
    path = runtime._image_receipt_path("comp1511")
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(receipt), encoding="utf-8")
    monkeypatch.setattr(
        runtime,
        "_image_id",
        lambda _image: pytest.fail("image IDs must not be trusted after source changes"),
    )

    with pytest.raises(ToolUnavailableError, match="source-build inputs changed"):
        runtime.ensure_profile_ready("comp1511")


def test_interactive_container_has_the_declared_security_boundary(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    pack = load_pack(make_pack(tmp_path / "pack"))
    bridge = tmp_path / "bridge"
    resources = tmp_path / "resources"
    (bridge / "requests").mkdir(parents=True)
    (bridge / "responses").mkdir()
    (bridge / "session.json").write_text("{}", encoding="utf-8")
    resources.mkdir()
    captured: list[list[str]] = []

    monkeypatch.setattr(runtime, "pinned_attempt_image", lambda _attempt: "sha256:fixed")
    monkeypatch.setattr(runtime, "_container_exists", lambda _name: False)
    monkeypatch.setattr(runtime, "_prepare_bridge", lambda _attempt: bridge)
    monkeypatch.setattr(runtime, "_prepare_resources", lambda _attempt, _pack: resources)
    monkeypatch.setattr(runtime, "_ensure_vscode_volume", lambda *_args: None)
    monkeypatch.setattr(runtime, "_ensure_owned_volume", lambda *_args: False)
    monkeypatch.setattr(runtime, "_initialize_workspace", lambda *_args: None)

    def fake_run(arguments, **_kwargs):
        captured.append(list(arguments))
        return CommandResult(tuple(arguments), 0, "", "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    runtime.start_container(_attempt(), pack, network="none")
    arguments = captured[-1]
    joined = " ".join(arguments)
    assert arguments[0] == "run"
    assert arguments[arguments.index("--network") + 1] == "none"
    assert arguments[arguments.index("--cap-drop") + 1] == "ALL"
    assert arguments[arguments.index("--security-opt") + 1] == "no-new-privileges"
    assert arguments[arguments.index("--user") + 1] == "student"
    assert "--read-only" in arguments
    assert "--cpus" in arguments
    assert "--memory" in arguments
    assert "--pids-limit" in arguments
    assert "/var/run/docker.sock" not in joined
    assert "/home/student/.vscode-server" not in joined
    assert arguments[-3:] == ["sha256:fixed", "sleep", "infinity"]


def test_judge_is_ephemeral_offline_and_mounts_only_read_only_inputs(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = DockerRuntime(paths)
    pack = load_pack(make_pack(tmp_path / "pack"))
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    submission = snapshot / "q1.c"
    submission.write_text("int main(void) { return 0; }\n", encoding="utf-8")
    if os.name != "nt":
        snapshot.chmod(0o700)
        submission.chmod(0o600)
    captured: list[list[str]] = []

    monkeypatch.setattr(runtime, "pinned_judge_image", lambda _attempt: "sha256:judge-fixed")

    def fake_run(arguments, **_kwargs):
        captured.append(list(arguments))
        submission_mount = next(
            value
            for value in arguments
            if value.startswith("type=bind,source=") and "target=/submission" in value
        )
        mounted_root = Path(
            submission_mount.removeprefix("type=bind,source=").split(",target=", 1)[0]
        )
        mounted_submission = mounted_root / "q1.c"
        assert mounted_root != snapshot.resolve()
        assert mounted_submission.read_text(encoding="utf-8") == submission.read_text(
            encoding="utf-8"
        )
        if os.name != "nt":
            assert stat.S_IMODE(mounted_root.stat().st_mode) & stat.S_IXOTH
            assert stat.S_IMODE(mounted_submission.stat().st_mode) & stat.S_IROTH
        return CommandResult(tuple(arguments), 0, '{"status":"PASS","groups":[]}\n', "")

    monkeypatch.setattr(runtime, "_run", fake_run)
    result = runtime.run_judge(
        attempt=_attempt(),
        pack=pack,
        question=pack.question("q1"),
        snapshot=snapshot,
        groups=pack.question("q1").test_groups,
    )
    assert result["status"] == "PASS"
    arguments = captured[-1]
    joined = " ".join(arguments)
    assert arguments[0:3] == ["run", "--rm", "--interactive"]
    assert arguments[arguments.index("--network") + 1] == "none"
    assert arguments[arguments.index("--cap-drop") + 1] == "ALL"
    assert arguments[arguments.index("--security-opt") + 1] == "no-new-privileges"
    assert arguments[arguments.index("--user") + 1] == "student"
    assert "--read-only" in arguments
    assert "target=/submission,readonly" in joined
    assert "target=/pack,readonly" in joined
    assert "/var/run/docker.sock" not in joined
    assert arguments[-4:] == ["sha256:judge-fixed", "python3", "-m", "csetty.judge"]
