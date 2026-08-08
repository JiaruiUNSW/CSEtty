# Solution

## Approach

Scan entries and retain a copied best name plus size. Replace it when a regular file is larger, or when sizes tie and its name compares smaller with `strcmp`.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `different-sizes`, runs `./c1521_fs_016 scan`.
The test installs `tests/five.txt -> scan/long, tests/two.txt -> scan/short` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
long 6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After each examined entry, the retained candidate is the specified maximum among regular entries seen so far: replacement handles both ordering criteria. Induction gives the correct candidate after the final entry; absence of a candidate means no regular file existed.

## Complexity

Scanning `n` entries takes `O(n)` metadata operations and stores `O(1)` candidate records plus one name.

## Common pitfalls

Do not rely on iteration order, forget the tie rule, use `stat` and follow links, or print an implementation-dependent directory size.
