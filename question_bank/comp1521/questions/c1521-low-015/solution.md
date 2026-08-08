# ASCII Class Code — solution guide

## Approach

Test the digit, uppercase, and lowercase intervals in order. Assign the corresponding category when both endpoints contain the input; otherwise retain zero.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `upper`, runs `mipsy c1521_low_015.s`.

Input:

```text
71
```

Expected standard output:

```text
2
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The three ASCII intervals are disjoint and exactly describe the requested classes. The first successful interval selects its code; if none succeeds, the required default is zero.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Inclusive endpoints are easy to exclude accidentally. Compare numeric ASCII codes, not the decimal digit value represented by a character.
