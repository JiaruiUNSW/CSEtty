# Release process and fail-closed gates

CSEExamTTY `0.1.0a1` is a source-only public alpha. A release may publish the Git
repository plus the `cseexamtty` wheel/sdist, checksums, and an SBOM. It must not
publish a course image, registry layer, BuildKit cache, OCI archive, DCC binary,
Debian package archive, VS Code Server, VSIX cache, or upstream mipsy content.

The release gate is engineering evidence, not legal advice. The owner must
review and set `owner_approved = true`; the script never infers approval.

## Local release dry run

From a clean checkout with an empty `dist/` directory:

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
input and checks that no workflow publishes images or runner artifacts. The
only permitted package publisher is the dedicated, full-SHA-pinned
`.github/workflows/publish-pypi.yml` Trusted Publishing workflow.
That DCC archive is not a CSEExamTTY release artifact because CSEExamTTY does
not convey a DCC binary or locally built course image.

`scripts/write_checksums.py` deliberately records only the wheel, sdist, and
Python SBOM. The local DCC corresponding-source verification copy must not be
listed in `SHA256SUMS` or attached to the GitHub Release.

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
remains, a workflow publishes forbidden artifacts or weakens the dedicated PyPI
OIDC job, or the local DCC verification copy is absent or has the wrong hash.

## Trusted Publisher configuration

Create a GitHub environment named exactly `pypi`. Protect it with a required
reviewer and restrict deployments to release tags accepted by the project. Do
not add a PyPI token, username, or password as a repository/environment secret.

In the existing `cseexamtty` project on PyPI, open **Manage > Publishing** and
add a GitHub publisher with these exact identity fields:

```text
Owner: JiaruiUNSW
Repository: CSEtty
Workflow name: publish-pypi.yml
Environment name: pypi
```

PyPI binds the OIDC identity to this workflow filename and environment. The
publish job alone receives `id-token: write`; it has no checkout and never
builds or installs project code. It downloads only the allowed assets from the
published GitHub Release, verifies their names, SHA-256 values, archive paths,
project name, and version, and then invokes the PyPA publisher pinned to a full
commit SHA. PyPI attestations remain enabled.

## Repeatable publish sequence

Use this order for each new version:

1. run the local checks and distribution dry-run;
2. scan the intended Git tree for credentials and prebuilt/forbidden artifacts;
3. push the untagged release candidate to `main` and wait for every required CI
   job to pass;
4. replace both platform values in `release/public-release.toml` with
   that exact Actions run URL and update the evidence record;
5. commit/push the evidence, wait for the new CI run, and use the newer passing
   run URL if the evidence-only commit generated it;
6. rebuild from the exact clean commit, run the public gate, and generate
   `SHA256SUMS`;
7. create and push a signed/annotated `vVERSION` tag;
8. create a **draft** GitHub Release for that exact tag and attach exactly the
   wheel, sdist, `cseexamtty-python.cdx.json`, and `SHA256SUMS`;
9. independently inspect the four asset names and hashes, then publish the draft
   release; and
10. approve the protected `pypi` environment deployment, wait for the workflow
    to publish with OIDC, then fresh-install from PyPI and repeat the wheel smoke
    test.

The release must remain a draft until all four assets are present. Publishing
the draft emits the `release.published` event; attaching assets afterwards is
too late and is not an accepted workflow. Do not enable `skip-existing`: a
duplicate or partial version must fail loudly.

Do not use a credential pasted into chat or committed in any file. Once the
first Trusted Publisher release succeeds, revoke any remaining long-lived PyPI
account token used for the bootstrap release.

The public package name is `cseexamtty`; the installed command remains
`csetty`. Release version `0.1.0a1` is intentionally pre-release and does not
claim the stable cross-platform desktop/VS Code acceptance planned for `0.1.0`.
