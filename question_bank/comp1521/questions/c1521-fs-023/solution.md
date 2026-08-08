# Solution

## Approach

Open the source, create/truncate the destination, and repeatedly `pread` from `OFFSET + copied` into a fixed buffer bounded by remaining length. Completely write each returned chunk and stop on length exhaustion or EOF.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `middle-range`, runs `./c1521_fs_023 source out 2 4`.
The test installs `tests/alphabet.txt -> source` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
4
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

At loop start, the destination contains exactly the first `copied` available bytes of the requested range. The next positioned read obtains the following bytes and the complete-write loop appends all of them, preserving the invariant. Termination therefore leaves exactly the available requested range.

## Complexity

For `k` copied bytes, time is `O(k)` and auxiliary space is `O(1)`.

## Common pitfalls

Do not leave old destination suffix bytes, assume one write is complete, treat EOF as failure, or permit source and destination to be the same literal path.
