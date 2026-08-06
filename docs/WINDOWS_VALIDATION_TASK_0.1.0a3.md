# Windows 11 validation task for CSEExamTTY 0.1.0a3

## 1. Objective

Run a real native-Windows acceptance pass for the `0.1.0a3` release candidate on
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
6. timed expiry automatically generates and opens the report;
7. a `CREATED` recovery URL reveals neither questions nor resources;
8. a non-reading browser-launch failure does not strand a running attempt;
9. a practice `--skip-reading` attempt preserves that choice across recovery;
10. a report created while working cannot trigger the final-report redirect;
    and
11. concurrent working/final report publishers cannot overwrite the final
    report or leave a stale report advertised as ready.

## 2. Target and boundaries

- Repository: `https://github.com/JiaruiUNSW/CSEtty.git`
- Pull request: `https://github.com/JiaruiUNSW/CSEtty/pull/2`
- Branch: `codex/exam-flow-report-theme-a2` (the legacy branch suffix is not the
  package version)
- Exact validation commit: the full 40-character SHA supplied by the originating
  task immediately before validation; do not validate a moving branch tip
- Expected package/CLI version: `0.1.0a3`
- Expected dependency: `csetty-mips==0.1.1`

Use a fresh checkout under a new directory such as
`$env:USERPROFILE\Documents\CSEExamTTY-Windows-Validation-a3`. Do not overwrite,
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

Create `docs/WINDOWS_VALIDATION_RESULTS_0.1.0a3.md` in the checkout. It must
contain:

- start/end timestamps and elapsed time;
- Windows edition/build/architecture and hardware architecture;
- PowerShell, Python, Git, Docker Desktop/Engine, WSL and VS Code versions;
- the expected validation SHA and proof that checkout HEAD equals it exactly;
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
$validationRoot = Join-Path $env:LOCALAPPDATA "CSEExamTTY\validation-0.1.0a3-$stamp"
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
4. `03a-comp1511-working-report-not-final.png`
5. `04-comp1511-finished-report.png`
6. `05-comp1521-reading-full-paper.png`
7. `06-comp1521-expired-report.png`

Use the computer/browser control available on the Windows host when possible.
If GUI control is unavailable, capture equivalent screenshots with a real local
browser automation tool and explicitly mark which observations could not be
made visually. Do not silently infer that a page opened from HTML generation
alone.

## 4. Fresh checkout and host inventory

Run from native PowerShell, not from inside a WSL shell. Record all output.

```powershell
$checkout = Join-Path $env:USERPROFILE 'Documents\CSEExamTTY-Windows-Validation-a3'
$expectedHead = '<40-character commit SHA supplied by the originating task>'
if ($expectedHead -notmatch '^[0-9a-f]{40}$') {
    throw 'Set expectedHead to the exact lowercase commit SHA supplied for this run'
}
if (Test-Path $checkout) {
    throw "Validation checkout already exists; choose a new directory: $checkout"
}
git clone --branch codex/exam-flow-report-theme-a2 --single-branch `
    https://github.com/JiaruiUNSW/CSEtty.git $checkout
Set-Location $checkout
git checkout --detach $expectedHead
git status --short --branch
$actualHead = git rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $actualHead -ne $expectedHead) {
    throw "Checkout mismatch: expected $expectedHead, got $actualHead"
}
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

Confirm that Windows checkout conversion did not alter any byte-exact test
fixture. This compares every working-tree fixture directly with its Git blob
without interpreting its contents as text:

```powershell
$fixtureFiles = git ls-files 'question_bank/**/tests/**' 'packs/**/tests/**'
foreach ($relative in $fixtureFiles) {
    $expected = git rev-parse "HEAD:$relative"
    $actual = git hash-object --no-filters -- $relative
    if ($LASTEXITCODE -ne 0 -or $actual -ne $expected) {
        throw "Fixture bytes differ from Git blob: $relative"
    }
}
```

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

Expected version: `csetty 0.1.0a3`. All lint, type and test commands must exit
zero. Record the exact pytest count; do not copy the macOS count into the result.

Build and smoke-test the Windows-produced wheel from a clean output directory:

```powershell
$wheelDir = Join-Path $validationRoot 'wheel'
New-Item -ItemType Directory -Force $wheelDir | Out-Null
.\.venv\Scripts\python.exe -m pip wheel --no-deps --wheel-dir $wheelDir .
.\.venv\Scripts\python.exe scripts\smoke_wheel.py $wheelDir
Get-ChildItem $wheelDir
Get-FileHash (Join-Path $wheelDir 'cseexamtty-0.1.0a3-py3-none-any.whl') -Algorithm SHA256
```

The smoke must prove it imported from its temporary installed wheel, exposed
both built-in papers, retained author/student-pack isolation, and staged the
wheel-installed Docker build context. Confirm the wheel contains
`csetty/web_theme.py` and declares `Version: 0.1.0a3`.

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

### Targeted recovery and report-readiness contracts

Run the named tests separately and preserve their verbose output as
`targeted-regressions.txt` under the evidence directory:

```powershell
$regressionLog = Join-Path $evidenceRoot 'targeted-regressions.txt'
$regressionTests = @(
    'tests/test_companion.py::test_companion_browser_failure_is_nonfatal_without_reading_callback',
    'tests/test_companion.py::test_created_companion_withholds_paper_and_resource_routes',
    'tests/test_cli_start.py::test_resume_created_attempt_preserves_skip_reading_choice',
    'tests/test_companion.py::test_stale_working_report_is_not_ready_until_finalization_completes',
    'tests/test_storage.py::test_report_lock_serializes_another_process',
    'tests/test_storage.py::test_windows_process_liveness_probe_does_not_terminate_process',
    'tests/test_cli_start.py::test_working_report_cannot_overwrite_a_concurrent_final_report',
    'tests/test_attempt_service.py::test_failed_report_rewrite_hides_the_previous_final_report',
    'tests/test_attempt_service.py::test_aborted_attempt_report_remains_ungraded_and_nonfinal'
)
& .\.venv\Scripts\pytest.exe -vv @regressionTests *> $regressionLog
$regressionExit = $LASTEXITCODE
Get-Content $regressionLog
if ($regressionExit -ne 0) {
    throw "Targeted regression tests failed with exit code $regressionExit"
}
Get-FileHash $regressionLog -Algorithm SHA256
```

The log must prove these exact states:

- an explicit `browser_open` false result without a reading callback returns a
  healthy companion instead of raising;
- `CREATED` renders only the waiting page and rejects question/resource access;
- a persisted practice `--skip-reading` attempt resumes directly into working;
  and
- a working-time HTML/JSON pair plus a terminal state and even a grade are not
  sufficient for `report_ready`; only the later finalization marker publishes
  the report;
- native-Windows processes serialize on the same per-attempt report lock, and a
  forced working-report/finalization race leaves the durable report graded and
  `FINISHED`; and
- the native-Windows liveness probe observes a running process without
  terminating it and reports it dead only after normal termination; and
- a failed rewrite clears the old finalization marker instead of continuing to
  advertise stale report files; and
- an `ABORTED` attempt remains ungraded and is never published as a final
  `FINISHED`/`EXPIRED` report.

## 7. Create validation-only short packs

Do not edit anything under the Git checkout's `packs` directory. Copy each pack
to `$validationRoot\packs` and edit only the copied top-level identity and timing
values. Preserve every question, resource, prompt, starter, solution and test.

Create these two copies:

| Copy | New ID | Reading | Working | Purpose |
|---|---|---:|---:|---|
| COMP1511 | `comp1511-windows-a3-smoke` | 90 s | 300 s | explicit finish |
| COMP1521 | `comp1521-windows-a3-smoke` | 90 s | 75 s | timed expiry |

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
    $replacements = @(
        @{ Old = "id = `"$OldId`""; New = "id = `"$NewId`"" },
        @{ Old = 'reading_time_seconds = 600'; New = "reading_time_seconds = $ReadingSeconds" },
        @{ Old = 'working_time_seconds = 10800'; New = "working_time_seconds = $WorkingSeconds" }
    )
    foreach ($replacement in $replacements) {
        $count = ([regex]::Matches(
            $text,
            [regex]::Escape($replacement.Old)
        )).Count
        if ($count -ne 1) {
            throw "Expected exactly one manifest value, found ${count}: $($replacement.Old)"
        }
        $updated = $text.Replace($replacement.Old, $replacement.New)
        if ($updated -eq $text) {
            throw "Manifest substitution made no change: $($replacement.Old)"
        }
        $text = $updated
    }
    foreach ($expected in @(
        "id = `"$NewId`"",
        "reading_time_seconds = $ReadingSeconds",
        "working_time_seconds = $WorkingSeconds"
    )) {
        $count = ([regex]::Matches($text, [regex]::Escape($expected))).Count
        if ($count -ne 1) {
            throw "Expected exactly one final manifest value, found ${count}: $expected"
        }
    }
    [System.IO.File]::WriteAllText(
        $manifest,
        $text,
        [System.Text.UTF8Encoding]::new($false)
    )
}

$comp1511ShortPack = Join-Path $validationPacks 'comp1511-windows-a3-smoke'
$comp1521ShortPack = Join-Path $validationPacks 'comp1521-windows-a3-smoke'
New-ShortPack `
    -Source (Join-Path $checkout 'packs\comp1511-original-a') `
    -Destination $comp1511ShortPack `
    -OldId 'comp1511-original-a' `
    -NewId 'comp1511-windows-a3-smoke' `
    -ReadingSeconds 90 `
    -WorkingSeconds 300
New-ShortPack `
    -Source (Join-Path $checkout 'packs\comp1521-original-a') `
    -Destination $comp1521ShortPack `
    -OldId 'comp1521-original-a' `
    -NewId 'comp1521-windows-a3-smoke' `
    -ReadingSeconds 90 `
    -WorkingSeconds 75
```

After creating each copy, run `csetty pack validate PATH` and record `PASS`. Also
run `git status --short` and confirm the Git working tree remains unchanged
except for the required results Markdown file.

Every new PowerShell tab must repeat the environment setup; variables and venv
activation from the first tab are not inherited. Replace the first two values
with the absolute paths selected earlier, then use `$csetty` in that tab:

```powershell
$checkout = 'C:\absolute\path\to\CSEtty'
$validationRoot = 'C:\absolute\path\to\csetty-windows-a3-validation'
$stateRoot = Join-Path $validationRoot 'state'
$env:CSETTY_STATE_DIR = $stateRoot
$csetty = Join-Path $checkout '.venv\Scripts\csetty.exe'
$comp1511ShortPack = Join-Path $validationRoot 'packs\comp1511-windows-a3-smoke'
$comp1521ShortPack = Join-Path $validationRoot 'packs\comp1521-windows-a3-smoke'
& $csetty --version
```

## 8. COMP1511 explicit-finish GUI flow

Run this from a real interactive Windows Terminal/PowerShell tab using the
validation-only COMP1511 pack path and default VS Code editor:

```powershell
& $csetty start $comp1511ShortPack --mode exam
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
10. While the attempt is `WORKING`, induce a non-reading browser-launch failure
    against the live companion by running the following validation-only probe
    from the checkout venv. Substitute the recorded UUID. Save the script and
    output under `$evidenceRoot`, not in the repository:

    ```python
    import sys
    from csetty.companion import launch_companion
    from csetty.docker_runtime import DockerRuntime
    from csetty.models import AttemptState
    from csetty.paths import AppPaths
    from csetty.storage import Store

    paths = AppPaths.discover()
    store = Store(paths)
    attempt = store.resolve_attempt(sys.argv[1])
    assert attempt.state is AttemptState.WORKING
    info = launch_companion(paths, attempt, browser_open=lambda _url: False)
    current = store.get_attempt(attempt.id)
    assert current.state is AttemptState.WORKING
    assert DockerRuntime(paths)._container_running(current.container_name)
    print(f"PASS state={current.state.value} url={info.url}")
    ```

    Run it with `& .\.venv\Scripts\python.exe PROBE_PATH UUID`, require exit 0,
    and record the output, command duration, and SHA-256. The existing exam page,
    container and VS Code window must remain usable; this is the required
    evidence that a failed browser request does not strand a running attempt.
11. Still while `WORKING`, run `& $csetty report UUID` once to create the
    non-final working report. Read the token and port from
    `$stateRoot\attempts\UUID\companion.json`, request its `status.json`, and
    require `state` to remain `WORKING` and `report_ready` to remain `false`.
    The browser must remain on the working paper rather than redirecting. Capture
    `03a-comp1511-working-report-not-final.png`, plus the status JSON and report
    command output.
12. In the exam terminal run `check`, then `exam finish --yes` without submitting
    real answers. The warning for missing submissions is acceptable.
13. Finish writes JSON and HTML reports and automatically opens the HTML report
    in the host default browser.
14. The finished report shows the same COMP1511 green course visual language,
    the correct candidate/attempt ID, `FINISHED`, score evidence, and the local
    estimate notice.
15. The report remains available through `& $csetty report` without requiring
    the user to recover the attempt ID; the explicit ID remains accepted.

Confirm the companion listener is loopback-only. Use the page port with
`Get-NetTCPConnection -LocalPort PORT` and record every observed local address.
Only `127.0.0.1` or `::1` is acceptable; reject `0.0.0.0`, `::`, and every other
address, including all LAN/VPN interface addresses.

## 9. COMP1521 timed-expiry GUI flow

Run the validation-only COMP1521 pack in a new interactive Windows Terminal tab.
Use terminal editor mode so expiry can be observed without another VS Code
window:

```powershell
& $csetty start $comp1521ShortPack --mode exam --editor terminal
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
8. `& $csetty report` can recover the newest durable result without an ID; an
   explicit attempt ID remains accepted.

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

Only `docs/WINDOWS_VALIDATION_RESULTS_0.1.0a3.md` may be the sole path reported
by `git status` (normally as untracked). Do not commit or push the result unless
the originating task explicitly asks after reviewing it. Send the complete
result summary and screenshot attachments back to the originating Codex task.
