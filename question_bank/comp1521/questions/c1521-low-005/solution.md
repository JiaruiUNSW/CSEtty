# Clamp a Control Value — solution guide

## Approach

Compare the value with `low`; if smaller, select `low`. Otherwise compare `high` with the value; if true, select `high`. Otherwise retain the original value.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `high`, runs `mipsy c1521_low_005.s`.

Input:

```text
18
0
10
```

Expected standard output:

```text
10
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The three branches partition all valid inputs into below-range, above-range, and inclusive in-range cases, and each branch selects the definition of clamping for that case.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Swapping the operands to `slt` reverses the condition. Values exactly equal to a bound must remain unchanged, though their printed number equals that bound.
