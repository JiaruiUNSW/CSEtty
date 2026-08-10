# Third-party notices and distribution status

CSEExamTTY is distributed as a source-only local simulator. This file records
the third-party components that a user may download or build during the explicit
`csetty prepare` phase. It is not a licence for CSEExamTTY itself; see
`LICENSES.md` for the path-based licence map.

## DCC 2.37

- Project: DCC (Debugging C Compiler)
- Upstream: <https://github.com/COMP1511UNSW/dcc>
- Release: <https://github.com/COMP1511UNSW/dcc/releases/tag/2.37>
- License: GNU General Public License version 3 (`GPL-3.0-only`)
- License text: <https://github.com/COMP1511UNSW/dcc/blob/2.37/LICENSE>
- License-text SHA-256:
  `3972dc9744f6499f0f9b2dbf76696f2ae7ad8af9b23dde66d6af86c9dfb36986`
- Annotated tag object: `ae01f91688d25ef0e81452d7b5eb3d156dd57175`
- Tag target commit: `0a888fdb2bfe130c611fb84514fdbf52d3efe149`
- Corresponding-source archive:
  <https://github.com/COMP1511UNSW/dcc/archive/refs/tags/2.37.tar.gz>
- Source-archive SHA-256:
  `7cd659bd559e178950b05bf85feabeeacac4bd5ecf0f00528bf808a8e5c18762`

During `csetty prepare`, BuildKit downloads only the pinned source archive,
verifies its SHA-256 before use, and builds DCC locally with the upstream
`make dcc` target. No DCC binary is distributed by this repository or downloaded
by its Dockerfiles. The locally built image stores the license and exact source
directions under `/usr/share/doc/dcc`. Anyone who independently conveys a locally
built DCC-containing image remains responsible for the GPLv3 obligations that
apply to that conveyance.

No warranty is provided by DCC's copyright holders or by CSEExamTTY; refer to
the full GPLv3 license text installed in the image.

## csetty-mips

- Project: csetty-mips
- Source: <https://github.com/JiaruiUNSW/CSEtty-MIPS>
- Distribution: <https://pypi.org/project/csetty-mips/0.1.2/>
- Version: `0.1.2`
- Pinned commit: `dd476ec4613e32da056746345a78d9f2b6dc7dd1`
- License: Mozilla Public License 2.0 (`MPL-2.0`)

The COMP1521 image uses this separately released dependency. Its component
NOTICE and full MPL-2.0 license are installed under
`/usr/share/doc/csetty-mips`; image labels record the engine, version, and
license. No upstream mipsy source or binary is included.

## Optional upstream mipsy comparison checkout

- Upstream: <https://github.com/insou22/mipsy>
- Pinned commit: `61f96b38626c30c2ead7925486304f163ec56b2b`
- Redistribution status: **not included or approved**

The reviewed upstream tree did not contain an explicit redistribution license.
The optional `csetty prepare --mipsy-source PATH` path therefore only validates
and records a clean checkout at the pinned commit for private black-box
comparison. It does not compile that checkout and never copies its source or
binary into the Python wheel or either course image. A preserved private oracle
must not be pushed, exported, or published.

## Visual Studio Code and extensions

The Python wheel does not contain Visual Studio Code, VS Code Server, or VSIX
packages. During the explicit networked `csetty prepare` phase, the user's
installed official VS Code client downloads or installs these components into
CSEExamTTY-owned local caches:

- Dev Containers (`ms-vscode-remote.remote-containers`)
- C/C++ (`ms-vscode.cpptools`)
- Mipsy Editor Features (`xavc.xavc-mipsy-features`, COMP1521 only)

Those local caches are not project release artifacts and are never uploaded by
CSEExamTTY. Each user's download and use remains subject to the applicable
Microsoft/Marketplace or extension-publisher terms. CSEExamTTY grants no right
to redistribute those components.

## Debian base and packages

Course images are built from the multi-architecture Debian 12 slim index pinned
in `checksums.lock` and install Debian packages through APT during the local
prepare phase. Package-specific copyright and license files remain available in
the locally built image under `/usr/share/doc`.

## Original exam packs

The bundled original practice-pack and question-bank manifests declare
`CC BY-NC-ND 4.0`. The same licence applies to every original file under
`packs/**` and `question_bank/**`, including question prose, starter files,
tests, worked explanations, solutions, reference implementations, manifests,
and fixtures. See `ASSESSMENT_MATERIALS_LICENSE.md` and `LICENSES.md`.
