# Largest of Three — solution guide

## Approach

Maintain a `maximum` register. Two signed `slt` comparisons decide whether the second and third inputs replace it.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `middle`, runs `mipsy c1521_low_004.s`.

Input:

```text
4
12
7
```

Expected standard output:

```text
12
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

After considering each input, the candidate is the maximum of the values seen so far. Applying this invariant to all three inputs leaves the maximum of the complete set.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

Unsigned comparison gives incorrect answers for negative inputs. Avoid a control-flow path that skips reading or considering the third value.
