# Solution

## Approach

For every regular child, find its last dot with `strrchr` and derive the extension under the stated rules. Find or create that group in a growing array, updating count and bytes. Sort groups by extension before printing.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `two-extensions`, runs `./c1521_fs_018 scan`.
The test installs `tests/aa.txt -> scan/a.c, tests/bbb.txt -> scan/b.c, tests/z.txt -> scan/note.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
c 2 7
txt 1 2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each immediate regular file maps to exactly one defined extension key and contributes its size once to that key. Non-regular entries never contribute. Aggregation therefore forms the exact groups, and sorting produces the required report order.

## Complexity

With `n` files and `g` extensions, a simple linear group lookup costs `O(ng)` and sorting `O(g log g)`; storage is `O(g)`.

## Common pitfalls

Use the last dot, classify a leading-only or trailing dot as no extension, do not include subdirectory contents, and avoid relying on `d_type`.
