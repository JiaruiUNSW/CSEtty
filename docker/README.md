# Local source-built course images

This directory contains public build definitions, not prebuilt images or image
layers. `Dockerfile.interactive` and `Dockerfile.judge` both build DCC 2.37 from
the hash-pinned upstream source archive on a digest-pinned Debian 12 base. The
COMP1521 targets additionally stage the source files of the pinned, separately
released MPL-2.0 `csetty-mips` dependency and install a small
`/usr/local/bin/mipsy` compatibility launcher. They do not use upstream mipsy.

Normal local builds are driven through:

```text
csetty prepare --profile comp1511
csetty prepare --profile comp1521
```

`csetty prepare` creates a temporary build context containing the CSEExamTTY
runtime source and the verified installed `csetty-mips` dependency source. It
then invokes the checked-in `compose.yaml` build services and records the exact
local image IDs. The temporary context is removed after the build.

An optional `--mipsy-source PATH` validates and records the pinned private
comparison checkout only; it does not change either course image.

`csetty start` never builds, pulls, or downloads. It requires both recorded
local image IDs to still match the prepared tags. Student and judge containers
run without the Docker socket and use a read-only root filesystem. The host
supervisor remains authoritative for time and submissions.
