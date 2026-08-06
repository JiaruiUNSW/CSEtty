# Add Two Readings — solution guide

## Approach

Read the first value into one temporary register and the second into another. Add the registers, print the result with syscall 1, then print ASCII newline with syscall 11.

## Correctness

The two input syscalls return exactly the operands in the two saved registers. Their addition is the required sum, and the two output syscalls emit that sum and exactly one newline.

## Complexity

The program performs a constant number of instructions and uses O(1) storage.

## Common pitfalls

Do not leave the first input in `$v0`, because the second syscall overwrites it. Do not print a prompt, and do not omit the final newline.
