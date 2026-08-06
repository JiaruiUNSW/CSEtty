# Solution

## Approach

Parse offset and length with overflow checks, open the file, and seek once. Repeatedly read the smaller of the remaining length and buffer capacity. Print a separator before every byte except the first.

## Correctness

After `lseek`, the descriptor position is exactly `OFFSET`. Each read returns the next bytes and reduces the remaining budget by that count. Thus the emitted sequence is precisely the available prefix of the requested window, and processing stops exactly on budget exhaustion or EOF.

## Complexity

If `k` bytes are available in the window, time is `O(k)` and auxiliary space is `O(1)`.

## Common pitfalls

Do not allocate `LENGTH` bytes, print signed `char` values, add a leading/trailing space, treat EOF as an error, or silently accept negative strings.
