# Solution: Find the first signed decimal

## Approach

Scan for either a digit or a sign followed by a digit. Record the sign, then accumulate consecutive digit values and store the signed result.

## Correctness

Every position before the selected start is rejected by the exact token-start predicate. At the selected start the loop consumes exactly its digit run and computes its positional decimal value, so the first valid token is returned.

## Complexity

`O(n)` time and `O(1)` space.

## Common pitfalls

Accepting a bare sign, skipping the digit after rejecting a sign, using `isdigit` on a negative plain `char`, or relying on prohibited conversion functions. Do not weaken the provided compiler settings or hard-code the sample cases; the marking group includes different boundary inputs.
