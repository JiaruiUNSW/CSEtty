# Signal State Advances — solution

## Approach

Convert the input character to an enum, repeat the enum transition the requested number of times, then convert the final enum back to its character.

## Correctness

Each loop iteration applies exactly one transition of the specified cycle. By induction on the number of iterations, the enum after `steps` iterations is the required final state.

## Complexity

O(steps) time and O(1) space.

## Common pitfalls

The cycle order is R to G to A to R, and zero steps must leave the state unchanged. Keep the submitted filename and required output format unchanged.

