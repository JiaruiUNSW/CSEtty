from __future__ import annotations

import tomllib
from importlib import metadata
from pathlib import Path

import csetty_mips

from csetty.docker_runtime import (
    CSETTY_MIPS_PACKAGE_TREE_SHA256,
    CSETTY_MIPS_VERSION,
)

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.1.1"
EXPECTED_COMMIT = "33410078667ad67942c6700d73411fc31be00c8f"
EXPECTED_PACKAGE_TREE_SHA256 = "2f96c71a9c7384327bd89d9addc055976183ba8b58b5d0597fe3a10d8800fdcb"


def test_mips_engine_is_an_external_release_with_pinned_source_provenance() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    lock = tomllib.loads((ROOT / "toolchains.lock").read_text(encoding="utf-8"))
    requirements = project["project"]["dependencies"]

    assert "csetty-mips==0.1.1" in requirements
    assert lock["csetty_mips"] == {
        "version": EXPECTED_VERSION,
        "source": "https://github.com/JiaruiUNSW/CSEtty-MIPS.git",
        "tag": "v0.1.1",
        "commit": EXPECTED_COMMIT,
        "package_tree_sha256": EXPECTED_PACKAGE_TREE_SHA256,
        "license": "MPL-2.0",
        "entrypoint": "python3 -m csetty_mips",
    }
    assert CSETTY_MIPS_VERSION == EXPECTED_VERSION
    assert CSETTY_MIPS_PACKAGE_TREE_SHA256 == EXPECTED_PACKAGE_TREE_SHA256
    assert not (ROOT / "src" / "csetty_mips").exists()


def test_installed_mips_distribution_matches_the_pin() -> None:
    distribution = metadata.distribution("csetty-mips")
    project_urls = distribution.metadata.get_all("Project-URL") or []

    assert distribution.version == EXPECTED_VERSION
    assert csetty_mips.__version__ == EXPECTED_VERSION
    assert (
        "Repository, https://github.com/JiaruiUNSW/CSEtty-MIPS.git"
        in project_urls
    )
    assert csetty_mips.__file__ is not None
    assert not Path(csetty_mips.__file__).resolve().is_relative_to(ROOT / "src")
