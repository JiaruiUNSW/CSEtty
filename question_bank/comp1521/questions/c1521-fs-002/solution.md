# Solution

## Approach

Parse each line with `strtoull`, split the value with shifts into four bytes, and write that array. Reopen the file, read four-byte units, reconstruct each word with shifts, and accumulate into `uint32_t` so arithmetic wraps modulo 2^32.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `three-words`, runs `./c1521_fs_002 words.bin`.

Input:

```text
1
256
65537
```

Expected standard output:

```text
count=3 checksum=65794
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The encoder places bits 31..24, 23..16, 15..8, and 7..0 into consecutive bytes. The decoder shifts those same fields back to their original positions, so each decoded value equals its input value. Counting decoded units and unsigned modular addition produces the required summary.

## Complexity

For `n` words, both time and file space are `O(n)`; auxiliary memory is `O(1)`.

## Common pitfalls

Host-endian `fwrite(&value, 4, 1, file)` is not portable. Also reject trailing junk, distinguish clean EOF from malformed input, and check `fclose` because buffered writes can fail there.
