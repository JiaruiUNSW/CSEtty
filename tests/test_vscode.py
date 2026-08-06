from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from types import SimpleNamespace

import pytest

from csetty.errors import ToolUnavailableError
from csetty.paths import AppPaths
from csetty.vscode import VSCodeManager


class RuntimeStub:
    pass


class ReadyRuntime:
    def __init__(self) -> None:
        self.checked_commit: str | None = None

    @staticmethod
    def image_for_profile(profile: str) -> str:
        return f"csetty/{profile}:dev"

    @staticmethod
    def image_exists(_image: str) -> bool:
        return True

    @staticmethod
    def image_provenance(_image: str) -> dict[str, object]:
        return {"image": {"id": "sha256:current"}}

    def vscode_cache_ready(
        self, _profile: str, _extensions: tuple[str, ...], server_commit: str
    ) -> bool:
        self.checked_commit = server_commit
        return True

    @staticmethod
    def vscode_server_ready(_container: str, _commit: str) -> bool:
        return True


def manager(tmp_path: Path) -> VSCodeManager:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    return VSCodeManager(paths, RuntimeStub())  # type: ignore[arg-type]


def test_isolated_environment_blocks_credentials(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("SSH_AUTH_SOCK", "/private/real-agent.sock")
    monkeypatch.setenv("GITHUB_TOKEN", "secret")
    environment = manager(tmp_path)._isolated_environment()
    assert environment["SSH_AUTH_SOCK"] == ""
    assert "GITHUB_TOKEN" not in environment


def test_exam_profile_settings_are_isolated_and_visibly_labelled(tmp_path: Path) -> None:
    vscode = manager(tmp_path)
    vscode._write_settings("comp1521")
    user_data, _extensions, _manifest = vscode._profile_paths("comp1521")
    settings = json.loads((user_data / "User" / "settings.json").read_text(encoding="utf-8"))
    assert settings["chat.disableAIFeatures"] is True
    assert settings["dev.containers.copyGitConfig"] is False
    assert settings["dev.containers.gitCredentialHelperConfigLocation"] == "none"
    assert settings["dev.containers.defaultExtensions"] == [
        "ms-vscode.cpptools",
        "xavc.xavc-mipsy-features",
    ]
    assert settings["window.title"].startswith("CSEExamTTY ISOLATED EXAM")
    assert settings["remote.autoForwardPorts"] is False


def test_offline_ready_requires_host_extension_and_exact_server_commit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()
    runtime = ReadyRuntime()
    vscode = VSCodeManager(paths, runtime)  # type: ignore[arg-type]
    monkeypatch.setattr(
        vscode,
        "version",
        lambda: {"version": "1.131.0", "commit": "e" * 40, "architecture": "arm64"},
    )
    _user_data, extensions, manifest = vscode._profile_paths("comp1511")
    host = extensions / "ms-vscode-remote.remote-containers-0.400.0"
    host.mkdir(parents=True)
    (host / "package.json").write_text("{}\n", encoding="utf-8")
    vscode._record_attach_trust("comp1511")
    manifest.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "profile": "comp1511",
                "code": {"commit": "e" * 40},
                "host_extension": "ms-vscode-remote.remote-containers",
                "remote_extensions": ["ms-vscode.cpptools"],
                "image_id": "sha256:current",
            }
        ),
        encoding="utf-8",
    )

    assert vscode.offline_ready("comp1511") == (True, "ready")
    assert runtime.checked_commit == "e" * 40

    (host / "package.json").unlink()
    ready, detail = vscode.offline_ready("comp1511")
    assert not ready
    assert "Dev Containers extension" in detail


def test_container_trust_is_recorded_only_in_isolated_profile(tmp_path: Path) -> None:
    vscode = manager(tmp_path)
    assert not vscode._attach_trust_recorded("comp1511")

    vscode._record_attach_trust("comp1511")

    assert vscode._attach_trust_recorded("comp1511")
    assert not vscode._attach_trust_recorded("comp1521")


def test_container_trust_rejects_malformed_isolated_extension_state(tmp_path: Path) -> None:
    vscode = manager(tmp_path)
    user_data, _extensions, _manifest = vscode._profile_paths("comp1511")
    database = user_data / "User" / "globalStorage" / "state.vscdb"
    database.parent.mkdir(parents=True)

    with sqlite3.connect(database) as connection:
        connection.execute(
            "CREATE TABLE ItemTable (key TEXT UNIQUE ON CONFLICT REPLACE, value BLOB)"
        )
        connection.execute(
            "INSERT INTO ItemTable(key, value) VALUES (?, ?)",
            ("ms-vscode-remote.remote-containers", b"null"),
        )

    with pytest.raises(ToolUnavailableError, match="unexpected format"):
        vscode._record_attach_trust("comp1511")


def test_attach_waits_for_matching_server_process(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()

    class AttachRuntime:
        checks = 0

        def vscode_server_ready(self, container: str, commit: str) -> bool:
            assert container == "csetty-attempt"
            assert commit == "e" * 40
            self.checks += 1
            return True

    runtime = AttachRuntime()
    vscode = VSCodeManager(paths, runtime)  # type: ignore[arg-type]
    monkeypatch.setattr(vscode, "_write_settings", lambda _profile: None)
    monkeypatch.setattr(vscode, "_base_args", lambda _profile: ["code"])
    monkeypatch.setattr(
        vscode,
        "version",
        lambda: {"version": "1.131.0", "commit": "e" * 40, "architecture": "arm64"},
    )
    monkeypatch.setattr(
        "csetty.vscode.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stderr=""),
    )
    attempt = SimpleNamespace(profile="comp1511", container_name="csetty-attempt")

    vscode.attach(attempt)  # type: ignore[arg-type]

    assert runtime.checks == 1


def test_attach_rejects_cli_false_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()

    class AttachRuntime:
        @staticmethod
        def vscode_server_ready(_container: str, _commit: str) -> bool:
            return False

    vscode = VSCodeManager(paths, AttachRuntime())  # type: ignore[arg-type]
    monkeypatch.setattr(vscode, "_write_settings", lambda _profile: None)
    monkeypatch.setattr(vscode, "_base_args", lambda _profile: ["code"])
    monkeypatch.setattr(
        vscode,
        "version",
        lambda: {"version": "1.131.0", "commit": "e" * 40, "architecture": "arm64"},
    )
    monkeypatch.setattr(
        "csetty.vscode.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stderr=""),
    )
    attempt = SimpleNamespace(profile="comp1511", container_name="csetty-attempt")

    with pytest.raises(ToolUnavailableError, match="Server did not start"):
        vscode.attach(attempt, wait_seconds=0)  # type: ignore[arg-type]


def test_prepare_requires_running_server_as_well_as_cached_files(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    paths = AppPaths.discover(tmp_path / "state")
    paths.ensure()

    class PrepareRuntime:
        @staticmethod
        def prepare_vscode_container(_profile: str) -> str:
            return "csetty-vscode-prep-comp1511"

        @staticmethod
        def vscode_cache_ready(
            _profile: str, _extensions: tuple[str, ...], _commit: str
        ) -> bool:
            return True

        @staticmethod
        def vscode_server_ready(_container: str, _commit: str) -> bool:
            return False

    vscode = VSCodeManager(paths, PrepareRuntime())  # type: ignore[arg-type]
    monkeypatch.setattr(vscode, "install_host_extension", lambda _profile: None)
    monkeypatch.setattr(vscode, "_record_attach_trust", lambda _profile: None)
    monkeypatch.setattr(vscode, "_base_args", lambda _profile: ["code"])
    monkeypatch.setattr(
        vscode,
        "version",
        lambda: {"version": "1.131.0", "commit": "e" * 40, "architecture": "arm64"},
    )
    monkeypatch.setattr(
        "csetty.vscode.subprocess.run",
        lambda *_args, **_kwargs: SimpleNamespace(returncode=0, stderr=""),
    )
    monotonic_values = iter((0.0, 0.0, 2.0))
    monkeypatch.setattr("csetty.vscode.time.monotonic", lambda: next(monotonic_values))
    monkeypatch.setattr("csetty.vscode.time.sleep", lambda _seconds: None)

    with pytest.raises(ToolUnavailableError, match="did not finish preparing"):
        vscode.prepare("comp1511", wait_seconds=1)
