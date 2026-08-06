# Worked solution — Q5

## Approach

Read each byte with `getchar`. Convert it to an unsigned value and count it when
its two high bits are not `10`, using `(byte & 0xC0u) != 0x80u`.

## Correctness

In valid UTF-8, every code point has exactly one byte that is not a continuation
byte: its ASCII byte or its multibyte leading byte. All remaining bytes of that
code point have prefix `10` and are excluded. Thus each code point contributes
exactly one to the counter, so the final count is correct.

## Complexity

For b input bytes, time is O(b) and extra space is O(1).

## Common pitfalls

- Counting bytes rather than leading bytes.
- Comparing a possibly signed `char` without an unsigned mask.
- Forgetting that an input newline is itself a code point.
- Claiming this shortcut validates malformed UTF-8; validity is guaranteed here.

