# Bounded Square Queue solution

## Approach

Build a shared context containing a fixed circular buffer, indices, count, capacity, done flag, mutex, two conditions, inputs, and output array. The producer waits for space, inserts each indexed task, and signals consumers; then marks done and broadcasts. A consumer waits for work while not done, removes one task, signals space, unlocks, and writes that task's square to its unique result index. Main joins and formats results.

## Correctness

The mutex serializes every queue transition. The full/empty predicates keep count within zero and capacity. Producer enqueues each index once; each dequeue removes one queued task, so consumers collectively process every task exactly once. Done is observed under the same mutex, so a consumer exits only when no future task can arrive and the queue is empty. Unique index storage plus post-join printing yields all correct squares in input order.

## Complexity

For (N\le16), total work is (O(N)), queue storage is (O(C)) for capacity (C\le8), and results use (O(N)). Synchronisation operations are constant per task.

## Common pitfalls

Using `if` around `pthread_cond_wait` mishandles spurious wakeups. Setting done without the mutex loses ordering. Forgetting the final broadcast can strand consumers, and holding the lock while computing/printing creates needless blocking.
