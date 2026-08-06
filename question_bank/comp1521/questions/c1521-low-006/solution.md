# Count Even Samples — solution guide

## Approach

Repeat five times: read a value, isolate bit zero, and increment the answer when that bit is zero. Print the final answer.

## Correctness

An integer is even exactly when its least-significant bit is zero. The loop examines every one of the five inputs once, so its counter equals the number of even inputs.

## Complexity

O(1) time for the fixed five inputs and O(1) storage.

## Common pitfalls

Do not count odd values by accidentally reversing the branch. Negative two's-complement values follow the same low-bit parity rule.
