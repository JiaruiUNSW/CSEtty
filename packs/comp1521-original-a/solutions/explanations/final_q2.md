# Worked solution — Q2

## Approach

Retain the first syscall result in `$t0`. After the second read, subtract `$v0`
from `$t0` and place the answer directly in `$a0`, then use syscall 1 to print
the signed integer.

## Correctness

Immediately before the subtraction, `$t0` equals the first input and `$v0`
equals the second. The instruction `sub $a0, $t0, $v0` therefore computes
`first - second`, which is exactly the requested output value. The following
print syscall emits that value and the supplied code emits the newline.

## Complexity

Time and extra space are O(1).

## Common pitfalls

- Subtracting in the opposite order.
- Forgetting that the second read overwrites `$v0`.
- Printing from `$v0` instead of moving the result to `$a0`.

