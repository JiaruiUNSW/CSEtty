# Bounded Square Queue solution

## Approach

Build a shared context containing a fixed circular buffer, indices, count, capacity, done flag, mutex, two conditions, inputs, and output array. The producer waits for space, inserts each indexed task, and signals consumers; then marks done and broadcasts. A consumer waits for work while not done, removes one task, signals space, unlocks, and writes that task's square to its unique result index. Main joins and formats results.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `capacity-one`, runs `./c1521_conc_017 1 1 2 -3`.

Input:

```text
(empty)
```

Expected standard output:

```text
0 square=4
1 square=9
total=13
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The mutex serializes every queue transition. The full/empty predicates keep count within zero and capacity. Producer enqueues each index once; each dequeue removes one queued task, so consumers collectively process every task exactly once. Done is observed under the same mutex, so a consumer exits only when no future task can arrive and the queue is empty. Unique index storage plus post-join printing yields all correct squares in input order.

## Complexity

For (N\le16), total work is (O(N)), queue storage is (O(C)) for capacity (C\le8), and results use (O(N)). Synchronisation operations are constant per task.

## Common pitfalls

Using `if` around `pthread_cond_wait` mishandles spurious wakeups. Setting done without the mutex loses ordering. Forgetting the final broadcast can strand consumers, and holding the lock while computing/printing creates needless blocking.
