# Solution

## Approach

Parse a strictly positive unsigned record size, call `stat`, verify `S_ISREG`, and divide `st_size` by that value. The quotient is the record count and the remainder is the trailing-byte count.

## Correctness

Euclidean division states that file size equals `R * RECORD_SIZE + T` with `0 <= T < RECORD_SIZE`. Integer quotient and remainder therefore produce exactly the required complete-record count and incomplete suffix length.

## Complexity

One metadata lookup and constant arithmetic require `O(1)` time and space in user code.

## Common pitfalls

Reject record size zero, directories, negative strings, and overflow. Do not cast file size to `int` or round up a partial record.
