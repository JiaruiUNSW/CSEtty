# Range Width Function — solution guide

## Approach

Pass the three inputs as arguments. In the leaf function, scan them to update local minimum and maximum registers, then return their difference.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `mixed`, runs `mipsy c1521_low_011.s`.

Input:

```text
-2
8
3
```

Expected standard output:

```text
10
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After each argument is considered, the two candidate registers contain the minimum and maximum seen. Thus after all three, their difference is exactly the range width.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Do not jump back to a hard-coded label instead of using `$ra`. Signed comparisons are required, and the returned value must survive until `main` prints it.
