# Joined Range Sum solution

## Approach

Allocate fixed arrays for at most eight thread objects and argument records. Compute each worker's half-open partition boundaries using integer division, translated to the required inclusive range. A worker loops through its range into its own partial field. The main thread joins all workers and then sums those fields.

## Correctness

Integer-division boundaries partition the first N positive integers into disjoint consecutive ranges whose union is 1 through N; some ranges may be empty. Each worker sums exactly its range into a unique slot, so there is no data race. Successful joins guarantee all slots are complete. Adding them therefore equals the sum of every integer 1 through N exactly once.

## Complexity

Total arithmetic work is (O(N)), main-thread storage is (O(T)), and each worker uses constant local storage for (T\le8).

## Common pitfalls

Passing `&i` to every thread causes all workers to observe changing state. Reading partials before join is a race. A mutex adds needless contention, while ignoring pthread error codes can read uninitialized slots.
