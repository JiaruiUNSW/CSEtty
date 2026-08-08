# Solution

## Approach

Convert hex pairs to bytes and reuse a strict sequence-width validator. For each valid sequence, increment the counter indexed by width and advance by that width.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `only-ascii`, runs `./c1521_fs_012 414243`.

Input:

```text
(empty)
```

Expected standard output:

```text
one=3 two=0 three=0 four=0
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The validator returns a width only for a complete canonical scalar encoding. Every successful iteration consumes exactly one such encoding, so incrementing the associated width bucket counts each scalar once in the correct category. First failure is reported at its current offset.

## Complexity

For `n` bytes, time is `O(n)` and the parsed byte array uses `O(n)` space.

## Common pitfalls

Do not count continuation bytes independently, accept truncated sequences, or report the byte after the invalid lead as the failure offset.
