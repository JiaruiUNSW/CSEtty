# Forked File Totals solution

## Approach

Create two pipes before forking. Each child closes all pipe ends except its own writer, opens its assigned file, scans bytes into signed integers, and sends one result structure with a complete-write helper. The parent closes all writers, completely reads one structure from each reader, then waits for the exact PIDs. It stores results by child index and prints only after collection.

## Correctness

Each input file is opened and scanned by exactly its assigned child, so every integer contributes once to that child's count and sum. A dedicated pipe has one writer, so the complete result cannot be mixed with another result. Index-based storage makes output independent of child completion order. Waiting for every recorded PID proves no child remains unreaped before successful return.

## Complexity

For total input size (B), work is (O(B)), pipe traffic is (O(1)) per child, and auxiliary memory is (O(1)). The two children may scan concurrently.

## Common pitfalls

Leaving pipe write ends open in the parent prevents EOF. Using `wait(NULL)` and printing immediately makes order nondeterministic. A single `read` or `write` is not guaranteed to transfer the whole structure, and child errors must be communicated rather than silently producing zeros.

