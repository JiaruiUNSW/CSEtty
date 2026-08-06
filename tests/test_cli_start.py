from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest
from test_pack import make_pack

import csetty.cli as cli
from csetty.models import AttemptMode, AttemptState, WorkspaceKind
from csetty.pack import load_pack
from csetty.paths import AppPaths
from csetty.storage import Store


class RuntimeStub:
    @staticmethod
    def image_for_profile(profile: str) -> str:
        return f"csetty/{profile}:dev"

    @staticmethod
    def image_exists(_image: str) -> bool:
        return True

    @staticmethod
    def ensure_profile_ready(_profile: str) -> None:
        return None

    @staticmethod
    def profile_provenance(profile: str) -> dict[str, object]:
        return {
            "image": {"id": f"sha256:csetty/{profile}:dev"},
            "judge_image": {"id": f"sha256:csetty/{profile}-judge:dev"},
            "tools": {},
        }


def test_start_records_an_attempt_owned_pack_snapshot(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_root = make_pack(tmp_path / "source-pack")
    (source_root / "solutions").mkdir()
    (source_root / "solutions" / "q1.c").write_text("secret", encoding="utf-8")
    source_pack = load_pack(source_root)
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    runtime = RuntimeStub()

    monkeypatch.setattr(cli.PackRepository, "get", lambda _self, _selector: source_pack)
    monkeypatch.setattr(cli, "_components", lambda: (paths, store, runtime, object()))
    monkeypatch.setattr(cli, "_launch_working", lambda **_kwargs: 0)

    args = cli._parser().parse_args(
        ["start", source_pack.id, "--editor", "terminal", "--skip-reading"]
    )
    assert cli._start(args) == 0

    (attempt,) = store.list_attempts()
    frozen_root = paths.attempts / attempt.id / "pack"
    assert Path(attempt.pack_path) == frozen_root
    assert frozen_root.is_dir()
    assert not (frozen_root / "solutions").exists()
    assert load_pack(frozen_root).digest == attempt.pack_digest == source_pack.digest

    (source_root / "starter" / "q1.c").write_text("changed\n", encoding="utf-8")
    assert cli._attempt_pack(attempt).digest == attempt.pack_digest
    assert (frozen_root / "starter" / "q1.c").read_text(encoding="utf-8") != "changed\n"


def test_working_launch_opens_isolated_code_and_companion(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    pack = load_pack(make_pack(tmp_path / "pack"))
    paths = AppPaths.discover(tmp_path / "state")
    store = Store(paths)
    now = datetime.now(UTC)
    attempt = store.create_attempt(
        pack_id=pack.id,
        pack_version=pack.version,
        pack_path=pack.root,
        pack_digest=pack.digest,
        course=pack.course,
        profile=pack.profile,
        mode=AttemptMode.EXAM,
        timed=True,
        created_at=now,
        workspace_kind=WorkspaceKind.VOLUME,
        workspace_ref="test-volume",
        image=pack.environment.image,
        editor="code",
        candidate_id="z1234567",
    )
    attempt = store.transition(
        attempt.id,
        AttemptState.WORKING,
        at=now,
        deadline_at=now + timedelta(hours=3),
    )
    events: list[str] = []

    class LaunchRuntime:
        @staticmethod
        def start_container(*_args: object, **_kwargs: object) -> None:
            events.append("container")

    class LaunchVSCode:
        @staticmethod
        def offline_ready(_profile: str) -> tuple[bool, str]:
            return True, "ready"

        @staticmethod
        def attach(_attempt: object) -> None:
            events.append("code")

    monkeypatch.setattr(cli, "ensure_supervisor", lambda *_args: events.append("supervisor"))
    monkeypatch.setattr(
        cli,
        "launch_companion",
        lambda *_args: events.append("page") or SimpleNamespace(url="http://127.0.0.1/test/"),
    )

    assert (
        cli._launch_working(
            attempt=attempt,
            pack=pack,
            paths=paths,
            store=store,
            runtime=LaunchRuntime(),  # type: ignore[arg-type]
            vscode=LaunchVSCode(),  # type: ignore[arg-type]
        )
        == 0
    )
    assert events == ["container", "supervisor", "page", "code"]
