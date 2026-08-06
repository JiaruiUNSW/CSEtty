from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from .docker_runtime import DockerRuntime
from .errors import ToolUnavailableError, ValidationError
from .models import Attempt
from .paths import AppPaths
from .util import atomic_write

_HOST_EXTENSION = "ms-vscode-remote.remote-containers"
_ATTACH_TRUST_KEY = "userConfirmedAttachToContainerRequiresTrust"
_REMOTE_EXTENSIONS = {
    "comp1511": ("ms-vscode.cpptools",),
    "comp1521": ("ms-vscode.cpptools", "xavc.xavc-mipsy-features"),
}


class VSCodeManager:
    def __init__(
        self, paths: AppPaths, runtime: DockerRuntime, *, executable: str = "code"
    ) -> None:
        self.paths = paths
        self.runtime = runtime
        self.executable = executable

    def _executable(self) -> str:
        found = shutil.which(self.executable)
        if found:
            return found
        mac = Path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")
        if mac.is_file():
            return str(mac)
        raise ToolUnavailableError("VS Code command-line launcher 'code' was not found")

    def _profile_paths(self, profile: str) -> tuple[Path, Path, Path]:
        if profile not in _REMOTE_EXTENSIONS:
            raise ValidationError(f"unsupported VS Code profile: {profile}")
        root = self.paths.vscode / profile
        return root / "user-data", root / "extensions", root / "readiness.json"

    def version(self) -> dict[str, str]:
        executable = self._executable()
        result = subprocess.run(
            [executable, "--version"], capture_output=True, text=True, check=False
        )
        if result.returncode != 0:
            raise ToolUnavailableError(result.stderr.strip() or "VS Code version check failed")
        lines = result.stdout.splitlines()
        return {
            "version": lines[0] if lines else "unknown",
            "commit": lines[1] if len(lines) > 1 else "unknown",
            "architecture": lines[2] if len(lines) > 2 else "unknown",
        }

    def _base_args(self, profile: str) -> list[str]:
        user_data, extensions, _manifest = self._profile_paths(profile)
        user_data.mkdir(parents=True, exist_ok=True)
        extensions.mkdir(parents=True, exist_ok=True)
        return [
            self._executable(),
            "--user-data-dir",
            str(user_data),
            "--extensions-dir",
            str(extensions),
            "--sync",
            "off",
        ]

    @staticmethod
    def _isolated_environment() -> dict[str, str]:
        environment = os.environ.copy()
        for name in (
            "GIT_ASKPASS",
            "SSH_ASKPASS",
            "GH_TOKEN",
            "GITHUB_TOKEN",
            "VSCODE_GIT_ASKPASS_NODE",
            "VSCODE_GIT_ASKPASS_MAIN",
            "VSCODE_GIT_IPC_HANDLE",
        ):
            environment.pop(name, None)
        # If SSH_AUTH_SOCK is removed, the macOS app can rediscover the agent.
        # An explicit empty value reaches Dev Containers but fails its truthy
        # socket check, so no forwarding bridge is created.
        environment["SSH_AUTH_SOCK"] = ""
        return environment

    def _write_settings(self, profile: str) -> None:
        user_data, _extensions, _manifest = self._profile_paths(profile)
        settings = {
            "chat.disableAIFeatures": True,
            "telemetry.telemetryLevel": "off",
            "window.title": (
                "CSEExamTTY ISOLATED EXAM — ${activeEditorShort}${separator}${rootName}"
            ),
            "window.restoreWindows": "none",
            "workbench.startupEditor": "none",
            "workbench.colorCustomizations": {
                "statusBar.background": "#7A1F1F",
                "statusBar.foreground": "#FFFFFF",
                "titleBar.activeBackground": "#7A1F1F",
                "titleBar.activeForeground": "#FFFFFF",
            },
            "extensions.autoUpdate": False,
            "extensions.autoCheckUpdates": False,
            "git.enabled": False,
            "git.autofetch": False,
            "settingsSync.ignoredSettings": ["*"],
            "dev.containers.defaultExtensions": list(_REMOTE_EXTENSIONS[profile]),
            "dev.containers.copyGitConfig": False,
            "dev.containers.gitCredentialHelperConfigLocation": "none",
            "dev.containers.dockerCredentialHelper": False,
            "dev.containers.githubCLILoginWithToken": False,
            "dev.containers.forwardWSLServices": False,
            "dev.containers.mountWaylandSocket": False,
            "remote.autoForwardPorts": False,
            "remote.restoreForwardedPorts": False,
            "remote.containers.copyGitConfig": False,
            "remote.containers.dotfiles.repository": "",
            "dotfiles.repository": "",
        }
        atomic_write(
            user_data / "User" / "settings.json",
            (json.dumps(settings, indent=2, sort_keys=True) + "\n").encode(),
        )

    @staticmethod
    def attached_uri(container_name: str, folder: str = "/home/student/exam") -> str:
        descriptor = (
            json.dumps({"containerName": f"/{container_name}"}, separators=(",", ":"))
            .encode()
            .hex()
        )
        return f"vscode-remote://attached-container+{descriptor}{folder}"

    def install_host_extension(self, profile: str) -> None:
        self._write_settings(profile)
        command = [*self._base_args(profile), "--install-extension", _HOST_EXTENSION]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
            env=self._isolated_environment(),
        )
        if result.returncode != 0:
            raise ToolUnavailableError(
                f"could not install the isolated Dev Containers extension: {result.stderr.strip()}"
            )

    def _host_extension_cached(self, profile: str) -> bool:
        _user_data, extensions, _manifest = self._profile_paths(profile)
        if not extensions.is_dir():
            return False
        prefix = f"{_HOST_EXTENSION.lower()}-"
        return any(
            child.is_dir()
            and (
                child.name.lower() == _HOST_EXTENSION.lower()
                or child.name.lower().startswith(prefix)
            )
            and (child / "package.json").is_file()
            for child in extensions.iterdir()
        )

    def _attach_trust_recorded(self, profile: str) -> bool:
        user_data, _extensions, _manifest = self._profile_paths(profile)
        database = user_data / "User" / "globalStorage" / "state.vscdb"
        if not database.is_file():
            return False
        try:
            with sqlite3.connect(database) as connection:
                row = connection.execute(
                    "SELECT value FROM ItemTable WHERE key = ?",
                    (_HOST_EXTENSION,),
                ).fetchone()
            if row is None:
                return False
            value = json.loads(row[0])
        except (OSError, sqlite3.Error, json.JSONDecodeError, TypeError):
            return False
        return isinstance(value, dict) and value.get(_ATTACH_TRUST_KEY) is True

    def _record_attach_trust(self, profile: str) -> None:
        """Record trust only inside the profile reserved for CSEExamTTY containers.

        Dev Containers otherwise shows a first-use modal before it performs any
        Docker operation. That modal can be hidden behind another VS Code window,
        leaving the remote resolver pending indefinitely. The isolated profile is
        never used to attach to arbitrary containers, so prepare records the same
        one-time acknowledgement before opening the preparation container.
        """
        user_data, _extensions, _manifest = self._profile_paths(profile)
        database = user_data / "User" / "globalStorage" / "state.vscdb"
        database.parent.mkdir(parents=True, exist_ok=True)
        try:
            with sqlite3.connect(database, timeout=10) as connection:
                connection.execute(
                    "CREATE TABLE IF NOT EXISTS ItemTable "
                    "(key TEXT UNIQUE ON CONFLICT REPLACE, value BLOB)"
                )
                row = connection.execute(
                    "SELECT value FROM ItemTable WHERE key = ?",
                    (_HOST_EXTENSION,),
                ).fetchone()
                value: dict[str, Any] = {}
                if row is not None:
                    loaded = json.loads(row[0])
                    if not isinstance(loaded, dict):
                        raise ToolUnavailableError(
                            "isolated VS Code extension state has an unexpected format"
                        )
                    value = loaded
                value[_ATTACH_TRUST_KEY] = True
                connection.execute(
                    "INSERT OR REPLACE INTO ItemTable(key, value) VALUES (?, ?)",
                    (_HOST_EXTENSION, json.dumps(value, sort_keys=True)),
                )
                connection.execute("PRAGMA user_version = 1")
        except (OSError, sqlite3.Error, json.JSONDecodeError, TypeError) as exc:
            raise ToolUnavailableError(
                "could not initialise the isolated VS Code container trust state"
            ) from exc

    def attach(self, attempt: Attempt, *, wait_seconds: int = 60) -> None:
        self._write_settings(attempt.profile)
        version = self.version()
        uri = self.attached_uri(attempt.container_name)
        command = [*self._base_args(attempt.profile), "--new-window", "--folder-uri", uri]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env=self._isolated_environment(),
        )
        if result.returncode != 0:
            raise ToolUnavailableError(
                result.stderr.strip() or "VS Code could not attach to the container"
            )
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            if self.runtime.vscode_server_ready(
                attempt.container_name,
                version["commit"],
            ):
                return
            time.sleep(1)
        raise ToolUnavailableError(
            "VS Code accepted the open request but its Server did not start in the "
            f"exam container within {wait_seconds} seconds; rerun csetty prepare "
            f"--profile {attempt.profile} and inspect the isolated Dev Containers log"
        )

    def show_preparation_complete(self, profile: str) -> None:
        workspace = self.paths.cache / "vscode-prep" / profile
        workspace.mkdir(parents=True, exist_ok=True)
        summary = workspace / "PREPARATION_COMPLETE.md"
        atomic_write(
            summary,
            (
                f"# {profile.upper()} preparation complete\n\n"
                "The VS Code Server and approved remote extensions are cached for offline use.\n\n"
                "This is an isolated CSEExamTTY profile. Your normal VS Code settings and "
                "extensions were not changed.\n\n"
                "This preparation window is no longer connected to a container and can be closed. "
                "Start an attempt with `csetty start`, or reopen one with `csetty code`.\n"
            ).encode(),
        )
        result = subprocess.run(
            [*self._base_args(profile), "--reuse-window", str(workspace)],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env=self._isolated_environment(),
        )
        if result.returncode != 0:
            raise ToolUnavailableError(
                result.stderr.strip() or "VS Code could not leave the preparation container"
            )
        # The CLI returns when the open request is accepted, before the window has fully detached.
        time.sleep(2)

    def prepare(self, profile: str, *, wait_seconds: int = 180) -> dict[str, Any]:
        self.install_host_extension(profile)
        self._record_attach_trust(profile)
        version = self.version()
        container = self.runtime.prepare_vscode_container(profile)
        uri = self.attached_uri(container)
        result = subprocess.run(
            [*self._base_args(profile), "--new-window", "--folder-uri", uri],
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env=self._isolated_environment(),
        )
        if result.returncode != 0:
            raise ToolUnavailableError(result.stderr.strip() or "VS Code cache preparation failed")
        extensions = _REMOTE_EXTENSIONS[profile]
        deadline = time.monotonic() + wait_seconds
        while time.monotonic() < deadline:
            if self.runtime.vscode_cache_ready(
                profile, extensions, version["commit"]
            ) and self.runtime.vscode_server_ready(container, version["commit"]):
                break
            time.sleep(2)
        else:
            raise ToolUnavailableError(
                "VS Code Server/extensions did not finish preparing; keep the "
                "preparation window open and run csetty prepare again"
            )
        image_provenance = self.runtime.image_provenance(self.runtime.image_for_profile(profile))
        _user_data, _extensions, manifest = self._profile_paths(profile)
        readiness = {
            "schema_version": 1,
            "profile": profile,
            "code": version,
            "host_extension": _HOST_EXTENSION,
            "remote_extensions": list(extensions),
            "image": self.runtime.image_for_profile(profile),
            "image_id": image_provenance["image"]["id"],
        }
        atomic_write(manifest, (json.dumps(readiness, indent=2, sort_keys=True) + "\n").encode())
        self.show_preparation_complete(profile)
        self.runtime.stop_vscode_prepare_container(profile)
        return readiness

    def offline_ready(self, profile: str) -> tuple[bool, str]:
        _user_data, _extensions, manifest = self._profile_paths(profile)
        if not manifest.is_file():
            return False, f"VS Code profile {profile} has not been prepared"
        try:
            readiness = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return False, f"VS Code readiness manifest is invalid for {profile}"
        if readiness.get("schema_version") != 1 or readiness.get("profile") != profile:
            return False, f"VS Code readiness manifest is invalid for {profile}"
        if readiness.get("host_extension") != _HOST_EXTENSION:
            return False, f"isolated Dev Containers metadata is invalid for {profile}"
        if readiness.get("remote_extensions") != list(_REMOTE_EXTENSIONS[profile]):
            return False, f"approved remote-extension metadata is invalid for {profile}"
        if not self._host_extension_cached(profile):
            return False, f"isolated Dev Containers extension is not cached for {profile}"
        if not self._attach_trust_recorded(profile):
            return False, f"isolated container trust is not prepared for {profile}"
        version = self.version()
        if readiness.get("code", {}).get("commit") != version["commit"]:
            return False, "VS Code was updated after preparation; rerun csetty prepare"
        if not self.runtime.image_exists(self.runtime.image_for_profile(profile)):
            return False, f"course image is missing for {profile}"
        current_image = self.runtime.image_provenance(self.runtime.image_for_profile(profile))
        if readiness.get("image_id") != current_image["image"]["id"]:
            return False, "course image changed after VS Code preparation; rerun csetty prepare"
        if not self.runtime.vscode_cache_ready(
            profile,
            _REMOTE_EXTENSIONS[profile],
            version["commit"],
        ):
            return False, f"VS Code Server or remote extensions are not cached for {profile}"
        return True, "ready"

    @staticmethod
    def extensions(profile: str) -> Sequence[str]:
        return _REMOTE_EXTENSIONS[profile]
