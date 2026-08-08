# Concurrent Account Ledger solution

## Approach

Main reads the file with `getline`, validates each non-empty line, and grows an operation array. It initializes a ledger and mutex, then starts workers with distinct initial indices and a common stride. For each operation a worker locks, finds or creates the account, applies the delta, and unlocks. Main joins, sorts the final account records, prints, and frees all owned memory.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-accounts`, runs `./c1521_conc_013 ledger.txt 2`.
The test installs `tests/two_accounts.txt -> ledger.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
alice=3
bob=3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Modulo-stride assignment partitions operation indices, so each parsed delta is applied exactly once. The mutex makes lookup/creation/addition atomic, preventing duplicate account entries and lost updates. Addition for each account is commutative, so any valid lock acquisition order yields the same balance. Sorting after join establishes deterministic lexical output.

## Complexity

For (R) operations and at most (A=64) accounts, linear lookup costs (O(RA)); sorting costs (O(A\log A)). Storage is (O(R+A+T)).

## Common pitfalls

Locking only the addition but not account creation can create duplicates. Printing in table insertion order leaks scheduling order. Workers must not use a `getline` buffer that main later frees, and failure paths still need joins, destruction, and deallocation.
