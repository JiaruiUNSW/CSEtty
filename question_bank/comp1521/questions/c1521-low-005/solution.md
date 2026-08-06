# Clamp a Control Value — solution guide

## Approach

Compare the value with `low`; if smaller, select `low`. Otherwise compare `high` with the value; if true, select `high`. Otherwise retain the original value.

## Correctness

The three branches partition all valid inputs into below-range, above-range, and inclusive in-range cases, and each branch selects the definition of clamping for that case.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Swapping the operands to `slt` reverses the condition. Values exactly equal to a bound must remain unchanged, though their printed number equals that bound.
