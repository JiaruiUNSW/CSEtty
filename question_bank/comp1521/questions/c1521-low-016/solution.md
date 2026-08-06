# First Maximum Index — solution guide

## Approach

Read the array, then scan it from index one using element zero as the initial maximum. On a strict increase, replace both maximum value and maximum index.

## Correctness

After scanning through index `i`, the saved value is the maximum of indices `0..i`, and the saved index is its earliest occurrence because equal values never replace it. The final index is therefore the required answer.

## Complexity

O(n) time and O(n) array storage, with O(1) working storage.

## Common pitfalls

Using greater-than-or-equal returns the last maximum. Do not confuse the byte offset with the element index returned to `main`.
