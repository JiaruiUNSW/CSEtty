# ASCII Class Code — solution guide

## Approach

Test the digit, uppercase, and lowercase intervals in order. Assign the corresponding category when both endpoints contain the input; otherwise retain zero.

## Correctness

The three ASCII intervals are disjoint and exactly describe the requested classes. The first successful interval selects its code; if none succeeds, the required default is zero.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Inclusive endpoints are easy to exclude accidentally. Compare numeric ASCII codes, not the decimal digit value represented by a character.
