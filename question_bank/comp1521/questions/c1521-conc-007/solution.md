# Child Exit Histogram solution

## Approach

Parse and validate the argument array first. Fork children into a PID array, where child (i) calls `_exit(codes[i])`. The parent waits for recorded PIDs, verifies `WIFEXITED`, extracts `WEXITSTATUS`, and increments an eight-element counter. Finally it scans the counter from zero to seven and prints nonzero entries.

## Correctness

Each validated argument creates exactly one child that exits with that value. Waiting for that child's stored PID associates one termination with one created child. POSIX status macros recover its normal exit code, so incrementing the indexed counter once per PID yields the exact histogram. Ascending array traversal gives deterministic output.

## Complexity

For (N\le8) children, time outside process creation is (O(N)), storage is (O(N)), and the histogram is constant size.

## Common pitfalls

Comparing the raw status integer to the requested code is incorrect. `wait(NULL)` can still count correctly but makes error attribution harder. Unvalidated values are truncated by `_exit`, and early parent returns can leave zombies.
