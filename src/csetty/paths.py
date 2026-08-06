from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from platformdirs import user_state_path


@dataclass(frozen=True)
class AppPaths:
    root: Path
    database: Path
    objects: Path
    attempts: Path
    reports: Path
    vscode: Path
    bridge: Path
    cache: Path

    @classmethod
    def discover(cls, override: Path | None = None) -> AppPaths:
        configured = os.environ.get("CSETTY_STATE_DIR")
        root = override or (Path(configured) if configured else user_state_path("csetty"))
        root = root.expanduser().resolve()
        return cls(
            root=root,
            database=root / "csetty.sqlite3",
            objects=root / "objects" / "sha256",
            attempts=root / "attempts",
            reports=root / "reports",
            vscode=root / "vscode",
            bridge=root / "bridge",
            cache=root / "cache",
        )

    def ensure(self) -> None:
        for directory in (
            self.root,
            self.objects,
            self.attempts,
            self.reports,
            self.vscode,
            self.bridge,
            self.cache,
        ):
            directory.mkdir(parents=True, exist_ok=True)
