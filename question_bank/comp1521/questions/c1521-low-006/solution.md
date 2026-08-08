# Count Even Samples — solution guide

## Approach

Repeat five times: read a value, isolate bit zero, and increment the answer when that bit is zero. Print the final answer.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_006.s`.

Input:

```text
1
2
3
4
6
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

An integer is even exactly when its least-significant bit is zero. The loop examines every one of the five inputs once, so its counter equals the number of even inputs.

## Complexity

O(1) time for the fixed five inputs and O(1) storage.

## Common pitfalls

Do not count odd values by accidentally reversing the branch. Negative two's-complement values follow the same low-bit parity rule.
