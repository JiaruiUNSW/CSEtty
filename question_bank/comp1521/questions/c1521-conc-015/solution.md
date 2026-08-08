# Indexed Pipe Worker Farm solution

## Approach

Create task channels plus a common results channel before forking. Worker (w) retains only task reader (w) and the result writer. Parent sends indexed tasks round-robin and one negative-index sentinel per channel, closes writers, then reads fixed result records. It places each record in an array at its index, waits for all workers, validates completeness, and prints the array.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-workers`, runs `./c1521_conc_015 2 2 -3 4`.

Input:

```text
(empty)
```

Expected standard output:

```text
0 value=2 square=4 cube=8
1 value=-3 square=9 cube=-27
2 value=4 square=16 cube=64
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Round-robin dispatch sends every task to exactly one worker. A worker emits one correctly computed result before accepting the next task and emits none for the sentinel. Atomic result-record writes prevent interleaving. The parent checks and stores each unique task index, so after receiving the task count its array contains every required result once; index traversal restores input order.

## Complexity

For (N\le16) tasks and (W\le4), work and pipe traffic are (O(N)), while descriptors and worker state are (O(W)) and result storage is (O(N)).

## Common pitfalls

Printing as results arrive is nondeterministic. Multiple writers cannot safely use a loop that splits one record into several writes. Forgetting a sentinel or retaining task writers leaves workers blocked, and accepting duplicate indices can hide corrupted protocol data.
