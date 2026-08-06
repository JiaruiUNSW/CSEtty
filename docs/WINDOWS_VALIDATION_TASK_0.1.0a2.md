# Windows 11 validation task for CSEExamTTY 0.1.0a2

## 1. Objective

Run a real native-Windows acceptance pass for the `0.1.0a2` release candidate on
`LAPTOP-Q77UG2SK`. This is not a source review and must not be replaced by the
GitHub Actions `windows-latest` host-contract job. The acceptance target is the
actual Windows 11 desktop combination of:

- native Windows Python and PowerShell/Windows Terminal;
- Docker Desktop using its WSL2 Linux-container backend;
- the installed desktop VS Code and its `code` command;
- the host default browser; and
- the exact CSEExamTTY branch and wheel described below.

The validation must exercise the visible defects addressed by the candidate:

1. the invoking terminal screen and scrollback are cleared before exam sign-in;
2. reading time opens the complete read-only paper, not only question names;
3. the attempt ID is printed and recoverable;
4. COMP1511 and COMP1521 live/report pages use their consistent course themes;
5. explicit finish automatically generates and opens the report; and
6. timed expiry automatically generates and opens the report.

## 2. Target and boundaries

- Repository: `https://github.com/JiaruiUNSW/CSEtty.git`
- Pull request: `https://github.com/JiaruiUNSW/CSEtty/pull/2`
- Branch: `codex/exam-flow-report-theme-a2`
- Implementation commit that must be an ancestor of the checkout:
  `71087b122b56fad132a3fb4d895887648dbb8ef4`
- Expected package/CLI version: `0.1.0a2`
- Expected dependency: `csetty-mips==0.1.1`

Use a fresh checkout under a new directory such as
`$env:USERPROFILE\Documents\CSEExamTTY-Windows-Validation-a2`. Do not overwrite,
reset, clean, or delete an existing checkout. Do not modify product source,
tests, manifests, release approval, tags, releases, PyPI, the user's normal VS
Code profile, or unrelated Docker resources.

The only permitted local test-content mutation is copying a supplied pack to a
new validation-only directory outside the Git working tree and shortening its
reading/working times as described in section 8. Never edit the supplied pack.

Use only dummy simulation credentials. A suitable candidate ID is `z5555555` and
the password can be `validation-only`. Never enter a real UNSW password or any
other credential. Do not publish screenshots containing secrets.

Normal project-scoped actions are authorized: clone/fetch the public repository,
create a `.venv`, install its declared development dependencies, build local
images, create temporary containers/volumes/state, open the isolated CSEExamTTY
VS Code profile, open loopback browser pages, and write validation evidence. A
Windows restart, Docker Desktop backend switch, admin elevation, firewall
change, or source-code fix is not pre-authorized: report the exact blocker and
wait for the user instead.

## 3. Required evidence and final output

Create `docs/WINDOWS_VALIDATION_RESULTS_0.1.0a2.md` in the checkout. It must
contain:

- start/end timestamps and elapsed time;
- Windows edition/build/architecture and hardware architecture;
- PowerShell, Python, Git, Docker Desktop/Engine, WSL and VS Code versions;
- exact checkout HEAD and proof that implementation commit `71087b1...` is an
  ancestor;
- every acceptance item below marked `PASS`, `FAIL`, `BLOCKED`, or `SKIPPED`;
- command, exit code, duration and a concise output excerpt for every automated
  check;
- exact attempt IDs and final state for both GUI flows;
- absolute paths and SHA-256 hashes for the built wheel and all screenshots;
- exact error text, log path and the earliest failing step for any failure;
- a final overall verdict; and
- a concise list of Windows-specific findings, including "none observed" when
  appropriate.

Keep raw logs and screenshots under a new validation directory, not in Git. For
example:

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$validationRoot = Join-Path $env:LOCALAPPDATA "CSEExamTTY\validation-0.1.0a2-$stamp"
$stateRoot = Join-Path $validationRoot 'state'
$evidenceRoot = Join-Path $validationRoot 'evidence'
New-Item -ItemType Directory -Force $stateRoot, $evidenceRoot | Out-Null
$env:CSETTY_STATE_DIR = $stateRoot
Start-Transcript -Path (Join-Path $evidenceRoot 'powershell-transcript.txt')
```

Take at least these screenshots and attach them to the remote Codex task's final
reply in addition to recording their absolute paths and hashes:

1. `01-terminal-signin-cleared.png`
2. `02-comp1511-reading-full-paper.png`
3. `03-comp1511-working-vscode.png`
4. `04-comp1511-finished-report.png`
5. `05-comp1521-reading-full-paper.png`
6. `06-comp1521-expired-report.png`

Use the computer/browser control available on the Windows host when possible.
If GUI control is unavailable, capture equivalent screenshots with a real local
browser automation tool and explicitly mark which observations could not be
made visually. Do not silently infer that a page opened from HTML generation
alone.

## 4. Fresh checkout and host inventory

Run from native PowerShell, not from inside a WSL shell. Record all output.

```powershell
$checkout = Join-Path $env:USERPROFILE 'Documents\CSEExamTTY-Windows-Validation-a2'
if (Test-Path $checkout) {
    throw "Validation checkout already exists; choose a new directory: $checkout"
}
git clone --branch codex/exam-flow-report-theme-a2 --single-branch `
    https://github.com/JiaruiUNSW/CSEtty.git $checkout
Set-Location $checkout
git status --short --branch
git rev-parse HEAD
git merge-base --is-ancestor 71087b122b56fad132a3fb4d895887648dbb8ef4 HEAD
if ($LASTEXITCODE -ne 0) { throw 'Required implementation commit is not an ancestor' }
```

Inventory commands:

```powershell
$PSVersionTable
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsBuildNumber, OsArchitecture
Get-CimInstance Win32_ComputerSystem | Select-Object Manufacturer, Model, SystemType
py -0p
python --version
git --version
docker version
docker info --format 'OSType={{.OSType}} Architecture={{.Architecture}} OperatingSystem={{.OperatingSystem}}'
wsl --version
wsl --status
code --version
Get-Command python, git, docker, wsl, code | Format-List Name, Source
```

Acceptance requirements:

- Windows 11 is identified with its exact build.
- Host Python is CPython 3.11, 3.12 or 3.13. Prefer 3.11 when installed.
- `docker info` reports Linux containers and an available daemon.
- Docker Desktop is using the WSL2 backend; record `wsl --status` rather than
  assuming this from Docker availability.
- desktop VS Code and the `code` command are available.

If Docker Desktop is merely stopped, starting the already installed application
is in scope. Do not change its backend or Windows features without user approval.

## 5. Native Windows host contract and exact-wheel smoke

Create a checkout-local virtual environment. Use Python 3.11 when available;
otherwise substitute another installed supported CPython and record it.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --disable-pip-version-check -e ".[dev]"
.\.venv\Scripts\csetty.exe --version
.\.venv\Scripts\ruff.exe check src tests scripts
.\.venv\Scripts\mypy.exe src/csetty
.\.venv\Scripts\pytest.exe -q
```

Expected version: `csetty 0.1.0a2`. All lint, type and test commands must exit
zero. Record the exact pytest count; do not copy the macOS count into the result.

Build and smoke-test the Windows-produced wheel from a clean output directory:

```powershell
$wheelDir = Join-Path $validationRoot 'wheel'
New-Item -ItemType Directory -Force $wheelDir | Out-Null
.\.venv\Scripts\python.exe -m pip wheel --no-deps --wheel-dir $wheelDir .
.\.venv\Scripts\python.exe scripts\smoke_wheel.py $wheelDir
Get-ChildItem $wheelDir
Get-FileHash (Join-Path $wheelDir 'cseexamtty-0.1.0a2-py3-none-any.whl') -Algorithm SHA256
```

The smoke must prove it imported from its temporary installed wheel, exposed
both built-in papers, retained author/student-pack isolation, and staged the
wheel-installed Docker build context. Confirm the wheel contains
`csetty/web_theme.py` and declares `Version: 0.1.0a2`.

## 6. Docker Desktop and fixed-content acceptance

Run the host doctor before changing project state:

```powershell
.\.venv\Scripts\csetty.exe doctor
```

Then run the explicit networked preparation phase. It may take substantial time
because DCC and both course images are built locally:

```powershell
.\.venv\Scripts\csetty.exe prepare --profile comp1511
.\.venv\Scripts\csetty.exe doctor --offline-ready comp1511
.\.venv\Scripts\csetty.exe prepare --profile comp1521
.\.venv\Scripts\csetty.exe doctor --offline-ready comp1521
```

During each prepare, visibly confirm:

- a separately labelled CSEExamTTY VS Code window opens;
- it uses the application-owned isolated profile, not the normal profile;
- host-side Dev Containers is available;
- COMP1511 has the remote C/C++ extension;
- COMP1521 has remote C/C++ and Mipsy Editor Features;
- preparation reaches its completion page; and
- the exact matching VS Code Server is observed even after the prepared
  container has networking disabled.

Do not count a command exit alone as GUI acceptance. Record any trust/extension
prompt and how it was resolved. A prompt requiring a policy decision is
`BLOCKED`, not permission to weaken isolation.

After both profiles are ready, run:

```powershell
.\.venv\Scripts\python.exe scripts\docker_acceptance.py --profile all
.\.venv\Scripts\csetty.exe pack verify packs\comp1511-original-a `
    --reference packs\comp1511-original-a\solutions\reference
.\.venv\Scripts\csetty.exe bank verify comp1511
.\.venv\Scripts\csetty.exe pack verify packs\comp1521-original-a `
    --reference packs\comp1521-original-a\solutions\reference
.\.venv\Scripts\csetty.exe bank verify comp1521
```

All must exit zero. Confirm `csetty-mips 0.1.1` is the COMP1521 runtime and no
upstream mipsy checkout or executable is used.

## 7. Create validation-only short packs

Do not edit anything under the Git checkout's `packs` directory. Copy each pack
to `$validationRoot\packs` and edit only the copied top-level identity and timing
values. Preserve every question, resource, prompt, starter, solution and test.

Create these two copies:

| Copy | New ID | Reading | Working | Purpose |
|---|---|---:|---:|---|
| COMP1511 | `comp1511-windows-a2-smoke` | 90 s | 300 s | explicit finish |
| COMP1521 | `comp1521-windows-a2-smoke` | 90 s | 75 s | timed expiry |

Use a PowerShell routine equivalent to:

```powershell
$validationPacks = Join-Path $validationRoot 'packs'
New-Item -ItemType Directory -Force $validationPacks | Out-Null

function New-ShortPack {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$OldId,
        [string]$NewId,
        [int]$ReadingSeconds,
        [int]$WorkingSeconds
    )
    Copy-Item $Source $Destination -Recurse
    $manifest = Join-Path $Destination 'pack.toml'
    $text = Get-Content $manifest -Raw
    $text = $text.Replace("id = `"$OldId`"", "id = `"$NewId`"")
    $text = $text.Replace('reading_time_seconds = 600', "reading_time_seconds = $ReadingSeconds")
    $text = $text.Replace('working_time_seconds = 10800', "working_time_seconds = $WorkingSeconds")
    [System.IO.File]::WriteAllText(
        $manifest,
        $text,
        [System.Text.UTF8Encoding]::new($false)
    )
}

$comp1511ShortPack = Join-Path $validationPacks 'comp1511-windows-a2-smoke'
$comp1521ShortPack = Join-Path $validationPacks 'comp1521-windows-a2-smoke'
New-ShortPack `
    -Source (Join-Path $checkout 'packs\comp1511-original-a') `
    -Destination $comp1511ShortPack `
    -OldId 'comp1511-original-a' `
    -NewId 'comp1511-windows-a2-smoke' `
    -ReadingSeconds 90 `
    -WorkingSeconds 300
New-ShortPack `
    -Source (Join-Path $checkout 'packs\comp1521-original-a') `
    -Destination $comp1521ShortPack `
    -OldId 'comp1521-original-a' `
    -NewId 'comp1521-windows-a2-smoke' `
    -ReadingSeconds 90 `
    -WorkingSeconds 75
```

After creating each copy, run `csetty pack validate PATH` and record `PASS`. Also
run `git status --short` and confirm the Git working tree remains unchanged
except for the required results Markdown file.

## 8. COMP1511 explicit-finish GUI flow

Run this from a real interactive Windows Terminal/PowerShell tab using the
validation-only COMP1511 pack path and default VS Code editor:

```powershell
.\.venv\Scripts\csetty.exe start $comp1511ShortPack --mode exam
```

Interact with dummy values `z5555555`, `validation-only`, and `yes`. Validate in
order:

1. After invoking the command and before the welcome/sign-in UI, the visible
   terminal and its scrollback no longer contain the command or earlier output.
   Capture `01-terminal-signin-cleared.png`.
2. After acknowledgement, an `Attempt created: UUID` line is printed. Record the
   UUID. In a second host terminal, `csetty attempts list` must list the same ID.
   Set that terminal's `CSETTY_STATE_DIR` to the same `$stateRoot` first.
3. Reading time automatically opens one browser tab on a tokenized
   `http://127.0.0.1:<port>/...` URL.
4. The reading page contains all 11 complete question prompts and the permitted
   bundled C reference. It must not be merely a list of titles.
5. Reading view contains no **Open VSC** control and no external course links.
6. No workspace, interactive course container or VS Code exam window exists
   before reading time ends.
7. The page visibly uses the COMP1511 green course variant (`#6abd6e`), has no
   unintended horizontal overflow at normal desktop width, and remains usable
   at a narrow/mobile-width browser viewport.
8. At the transition to working time, the existing page refreshes rather than
   opening a duplicate companion tab; the starter workspace/container and
   isolated VS Code window then open.
9. The working view exposes **Open VSC**. Invoke it once and confirm it reconnects
   to the same attempt/container rather than creating a new attempt.
10. In the exam terminal run `check`, then `exam finish --yes` without submitting
    real answers. The warning for missing submissions is acceptable.
11. Finish writes JSON and HTML reports and automatically opens the HTML report
    in the host default browser.
12. The finished report shows the same COMP1511 green course visual language,
    the correct candidate/attempt ID, `FINISHED`, score evidence, and the local
    estimate notice.
13. The report remains available through `csetty report ATTEMPT_ID`.

Confirm the companion listener is loopback-only. Use the page port with
`Get-NetTCPConnection -LocalPort PORT` and record that it is not bound to
`0.0.0.0` or a LAN interface.

## 9. COMP1521 timed-expiry GUI flow

Run the validation-only COMP1521 pack in a new interactive Windows Terminal tab.
Use terminal editor mode so expiry can be observed without another VS Code
window:

```powershell
.\.venv\Scripts\csetty.exe start $comp1521ShortPack --mode exam --editor terminal
```

Use the same dummy simulation credentials and validate:

1. terminal clear/sign-in behavior remains correct;
2. the attempt ID is printed and recoverable with `csetty attempts list`;
3. reading time opens all 10 complete prompts and the permitted bundled C/MIPS
   reference, with no workspace/container during reading;
4. the live page visibly uses the COMP1521 teal variant (`#42a097`) and is usable
   at desktop and narrow viewport widths;
5. after reading time, allow the 75-second working deadline to expire without
   calling `exam finish`;
6. expiry stops the interactive container, grades the latest accepted snapshots,
   writes JSON/HTML reports and automatically opens the HTML report;
7. the report uses the same COMP1521 teal course visual language and records the
   attempt as `EXPIRED`; and
8. `csetty report ATTEMPT_ID` can recover the durable result.

Do not manually open the report before deciding whether automatic opening
worked. If it does not open, record whether the report file still exists and the
exact supervisor/companion log messages.

## 10. Windows-specific process, path and isolation checks

For both attempts, record evidence that:

- generated paths use valid Windows semantics and contain no literal POSIX-only
  executable path assumptions on the host;
- detached companion/supervisor processes remain alive when required and exit
  or become harmless after terminal attempt completion;
- browser file URLs correctly handle Windows drive letters and spaces;
- the normal VS Code profile and extensions remain unchanged;
- exam containers have no Docker socket, Git config, SSH agent or forwarded
  credentials;
- exam containers use no network by default;
- their root filesystem/security limits match `docker_acceptance.py`; and
- no unexpected Docker image, registry push, Git tag, GitHub Release or PyPI
  publication occurs.

Use read-only inspection first. Do not delete broad Docker caches, volumes,
images, user settings or state as part of validation.

## 11. Verdict rules

Overall `PASS` requires every mandatory item in sections 4–10 to pass. Use:

- `FAIL` for reproducible product behavior that violates the contract;
- `BLOCKED` for an environmental or approval gate that prevents a conclusion;
- `SKIPPED` only for an explicitly optional observation, with justification.

Do not convert a failure into a pass by editing source or tests. On failure,
perform bounded read-only diagnosis, preserve logs/screenshots, identify the
smallest likely component, and report back. Do not implement a fix in this task.

Before finalizing, run:

```powershell
.\.venv\Scripts\pytest.exe -q
git status --short --branch
Stop-Transcript
```

Only `docs/WINDOWS_VALIDATION_RESULTS_0.1.0a2.md` may be a new/modified tracked
file. Do not commit or push the result unless the originating task explicitly
asks after reviewing it. Send the complete result summary and screenshot
attachments back to the originating Codex task.
