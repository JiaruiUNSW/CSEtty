# Joined Range Sum solution

## Approach

Allocate fixed arrays for at most eight thread objects and argument records. Compute each worker's half-open partition boundaries using integer division, translated to the required inclusive range. A worker loops through its range into its own partial field. The main thread joins all workers and then sums those fields.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `ten-two`, runs `./c1521_conc_010 10 2`.

Input:

```text
(empty)
```

Expected standard output:

```text
sum=55
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Integer-division boundaries partition the first N positive integers into disjoint consecutive ranges whose union is 1 through N; some ranges may be empty. Each worker sums exactly its range into a unique slot, so there is no data race. Successful joins guarantee all slots are complete. Adding them therefore equals the sum of every integer 1 through N exactly once.

## Complexity

Total arithmetic work is (O(N)), main-thread storage is (O(T)), and each worker uses constant local storage for (T\le8).

## Common pitfalls

Passing `&i` to every thread causes all workers to observe changing state. Reading partials before join is a race. A mutex adds needless contention, while ignoring pthread error codes can read uninitialized slots.
