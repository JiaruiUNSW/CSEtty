# Interleave Two Coordinate Words — solution guide

## Approach

Initialise the result to zero. For each bit index, extract the matching bit of `x` and `y`, then OR them into result positions `2i` and `2i+1`.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `small`, runs `./c1521_low_021`.

Input:

```text
0003 0001
```

Expected standard output:

```text
00000007
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Each iteration writes exactly the two output positions assigned to one input index, and no two iterations overlap. After all 16 indices, every output bit has the specified source.

## Complexity

O(16), hence O(1), time and O(1) storage.

## Common pitfalls

Do not place `y` in the even positions. Shift unsigned values, and promote to `uint32_t` before moving a bit as high as position 31.
