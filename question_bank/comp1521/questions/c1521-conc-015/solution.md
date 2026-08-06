# Indexed Pipe Worker Farm solution

## Approach

Create task channels plus a common results channel before forking. Worker (w) retains only task reader (w) and the result writer. Parent sends indexed tasks round-robin and one negative-index sentinel per channel, closes writers, then reads fixed result records. It places each record in an array at its index, waits for all workers, validates completeness, and prints the array.

## Correctness

Round-robin dispatch sends every task to exactly one worker. A worker emits one correctly computed result before accepting the next task and emits none for the sentinel. Atomic result-record writes prevent interleaving. The parent checks and stores each unique task index, so after receiving the task count its array contains every required result once; index traversal restores input order.

## Complexity

For (N\le16) tasks and (W\le4), work and pipe traffic are (O(N)), while descriptors and worker state are (O(W)) and result storage is (O(N)).

## Common pitfalls

Printing as results arrive is nondeterministic. Multiple writers cannot safely use a loop that splits one record into several writes. Forgetting a sentinel or retaining task writers leaves workers blocked, and accepting duplicate indices can hide corrupted protocol data.
