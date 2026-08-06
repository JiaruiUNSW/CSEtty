# Release process and fail-closed gates

CSEExamTTY `0.1.0a1` is a source-only public alpha. A release may publish the Git
repository plus the `cseexamtty` wheel/sdist, checksums, and an SBOM. It must not
publish a course image, registry layer, BuildKit cache, OCI archive, DCC binary,
Debian package archive, VS Code Server, VSIX cache, or upstream mipsy content.

The release gate is engineering evidence, not legal advice. The owner must
review and set `owner_approved = true`; the script never infers approval.

## Local release dry run

From a clean checkout:

```sh
uv sync --extra dev --locked
uv run ruff check src tests scripts
uv run mypy src/csetty
uv run pytest -q
PYTHONPATH=src uv run python scripts/docker_acceptance.py --profile all
uv run csetty bank verify comp1511
uv run csetty bank verify comp1521
uv run python scripts/stage_source_build.py /tmp/csetty-source-build
docker buildx build --platform linux/amd64,linux/arm64 --target comp1511 \
  --file /tmp/csetty-source-build/docker/Dockerfile.interactive \
  --sbom=true --provenance=mode=max \
  --output type=oci,dest=/tmp/csetty-comp1511-interactive.oci \
  /tmp/csetty-source-build
uv run python scripts/verify_oci.py /tmp/csetty-comp1511-interactive.oci \
  --profile comp1511 --role interactive
docker buildx build --platform linux/amd64,linux/arm64 --target comp1511 \
  --file /tmp/csetty-source-build/docker/Dockerfile.judge \
  --sbom=true --provenance=mode=max \
  --output type=oci,dest=/tmp/csetty-comp1511-judge.oci \
  /tmp/csetty-source-build
uv run python scripts/verify_oci.py /tmp/csetty-comp1511-judge.oci \
  --profile comp1511 --role judge
docker buildx build --platform linux/amd64,linux/arm64 --target comp1521 \
  --file /tmp/csetty-source-build/docker/Dockerfile.interactive \
  --sbom=true --provenance=mode=max \
  --output type=oci,dest=/tmp/csetty-comp1521-interactive.oci \
  /tmp/csetty-source-build
uv run python scripts/verify_oci.py /tmp/csetty-comp1521-interactive.oci \
  --profile comp1521 --role interactive
docker buildx build --platform linux/amd64,linux/arm64 --target comp1521 \
  --file /tmp/csetty-source-build/docker/Dockerfile.judge \
  --sbom=true --provenance=mode=max \
  --output type=oci,dest=/tmp/csetty-comp1521-judge.oci \
  /tmp/csetty-source-build
uv run python scripts/verify_oci.py /tmp/csetty-comp1521-judge.oci \
  --profile comp1521 --role judge
uv build
uv export --preview-features sbom-export --format cyclonedx1.5 \
  --no-dev --locked --output-file dist/cseexamtty-python.cdx.json
uv run python scripts/fetch_dcc_source.py dist
uv run python scripts/release_gate.py --level private --dist dist
uv run python scripts/write_checksums.py dist
```

The source build uses `compose.yaml`, separate interactive/judge Dockerfiles,
the Debian and source integrity values in `checksums.lock`, and a temporary
context containing the verified installed `csetty-mips` source. It never pushes
an image, OCI archive, layer cache, or dry-run artifact.

The dry-run gate proves that the wheel declares the pinned external MIPS
dependency, contains notices and host-only original author materials, and
contains no upstream mipsy binary.
The wheel smoke then proves that
student pack snapshots and Docker build contexts exclude those author materials.
It also downloads the exact DCC source archive as a local hash-verification
input and checks that workflows contain no package/image publishing command.
That DCC archive is not a CSEExamTTY release artifact because CSEExamTTY does
not convey a DCC binary or locally built course image.

The COMP1521 multi-architecture build must identify
`io.csetty.mips.engine=csetty-mips`, version `0.1.1`, and license `MPL-2.0`.
An upstream comparison executable or checkout is never a release artifact.

## Public alpha gate

Public source/Python release requires all of the following before tagging or
uploading the Python distributions:

1. the committed Apache-2.0 project `LICENSE` and packaging metadata are reviewed;
2. both pack manifests and the file-level prose/code/test licence mapping are reviewed;
3. DCC notices and equivalent access to corresponding source are reviewed;
4. the separately released `csetty-mips` provenance, NOTICE, and MPL-2.0 license
   are reviewed and the image is confirmed free of upstream mipsy content;
5. VS Code Server and extension download/redistribution terms are reviewed;
6. branding and project naming are reviewed;
7. the alpha host-contract matrix passes on macOS, Windows, and Linux; and
8. linux/amd64 and linux/arm64 source-build acceptance plus multi-arch OCI
   verification passes without uploading the outputs.

`release/public-release.toml` records the owner's approval and durable evidence.
Bare values such as `yes`, `approved`, or `done` are rejected. Platform entries
must be the URL of the passing public GitHub Actions run. Then run:

```sh
uv run python scripts/release_gate.py --level public --dist dist \
  --approval release/public-release.toml
```

The script deliberately fails if evidence is blank/weak/pending, versions or
licence metadata differ, the wheel/sdist omits required licence files, pack or
bank labels differ from CC BY-NC-ND 4.0, legacy upstream-private image metadata
remains, a workflow publishes artifacts, or the local DCC verification copy is
absent or has the wrong hash.

## Bootstrap and publish sequence

For an empty public repository, use this order so the first CI run itself can
become release evidence:

1. run the local checks and distribution dry-run;
2. scan the intended Git tree for credentials and prebuilt/forbidden artifacts;
3. push the untagged release candidate to `main`;
4. wait for every job in the public CI run to pass;
5. replace both pending platform values in `release/public-release.toml` with
   that exact Actions run URL and update the evidence record;
6. commit/push the evidence, wait for the new CI run, and use the newer passing
   run URL if the evidence-only commit generated it;
7. rebuild from the exact clean commit and run the public gate;
8. create and push signed/annotated tag `v0.1.0a1`; and
9. upload only the checked wheel and sdist to PyPI, then fresh-install from
   PyPI and repeat the wheel smoke test.

Do not use a credential pasted into chat or committed in any file. Prefer PyPI
Trusted Publishing. If the first project upload must use a token, create a new
short-lived account token, pass it only through process environment/stdin, then
revoke it and replace it with a project-scoped token or Trusted Publisher.

The public package name is `cseexamtty`; the installed command remains
`csetty`. Release version `0.1.0a1` is intentionally pre-release and does not
claim the stable cross-platform desktop/VS Code acceptance planned for `0.1.0`.
