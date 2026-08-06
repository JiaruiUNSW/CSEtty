# Solution

## Approach

Parse each line with `strtoull`, split the value with shifts into four bytes, and write that array. Reopen the file, read four-byte units, reconstruct each word with shifts, and accumulate into `uint32_t` so arithmetic wraps modulo 2^32.

## Correctness

The encoder places bits 31..24, 23..16, 15..8, and 7..0 into consecutive bytes. The decoder shifts those same fields back to their original positions, so each decoded value equals its input value. Counting decoded units and unsigned modular addition produces the required summary.

## Complexity

For `n` words, both time and file space are `O(n)`; auxiliary memory is `O(1)`.

## Common pitfalls

Host-endian `fwrite(&value, 4, 1, file)` is not portable. Also reject trailing junk, distinguish clean EOF from malformed input, and check `fclose` because buffered writes can fail there.
