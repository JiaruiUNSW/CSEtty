from __future__ import annotations

import argparse
import hashlib
import re
import sys
import tarfile
import tomllib
import zipfile
from email.parser import BytesParser
from email.policy import default
from pathlib import Path
from typing import Any

_CHUNK_SIZE = 1024 * 1024
_PUBLIC_GATES = (
    "project_license",
    "dcc_source_distribution",
    "csetty_mips_provenance_and_license",
    "vscode_and_extensions_terms",
    "pack_content_license",
    "branding_and_name_review",
    "cross_platform_acceptance",
    "multiarch_acceptance",
)
_ASSESSMENT_LICENSE = "CC BY-NC-ND 4.0"
_LICENSE_EXPRESSION = "Apache-2.0 AND CC-BY-NC-ND-4.0"
_SOURCE_ONLY_POLICY = "source-only-no-prebuilt-images"
_REQUIRED_RELEASE_FILES = (
    "LICENSE",
    "NOTICE",
    "LICENSES.md",
    "ASSESSMENT_MATERIALS_LICENSE.md",
    "TRADEMARKS.md",
    "THIRD_PARTY_NOTICES.md",
)
_TRUSTED_PUBLISH_WORKFLOW = Path(".github/workflows/publish-pypi.yml")
_TRUSTED_PUBLISH_ACTION = (
    "pypa/gh-action-pypi-publish@dc37677b2e1c63e2034f94d8a5b11f265b73ba33"
)
_PUBLISH_PATTERNS = (
    re.compile(r"\bdocker\s+(?:buildx\s+build[^\n]*--push|push)\b", re.IGNORECASE),
    re.compile(r"\b(?:twine\s+upload|uv\s+publish)\b", re.IGNORECASE),
    re.compile(r"pypa/gh-action-pypi-publish", re.IGNORECASE),
    re.compile(r"actions/upload-artifact", re.IGNORECASE),
)


def _digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_CHUNK_SIZE), b""):
            result.update(chunk)
    return result.hexdigest()


def _load_toml(path: Path) -> dict[str, Any]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise SystemExit(f"could not read {path}: {exc}") from exc


def _verify_dcc_source(project_root: Path, dist: Path) -> Path:
    dcc = _load_toml(project_root / "toolchains.lock").get("dcc")
    if not isinstance(dcc, dict):
        raise SystemExit("toolchains.lock does not contain [dcc]")
    version = str(dcc.get("version", ""))
    expected = str(dcc.get("source_sha256", ""))
    source = dist / f"dcc-{version}-source.tar.gz"
    if not source.is_file():
        raise SystemExit(
            f"missing local DCC source verification copy: {source}; "
            "run scripts/fetch_dcc_source.py first"
        )
    actual = _digest(source)
    if actual != expected:
        raise SystemExit(
            f"DCC source verification digest mismatch: expected {expected}, found {actual}"
        )
    return source


def _project_metadata(project_root: Path) -> tuple[str, str]:
    project = _load_toml(project_root / "pyproject.toml").get("project")
    if not isinstance(project, dict):
        raise SystemExit("pyproject.toml does not contain [project]")
    version = str(project.get("version", "")).strip()
    license_expression = str(project.get("license", "")).strip()
    if not version:
        raise SystemExit("pyproject.toml does not declare a project version")
    if license_expression != _LICENSE_EXPRESSION:
        raise SystemExit(
            "pyproject.toml must declare the mixed distribution licence expression "
            f"{_LICENSE_EXPRESSION!r}"
        )
    return version, license_expression


def _verify_wheel(project_root: Path, dist: Path) -> Path:
    wheels = sorted(dist.glob("cseexamtty-*.whl"))
    if len(wheels) != 1:
        raise SystemExit(f"expected exactly one cseexamtty wheel in {dist}, found {len(wheels)}")
    wheel = wheels[0]
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        metadata_names = [name for name in names if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise SystemExit("wheel must contain exactly one dist-info/METADATA file")
        metadata = BytesParser(policy=default).parsebytes(archive.read(metadata_names[0]))
    project_version, license_expression = _project_metadata(project_root)
    if metadata.get("Version") != project_version:
        raise SystemExit(
            f"wheel version mismatch: expected {project_version}, found {metadata.get('Version')}"
        )
    if metadata.get("License-Expression") != license_expression:
        raise SystemExit("wheel metadata does not contain the reviewed licence expression")
    for filename in _REQUIRED_RELEASE_FILES:
        if not any(name.endswith(f"share/csetty/{filename}") for name in names):
            raise SystemExit(f"wheel does not contain {filename}")
    # Original worked solutions stay in the host package so a finished local
    # attempt can display the exact snapshotted explanation/reference. The
    # student-pack and Docker-context gates enforce the actual trust boundary.
    author_materials = [name for name in names if "/packs/" in name and "/solutions/" in name]
    if not any("/solutions/explanations/" in name for name in author_materials):
        raise SystemExit("wheel is missing host-only worked solutions")
    if not any("/solutions/reference/" in name for name in author_materials):
        raise SystemExit("wheel is missing host-only reference implementations")
    forbidden = [name for name in names if Path(name).name.lower() == "mipsy"]
    if forbidden:
        raise SystemExit(f"wheel contains an upstream mipsy binary: {forbidden!r}")
    return wheel


def _verify_sdist(project_root: Path, dist: Path) -> Path:
    project_version, _ = _project_metadata(project_root)
    sdists = sorted(dist.glob("cseexamtty-*.tar.gz"))
    if len(sdists) != 1:
        raise SystemExit(f"expected exactly one cseexamtty sdist in {dist}, found {len(sdists)}")
    sdist = sdists[0]
    expected_root = f"cseexamtty-{project_version}"
    with tarfile.open(sdist, mode="r:gz") as archive:
        members = archive.getmembers()
    unsafe = [
        member.name
        for member in members
        if member.issym()
        or member.islnk()
        or Path(member.name).is_absolute()
        or ".." in Path(member.name).parts
    ]
    if unsafe:
        raise SystemExit(f"sdist contains unsafe archive members: {unsafe[:5]!r}")
    names = {member.name for member in members if member.isfile()}
    for filename in _REQUIRED_RELEASE_FILES:
        if f"{expected_root}/{filename}" not in names:
            raise SystemExit(f"sdist does not contain {filename}")
    forbidden_suffixes = (".deb", ".vsix", ".oci")
    forbidden = [name for name in names if name.lower().endswith(forbidden_suffixes)]
    if forbidden:
        raise SystemExit(f"sdist contains forbidden prebuilt artifacts: {forbidden[:5]!r}")
    return sdist


def _verify_trusted_publish_workflow(project_root: Path, path: Path, text: str) -> None:
    relative_path = path.relative_to(project_root)
    if relative_path != _TRUSTED_PUBLISH_WORKFLOW:
        raise SystemExit(f"trusted publishing is only allowed in {_TRUSTED_PUBLISH_WORKFLOW}")

    required_fragments = (
        "on:\n  release:\n    types: [published]",
        "permissions: {}",
        "github.repository == 'JiaruiUNSW/CSEtty'",
        "github.event.action == 'published'",
        "startsWith(github.event.release.tag_name, 'v')",
        "environment:\n      name: pypi\n      url: https://pypi.org/p/cseexamtty",
        "permissions:\n      contents: read\n      id-token: write",
        'GH_TOKEN: ${{ github.token }}',
        'gh release download "$RELEASE_TAG"',
        '--pattern "cseexamtty-${release_version}-py3-none-any.whl"',
        '--pattern "cseexamtty-${release_version}.tar.gz"',
        '--pattern "cseexamtty-python.cdx.json"',
        '--pattern "SHA256SUMS"',
        '[[ ! "$RELEASE_TAG" =~ ^v[0-9]+\\.[0-9]+\\.[0-9]+',
        "if actual_files != expected_files:",
        "if set(checksums) != expected_payloads:",
        'hashlib.file_digest(stream, "sha256")',
        'wheel_metadata.get("Version") != version',
        'sdist_metadata.get("Version") != version',
        'sbom.get("bomFormat") != "CycloneDX"',
        "install -m 0644",
        "packages-dir: pypi-dist/",
        "attestations: true",
        "print-hash: true",
    )
    missing = [fragment for fragment in required_fragments if fragment not in text]
    if missing:
        raise SystemExit(
            "trusted publish workflow is missing required fail-closed controls: "
            + ", ".join(repr(fragment) for fragment in missing)
        )

    job_headers = re.findall(r"(?m)^  ([A-Za-z][A-Za-z0-9_-]*):\s*$", text.split("jobs:", 1)[-1])
    if job_headers != ["publish"]:
        raise SystemExit(
            "trusted publish workflow must contain only the isolated publish job; "
            f"found {job_headers!r}"
        )
    action_uses = re.findall(r"(?m)^\s*uses:\s*([^\s#]+)", text)
    if action_uses != [_TRUSTED_PUBLISH_ACTION]:
        raise SystemExit(
            "trusted publish workflow must use only the full-SHA-pinned PyPI action; "
            f"found {action_uses!r}"
        )
    if text.count("id-token: write") != 1:
        raise SystemExit("trusted publish workflow must grant id-token: write exactly once")
    if text.count("permissions: {}") != 1:
        raise SystemExit("trusted publish workflow must deny top-level permissions")
    if text.count("run: |") != 1:
        raise SystemExit("trusted publish workflow must contain one asset-validation run step")

    forbidden_patterns = (
        re.compile(r"(?m)^\s+(?:push|pull_request|workflow_dispatch|schedule):"),
        re.compile(r"\$\{\{\s*secrets\."),
        re.compile(r"(?im)^\s+(?:password|user|repository-url|skip-existing):"),
        re.compile(r"actions/checkout@", re.IGNORECASE),
        re.compile(r"\b(?:curl|wget|git|sudo)\b", re.IGNORECASE),
        re.compile(r"\b(?:pip|uv|python(?:3)?)\s+(?:build|install|publish)\b", re.IGNORECASE),
    )
    for pattern in forbidden_patterns:
        if pattern.search(text):
            raise SystemExit(
                "trusted publish workflow contains a forbidden trigger, credential, "
                f"checkout, download, or build command: {pattern.pattern}"
            )


def _verify_private_workflows(project_root: Path) -> None:
    workflows = project_root / ".github" / "workflows"
    trusted_publish_path = project_root / _TRUSTED_PUBLISH_WORKFLOW
    if not trusted_publish_path.is_file():
        raise SystemExit(f"missing trusted publish workflow: {_TRUSTED_PUBLISH_WORKFLOW}")
    for path in sorted(workflows.glob("*.y*ml")):
        text = path.read_text(encoding="utf-8")
        if path == trusted_publish_path:
            _verify_trusted_publish_workflow(project_root, path, text)
        for pattern in _PUBLISH_PATTERNS:
            if pattern.search(text):
                if path == trusted_publish_path and pattern.pattern.startswith(
                    "pypa/gh-action-pypi-publish"
                ):
                    continue
                raise SystemExit(
                    f"private release gate found a publishing command in {path}: {pattern.pattern}"
                )


def _verify_source_build_contract(project_root: Path) -> None:
    required = (
        project_root / "compose.yaml",
        project_root / "checksums.lock",
        project_root / "docker" / "Dockerfile.interactive",
        project_root / "docker" / "Dockerfile.judge",
        project_root / "docker" / "build-dcc.sh",
        project_root / "NOTICE",
    )
    missing = [str(path.relative_to(project_root)) for path in required if not path.is_file()]
    if missing:
        raise SystemExit("source-build contract is missing: " + ", ".join(missing))

    toolchains = _load_toml(project_root / "toolchains.lock")
    checksums = _load_toml(project_root / "checksums.lock")
    base = toolchains.get("base")
    dcc = toolchains.get("dcc")
    csetty_mips = toolchains.get("csetty_mips")
    debian = checksums.get("debian")
    dcc_source = checksums.get("dcc_source")
    csetty_mips_source = checksums.get("csetty_mips_source")
    if not all(
        isinstance(item, dict)
        for item in (base, dcc, csetty_mips, debian, dcc_source, csetty_mips_source)
    ):
        raise SystemExit("source-build locks are missing required tables")
    assert isinstance(base, dict)
    assert isinstance(dcc, dict)
    assert isinstance(csetty_mips, dict)
    assert isinstance(debian, dict)
    assert isinstance(dcc_source, dict)
    assert isinstance(csetty_mips_source, dict)
    expected_base = f"{debian.get('tag', '')}@{debian.get('index_digest', '')}"
    if base.get("image") != expected_base:
        raise SystemExit("Debian image reference and checksums.lock digest do not match")
    for source_key, checksum_key in (
        ("version", "version"),
        ("source_url", "url"),
        ("source_sha256", "sha256"),
        ("source_commit", "commit"),
    ):
        if dcc.get(source_key) != dcc_source.get(checksum_key):
            raise SystemExit(f"DCC lock mismatch for {source_key}")
    for toolchain_key, checksum_key in (
        ("version", "version"),
        ("source", "repository"),
        ("commit", "commit"),
        ("package_tree_sha256", "package_tree_sha256"),
        ("license", "license"),
    ):
        if csetty_mips.get(toolchain_key) != csetty_mips_source.get(checksum_key):
            raise SystemExit(f"csetty-mips lock mismatch for {toolchain_key}")

    for path in required[2:4]:
        text = path.read_text(encoding="utf-8")
        for value in (
            str(base["image"]),
            str(dcc["source_url"]),
            str(dcc["source_sha256"]),
            "sh /tmp/build-dcc.sh",
        ):
            if value not in text:
                raise SystemExit(f"{path} does not contain locked source-build value: {value}")
        if "/releases/download/" in text:
            raise SystemExit(f"{path} downloads a DCC binary instead of building source")

    compose = (project_root / "compose.yaml").read_text(encoding="utf-8")
    for service in (
        "comp1511-interactive",
        "comp1521-interactive",
        "comp1511-judge",
        "comp1521-judge",
    ):
        if f"  {service}:" not in compose:
            raise SystemExit(f"compose.yaml is missing build service {service}")


def _verify_local_evidence(project_root: Path, gate: str, reference: str) -> None:
    if "#" not in reference:
        raise SystemExit(f"{gate} evidence must be PATH#ANCHOR or an approved CI URL")
    path_text, anchor = reference.split("#", maxsplit=1)
    candidate = (project_root / path_text).resolve()
    if not candidate.is_relative_to(project_root.resolve()) or not candidate.is_file():
        raise SystemExit(f"{gate} evidence path is missing or unsafe: {path_text}")
    if not anchor or f'id="{anchor}"' not in candidate.read_text(encoding="utf-8"):
        raise SystemExit(f"{gate} evidence anchor is missing: {reference}")


def _verify_public_approval(project_root: Path, approval_path: Path) -> None:
    project_license = project_root / "LICENSE"
    if not project_license.is_file() or not project_license.read_text(encoding="utf-8").strip():
        raise SystemExit("public release requires an owner-selected non-empty project LICENSE")

    data = _load_toml(approval_path)
    release = data.get("release")
    if not isinstance(release, dict):
        raise SystemExit(f"{approval_path} must contain a [release] table")
    project_version, _ = _project_metadata(project_root)
    if release.get("version") != project_version:
        raise SystemExit("public release approval version does not match pyproject.toml")
    if release.get("channel") != "alpha":
        raise SystemExit("the current approval contract is for the alpha channel")
    if release.get("artifact_policy") != _SOURCE_ONLY_POLICY:
        raise SystemExit(f"artifact_policy must be {_SOURCE_ONLY_POLICY!r}")
    if release.get("owner_approved") is not True:
        raise SystemExit("public release requires owner_approved = true")

    gates = data.get("gates")
    if not isinstance(gates, dict):
        raise SystemExit(f"{approval_path} must contain a [gates] table")
    incomplete = [name for name in _PUBLIC_GATES if not str(gates.get(name, "")).strip()]
    if incomplete:
        raise SystemExit(
            "public release approval is missing evidence for: " + ", ".join(incomplete)
        )
    weak_values = {"yes", "true", "approved", "done", "n/a", "na"}
    for gate in _PUBLIC_GATES:
        reference = str(gates[gate]).strip()
        lowered = reference.lower()
        has_placeholder = any(marker in lowered for marker in ("pending", "todo", "tbd"))
        if lowered in weak_values or has_placeholder:
            raise SystemExit(f"{gate} requires durable evidence, not {reference!r}")
        if gate in {"cross_platform_acceptance", "multiarch_acceptance"}:
            if not re.fullmatch(
                r"https://github\.com/JiaruiUNSW/CSEtty/actions/runs/[0-9]+", reference
            ):
                raise SystemExit(f"{gate} must reference the passing GitHub Actions run")
        else:
            _verify_local_evidence(project_root, gate, reference)

    for manifest in sorted((project_root / "packs").glob("*/pack.toml")):
        license_label = _load_toml(manifest).get("license")
        if license_label != _ASSESSMENT_LICENSE:
            raise SystemExit(f"public release requires {_ASSESSMENT_LICENSE!r} in {manifest}")
    for manifest in sorted((project_root / "question_bank").glob("*/bank.toml")):
        license_label = _load_toml(manifest).get("license")
        if license_label != _ASSESSMENT_LICENSE:
            raise SystemExit(f"public release requires {_ASSESSMENT_LICENSE!r} in {manifest}")

    licence_map = (project_root / "LICENSES.md").read_text(encoding="utf-8")
    for marker in ("src/csetty/**", "packs/**", "question_bank/**", _ASSESSMENT_LICENSE):
        if marker not in licence_map:
            raise SystemExit(f"LICENSES.md is missing required scope marker: {marker}")

    dockerfile = "\n".join(
        (project_root / "docker" / filename).read_text(encoding="utf-8")
        for filename in ("Dockerfile.interactive", "Dockerfile.judge")
    )
    legacy_upstream_markers = (
        "io.csetty.mipsy.",
        "COPY --from=mipsy",
        "cargo build --release --locked --package mipsy",
    )
    if any(marker in dockerfile for marker in legacy_upstream_markers):
        raise SystemExit(
            "COMP1521 Dockerfile still contains a legacy upstream-mipsy build or label; "
            "public artifacts must use only the reviewed local engine"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail closed unless release prerequisites hold")
    parser.add_argument("--level", choices=("private", "public"), required=True)
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument(
        "--approval",
        type=Path,
        default=Path("release/public-release.toml"),
        help="owner-reviewed evidence file required for a public release",
    )
    arguments = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    dist = arguments.dist.expanduser().resolve(strict=True)
    notice = project_root / "THIRD_PARTY_NOTICES.md"
    if not notice.is_file() or not notice.read_text(encoding="utf-8").strip():
        raise SystemExit("THIRD_PARTY_NOTICES.md is missing or empty")

    _verify_source_build_contract(project_root)
    source = _verify_dcc_source(project_root, dist)
    wheel = _verify_wheel(project_root, dist)
    sdist = _verify_sdist(project_root, dist)
    if arguments.level == "private":
        _verify_private_workflows(project_root)
        print("SOURCE RELEASE DRY-RUN GATE PASSED")
        print("Owner approval and public evidence were not inferred by this dry run.")
    else:
        approval = arguments.approval
        if not approval.is_absolute():
            approval = project_root / approval
        _verify_public_approval(project_root, approval)
        _verify_private_workflows(project_root)
        print("PUBLIC RELEASE GATE PASSED")
    print(f"Wheel: {wheel}")
    print(f"Source distribution: {sdist}")
    print(f"Local DCC source verification copy: {source}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
