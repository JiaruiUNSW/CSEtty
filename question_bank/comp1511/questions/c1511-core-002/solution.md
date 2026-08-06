# Longest Gentle Climb — solution

## Approach

Start both lengths at one. For every later element, extend the current run when it is at least its predecessor; otherwise restart at one, then update the maximum.

## Correctness

The current counter equals the length of the non-decreasing run ending at the current index. Taking the maximum of these exact ending lengths over all indices yields the longest run.

## Complexity

The algorithm runs in O(n) time and stores O(n) input values.

## Common pitfalls

Equality extends a run. Remember that n may be one, and update the maximum after every element. Also check every `scanf` target and preserve the required output format.

