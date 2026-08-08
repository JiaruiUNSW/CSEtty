# Parallel Chunk Checksum

## Background

Large regular files can be divided into independent byte ranges. `pread` lets each worker read at explicit offsets without sharing a mutable file position.

## Requirements

- Implement `c1521_conc_004.c`, invoked as `./c1521_conc_004 FILE WORKERS`, where WORKERS is 1 through 8.
- Use `fstat` to obtain the regular-file length, split byte offsets with `start = size*i/WORKERS` and `end = size*(i+1)/WORKERS`, then fork one child per range.
- Each child opens the file, uses `pread`, and sends its byte count, unsigned-byte sum, and weighted sum through a dedicated pipe.
- A byte at absolute offset (k) contributes `byte * (k + 1)` to the weighted sum.
- The parent checks every result and wait status, adds partial values, and prints `bytes=N sum=S weighted=W`.
- All provided totals fit `unsigned long long`.

## Examples

Command:

```text
./c1521_conc_004 data.bin 1
```

Files provided for this example:

- `data.bin` (4 bytes) contains:

  ```text
  ABC
  ```

Output:

```text
bytes=4 sum=208 weighted=438
```

## Implementation notes

Use absolute offsets in the weighted calculation; a chunk-local index is wrong. Empty chunks are valid. Close unused pipe ends after `fork`, loop for partial pipe transfers, retry `pread` on `EINTR`, and reap recorded PIDs. No shared-memory synchronisation is needed. Submit only `c1521_conc_004.c`.
