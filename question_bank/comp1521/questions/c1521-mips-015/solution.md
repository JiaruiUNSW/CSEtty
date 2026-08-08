# MIPS Last Buffer Reading — worked solution

## Idea in one sentence

Translate the loop invariant for mips last buffer reading into a leaf MIPS function.

## Exact rule

Return the final array element, or 0 for an empty array.

## Approach

Translate the loop invariant for mips last buffer reading into a leaf MIPS function. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Handle the zero-length base case before loading element zero.
2. Copy pointer/count arguments into temporary registers.
3. Update the accumulator and pointer once per element.
4. Return through `$ra` with the final value in `$v0`.

## Worked example

Command arguments: `(no command-line arguments)`

Input:

```text
6
3 -1 -1 4 0 -2
```

Output:

```text
-2
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

At each loop header, the accumulator equals the required metric for the already-consumed prefix and the pointer names the next word. One iteration adds exactly that word's contribution, so termination after `n` words returns the full metric.

## Complexity

The routine uses `O(n)` instructions and `O(1)` extra storage.

## Common pitfalls

Do not overwrite `$ra`, confuse byte and word offsets, load before checking `n == 0`, or leave the result in a temporary register.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
