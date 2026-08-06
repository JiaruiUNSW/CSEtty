# Solution

## Approach

Open the source, create/truncate the destination, and repeatedly `pread` from `OFFSET + copied` into a fixed buffer bounded by remaining length. Completely write each returned chunk and stop on length exhaustion or EOF.

## Correctness

At loop start, the destination contains exactly the first `copied` available bytes of the requested range. The next positioned read obtains the following bytes and the complete-write loop appends all of them, preserving the invariant. Termination therefore leaves exactly the available requested range.

## Complexity

For `k` copied bytes, time is `O(k)` and auxiliary space is `O(1)`.

## Common pitfalls

Do not leave old destination suffix bytes, assume one write is complete, treat EOF as failure, or permit source and destination to be the same literal path.
