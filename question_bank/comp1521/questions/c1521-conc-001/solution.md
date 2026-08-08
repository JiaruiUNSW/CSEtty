# Forked File Totals solution

## Approach

Create two pipes before forking. Each child closes all pipe ends except its own writer, opens its assigned file, scans bytes into signed integers, and sends one result structure with a complete-write helper. The parent closes all writers, completely reads one structure from each reader, then waits for the exact PIDs. It stores results by child index and prints only after collection.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `small-positive`, runs `./c1521_conc_001 left.txt right.txt`.
The test installs `tests/public_left.txt -> left.txt, tests/public_right.txt -> right.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
0 count=3 sum=6
1 count=2 sum=30
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each input file is opened and scanned by exactly its assigned child, so every integer contributes once to that child's count and sum. A dedicated pipe has one writer, so the complete result cannot be mixed with another result. Index-based storage makes output independent of child completion order. Waiting for every recorded PID proves no child remains unreaped before successful return.

## Complexity

For total input size (B), work is (O(B)), pipe traffic is (O(1)) per child, and auxiliary memory is (O(1)). The two children may scan concurrently.

## Common pitfalls

Leaving pipe write ends open in the parent prevents EOF. Using `wait(NULL)` and printing immediately makes order nondeterministic. A single `read` or `write` is not guaranteed to transfer the whole structure, and child errors must be communicated rather than silently producing zeros.
