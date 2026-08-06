# Worked solution — Q4

## Approach

Keep `n` in `$t0`, the running sum in `$t1`, and a counter beginning at 1 in
`$t2`. At the loop head, branch to the output when the counter is greater than
`n`; otherwise add it to the sum, increment it, and repeat.

## Correctness

Before each iteration with counter `i`, the running sum equals
`1 + ... + (i - 1)`. If `i <= n`, adding `i` and incrementing preserves the
invariant. When `i > n`, the invariant says the sum is `1 + ... + n`, so the
printed value is correct. With `n = 0`, the first test exits with the initial
sum 0.

## Complexity

Time is O(n) and extra space is O(1).

## Common pitfalls

- An off-by-one branch that omits `n` or adds `n + 1`.
- Overwriting the input register with syscall values.
- Forgetting the zero-input behaviour.

