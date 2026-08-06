# csetty-mips integration contract

CSEExamTTY consumes `csetty-mips` as an independently released dependency:

- source: <https://github.com/JiaruiUNSW/CSEtty-MIPS>
- PyPI: <https://pypi.org/project/csetty-mips/0.1.1/>
- package version: `0.1.1`
- Git commit: `33410078667ad67942c6700d73411fc31be00c8f`
- source license: Mozilla Public License 2.0 (`MPL-2.0`)

`pyproject.toml` pins the exact PyPI version; `toolchains.lock`,
`checksums.lock`, and Docker image labels retain the corresponding Git tag
and commit as source provenance. The locks also record a canonical SHA-256 of
the installed package source tree and MPL license, which `prepare` verifies
before staging Docker build inputs. The MIPS implementation, pure-engine
tests, specification, acceptance matrix, and clean-room provenance record
live only in the independent repository.

This repository retains two downstream integration suites:

- `tests/test_csetty_mips_pack.py` executes the fixed COMP1521 pack references;
- `tests/test_csetty_mips_question_bank.py` executes the COMP1521 question-bank
  references.

During `csetty prepare`, the Docker build-context staging step copies the
installed dependency package and its MPL-2.0 license into a temporary local
context. The COMP1521 Docker target installs those files under `/opt/csetty`
and `/usr/share/doc/csetty-mips`. The context is not a published artifact, and
no upstream mipsy source or binary is used.
