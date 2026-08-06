# Worked solution — Q1

## Approach

For a non-zero amount, shift the word right to place the low portion and shift
it left by the complementary distance to wrap the discarded bits into the high
positions. Combine the two parts with bitwise OR. Return early when the amount
is zero so that no expression shifts by 32.

## Correctness

Let `k` be the rotation amount. `value >> k` places original bits `k..31` in
result positions `0..31-k`. `value << (32-k)` places original bits `0..k-1` in
result positions `32-k..31`. These position sets are disjoint and cover all 32
positions, so their OR is exactly a right rotation. For `k = 0`, returning the
unchanged input is the required rotation.

## Complexity

Time is O(1) and extra space is O(1).

## Common pitfalls

- Shifting by 32 in the zero case, which is undefined in C.
- Using a signed value and getting an arithmetic right shift.
- Reversing the complementary shift or using logical OR (`||`).

