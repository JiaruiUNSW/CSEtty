from __future__ import annotations

import argparse
import json
import tarfile
from pathlib import Path
from typing import Any

_EXPECTED_PLATFORMS = {("linux", "amd64"), ("linux", "arm64")}
_SBOM_PREDICATE = "https://spdx.dev/Document"
_PROVENANCE_PREDICATES = {
    "https://slsa.dev/provenance/v0.2",
    "https://slsa.dev/provenance/v1",
}


def _json_member(archive: tarfile.TarFile, name: str) -> dict[str, Any]:
    try:
        member = archive.getmember(name)
    except KeyError as exc:
        raise SystemExit(f"OCI archive references a missing member: {name}") from exc
    stream = archive.extractfile(member)
    if stream is None:
        raise SystemExit(f"OCI archive member is not readable: {name}")
    payload = json.loads(stream.read())
    if not isinstance(payload, dict):
        raise SystemExit(f"OCI archive member is not a JSON object: {name}")
    return payload


def _blob_name(digest: str) -> str:
    algorithm, separator, value = digest.partition(":")
    if algorithm != "sha256" or not separator or len(value) != 64:
        raise SystemExit(f"unsupported OCI digest: {digest!r}")
    return f"blobs/sha256/{value}"


def _leaf_descriptors(
    archive: tarfile.TarFile,
    index: dict[str, Any],
) -> list[dict[str, Any]]:
    for _depth in range(4):
        descriptors = index.get("manifests")
        if not isinstance(descriptors, list) or not all(
            isinstance(descriptor, dict) for descriptor in descriptors
        ):
            raise SystemExit("OCI index does not contain a valid manifest list")
        if (
            len(descriptors) == 1
            and descriptors[0].get("mediaType") == "application/vnd.oci.image.index.v1+json"
        ):
            index = _json_member(archive, _blob_name(str(descriptors[0].get("digest", ""))))
            continue
        return descriptors
    raise SystemExit("OCI index nesting exceeds the supported depth")


def _verify_attestation_predicates(image_digest: str, predicates: set[str]) -> None:
    has_sbom = _SBOM_PREDICATE in predicates
    has_provenance = not predicates.isdisjoint(_PROVENANCE_PREDICATES)
    if not has_sbom or not has_provenance:
        raise SystemExit(
            f"attestation for {image_digest} lacks SBOM/provenance: {sorted(predicates)}"
        )


def verify(path: Path, *, profile: str, role: str) -> None:
    with tarfile.open(path, mode="r:*") as archive:
        layout = _json_member(archive, "oci-layout")
        if layout.get("imageLayoutVersion") != "1.0.0":
            raise SystemExit(f"unexpected OCI layout: {layout!r}")
        index = _json_member(archive, "index.json")
        descriptors = _leaf_descriptors(archive, index)

        images: dict[tuple[str, str], dict[str, Any]] = {}
        attestations: dict[str, dict[str, Any]] = {}
        for descriptor in descriptors:
            if not isinstance(descriptor, dict):
                continue
            annotations = descriptor.get("annotations") or {}
            if annotations.get("vnd.docker.reference.type") == "attestation-manifest":
                reference = annotations.get("vnd.docker.reference.digest")
                if isinstance(reference, str):
                    attestations[reference] = descriptor
                continue
            platform = descriptor.get("platform") or {}
            key = (str(platform.get("os", "")), str(platform.get("architecture", "")))
            if key in _EXPECTED_PLATFORMS:
                images[key] = descriptor

        if set(images) != _EXPECTED_PLATFORMS:
            raise SystemExit(
                f"OCI platforms mismatch: expected {sorted(_EXPECTED_PLATFORMS)}, "
                f"found {sorted(images)}"
            )
        image_digests = {str(descriptor.get("digest", "")) for descriptor in images.values()}
        missing_attestations = image_digests - attestations.keys()
        if missing_attestations:
            raise SystemExit(
                "OCI index is missing SBOM/provenance attestation manifests for: "
                + ", ".join(sorted(missing_attestations))
            )

        for image_digest in sorted(image_digests):
            attestation = _json_member(
                archive,
                _blob_name(str(attestations[image_digest].get("digest", ""))),
            )
            layers = attestation.get("layers")
            if not isinstance(layers, list):
                raise SystemExit(f"attestation manifest for {image_digest} has no layers")
            predicates = {
                str((layer.get("annotations") or {}).get("in-toto.io/predicate-type", ""))
                for layer in layers
                if isinstance(layer, dict)
            }
            _verify_attestation_predicates(image_digest, predicates)

        for platform, descriptor in sorted(images.items()):
            manifest = _json_member(archive, _blob_name(str(descriptor["digest"])))
            config_descriptor = manifest.get("config")
            if not isinstance(config_descriptor, dict):
                raise SystemExit(f"OCI image {platform} has no config descriptor")
            config = _json_member(archive, _blob_name(str(config_descriptor.get("digest", ""))))
            if (config.get("os"), config.get("architecture")) != platform:
                raise SystemExit(f"OCI config platform mismatch for {platform}: {config!r}")
            labels = (config.get("config") or {}).get("Labels") or {}
            if labels.get("io.csetty.profile") != profile:
                raise SystemExit(f"OCI {platform} has wrong profile label: {labels!r}")
            if labels.get("io.csetty.image.role") != role:
                raise SystemExit(f"OCI {platform} has wrong image role label: {labels!r}")
            if labels.get("io.csetty.dcc.license") != "GPL-3.0-only":
                raise SystemExit(f"OCI {platform} is missing the DCC license label")
            if labels.get("io.csetty.dcc.build") != "verified-source":
                raise SystemExit(f"OCI {platform} was not marked as a DCC source build")
            if profile == "comp1521":
                if labels.get("io.csetty.mips.engine") != "csetty-mips":
                    raise SystemExit(f"OCI {platform} has the wrong MIPS engine")
                if labels.get("io.csetty.mips.version") != "0.1.2":
                    raise SystemExit(f"OCI {platform} has the wrong csetty-mips version")
                if labels.get("io.csetty.mips.license") != "MPL-2.0":
                    raise SystemExit(f"OCI {platform} has the wrong csetty-mips license")
            print(f"{platform[0]}/{platform[1]}: {descriptor['digest']} PASS")

    print(f"OCI ACCEPTANCE PASSED: {profile}/{role} ({path})")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify CSEExamTTY multi-platform OCI layout, labels, and attestations"
    )
    parser.add_argument("archive", type=Path)
    parser.add_argument("--profile", choices=("comp1511", "comp1521"), required=True)
    parser.add_argument("--role", choices=("interactive", "judge"), default="interactive")
    arguments = parser.parse_args()
    verify(
        arguments.archive.expanduser().resolve(strict=True),
        profile=arguments.profile,
        role=arguments.role,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
