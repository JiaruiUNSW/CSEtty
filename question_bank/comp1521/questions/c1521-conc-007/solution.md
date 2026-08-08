# Child Exit Histogram solution

## Approach

Parse and validate the argument array first. Fork children into a PID array, where child (i) calls `_exit(codes[i])`. The parent waits for recorded PIDs, verifies `WIFEXITED`, extracts `WEXITSTATUS`, and increments an eight-element counter. Finally it scans the counter from zero to seven and prints nonzero entries.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `mixed`, runs `./c1521_conc_007 0 1 1 3`.

Input:

```text
(empty)
```

Expected standard output:

```text
status 0 count=1
status 1 count=2
status 3 count=1
children=4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each validated argument creates exactly one child that exits with that value. Waiting for that child's stored PID associates one termination with one created child. POSIX status macros recover its normal exit code, so incrementing the indexed counter once per PID yields the exact histogram. Ascending array traversal gives deterministic output.

## Complexity

For (N\le8) children, time outside process creation is (O(N)), storage is (O(N)), and the histogram is constant size.

## Common pitfalls

Comparing the raw status integer to the requested code is incorrect. `wait(NULL)` can still count correctly but makes error attribution harder. Unvalidated values are truncated by `_exit`, and early parent returns can leave zombies.
