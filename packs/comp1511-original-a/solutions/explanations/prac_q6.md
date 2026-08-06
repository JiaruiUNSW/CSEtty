# Worked solution

## Approach

Initialise the sum to zero and add each integer from one through `n` in an inclusive loop.

## Correctness

After iteration `i`, the accumulator equals the sum from one through `i`; on termination it therefore equals the requested inclusive sum.

## Complexity

Time is `O(n)` and extra space is `O(1)`.

## Common pitfalls

Using `< n` omits the final term; starting from zero is harmless but can obscure the intended invariant.

