# Encode a MIPS I-Format Word — solution guide

## Approach

Mask and shift each unsigned field to its assigned location, convert the signed immediate to its 16-bit representation, and OR all four non-overlapping pieces.

## Correctness

Each masked field occupies exactly the bits defined by I-format and the ranges do not overlap. OR therefore constructs the unique instruction word with those fields.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Sign-extending the immediate into the upper half overwrites other fields. Decimal input and hexadecimal output use different format specifiers.
