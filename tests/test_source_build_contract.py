from __future__ import annotations

import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_source_build_locks_match_both_dockerfiles() -> None:
    toolchains = tomllib.loads((ROOT / "toolchains.lock").read_text(encoding="utf-8"))
    checksums = tomllib.loads((ROOT / "checksums.lock").read_text(encoding="utf-8"))
    base = toolchains["base"]
    dcc = toolchains["dcc"]
    debian = checksums["debian"]
    dcc_source = checksums["dcc_source"]

    assert checksums["schema_version"] == 1
    assert base["image"] == f"{debian['tag']}@{debian['index_digest']}"
    assert dcc["version"] == dcc_source["version"]
    assert dcc["source_url"] == dcc_source["url"]
    assert dcc["source_sha256"] == dcc_source["sha256"]
    assert dcc["source_commit"] == dcc_source["commit"]

    for filename in ("Dockerfile.interactive", "Dockerfile.judge"):
        dockerfile = (ROOT / "docker" / filename).read_text(encoding="utf-8")
        assert base["image"] in dockerfile
        assert dcc["source_url"] in dockerfile
        assert dcc["source_sha256"] in dockerfile
        assert "sh /tmp/build-dcc.sh" in dockerfile
        assert "io.csetty.dcc.build=\"verified-source\"" in dockerfile
        assert "COPY NOTICE /usr/share/doc/csetty/NOTICE" in dockerfile
        assert "/releases/download/" not in dockerfile

    builder = (ROOT / "docker" / "build-dcc.sh").read_text(encoding="utf-8")
    assert "make dcc" in builder
    assert "Built locally from verified source" in builder
    assert "/out/usr/local/lib/csetty/dcc-upstream" in builder

    wrapper = (ROOT / "docker" / "dcc-command").read_text(encoding="utf-8")
    assert "wsl2" in wrapper.lower()
    assert "mode=valgrind" in wrapper
    assert 'exec "$upstream" --valgrind "$@"' in wrapper


def test_windows_checkout_keeps_linux_build_entrypoints_lf_only() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8").splitlines()
    assert "*.sh text eol=lf" in attributes
    assert "docker/Dockerfile.* text eol=lf" in attributes
    assert "docker/dcc-command text eol=lf" in attributes
    assert "docker/exam-command text eol=lf" in attributes
    assert "docker/mipsy-command text eol=lf" in attributes

    for relative in (
        "docker/build-dcc.sh",
        "docker/Dockerfile.interactive",
        "docker/Dockerfile.judge",
        "docker/dcc-command",
        "docker/exam-command",
        "docker/mipsy-command",
    ):
        assert b"\r\n" not in (ROOT / relative).read_bytes()


def test_compose_declares_only_local_interactive_and_judge_builds() -> None:
    compose = (ROOT / "compose.yaml").read_text(encoding="utf-8")
    expected = {
        "comp1511-interactive": "csetty/comp1511:dev",
        "comp1521-interactive": "csetty/comp1521:dev",
        "comp1511-judge": "csetty/comp1511-judge:dev",
        "comp1521-judge": "csetty/comp1521-judge:dev",
    }
    for service, image in expected.items():
        assert f"  {service}:" in compose
        assert f"    image: {image}" in compose
    assert "registry" not in compose.lower()


def test_ci_stages_external_mips_source_and_publishes_no_build_artifacts() -> None:
    workflows = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / ".github" / "workflows").glob("*.yml"))
    )
    assert "scripts/stage_source_build.py" in workflows
    assert "Dockerfile.interactive" in workflows
    assert "Dockerfile.judge" in workflows
    assert "actions/upload-artifact" not in workflows
    assert "--push" not in workflows
    assert "cache-to=type=registry" not in workflows
    assert "src/csetty_mips" not in workflows


def test_bundled_manifests_use_the_selected_cc_license_label() -> None:
    manifests = (
        *(ROOT / "packs").glob("*/pack.toml"),
        *(ROOT / "question_bank").glob("*/bank.toml"),
    )
    assert manifests
    for manifest in manifests:
        data = tomllib.loads(manifest.read_text(encoding="utf-8"))
        assert data["license"] == "CC BY-NC-ND 4.0"
