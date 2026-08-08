# First Maximum Index — solution guide

## Approach

Read the array, then scan it from index one using element zero as the initial maximum. On a strict increase, replace both maximum value and maximum index.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `tie`, runs `mipsy c1521_low_016.s`.

Input:

```text
5
3
9
2
9
4
```

Expected standard output:

```text
1
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After scanning through index `i`, the saved value is the maximum of indices `0..i`, and the saved index is its earliest occurrence because equal values never replace it. The final index is therefore the required answer.

## Complexity

O(n) time and O(n) array storage, with O(1) working storage.

## Common pitfalls

Using greater-than-or-equal returns the last maximum. Do not confuse the byte offset with the element index returned to `main`.
