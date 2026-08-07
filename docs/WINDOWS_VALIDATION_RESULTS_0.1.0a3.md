# Windows Validation Results — CSEExamTTY 0.1.0a3

## Overall verdict

**PASS** — every mandatory acceptance item in sections 4–10 of
`docs/WINDOWS_VALIDATION_TASK_0.1.0a3.md` passed on the native Windows host.
No product source, tests, manifests, tags, releases, registries, PyPI packages,
or remotes were modified or published.

Expected and tested commit:
`bc9d47bb65ee246e488d3a14156c0965e530c754`.

## Run identity and timing

- Host: `LAPTOP-Q77UG2SK`
- Validation start: `2026-08-07T04:00:21.5052706+10:00`
  (`2026-08-06T18:00:21.5084902Z`)
- Evidence-complete/cleanup audit: `2026-08-07T04:48:57.2710570+10:00`
- Elapsed: `00:48:35.766`
- Checkout: `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\work\a3-windows-validation-bc9d47b\repo`
- Evidence root: `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b`
- Isolated exact-wheel venv: `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\work\a3-windows-validation-bc9d47b\venvs\wheel`
- Dummy candidate only: `z5555555`; no real credential was used or retained in screenshots.

## 4. Fresh checkout and host inventory

| Acceptance item | Verdict | Evidence |
|---|---:|---|
| Fresh remote clone, detached exact HEAD | PASS | `git rev-parse HEAD` returned exactly `bc9d47bb65ee246e488d3a14156c0965e530c754`; `git status --short --branch` initially returned only `## HEAD (no branch)` |
| Windows checkout conversion | PASS | `core.autocrlf=true` |
| Fixture bytes equal Git blobs | PASS | 102/102, 0 mismatches, exit 0, 10.894 s |
| Required Docker/build command files remain LF | PASS | `docker/build-dcc.sh`, both Dockerfiles, `docker/dcc-command`, `exam-command`, and `mipsy-command`: zero CRLF and working-tree hash equals blob |
| Supported native Windows host | PASS | Windows 11 Pro for Workstations, version `10.0.26200`, build `26200`, 64-bit, x64 |
| Docker Linux/WSL2 backend | PASS | Docker reports `OSType=linux Architecture=x86_64 OperatingSystem=Docker Desktop`; WSL default distribution Ubuntu, default version 2 |
| Desktop VS Code/CLI | PASS | `code --version` exited 0 and reported 1.132.0 x64 |

Host inventory:

- ASUS ROG Strix SCAR 16 `G634JYR_G634JYR`, x64-based PC, 33,959,571,456 bytes RAM.
- PowerShell 7.6.4 Core.
- CPython 3.12.13.
- Git 2.53.0.windows.3.
- Docker Desktop 4.85.0; client/Engine 29.6.2; Engine `linux/amd64`.
- WSL 2.6.3.0; Linux kernel 6.6.87.2-1; Ubuntu WSL2 default.
- VS Code 1.132.0 (`df53daabb18cd157bdb08c7f01c34df936cf12f4`).

Raw inventory and byte-contract logs:

- `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\logs\host-inventory.txt`
- `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\logs\fixture-byte-hashes.tsv`
- `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\logs\lf-contract.txt`

## 5. Native Windows host contract and exact-wheel smoke

| Command/check | Exit | Duration | Result/excerpt |
|---|---:|---:|---|
| `csetty --version` | 0 | <1 s | `csetty 0.1.0a3` |
| `ruff check src tests scripts` | 0 | 1.736 s | `All checks passed!` |
| `mypy src/csetty` (strict project config) | 0 | 3.531 s | `Success: no issues found in 27 source files` |
| `pytest -q` | 0 | 16.770 s | `256 passed, 5 skipped in 16.33s` |
| exact 13-test targeted regression list | 0 | 3.177 s | `13 passed in 2.86s` |
| `python -m build --wheel --sdist` | 0 | 21.872 s | both distributions built successfully |
| fresh exact-wheel install/import/version checks | 0 | included below | import resolved to the isolated wheel venv; version `0.1.0a3` |
| `scripts/smoke_wheel.py` against the Windows-built wheel | 0 | 13.395 s | both papers exposed; author/student isolation PASS; wheel-installed Docker context PASS |

The five skips are expected platform skips: three Linux-container path helpers
and two Windows symlink tests requiring Developer Mode/elevation. No test failed.
The final post-GUI host rerun also passed: `256 passed, 5 skipped in 15.96s`,
Ruff passed, and strict mypy passed for 27 source files.

The targeted run independently passed all 13 exact tests, including CREATED
paper/report withholding, bounded cross-process report-lock behavior, working
report/finalization races, failed rewrite hiding stale final reports, ABORTED
remaining non-final, native Windows liveness, same-origin Open VSC, and the
Windows venv supervisor redirector lease. Log SHA-256:
`4A424E98BA6599BD8A43BB2B4414DBFC7E02ADDD6A0DD2029E75916456CC17D4`.

Artifacts:

| Artifact | Absolute path | SHA-256 |
|---|---|---|
| wheel | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\artifacts\dist\cseexamtty-0.1.0a3-py3-none-any.whl` | `FDAFA6BC042838E8F1FDC14D84EDAC4D8F8A51245D7EC6B165661CE56596BE12` |
| sdist | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\artifacts\dist\cseexamtty-0.1.0a3.tar.gz` | `35ED8202DAB3ECC707DB2809C5BA63C5A661C9CA00B7412D7B2C41F88F01BD1F` |

The wheel contains `csetty/web_theme.py` and declares version `0.1.0a3`.

## 6. Docker Desktop and fixed-content acceptance

Fresh-image precondition recorded all four expected tags absent. Both profiles
were then prepared from the exact-wheel staged source context; no old receipt,
wheel, image, or state was reused.

| Check | Exit | Duration | Result |
|---|---:|---:|---|
| `csetty doctor` | 0 | 5.727 s | host Python/state/Docker/VS Code/two packs PASS |
| `csetty prepare --profile comp1511` | 0 | 41.412 s | source build plus isolated VS Code completion PASS |
| `csetty doctor --offline-ready comp1511` | 0 | 7.695 s | matching images and offline VS Code PASS |
| `csetty prepare --profile comp1521` | 0 | 44.959 s | source build plus isolated VS Code completion PASS |
| `csetty doctor --offline-ready comp1521` | 0 | 8.140 s | matching images and offline VS Code PASS |
| `scripts/docker_acceptance.py --profile all` | 0 | 12.259 s | `DOCKER ACCEPTANCE PASSED` |

Prepare was visually verified in separately labelled, application-owned VS
Code windows. Dev Containers, the COMP1511 remote C/C++ extension, the COMP1521
remote C/C++ and Mipsy Editor Features extensions, the completion page, and the
matching offline VS Code Server were present. The normal VS Code profile was
not changed.

All four images used source-context digest
`5d3f757d4f46dfdfe70ee8f64bed4adf1b2d506443794839988ee6021c855b1d`:

| Image | Exact image ID |
|---|---|
| `csetty/comp1511:dev` | `sha256:c0b04fa0a53ebfb25211ae347e6a16776f2a865ee5ccf768afa96894b12b99f0` |
| `csetty/comp1511-judge:dev` | `sha256:6a2b520c3ba1dfd031dd561e950e4690763bb489e7ac26293a195fb70b30a478` |
| `csetty/comp1521:dev` | `sha256:90b46f73b8b9800b1c285355255ebc2166fc535349b0a20da3c5f09a322c0593` |
| `csetty/comp1521-judge:dev` | `sha256:b142255dcaa1d211909fcb4f03a2d3a9431191443979a712aa5da37e0ae89cdf` |

Labels verified DCC 2.37 from the recorded source, WSL2 runtime mode
`valgrind`, interactive/judge roles, and profile identity. COMP1521 additionally
verified local `csetty-mips 0.1.1` and its provenance; no upstream mipsy checkout
or executable was used.

Docker acceptance verified no network, no Docker socket/host Git/SSH material,
read-only/security boundaries, capability drop, no-new-privileges, PID/fork
containment, crashing-child containment, tool versions, and live PTY deadline
broadcast behavior.

Fixed-content matrix, all from the fresh exact-wheel images:

| Matrix | Exit | Duration | Pass count | Failed IDs | TIMEOUT |
|---|---:|---:|---:|---|---:|
| COMP1511 built-in practice pack | 0 | 27.842 s | 11/11 | none | 0 |
| COMP1511 full bank | 0 | 254.601 s | 75/75 | none | 0 |
| COMP1521 built-in practice pack | 0 | 21.300 s | 10/10 | none | 0 |
| COMP1521 full bank | 0 | 200.274 s | 75/75 | none | 0 |

## 7. Validation-only short packs

The copies were made outside the Git checkout. Each old literal and each new
literal was regex-counted and required to occur exactly once; all prompt,
resource, starter, solution, and test content remained unchanged.

| Pack | Timing | Validate | Duration | Digest |
|---|---|---:|---:|---|
| `comp1511-windows-a3-smoke@1.0.0` | reading 90 s; working 300 s | PASS/exit 0 | 0.390 s | `1edfa3c18210b0ba969e8f5cfe5bfca871efd6abf39688e6ace6f5e7cf8b0bc9` |
| `comp1521-windows-a3-smoke@1.0.0` | reading 90 s; working 75 s | PASS/exit 0 | 0.399 s | `7c5890052e4248f00a6b2a99f953ed60f6d3384feeb73f558f827f17922fe780` |

## 8. COMP1511 explicit-finish GUI flow

**PASS** — final accepted attempt:
`c1eeb326-9f9a-4e14-a5d1-d7bd877cc530`.

- Windows Terminal visibly cleared the entered start command and old scrollback
  before the welcome/sign-in UI. No literal ESC was displayed.
- `Attempt created:` printed the exact UUID and `csetty attempts list` in the
  same isolated state returned it during READING.
- CREATED at `2026-08-06T18:38:48.007287Z`; browser opened successfully and only
  then READING began at `2026-08-06T18:38:48.708375Z`.
- Edge opened one tokenized `http://127.0.0.1:50832/...` page. The companion
  listener was observed only on `127.0.0.1`.
- The true READING page visually used the COMP1511 green theme, contained all
  11 full prompts and the permitted bundled C reference, and had no Open VSC,
  external HTTP links, workspace, course container, or exam VS Code window.
  DOM evidence: 11 exact question IDs, 11 articles, 1 resource, Open VSC count
  0, external HTTP-link count 0.
- The existing page refreshed into WORKING at
  `2026-08-06T18:40:18.718373Z`; container and isolated VS Code were ready about
  6.41 s later, inside the 30 s window. The VS Code window used the exact image,
  same attempt/container, and showed the 11 starter files.
- Real Edge Open VSC produced
  `POST /92BO3ZNDmVRDffyqD7e4bZaRG2yqrF2C9n8R0ApseI4/reopen-code HTTP/1.1`
  status 200, displayed the success message, reused the same attempt/container,
  and showed no `Not found`. A later browser resubmission after the attempt was
  already FINISHED correctly received 409; it did not affect the successful
  required WORKING action or final report.
- The live non-reading `browser_open=lambda _: False` probe returned exit 0 in
  0.340 s and printed `PASS state=WORKING`; the existing container/page/VS Code
  remained usable. Log SHA-256:
  `8544141AFEAEF4E89A8CB062681F2FE452C76B030C8C92BE8D45F023FA19F84A`.
- While WORKING, `csetty report UUID` returned a non-final working report;
  `status.json` remained `WORKING` with `report_ready=false`, and the browser did
  not redirect. The required not-final screenshot was captured.
- Visible exam-terminal `check` exited 0, followed by `exam finish --yes` exit 0.
  The missing-submission warning and dummy 0/100 estimate were expected.
- Final state `FINISHED` at `2026-08-06T18:43:19.782532Z`, reason `student`.
  JSON/HTML report finalization completed and the existing companion page
  automatically opened authenticated HTTP `/report`; Edge showed the correct
  candidate/attempt, green theme, score evidence, and local-estimate notice.
  No Windows “Pick an app” dialog appeared.
- `csetty report` without an attempt ID and with the explicit ID both exited 0.

Two earlier COMP1511 evidence attempts were deliberately excluded from the
verdict and cleaned: `8999…` lacked a provable saved READING screenshot, and
`b556…` omitted the required visible `check` before finish. They were procedural
evidence gaps, not product failures. The complete flow above was rerun from
fresh state and is the sole COMP1511 verdict basis.

## 9. COMP1521 timed-expiry GUI flow

**PASS** — attempt:
`8a299437-24b1-4cf0-a4e2-7f2ebbf993cf`.

- Terminal clear/sign-in and printed/recoverable Attempt ID passed.
- CREATED at `2026-08-06T18:33:09.739959Z`; after successful browser opening,
  READING began at `2026-08-06T18:33:10.402280Z`.
- Edge opened the tokenized loopback page on `127.0.0.1:55252`. The teal true
  READING page contained all 10 complete prompts plus permitted C/MIPS resource.
  DOM evidence: 10 exact question IDs, 10 articles, 1 resource, 20 reading-lock
  markers, Open VSC count 0, external HTTP-link count 0. No container or VS Code
  workspace existed during READING.
- It automatically entered WORKING at `2026-08-06T18:34:40.410810Z` and exposed
  the live terminal exam prompt; the container network was `none`.
- No finish command was sent. The 75 s deadline expired at
  `2026-08-06T18:35:55.463090Z`, reason `deadline`; the interactive container
  stopped and the attempt became `EXPIRED`.
- JSON/HTML reports finalized, the original page automatically opened the
  authenticated HTTP `/report`, and Edge showed the same teal theme, correct
  candidate/attempt, `EXPIRED`, and expected dummy 0/100 evidence. No file URL,
  Pick-an-app dialog, or manual pre-open was used.
- `csetty report` without ID and with the explicit ID both exited 0.

## 10. Windows process, path, isolation, and cleanup checks

| Acceptance item | Verdict | Evidence |
|---|---:|---|
| Real detached companion probe | PASS | exact-wheel product `launch_companion`; health 200 before/after liveness; launch 0.766739 s; PID 13580 remained alive; exact cleanup left no process |
| Windows venv redirector supervisor probe | PASS | `ensure_supervisor` returned in 0.777065 s; wrapper PID 31288 and live lease/interpreter PID 48980 differed and were both alive; no 30 s timeout; exact cleanup empty |
| GUI startup windows | PASS | companion/supervisor and actual WORKING startup were within the required 30 s window |
| Windows paths | PASS | all state, wheel, report, bridge, pack, and workspace paths used valid drive-letter/backslash host semantics |
| Browser/report path behavior | PASS | tokenized authenticated loopback HTTP pages/reports; no file-URL drive-letter problem and no Pick-an-app dialog |
| User/state isolation | PASS | each final state root listed only its own final attempt; owner `LAPTOP-Q77UG2SK\Jiarui`; normal VS Code settings unchanged since 2026-02-11 |
| Container credential/isolation boundary | PASS | no Docker socket, host Git config, SSH agent, forwarded credentials, or network; rootfs/security/resource contract passed |
| Publication boundary | PASS | no registry push, Git tag, GitHub release, PyPI publication, or unexpected image occurred |
| Cleanup | PASS | current Docker containers 6 equal baseline 6; volumes 10 equal baseline 10; no new/missing IDs/names; four fresh image IDs absent; no current-run processes; isolated attempt/probe state sent to Recycle Bin |

Image receipts were state-local and exact:
COMP1511 SHA-256
`35335B790B3A44233F8F9B73246399F8A8003B2CE7B70195C28F0360FE278723`;
COMP1521 SHA-256
`39967C9778A42483BE0020364F9F55A2E5FC373B7001AC354E978D7CC2441251`.

Cleanup removed only this run's two stopped prepare containers, two prepare
volumes, two GUI attempt containers/volumes, probe/attempt processes, four fresh
image tags/IDs, and five isolated state directories. The five state directories
were moved to the Windows Recycle Bin and are recoverable until it is emptied.
Pre-existing a2 containers and volumes were left untouched.

Cleanup audit:
`C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\logs\final-cleanup-audit.json`.

## Required screenshots

| Screenshot | Absolute path | SHA-256 |
|---|---|---|
| terminal cleared/sign-in | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\01-terminal-signin-cleared.png` | `7E4AA1AA6071D0858C149A18DD23CA8F38B89894A1F58E6FCA3B34D4416688E2` |
| COMP1511 true READING full paper | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\02-comp1511-reading-full-paper.png` | `27FA2071D39C6E12B68C75FD802D95E79E71EA9C9607ABFC776AD09CE500CF60` |
| COMP1511 WORKING VS Code | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\03-comp1511-working-vscode.png` | `350CA6729AD158FEA95547C6769ED66567A9363CAF92B5C55F2E5200C0CDC85F` |
| COMP1511 WORKING report not final | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\03a-comp1511-working-report-not-final.png` | `07BB82B4A2DB4286762055D7D26E4C1AFC5D86100A10114F0D1B630DC63C39D1` |
| COMP1511 FINISHED HTTP report | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\04-comp1511-finished-report.png` | `96954CD7717AEA7B413647927BE0EFDC182B54FC5B4FDEC24819384254E2C42D` |
| COMP1521 true READING full paper | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\05-comp1521-reading-full-paper.png` | `AED7E18B20C403D774923FB81BB0BC3E3C8A4058C63C591C09289017BAF5A785` |
| COMP1521 EXPIRED HTTP report | `C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots\06-comp1521-expired-report.png` | `8866B25F8BD17A88E99C865F11445E841DE0BE0B8B3C08345D4034142C4BE945` |

The COMP1511 and COMP1521 READING images are real browser-state evidence, not
WORKING pages or terminal substitutes.

## Evidence index

Raw logs:
`C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\logs`.

Screenshots:
`C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\screenshots`.

Distributions:
`C:\Users\Jiarui\Documents\Codex\2026-08-06\l\outputs\windows-validation-0.1.0a3-bc9d47b\artifacts\dist`.

Key raw-log SHA-256 values:

- targeted regressions: `4A424E98BA6599BD8A43BB2B4414DBFC7E02ADDD6A0DD2029E75916456CC17D4`
- COMP1511 fixed: `7AAAAD4120BB6FAAB2F66EE32E467993242AA3354494116537B68ADD8C8A1F53`
- COMP1511 bank: `9F15782D9DCE3C20801B90B578C90B8C330AB19C088506FE9A8D6E40DDC3DBC0`
- COMP1521 fixed: `0202B31FC57B6D93C5E5C4CC3243D5F30B22AE9F4AFB756D0AA9758FD7BD4111`
- COMP1521 bank: `A9B59E39E718DCD1FC90FDBD4CD20CCED2C8F50964425E66D9D032E60919A795`
- detached companion probe: `3E93D7079E0AEC320C473460743F8A84FDA07A617012A2C15A33EB1BC6FC8318`
- supervisor redirector probe: `56E4DF30A9A162C5586F41D6C3CC551CA5B837488AA8CF9203644542EC3489AF`
- COMP1511 reading evidence: `58B3FDA71BEA67FF09EA3E9BF50A1AE2040A3ABD4A196DF61716FE9B528F1372`
- COMP1521 reading evidence: `B44E156441AFC76225D6EDAF332D39DF987373A61EA5C55FDE7B251F6013802D`
- final host pytest: `22C136DEC5FC3B230A82B320C61E27866B4289B6791A69BA2952A6CD3104980A`
- final Ruff: `A4443AFDCFB6D7363ADB285762515CCF7CF50473B1A05C20C1A50F6BED4D26B0`
- final mypy: `E7C982786727C1EA6B0E5E0346E1E60BA39748267137C4655285186D19E1C5E8`

## Final checkout state and Windows-specific findings

Final HEAD remained exactly
`bc9d47bb65ee246e488d3a14156c0965e530c754`, detached. The sole working-tree
path is the required untracked
`docs/WINDOWS_VALIDATION_RESULTS_0.1.0a3.md`. No commit or push was made.

Windows-specific product findings: **none observed**. Native process creation,
venv redirector PID handling, loopback browser flow, same-origin Open VSC,
terminal VT clearing, paths, isolation, finalization, and cleanup all matched
the a3 contract on this host.
