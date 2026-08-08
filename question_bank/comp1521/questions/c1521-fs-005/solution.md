# Solution

## Approach

Parse offset and length with overflow checks, open the file, and seek once. Repeatedly read the smaller of the remaining length and buffer capacity. Print a separator before every byte except the first.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `middle-window`, runs `./c1521_fs_005 data 2 4`.
The test installs `tests/digits.txt -> data` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
32 33 34 35
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After `lseek`, the descriptor position is exactly `OFFSET`. Each read returns the next bytes and reduces the remaining budget by that count. Thus the emitted sequence is precisely the available prefix of the requested window, and processing stops exactly on budget exhaustion or EOF.

## Complexity

If `k` bytes are available in the window, time is `O(k)` and auxiliary space is `O(1)`.

## Common pitfalls

Do not allocate `LENGTH` bytes, print signed `char` values, add a leading/trailing space, treat EOF as an error, or silently accept negative strings.
