# Decode a MIPS R-Format Word — solution guide

## Approach

Apply a right shift and width mask for each field, then print all five unsigned values in the specified order.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `add`, runs `./c1521_low_030`.

Input:

```text
012a4020
```

Expected standard output:

```text
9 10 8 0 32
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The extraction intervals match the non-overlapping R-format field definitions. Shifting normalises each interval and masking removes unrelated high bits, so every printed field is exact.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not print the opcode or reorder `rd` and `rt`. The function field is six bits, not five.
