#!/bin/sh
set -eu

: "${DCC_VERSION:?DCC_VERSION is required}"
: "${DCC_SOURCE_URL:?DCC_SOURCE_URL is required}"
: "${DCC_SOURCE_SHA256:?DCC_SOURCE_SHA256 is required}"
: "${DCC_SOURCE_COMMIT:?DCC_SOURCE_COMMIT is required}"

echo "${DCC_SOURCE_SHA256}  /tmp/dcc-source.tar.gz" | sha256sum --check --strict
mkdir -p /tmp/dcc-source /out/usr/local/lib/csetty /out/usr/share/doc/dcc
tar --extract --gzip --file /tmp/dcc-source.tar.gz \
    --directory /tmp/dcc-source --strip-components 1

# DCC's upstream Makefile obtains its version with `git describe`. GitHub's
# verified source archive intentionally has no .git directory, so recreate the
# minimum local repository metadata needed by the upstream build without
# changing the source files.
cd /tmp/dcc-source
git init --quiet
git config user.name CSEExamTTY-source-build
git config user.email source-build.invalid
git add --all
GIT_AUTHOR_DATE=2024-01-01T00:00:00Z \
GIT_COMMITTER_DATE=2024-01-01T00:00:00Z \
    git commit --quiet --message "DCC ${DCC_VERSION} verified source"
git tag "${DCC_VERSION}"

make dcc
./dcc --version | grep -F "dcc version ${DCC_VERSION}"
install -m 0755 dcc /out/usr/local/lib/csetty/dcc-upstream
install -m 0644 LICENSE /out/usr/share/doc/dcc/LICENSE
printf '%s\n' \
    "DCC version: ${DCC_VERSION}" \
    "Built locally from verified source; no upstream binary was downloaded." \
    "Source: ${DCC_SOURCE_URL}" \
    "Source SHA-256: ${DCC_SOURCE_SHA256}" \
    "Source commit: ${DCC_SOURCE_COMMIT}" \
    > /out/usr/share/doc/dcc/SOURCE
