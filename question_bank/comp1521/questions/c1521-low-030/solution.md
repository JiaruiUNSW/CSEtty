# Decode a MIPS R-Format Word — solution guide

## Approach

Apply a right shift and width mask for each field, then print all five unsigned values in the specified order.

## Correctness

The extraction intervals match the non-overlapping R-format field definitions. Shifting normalises each interval and masking removes unrelated high bits, so every printed field is exact.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not print the opcode or reorder `rd` and `rt`. The function field is six bits, not five.
