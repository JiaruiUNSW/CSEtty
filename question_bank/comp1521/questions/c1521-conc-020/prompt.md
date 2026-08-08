# Forked Threaded Parity Scan

## Background

Threads created after `fork` live only inside the child process. Their shared-memory result must be joined and then explicitly transferred through IPC before the parent can observe it.

## Requirements

- Implement `c1521_conc_020.c` for one text file containing 1 to 1000 signed integers.
- Create one pipe and fork one child.
- The child opens/parses the file into owned memory, creates exactly three worker threads, and assigns indices `i, i+3, ...` to worker (i).
- Each worker computes local count, even/odd counts and sums, minimum, and maximum; it then locks one mutex and merges the entire local summary into child-shared state.
- The child joins all threads and sends one success-tagged summary to the parent.
- Parent reads it, waits for the child, and prints the specified fields in one line.
- Print exactly one line as `count=N even=E even_sum=ES odd=O odd_sum=OS min=MIN max=MAX`.

## Examples

Command:

```text
./c1521_conc_020 input.txt
```

Files provided for this example:

- `input.txt` (8 bytes) contains:

  ```text
  1 2 3 4
  ```

Output:

```text
count=4 even=2 even_sum=6 odd=2 odd_sum=4 min=1 max=4
```

## Implementation notes

The parent cannot read the child's mutex-protected memory directly because `fork` creates a separate address space. Merge min/max only from a local summary that has at least one value; zero is not a safe initial minimum. Close pipe ends, join all child threads, destroy the child mutex, use a complete structure transfer, and check `waitpid`. Submit `c1521_conc_020.c`.
