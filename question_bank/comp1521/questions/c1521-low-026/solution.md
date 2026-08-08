# Encode a MIPS I-Format Word — solution guide

## Approach

Mask and shift each unsigned field to its assigned location, convert the signed immediate to its 16-bit representation, and OR all four non-overlapping pieces.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `addi`, runs `./c1521_low_026`.

Input:

```text
8 9 10 -4
```

Expected standard output:

```text
212afffc
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each masked field occupies exactly the bits defined by I-format and the ranges do not overlap. OR therefore constructs the unique instruction word with those fields.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Sign-extending the immediate into the upper half overwrites other fields. Decimal input and hexadecimal output use different format specifiers.
