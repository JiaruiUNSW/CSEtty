from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from runpy import run_path
from typing import cast

import pytest

_VERIFY_OCI = run_path(str(Path(__file__).parents[1] / "scripts" / "verify_oci.py"))
_verify_attestation_predicates = cast(
    Callable[[str, set[str]], None],
    _VERIFY_OCI["_verify_attestation_predicates"],
)


@pytest.mark.parametrize(
    "provenance",
    [
        "https://slsa.dev/provenance/v0.2",
        "https://slsa.dev/provenance/v1",
    ],
)
def test_attestation_accepts_supported_slsa_provenance(provenance: str) -> None:
    _verify_attestation_predicates(
        "sha256:image",
        {"https://spdx.dev/Document", provenance},
    )


@pytest.mark.parametrize(
    "predicates",
    [
        {"https://spdx.dev/Document"},
        {"https://slsa.dev/provenance/v1"},
        set(),
    ],
)
def test_attestation_requires_both_sbom_and_provenance(predicates: set[str]) -> None:
    with pytest.raises(SystemExit, match="lacks SBOM/provenance"):
        _verify_attestation_predicates("sha256:image", predicates)
