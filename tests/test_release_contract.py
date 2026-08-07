from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_VERSION = "0.1.0a3"
EXPECTED_LICENSE_EXPRESSION = "Apache-2.0 AND CC-BY-NC-ND-4.0"
EXPECTED_ASSESSMENT_LICENSE = "CC BY-NC-ND 4.0"


def test_public_alpha_version_and_mixed_license_metadata_match() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]
    package_init = (ROOT / "src" / "csetty" / "__init__.py").read_text(encoding="utf-8")

    assert project["name"] == "cseexamtty"
    assert project["version"] == EXPECTED_VERSION
    assert project["license"] == EXPECTED_LICENSE_EXPRESSION
    assert f'__version__ = "{EXPECTED_VERSION}"' in package_init
    assert set(project["license-files"]) == {
        "LICENSE",
        "NOTICE",
        "LICENSES.md",
        "ASSESSMENT_MATERIALS_LICENSE.md",
    }


def test_file_level_license_map_covers_all_original_assessment_trees() -> None:
    licence_map = (ROOT / "LICENSES.md").read_text(encoding="utf-8")
    assessment = (ROOT / "ASSESSMENT_MATERIALS_LICENSE.md").read_text(encoding="utf-8")
    for marker in ("src/csetty/**", "packs/**", "question_bank/**"):
        assert marker in licence_map
    assert EXPECTED_ASSESSMENT_LICENSE in licence_map
    assert "creativecommons.org/licenses/by-nc-nd/4.0/legalcode" in assessment

    manifests = (
        *(ROOT / "packs").glob("*/pack.toml"),
        *(ROOT / "question_bank").glob("*/bank.toml"),
    )
    assert manifests
    for manifest in manifests:
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        assert data["license"] == EXPECTED_ASSESSMENT_LICENSE


def test_public_release_candidate_is_versioned_and_fails_closed() -> None:
    approval = tomllib.loads(
        (ROOT / "release" / "public-release.toml").read_text(encoding="utf-8")
    )
    assert approval["release"] == {
        "version": EXPECTED_VERSION,
        "channel": "alpha",
        "artifact_policy": "source-only-no-prebuilt-images",
        "owner_approved": False,
        "approval_date": "PENDING_OWNER_APPROVAL",
    }
    run_url = re.compile(r"https://github\.com/JiaruiUNSW/CSEtty/actions/runs/[0-9]+")
    for gate in ("cross_platform_acceptance", "multiarch_acceptance"):
        value = approval["gates"][gate]
        assert value == "PENDING_0.1.0a3_CI_RUN" or run_url.fullmatch(value)


def test_ci_has_native_arm64_live_acceptance_and_no_artifact_upload() -> None:
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "docker-arm64-live:" in workflow
    assert "runs-on: ubuntu-24.04-arm" in workflow
    assert "scripts/docker_acceptance.py --profile ${{ matrix.profile }}" in workflow
    assert "actions/upload-artifact" not in workflow
    assert "cache-to=type=registry" not in workflow
    assert "--push" not in workflow
