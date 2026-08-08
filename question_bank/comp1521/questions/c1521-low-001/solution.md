# Add Two Readings — solution guide

## Approach

Read the first value into one temporary register and the second into another. Add the registers, print the result with syscall 1, then print ASCII newline with syscall 11.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `positive`, runs `mipsy c1521_low_001.s`.

Input:

```text
3
4
```

Expected standard output:

```text
7
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The two input syscalls return exactly the operands in the two saved registers. Their addition is the required sum, and the two output syscalls emit that sum and exactly one newline.

## Complexity

The program performs a constant number of instructions and uses O(1) storage.

## Common pitfalls

Do not leave the first input in `$v0`, because the second syscall overwrites it. Do not print a prompt, and do not omit the final newline.
