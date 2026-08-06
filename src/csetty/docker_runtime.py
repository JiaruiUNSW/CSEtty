from __future__ import annotations

import base64
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import tempfile
from collections.abc import Iterable, Iterator, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .assets import assets_root
from .errors import CSETTYError, StateError, ToolUnavailableError, ValidationError
from .models import Attempt, WorkspaceKind
from .pack import Pack, Question, TestGroup, copy_pack_files
from .paths import AppPaths
from .util import atomic_write, canonical_json, resolve_under, safe_relative_path

PINNED_MIPSY_ORACLE_COMMIT = "61f96b38626c30c2ead7925486304f163ec56b2b"
CSETTY_MIPS_DISTRIBUTION = "csetty-mips"
CSETTY_MIPS_VERSION = "0.1.1"
CSETTY_MIPS_PACKAGE_TREE_SHA256 = "2f96c71a9c7384327bd89d9addc055976183ba8b58b5d0597fe3a10d8800fdcb"


@dataclass(frozen=True)
class CommandResult:
    argv: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str


class DockerRuntime:
    def __init__(self, paths: AppPaths, *, executable: str = "docker") -> None:
        self.paths = paths
        self.executable = executable
        self.assets_root = assets_root()

    def _run(
        self,
        arguments: Sequence[str],
        *,
        input_text: str | None = None,
        check: bool = True,
        timeout: float | None = None,
    ) -> CommandResult:
        argv = (self.executable, *arguments)
        try:
            completed = subprocess.run(
                argv,
                input=input_text,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
        except FileNotFoundError as exc:
            raise ToolUnavailableError("Docker CLI was not found") from exc
        except subprocess.TimeoutExpired as exc:
            raise ToolUnavailableError(f"Docker command timed out: {' '.join(argv)}") from exc
        result = CommandResult(
            argv=argv,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )
        if check and result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip() or "unknown Docker error"
            raise ToolUnavailableError(f"Docker command failed: {detail}")
        return result

    def doctor(self) -> dict[str, Any]:
        version = self._run(["--version"], check=False, timeout=10)
        info = self._run(["info", "--format", "{{json .ServerVersion}}"], check=False, timeout=10)
        return {
            "cli": version.returncode == 0,
            "cli_version": version.stdout.strip() or version.stderr.strip(),
            "daemon": info.returncode == 0 and bool(info.stdout.strip().strip('"')),
            "server_version": info.stdout.strip().strip('"'),
            "error": "" if info.returncode == 0 else info.stderr.strip(),
        }

    @staticmethod
    def image_for_profile(profile: str) -> str:
        if profile not in {"comp1511", "comp1521"}:
            raise ValidationError(f"unsupported image profile: {profile}")
        return f"csetty/{profile}:dev"

    @staticmethod
    def judge_image_for_profile(profile: str) -> str:
        if profile not in {"comp1511", "comp1521"}:
            raise ValidationError(f"unsupported image profile: {profile}")
        return f"csetty/{profile}-judge:dev"

    def image_exists(self, image: str) -> bool:
        return self._run(["image", "inspect", image], check=False, timeout=15).returncode == 0

    def pinned_attempt_image(self, attempt: Attempt) -> str:
        image_metadata = attempt.provenance.get("image")
        recorded_id = image_metadata.get("id") if isinstance(image_metadata, Mapping) else None
        if isinstance(recorded_id, str) and recorded_id:
            if not self.image_exists(recorded_id):
                raise ToolUnavailableError(
                    f"the image recorded for attempt {attempt.id} is no longer available: "
                    f"{recorded_id}"
                )
            return recorded_id
        if not self.image_exists(attempt.image):
            raise ToolUnavailableError(
                f"course image is not prepared: {attempt.image}; run csetty prepare first"
            )
        return attempt.image

    def pinned_judge_image(self, attempt: Attempt) -> str:
        image_metadata = attempt.provenance.get("judge_image")
        recorded_id = image_metadata.get("id") if isinstance(image_metadata, Mapping) else None
        if isinstance(recorded_id, str) and recorded_id:
            if not self.image_exists(recorded_id):
                raise ToolUnavailableError(
                    f"the judge image recorded for attempt {attempt.id} is no longer available: "
                    f"{recorded_id}"
                )
            return recorded_id
        self.ensure_profile_ready(attempt.profile)
        return self.judge_image_for_profile(attempt.profile)

    def image_provenance(self, image: str) -> dict[str, Any]:
        inspected = self._run(["image", "inspect", image], timeout=30)
        try:
            records = json.loads(inspected.stdout)
            record = records[0]
        except (json.JSONDecodeError, IndexError, KeyError, TypeError) as exc:
            raise ToolUnavailableError("Docker returned invalid image metadata") from exc
        script = r"""
import json
import subprocess

commands = {
    "python": ["python3", "--version"],
    "gcc": ["gcc", "--version"],
    "clang": ["clang", "--version"],
    "dcc": ["dcc", "--version"],
    "make": ["make", "--version"],
    "gdb": ["gdb", "--version"],
    "valgrind": ["valgrind", "--version"],
    "mipsy": ["mipsy", "--version"],
}
tools = {}
for name, argv in commands.items():
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=10, check=False)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        continue
    output = (result.stdout or result.stderr).strip().splitlines()
    tools[name] = {
        "version": output[0] if output else "unknown",
        "returncode": result.returncode,
    }
print(json.dumps(tools, sort_keys=True))
"""
        versions = self._run(
            [
                "run",
                "--rm",
                "--network",
                "none",
                "--read-only",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges",
                "--user",
                "student",
                image,
                "python3",
                "-c",
                script,
            ],
            timeout=60,
        )
        try:
            tools = json.loads(versions.stdout)
        except json.JSONDecodeError as exc:
            raise ToolUnavailableError("course image returned invalid toolchain metadata") from exc
        config = record.get("Config") or {}
        return {
            "image": {
                "reference": image,
                "id": str(record.get("Id", "")),
                "repo_digests": list(record.get("RepoDigests") or []),
                "architecture": str(record.get("Architecture", "")),
                "os": str(record.get("Os", "")),
                "created": str(record.get("Created", "")),
                "labels": dict(config.get("Labels") or {}),
            },
            "tools": tools,
        }

    @contextmanager
    def _staged_build_context(self) -> Iterator[Path]:
        self.paths.cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="csetty-image-context-", dir=self.paths.cache
        ) as temporary:
            context = Path(temporary)
            docker = context / "docker"
            docker.mkdir()
            for filename in (
                "Dockerfile.interactive",
                "Dockerfile.judge",
                "build-dcc.sh",
                "exam-command",
                "mipsy-command",
            ):
                shutil.copy2(self.assets_root / "docker" / filename, docker / filename)
            for filename in ("compose.yaml", "toolchains.lock", "checksums.lock"):
                shutil.copy2(self.assets_root / filename, context / filename)
            shutil.copy2(
                self.assets_root / "THIRD_PARTY_NOTICES.md",
                context / "THIRD_PARTY_NOTICES.md",
            )
            shutil.copy2(self.assets_root / "LICENSE", context / "LICENSE")
            shutil.copy2(self.assets_root / "NOTICE", context / "NOTICE")
            shutil.copytree(
                Path(__file__).resolve().parent,
                context / "src" / "csetty",
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
            )
            mips_package, mips_package_license, mips_notice, mips_source_files = (
                self._csetty_mips_distribution_files()
            )
            mips_root = context / "build-inputs" / "csetty-mips"
            target_package = mips_root / "csetty_mips"
            for relative in mips_source_files:
                target = target_package / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(mips_package / relative, target)
            shutil.copy2(mips_package_license, mips_root / "LICENSE")
            shutil.copy2(mips_notice, mips_root / "NOTICE")
            atomic_write(
                context / ".dockerignore",
                b"__pycache__/\n*.py[cod]\n.git/\npacks/\nquestion_bank/\ntests/\ndocs/\n",
                mode=0o644,
            )
            yield context

    @staticmethod
    def _csetty_mips_distribution_files() -> tuple[Path, Path, Path, tuple[Path, ...]]:
        try:
            distribution = importlib.metadata.distribution(CSETTY_MIPS_DISTRIBUTION)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ToolUnavailableError(
                "csetty-mips is not installed; reinstall CSEExamTTY dependencies"
            ) from exc
        if distribution.version != CSETTY_MIPS_VERSION:
            raise ToolUnavailableError(
                "csetty-mips version mismatch: "
                f"expected {CSETTY_MIPS_VERSION}, found {distribution.version}"
            )
        package_root = Path(str(distribution.locate_file("csetty_mips"))).resolve()
        if not (package_root / "__init__.py").is_file():
            raise ToolUnavailableError("installed csetty-mips package files are missing")
        distribution_files = distribution.files or ()
        source_manifest: list[Path] = []
        for item in distribution_files:
            if (
                not item.parts
                or item.parts[0] != "csetty_mips"
                or "__pycache__" in item.parts
                or item.suffix in {".pyc", ".pyo"}
            ):
                continue
            relative = Path(*item.parts[1:])
            candidate = Path(str(distribution.locate_file(item)))
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or candidate.is_symlink()
                or not candidate.is_file()
                or not candidate.resolve().is_relative_to(package_root)
            ):
                raise ToolUnavailableError(
                    f"installed csetty-mips contains an unsafe package file: {item}"
                )
            source_manifest.append(relative)
        source_files = tuple(sorted(source_manifest))
        if Path("__init__.py") not in source_files or Path("machine.py") not in source_files:
            raise ToolUnavailableError("installed csetty-mips source manifest is incomplete")
        notice_path = package_root / "NOTICE"
        if not notice_path.is_file():
            raise ToolUnavailableError("installed csetty-mips NOTICE is missing")
        license_path = next(
            (
                Path(str(distribution.locate_file(item)))
                for item in distribution_files
                if item.name == "LICENSE" and ".dist-info/licenses/" in item.as_posix()
            ),
            None,
        )
        if license_path is None or license_path.is_symlink() or not license_path.is_file():
            raise ToolUnavailableError("installed csetty-mips MPL-2.0 license is missing")
        license_path = license_path.resolve()
        digest = hashlib.sha256()
        entries = [
            (f"csetty_mips/{relative.as_posix()}", package_root / relative)
            for relative in source_files
        ]
        entries.append(("LICENSE", license_path))
        for logical_name, path in sorted(entries):
            digest.update(logical_name.encode())
            digest.update(b"\0")
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
        installed_digest = digest.hexdigest()
        if installed_digest != CSETTY_MIPS_PACKAGE_TREE_SHA256:
            raise ToolUnavailableError(
                "csetty-mips package content digest mismatch: "
                f"expected {CSETTY_MIPS_PACKAGE_TREE_SHA256}, found {installed_digest}"
            )
        return package_root, license_path, notice_path, source_files

    @staticmethod
    def _build_context_digest(context: Path) -> str:
        digest = hashlib.sha256()
        for path in sorted(context.rglob("*")):
            if not path.is_file() or path.is_symlink():
                continue
            relative = path.relative_to(context).as_posix().encode()
            digest.update(relative)
            digest.update(b"\0")
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(chunk)
            digest.update(b"\0")
        return digest.hexdigest()

    def stage_build_context(self, destination: Path) -> str:
        destination = destination.expanduser().resolve()
        if destination.exists() and any(destination.iterdir()):
            raise ValidationError("source-build context destination must be empty")
        destination.mkdir(parents=True, exist_ok=True)
        with self._staged_build_context() as context:
            shutil.copytree(context, destination, dirs_exist_ok=True)
        return self._build_context_digest(destination)

    def _image_receipt_path(self, profile: str) -> Path:
        self.image_for_profile(profile)
        return self.paths.cache / "images" / f"{profile}.json"

    def _write_image_receipt(self, profile: str, context_digest: str) -> None:
        images = {
            "interactive": self.image_for_profile(profile),
            "judge": self.judge_image_for_profile(profile),
        }
        records: dict[str, dict[str, str]] = {}
        for role, reference in images.items():
            image_id = self._image_id(reference)
            labels_result = self._run(
                ["image", "inspect", "--format", "{{json .Config.Labels}}", reference],
                timeout=15,
            )
            try:
                labels = json.loads(labels_result.stdout)
            except json.JSONDecodeError as exc:
                raise ToolUnavailableError(
                    f"Docker returned invalid labels for {reference}"
                ) from exc
            if not isinstance(labels, dict):
                raise ToolUnavailableError(f"Docker returned no labels for {reference}")
            if labels.get("io.csetty.profile") != profile:
                raise ToolUnavailableError(
                    f"prepared image has the wrong profile label: {reference}"
                )
            if labels.get("io.csetty.image.role") != role:
                raise ToolUnavailableError(f"prepared image has the wrong role label: {reference}")
            records[role] = {"reference": reference, "id": image_id}
        receipt = {
            "schema_version": 1,
            "profile": profile,
            "build_context_sha256": context_digest,
            "images": records,
        }
        path = self._image_receipt_path(profile)
        path.parent.mkdir(parents=True, exist_ok=True)
        atomic_write(path, canonical_json(receipt), mode=0o600)

    def _read_image_receipt(self, profile: str) -> dict[str, Any]:
        path = self._image_receipt_path(profile)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ToolUnavailableError(
                f"{profile} images have not been prepared; run csetty prepare"
            ) from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise ToolUnavailableError(f"invalid prepared-image receipt: {path}") from exc
        if not isinstance(payload, dict) or payload.get("schema_version") != 1:
            raise ToolUnavailableError(f"invalid prepared-image receipt: {path}")
        return payload

    def ensure_profile_ready(self, profile: str) -> None:
        receipt = self._read_image_receipt(profile)
        if receipt.get("profile") != profile:
            raise ToolUnavailableError("prepared-image receipt has the wrong profile")
        with self._staged_build_context() as context:
            current_digest = self._build_context_digest(context)
        if receipt.get("build_context_sha256") != current_digest:
            raise ToolUnavailableError(
                f"{profile} source-build inputs changed; rerun csetty prepare"
            )
        images = receipt.get("images")
        if not isinstance(images, dict):
            raise ToolUnavailableError("prepared-image receipt is missing image records")
        for role, reference in (
            ("interactive", self.image_for_profile(profile)),
            ("judge", self.judge_image_for_profile(profile)),
        ):
            record = images.get(role)
            expected_id = record.get("id") if isinstance(record, dict) else None
            if not isinstance(expected_id, str) or not expected_id:
                raise ToolUnavailableError(f"prepared-image receipt is missing the {role} ID")
            if self._image_id(reference) != expected_id:
                raise ToolUnavailableError(
                    f"local {role} image no longer matches csetty prepare: {reference}"
                )

    def profile_provenance(self, profile: str) -> dict[str, Any]:
        self.ensure_profile_ready(profile)
        provenance = self.image_provenance(self.image_for_profile(profile))
        receipt = self._read_image_receipt(profile)
        judge_record = receipt["images"]["judge"]
        provenance["judge_image"] = dict(judge_record)
        provenance["source_build"] = {
            "context_sha256": receipt["build_context_sha256"],
            "receipt_schema": receipt["schema_version"],
        }
        return provenance

    @staticmethod
    def validate_mipsy_oracle_source(mipsy_source: Path) -> str:
        source = mipsy_source.expanduser().resolve()
        if not (source / "Cargo.toml").is_file() or not (source / "Cargo.lock").is_file():
            raise ValidationError("mipsy oracle source must contain Cargo.toml and Cargo.lock")
        revision = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        dirty = subprocess.run(
            ["git", "-C", str(source), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        )
        if revision.returncode != 0 or dirty.returncode != 0:
            raise ValidationError("mipsy oracle source must be a valid Git checkout")
        if dirty.stdout.strip():
            raise ValidationError(
                "mipsy oracle source must be clean so its commit identifies the comparison"
            )
        actual_commit = revision.stdout.strip()
        if actual_commit != PINNED_MIPSY_ORACLE_COMMIT:
            raise ValidationError(
                "mipsy oracle source is at "
                f"{actual_commit or 'an unknown commit'}; "
                f"expected {PINNED_MIPSY_ORACLE_COMMIT}"
            )
        return actual_commit

    def build_image(self, profile: str) -> str:
        image = self.image_for_profile(profile)
        with self._staged_build_context() as context:
            context_digest = self._build_context_digest(context)
            arguments = [
                "compose",
                "--profile",
                "build",
                "--project-directory",
                str(context),
                "--file",
                str(context / "compose.yaml"),
                "build",
                f"{profile}-interactive",
                f"{profile}-judge",
            ]
            self._run(arguments, timeout=1800)
            self._write_image_receipt(profile, context_digest)
        return image

    def _container_exists(self, name: str) -> bool:
        return self._run(["container", "inspect", name], check=False, timeout=10).returncode == 0

    def _container_running(self, name: str) -> bool:
        result = self._run(
            ["container", "inspect", "--format", "{{.State.Running}}", name],
            check=False,
            timeout=10,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"

    def _container_image_id(self, name: str) -> str | None:
        result = self._run(
            ["container", "inspect", "--format", "{{.Image}}", name],
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return None
        image_id = result.stdout.strip()
        return image_id or None

    def _image_id(self, image: str) -> str:
        result = self._run(
            ["image", "inspect", "--format", "{{.Id}}", image],
            check=False,
            timeout=15,
        )
        image_id = result.stdout.strip()
        if result.returncode != 0 or not image_id:
            raise ToolUnavailableError(f"course image is not prepared: {image}")
        return image_id

    def _volume_exists(self, name: str) -> bool:
        return self._run(["volume", "inspect", name], check=False, timeout=10).returncode == 0

    def _ensure_owned_volume(self, name: str, image: str) -> bool:
        created = not self._volume_exists(name)
        if created:
            self._run(["volume", "create", name], timeout=30)
            self._run(
                [
                    "run",
                    "--rm",
                    "--user",
                    "0",
                    "--mount",
                    f"type=volume,source={name},target=/target",
                    image,
                    "chown",
                    "1000:1000",
                    "/target",
                ],
                timeout=30,
            )
        return created

    def _ensure_vscode_volume(self, name: str, profile: str, image: str) -> None:
        created = self._ensure_owned_volume(name, image)
        prepared = f"csetty-vscode-prep-{profile}"
        if created and self._volume_exists(prepared):
            self._run(
                [
                    "run",
                    "--rm",
                    "--user",
                    "0",
                    "--mount",
                    f"type=volume,source={prepared},target=/source,readonly",
                    "--mount",
                    f"type=volume,source={name},target=/target",
                    image,
                    "cp",
                    "-a",
                    "/source/.",
                    "/target/",
                ],
                timeout=120,
            )
            self._run(
                [
                    "run",
                    "--rm",
                    "--user",
                    "0",
                    "--mount",
                    f"type=volume,source={name},target=/target",
                    image,
                    "chown",
                    "-R",
                    "1000:1000",
                    "/target",
                ],
                timeout=120,
            )

    def bridge_directory(self, attempt_id: str) -> Path:
        return self.paths.bridge / attempt_id

    def _prepare_bridge(self, attempt: Attempt) -> Path:
        bridge = self.bridge_directory(attempt.id)
        bridge.mkdir(parents=True, exist_ok=True)
        bridge.chmod(0o755)
        for child in (bridge / "requests", bridge / "responses"):
            child.mkdir(parents=True, exist_ok=True)
            child.chmod(0o777)
        processed = bridge / "processed"
        processed.mkdir(parents=True, exist_ok=True)
        processed.chmod(0o700)
        atomic_write(
            bridge / "session.json",
            canonical_json(
                {
                    "protocol": 1,
                    "attempt_id": attempt.id,
                    "session_token": attempt.session_token,
                }
            ),
            mode=0o644,
        )
        return bridge

    def _prepare_resources(self, attempt: Attempt, pack: Pack) -> Path:
        destination = self.paths.attempts / attempt.id / "resources"
        if destination.exists():
            return destination
        destination.mkdir(parents=True, exist_ok=True)
        paper_source = resolve_under(pack.root, pack.paper)
        paper_target = destination / "paper" / Path(pack.paper).name
        paper_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(paper_source, paper_target)
        for resource in pack.resources:
            source = resolve_under(pack.root, resource.path)
            target = destination / "resources" / Path(resource.path).name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        return destination

    def start_container(self, attempt: Attempt, pack: Pack, *, network: str = "none") -> None:
        pinned_image = self.pinned_attempt_image(attempt)
        if self._container_exists(attempt.container_name):
            if not self._container_running(attempt.container_name):
                self._run(["start", attempt.container_name], timeout=30)
            return
        bridge = self._prepare_bridge(attempt)
        resources = self._prepare_resources(attempt, pack)
        vscode_arguments: list[str] = []
        if attempt.editor == "code":
            vscode_volume = f"csetty-vscode-{attempt.id[:12]}"
            self._ensure_vscode_volume(vscode_volume, attempt.profile, pinned_image)
            vscode_arguments = [
                "--mount",
                f"type=volume,source={vscode_volume},target=/home/student/.vscode-server",
            ]
        if attempt.workspace_kind is WorkspaceKind.VOLUME:
            self._ensure_owned_volume(attempt.workspace_ref, pinned_image)
            workspace_mount = (
                f"type=volume,source={attempt.workspace_ref},target=/home/student/exam"
            )
        else:
            workspace = Path(attempt.workspace_ref).expanduser().resolve()
            workspace.mkdir(parents=True, exist_ok=True)
            workspace_mount = f"type=bind,source={workspace},target=/home/student/exam"

        arguments = [
            "run",
            "--detach",
            "--name",
            attempt.container_name,
            "--hostname",
            "exam",
            "--label",
            f"io.csetty.attempt={attempt.id}",
            "--network",
            network,
            "--cpus",
            str(pack.environment.cpus),
            "--memory",
            f"{pack.environment.memory_mb}m",
            "--pids-limit",
            str(pack.environment.pids),
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,nosuid,nodev,exec,size=256m",
            "--tmpfs",
            "/home/student:rw,nosuid,nodev,uid=1000,gid=1000,mode=0755",
            "--mount",
            workspace_mount,
            *vscode_arguments,
            "--mount",
            (
                f"type=bind,source={bridge / 'session.json'},"
                "target=/run/csetty-bridge/session.json,readonly"
            ),
            "--mount",
            f"type=bind,source={bridge / 'requests'},target=/run/csetty-bridge/requests",
            "--mount",
            f"type=bind,source={bridge / 'responses'},target=/run/csetty-bridge/responses",
            "--mount",
            f"type=bind,source={resources},target=/exam-resources,readonly",
            "--env",
            f"CSETTY_ATTEMPT_ID={attempt.id}",
            "--env",
            f"CSETTY_SESSION_TOKEN={attempt.session_token}",
            "--env",
            f"CSETTY_PROFILE={attempt.profile}",
            "--env",
            f"CSETTY_CANDIDATE_ID={attempt.candidate_id or 'student'}",
            "--env",
            "HOME=/home/student",
            "--user",
            "student",
            pinned_image,
            "sleep",
            "infinity",
        ]
        self._run(arguments, timeout=60)
        self._initialize_workspace(attempt, pack)

    def prepare_vscode_container(self, profile: str) -> str:
        image = self.image_for_profile(profile)
        if not self.image_exists(image):
            raise ToolUnavailableError(f"course image is not prepared: {image}")
        name = f"csetty-vscode-prep-{profile}"
        volume = name
        self._ensure_owned_volume(volume, image)
        container_exists = self._container_exists(name)
        if container_exists and self._container_image_id(name) != self._image_id(image):
            # A preparation container is disposable, while its named cache volume is
            # deliberately persistent. Recreate only the container when the course
            # image changes so prepare never validates a stale image by accident.
            self._run(["container", "rm", "--force", name], timeout=30)
            container_exists = False
        if container_exists:
            # Successful preparation quarantines this container. A later explicit
            # prepare operation is the only path that reconnects it for updates.
            self._run(["network", "connect", "bridge", name], check=False, timeout=15)
            if not self._container_running(name):
                self._run(["start", name], timeout=30)
            return name
        workspace = self.paths.cache / "vscode-prep" / profile
        workspace.mkdir(parents=True, exist_ok=True)
        self._run(
            [
                "run",
                "--detach",
                "--name",
                name,
                "--network",
                "bridge",
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges",
                "--read-only",
                "--tmpfs",
                "/tmp:rw,nosuid,nodev,size=256m",
                "--tmpfs",
                "/home/student:rw,nosuid,nodev,uid=1000,gid=1000,mode=0755",
                "--mount",
                f"type=bind,source={workspace},target=/home/student/exam",
                "--mount",
                f"type=volume,source={volume},target=/home/student/.vscode-server",
                "--env",
                "HOME=/home/student",
                "--user",
                "student",
                image,
                "sleep",
                "infinity",
            ],
            timeout=60,
        )
        return name

    def stop_vscode_prepare_container(self, profile: str) -> None:
        name = f"csetty-vscode-prep-{profile}"
        if self._container_running(name):
            # The Dev Containers window may automatically restart its attached container.
            # Remove the preparation-only network first so such a restart remains offline.
            self._run(["network", "disconnect", "bridge", name], check=False, timeout=15)
            self._run(["stop", "--timeout", "2", name], timeout=15)

    def vscode_cache_ready(
        self,
        profile: str,
        extension_ids: Sequence[str],
        server_commit: str,
    ) -> bool:
        volume = f"csetty-vscode-prep-{profile}"
        image = self.image_for_profile(profile)
        if not self._volume_exists(volume) or not self.image_exists(image):
            return False
        script = r"""
from pathlib import Path
import sys

root = Path("/cache")
commit = sys.argv[1]
wanted = [value.lower() for value in sys.argv[2:]]
server_candidates = (
    root / "bin" / commit / "bin" / "code-server",
    root / "cli" / "servers" / f"Stable-{commit}" / "server" / "bin" / "code-server",
    root / "cli" / "servers" / f"Stable-{commit}" / "server" / "bin" / "remote-cli" / "code",
)
server_ready = bool(commit) and any(path.is_file() for path in server_candidates)
extensions = root / "extensions"
names = (
    [path.name.lower() for path in extensions.iterdir() if path.is_dir()]
    if extensions.is_dir()
    else []
)
extensions_ready = all(
    any(name == extension or name.startswith(extension + "-") for name in names)
    for extension in wanted
)
raise SystemExit(0 if server_ready and extensions_ready else 1)
"""
        result = self._run(
            [
                "run",
                "--rm",
                "--network",
                "none",
                "--read-only",
                "--mount",
                f"type=volume,source={volume},target=/cache,readonly",
                "--user",
                "student",
                image,
                "python3",
                "-c",
                script,
                server_commit,
                *extension_ids,
            ],
            check=False,
            timeout=30,
        )
        return result.returncode == 0

    def vscode_server_ready(self, container_name: str, server_commit: str) -> bool:
        """Return whether the exact cached VS Code Server is running in a container."""
        if not server_commit or not self._container_running(container_name):
            return False
        script = r"""
from pathlib import Path
import sys

needle = (
    f"/home/student/.vscode-server/bin/{sys.argv[1]}/out/server-main.js"
).encode()
for process in Path("/proc").iterdir():
    if not process.name.isdigit():
        continue
    try:
        command = (process / "cmdline").read_bytes().replace(b"\0", b" ")
    except OSError:
        continue
    if needle in command:
        raise SystemExit(0)
raise SystemExit(1)
"""
        result = self._run(
            [
                "exec",
                "--user",
                "student",
                container_name,
                "python3",
                "-c",
                script,
                server_commit,
            ],
            check=False,
            timeout=10,
        )
        return result.returncode == 0

    def _initialized(self, attempt: Attempt) -> bool:
        result = self._run(
            [
                "exec",
                "--user",
                "student",
                attempt.container_name,
                "python3",
                "-m",
                "csetty.container_inspect",
                ".csetty-initialized",
            ],
            check=False,
            timeout=10,
        )
        return result.returncode == 0

    def _initialize_workspace(self, attempt: Attempt, pack: Pack) -> None:
        if self._initialized(attempt):
            return
        if attempt.workspace_kind is WorkspaceKind.BIND:
            root = Path(attempt.workspace_ref)
            existing = [item for item in root.iterdir() if item.name != ".DS_Store"]
            if existing:
                raise StateError("bind workspace must be empty when an attempt is initialized")
        for question in pack.questions:
            for starter in question.starter_files:
                self.write_workspace_file(
                    attempt,
                    Pack.starter_target(starter).as_posix(),
                    pack.starter_source(starter).read_bytes(),
                    overwrite=False,
                )
        settings = {
            "chat.disableAIFeatures": True,
            "telemetry.telemetryLevel": "off",
            "extensions.autoUpdate": False,
            "extensions.autoCheckUpdates": False,
            "git.enabled": False,
            "git.autofetch": False,
            "terminal.integrated.env.linux": {
                "GIT_ASKPASS": None,
                "SSH_ASKPASS": None,
                "SSH_AUTH_SOCK": None,
            },
            "C_Cpp.default.compilerPath": "/usr/bin/clang",
            "C_Cpp.default.cStandard": "c11",
            "terminal.integrated.defaultProfile.linux": "bash",
        }
        recommendations = ["ms-vscode.cpptools"]
        if attempt.profile == "comp1521":
            recommendations.append("xavc.xavc-mipsy-features")
        self.write_workspace_file(
            attempt,
            ".vscode/settings.json",
            (json.dumps(settings, indent=2, sort_keys=True) + "\n").encode(),
            overwrite=False,
        )
        self.write_workspace_file(
            attempt,
            ".vscode/extensions.json",
            (json.dumps({"recommendations": recommendations}, indent=2) + "\n").encode(),
            overwrite=False,
        )
        self.write_workspace_file(attempt, ".csetty-initialized", b"1\n", overwrite=False)

    def write_workspace_file(
        self,
        attempt: Attempt,
        relative: str,
        data: bytes,
        *,
        overwrite: bool,
    ) -> str:
        safe = safe_relative_path(relative, label="workspace path")
        payload = json.dumps(
            {"content": base64.b64encode(data).decode(), "overwrite": overwrite},
            sort_keys=True,
        )
        response = self._run(
            [
                "exec",
                "--interactive",
                "--user",
                "student",
                attempt.container_name,
                "python3",
                "-m",
                "csetty.container_write",
                safe.as_posix(),
            ],
            input_text=payload,
            check=False,
            timeout=30,
        )
        try:
            result = json.loads(response.stdout)
        except json.JSONDecodeError as exc:
            raise CSETTYError(
                f"container returned invalid write result: {response.stderr}"
            ) from exc
        if response.returncode != 0 or not result.get("ok"):
            raise ValidationError(result.get("error", "container could not write starter file"))
        return str(result["status"])

    def read_workspace_files(
        self, attempt: Attempt, relative_paths: Iterable[str]
    ) -> dict[str, bytes]:
        paths = tuple(relative_paths)
        for value in paths:
            safe_relative_path(value, label="submission path")
        response = self._run(
            [
                "exec",
                "--user",
                "student",
                attempt.container_name,
                "python3",
                "-m",
                "csetty.container_inspect",
                *paths,
            ],
            check=False,
            timeout=30,
        )
        try:
            payload = json.loads(response.stdout)
        except json.JSONDecodeError as exc:
            raise CSETTYError(
                f"container returned invalid snapshot data: {response.stderr}"
            ) from exc
        if response.returncode != 0 or not payload.get("ok"):
            raise ValidationError(payload.get("error", "container could not read submission files"))
        return {item["path"]: base64.b64decode(item["content"]) for item in payload["files"]}

    def stop_container(self, attempt: Attempt) -> None:
        if self._container_running(attempt.container_name):
            self._run(["stop", "--timeout", "2", attempt.container_name], check=False, timeout=15)

    def broadcast_terminal(self, attempt: Attempt, message: str) -> int:
        """Write a fixed host-originated notice to every open student pseudo-terminal."""
        script = r"""
import glob
import os
import stat
import sys

payload = ("\r\n" + sys.argv[1] + "\r\n").encode()
written = 0
for path in glob.glob("/dev/pts/[0-9]*"):
    try:
        if not stat.S_ISCHR(os.stat(path).st_mode):
            continue
        descriptor = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
        try:
            os.write(descriptor, payload)
            written += 1
        finally:
            os.close(descriptor)
    except OSError:
        pass
print(written)
"""
        result = self._run(
            [
                "exec",
                "--user",
                "student",
                attempt.container_name,
                "python3",
                "-c",
                script,
                message,
            ],
            check=False,
            timeout=10,
        )
        if result.returncode != 0:
            return 0
        try:
            return max(0, int(result.stdout.strip()))
        except ValueError:
            return 0

    def attach_terminal(self, attempt: Attempt) -> int:
        argv = [
            self.executable,
            "exec",
            "--interactive",
            "--tty",
            "--user",
            "student",
            "--workdir",
            "/home/student/exam",
            attempt.container_name,
            "bash",
            "--login",
        ]
        return subprocess.run(argv, check=False).returncode

    def export_workspace(self, attempt: Attempt, destination: Path) -> None:
        destination = destination.expanduser().resolve()
        if destination.exists() and any(destination.iterdir()):
            raise ValidationError("export destination must be empty")
        destination.mkdir(parents=True, exist_ok=True)
        if attempt.workspace_kind is WorkspaceKind.BIND:
            source = Path(attempt.workspace_ref).resolve()
            for current, directory_names, file_names in os.walk(source, followlinks=False):
                current_path = Path(current)
                relative_root = current_path.relative_to(source)
                for directory_name in directory_names:
                    directory = current_path / directory_name
                    if directory.is_symlink():
                        raise ValidationError(
                            f"export refused symlink: {directory.relative_to(source)}"
                        )
                    (destination / relative_root / directory_name).mkdir(
                        parents=True, exist_ok=True
                    )
                for file_name in file_names:
                    file_path = current_path / file_name
                    relative = file_path.relative_to(source)
                    if relative_root == Path(".") and file_name.startswith(".csetty-"):
                        continue
                    if file_path.is_symlink() or not file_path.is_file():
                        raise ValidationError(f"export refused non-regular file: {relative}")
                    resolved = file_path.resolve(strict=True)
                    if not resolved.is_relative_to(source):
                        raise ValidationError(f"export path escapes workspace: {relative}")
                    target = destination / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(resolved, target)
            return
        self._run(
            ["cp", f"{attempt.container_name}:/home/student/exam/.", str(destination)], timeout=60
        )
        (destination / ".csetty-initialized").unlink(missing_ok=True)
        for exported in destination.rglob("*"):
            if exported.is_symlink():
                raise ValidationError(
                    f"export refused symlink: {exported.relative_to(destination)}"
                )

    @staticmethod
    def _serialize_group(pack: Pack, group: TestGroup) -> dict[str, Any]:
        tests = []
        for test in group.tests:
            expected_files = []
            for expected in test.expected_files:
                content = expected.content
                if expected.source is not None:
                    content = resolve_under(pack.root, expected.source).read_text(encoding="utf-8")
                expected_files.append({"path": expected.path, "content": content})
            tests.append(
                {
                    "id": test.id,
                    "argv": list(test.argv),
                    "stdin": test.stdin,
                    "expected_stdout": test.expected_stdout,
                    "expected_stderr": test.expected_stderr,
                    "expected_exit": test.expected_exit,
                    "timeout_ms": test.timeout_ms,
                    "comparison": test.comparison,
                    "selected_characters": test.selected_characters,
                    "fixtures": [
                        {"source": fixture.source, "path": fixture.path}
                        for fixture in test.fixtures
                    ],
                    "expected_files": expected_files,
                }
            )
        return {"id": group.id, "visibility": group.visibility.value, "tests": tests}

    @staticmethod
    def _copy_judge_pack(pack: Pack, destination: Path) -> None:
        """Copy test assets without exposing author-only reference solutions."""
        copy_pack_files(pack.root, destination)

    def run_judge(
        self,
        *,
        attempt: Attempt,
        pack: Pack,
        question: Question,
        snapshot: Path,
        groups: Sequence[TestGroup],
    ) -> dict[str, Any]:
        config = {
            "source_dir": "/submission",
            "pack_dir": "/pack",
            "build_argv": list(question.build_argv),
            "build_timeout_ms": 30_000,
            "output_limit_kb": pack.environment.output_limit_kb,
            "groups": [self._serialize_group(pack, group) for group in groups],
        }
        self.paths.cache.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(
            prefix="csetty-judge-pack-", dir=self.paths.cache
        ) as judge_pack_name:
            judge_pack = Path(judge_pack_name)
            self._copy_judge_pack(pack, judge_pack)
            arguments = [
                "run",
                "--rm",
                "--interactive",
                "--network",
                "none",
                "--cpus",
                str(pack.environment.cpus),
                "--memory",
                f"{pack.environment.memory_mb}m",
                "--pids-limit",
                str(pack.environment.pids),
                "--cap-drop",
                "ALL",
                "--security-opt",
                "no-new-privileges",
                "--read-only",
                "--tmpfs",
                "/tmp:rw,nosuid,nodev,exec,size=256m",
                "--tmpfs",
                "/judge:rw,nosuid,nodev,exec,uid=1000,gid=1000,size=512m",
                "--mount",
                f"type=bind,source={snapshot.resolve()},target=/submission,readonly",
                "--mount",
                f"type=bind,source={judge_pack},target=/pack,readonly",
                "--user",
                "student",
                "--env",
                "TMPDIR=/judge",
                self.pinned_judge_image(attempt),
                "python3",
                "-m",
                "csetty.judge",
            ]
            result = self._run(
                arguments,
                input_text=json.dumps(config),
                check=False,
                timeout=max(60, sum(len(group.tests) for group in groups) * 10),
            )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise CSETTYError(
                f"judge returned invalid JSON (exit {result.returncode}): {result.stderr}"
            ) from exc
        if result.returncode not in {0, 5}:
            raise CSETTYError(f"judge container failed: {result.stderr.strip()}")
        if not isinstance(payload, dict) or not all(isinstance(key, str) for key in payload):
            raise CSETTYError("judge returned a JSON value that is not an object")
        return {str(key): value for key, value in payload.items()}
