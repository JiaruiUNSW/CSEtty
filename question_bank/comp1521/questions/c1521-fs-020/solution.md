# Solution

## Approach

Validate file size is divisible by six, compare index with the quotient, and compute `index * 6`. Call `pread` for exactly six bytes, verify the final byte is newline, and write the first five.

## Correctness

Divisibility establishes a complete-record sequence. For an in-range index, fixed-width arithmetic identifies exactly its first byte and `pread` returns that record independently of descriptor position. The validated newline separates the data, so output is precisely the five-byte payload.

## Complexity

The operation reads a constant six bytes and uses `O(1)` time and space apart from filesystem lookup.

## Common pitfalls

Reject a partial final record, guard offset multiplication, handle a short `pread`, and do not treat payload bytes as a zero-terminated string.
