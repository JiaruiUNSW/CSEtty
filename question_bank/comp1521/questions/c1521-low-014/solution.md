# Rotate an Eight-Bit Dial — solution guide

## Approach

For zero rotation, return `x`. Otherwise form the left and wrapped right pieces using variable shifts, OR them, and retain only the low byte.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `wrap`, runs `mipsy c1521_low_014.s`.

Input:

```text
129
1
```

Expected standard output:

```text
3
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

For nonzero `k`, the left piece moves every retained bit up by `k`, while the right piece places the `k` bits that crossed bit 7 back at the bottom. Their OR is exactly an eight-bit rotation; masking removes higher copies.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

A 32-bit rotation is not the same operation. Do not use `8-k` when `k=0` unless you have explicitly handled that case.
