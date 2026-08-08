# Concurrent Account Ledger

## Background

Ledger deltas are additive, so records can be applied in parallel if updates to the shared account table are protected. Sorting after the workers finish removes dependence on creation order.

## Requirements

- Implement `c1521_conc_013.c` as `./c1521_conc_013 FILE THREADS`, with 1 to 8 threads.
- The input has at most 1000 non-empty lines `account delta`; account names contain lowercase letters/digits, are at most 31 bytes, and there are at most 64 distinct accounts.
- Main must parse all operations first.
- Worker (i) applies operation indices `i, i+THREADS, ...` to a shared account table.
- Protect lookup/creation and addition as one mutex critical section.
- Join all threads, sort accounts lexicographically, and print `account=balance`, including zero balances.
- Values and sums fit `long long`.

## Examples

Command:

```text
./c1521_conc_013 ledger.txt 2
```

Files provided for this example:

- `ledger.txt` (23 bytes) contains:

  ```text
  alice 5
  bob 3
  alice -2
  ```

Output:

```text
alice=3
bob=3
```

## Implementation notes

Use stable arrays for parsed operations and thread arguments. Creating an account and applying its first delta must occur under the same lock. Keep error flags per job or protect a shared error. Join every created thread and destroy the mutex. Blank lines may be ignored; malformed non-empty lines return 1. Submit `c1521_conc_013.c`.
