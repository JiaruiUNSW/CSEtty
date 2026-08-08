# Exec-Squared Workers solution

## Approach

Recognize `--worker` before normal argument validation. Worker mode parses, squares, and prints. Normal mode creates all pipes, forks one process per input, redirects its selected writer to descriptor one, closes channel descriptors, and executes `argv[0]` in worker mode. The parent uses `fdopen`/`fscanf` on each reader, waits for stored PIDs, then prints stored squares by index.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `mixed-sign`, runs `./c1521_conc_008 2 -3 10`.

Input:

```text
(empty)
```

Expected standard output:

```text
0 square=4
1 square=9
2 square=100
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

A successful child image receives exactly its assigned textual value and worker mode prints that value squared to the pipe now attached to stdout. Dedicated channels prevent mixing. Parent index slots preserve the input association, and successful normal exit proves the exec'd worker completed. Thus each output line contains the required square in argument order.

## Complexity

With (N\le6), process/descriptor storage is (O(N)), each worker performs (O(1)) computation, and pipe traffic is (O(N)) short lines.

## Common pitfalls

Executing after leaving unrelated pipe writers open can prevent EOF. Using `execvp` with uncontrolled commands broadens the task unnecessarily. Forgetting that exec returns only on failure, failing to flush worker stdout, or printing results in reap order breaks the contract.
