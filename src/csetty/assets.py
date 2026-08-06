from __future__ import annotations

import sysconfig
from pathlib import Path

from .errors import ToolUnavailableError


def assets_root() -> Path:
    """Locate source-checkout assets or their wheel-installed data-files copy."""
    source_root = Path(__file__).resolve().parents[2]
    installed_root = Path(sysconfig.get_path("data")) / "share" / "csetty"
    for candidate in (source_root, installed_root):
        required = (
            candidate / "compose.yaml",
            candidate / "checksums.lock",
            candidate / "docker" / "Dockerfile.interactive",
            candidate / "docker" / "Dockerfile.judge",
        )
        if all(path.is_file() for path in required) and (candidate / "packs").is_dir():
            return candidate
    raise ToolUnavailableError(
        "CSEExamTTY runtime assets are missing; reinstall the package from a complete wheel"
    )
