# Release evidence: CSEExamTTY 0.1.0a1

Evidence date: 2026-08-06  
Release channel: public alpha  
Artifact policy: source-only; no prebuilt course images or third-party caches

This record supports the fail-closed release gate. `PASS` means the stated
alpha boundary was reviewed or mechanically verified; it is not legal advice.
The alpha intentionally makes a narrower platform claim than a future stable
release.

<a id="project-license"></a>
## Project and file-level licences — PASS

- Original host software, build definitions, workflows, tests, and project
  documentation are Apache-2.0 under `LICENSE` and `LICENSES.md`.
- Every original file in `packs/**` and `question_bank/**` is CC BY-NC-ND 4.0,
  including prose, starter code, tests, worked explanations, solutions, and
  references. Both pack and bank manifests carry the same label.
- Package metadata declares the aggregate expression
  `Apache-2.0 AND CC-BY-NC-ND-4.0`; wheel and sdist gates require the licence
  files and path map.
- Creative Commons identifies its English legal code as the operative layer:
  <https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode.en>.

<a id="dcc-source"></a>
## DCC source-build and GPL boundary — PASS

- DCC is pinned to tag 2.37, commit
  `0a888fdb2bfe130c611fb84514fdbf52d3efe149`, with its source archive and
  GPL-3.0-only licence hashes in `toolchains.lock` and `checksums.lock`.
- Both Dockerfiles download the pinned source archive and run the upstream
  `make dcc` target. They do not download a DCC binary.
- The release gate independently downloads a local verification copy and checks
  SHA-256. That verification copy is not a published CSEExamTTY artifact.
- The repository, PyPI package, and CI do not convey a DCC binary or a locally
  built DCC-containing image. A user who redistributes a local image is warned
  to meet the GPL obligations of that conveyance.
- Upstream licence: <https://github.com/COMP1511UNSW/dcc/blob/2.37/LICENSE>.

<a id="csetty-mips"></a>
## csetty-mips provenance and licence — PASS

- Runtime dependency: `csetty-mips==0.1.1` from
  <https://pypi.org/project/csetty-mips/0.1.1/>.
- Canonical source: <https://github.com/JiaruiUNSW/CSEtty-MIPS>, commit
  `33410078667ad67942c6700d73411fc31be00c8f`, MPL-2.0.
- Package-tree SHA-256 is pinned and verified before its source is staged into
  a local COMP1521 build context. NOTICE and MPL text are installed in the
  locally built image.
- Upstream `insou22/mipsy` source and binaries are excluded from CSEExamTTY
  wheels, sdists, Docker build contexts, and course images.

<a id="vscode-terms"></a>
## VS Code, Server, and extension boundary — PASS for source-only alpha

- CSEExamTTY does not package, mirror, publish, or upload VS Code, VS Code
  Server, or VSIX files. `prepare` invokes the user's licensed VS Code client to
  acquire them into an application-owned local cache.
- Microsoft's VS Code terms permit installation/use subject to their terms and
  state that extensions have separate licences:
  <https://code.visualstudio.com/license>.
- The Server documentation points users to separate Server terms:
  <https://code.visualstudio.com/docs/remote/vscode-server>.
- Marketplace offerings are governed by the Marketplace Terms and offering
  terms: <https://aka.ms/vsmarketplace-ToU>.
- The configured extensions are identified in `THIRD_PARTY_NOTICES.md`; local
  acquisition does not become a redistribution grant. The alpha does not make
  any claim about a publisher's compliance for third-party extension content.

<a id="pack-license"></a>
## Original assessment content — PASS

- The owner selected CC BY-NC-ND 4.0 for every original file under `packs/**`
  and `question_bank/**`.
- `ASSESSMENT_MATERIALS_LICENSE.md` supplies the exact scope, attribution, and
  canonical legal-code link.
- Public course pages are referenced for curriculum/workflow shape only. They
  are not copied into packs, banks, reports, or the package.

<a id="branding"></a>
## Branding and name review — PASS for alpha naming boundary

- The project uses the independent names CSEExamTTY/CSEtty and an explicit
  non-affiliation statement; it does not use an UNSW logo.
- `TRADEMARKS.md` reserves project marks and states that UNSW names and marks
  belong to their owners.
- This is an owner product-name review, not a formal trademark clearance
  opinion. The alpha must never describe itself as an official UNSW service.

<a id="cross-platform"></a>
## Cross-platform alpha acceptance — PASS

Public GitHub Actions run
[31081135512](https://github.com/JiaruiUNSW/CSEtty/actions/runs/31081135512)
passed at commit `c91b91664d61c9c9a65cc71b34b6b9e1b9e61a91`. Its host
matrix covered:

- Windows Server 2025 x64 with Python 3.11;
- Ubuntu x64 with Python 3.11, 3.12, and 3.13;
- Ubuntu 24.04 arm64 with Python 3.11;
- macOS Apple Silicon with Python 3.11; and
- macOS Intel with Python 3.11.

Every host job ran Ruff, mypy, pytest, built the wheel, and smoke-tested a fresh
wheel installation. Separate native arm64 jobs built and exercised the local
COMP1511 and COMP1521 source images. The same candidate passed local Apple
Silicon fixed-pack, full question-bank, and live Docker acceptance before the
public run.

This alpha does not claim completed Docker Desktop/WSL2 or offline VS Code
acceptance outside the locally tested Apple Silicon system; those remain
stable-release gates.

<a id="multiarch"></a>
## Linux image architecture acceptance — PASS

The same passing run completed independent COMP1511 and COMP1521 source-build
jobs. For each profile it:

- built and recorded local interactive and judge images from pinned sources;
- passed every fixed-pack reference, all 75 question-bank references, and live
  container acceptance;
- built runner-local interactive and judge OCI archives for both linux/amd64
  and linux/arm64 without pushing them; and
- verified both platforms, profile/role/toolchain licence labels, SPDX SBOM,
  and SLSA provenance attestations in every OCI archive.

The four OCI archives and BuildKit outputs remained runner-local and were not
published as workflow artifacts, registry layers, or public caches.

<a id="artifact-inventory"></a>
## Published artifact inventory

Allowed:

- the Git repository and automatically generated GitHub source archives;
- the `cseexamtty` wheel and sdist;
- release notes, checksums, and an SBOM that contain no bundled binaries; and
- links to the separately published `csetty-mips` project.

Forbidden:

- Docker/OCI images, registry layers, or public BuildKit caches;
- DCC binaries, Debian package archives, or upstream mipsy source/binaries;
- VS Code Server or VSIX caches; and
- credentials, local state databases, attempts, submissions, or reports.
