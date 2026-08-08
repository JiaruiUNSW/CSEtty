# Solution

## Approach

Parse the positive target number, then scan one character at a time while tracking the current line. Emit characters only while on the target line. A newline completes it; EOF completes an unterminated selected line and requires an added newline.


## Step-by-step

1. Validate arguments, open the resource in the required mode, and check every system call.
2. Process one byte, record, or directory entry at a time while maintaining the stated invariant.
3. Handle short reads, empty input, and boundary offsets before formatting the result.
4. Close descriptors and free owned memory on both success and error paths.

## Worked example

The first public test, `middle-line`, runs `./c1521_fs_004 input.txt 2`.
The test installs `tests/colours.txt -> input.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
green
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The line counter advances exactly at each newline, so before every character it identifies that character's logical line. Consequently only target-line characters are copied. If scanning reaches EOF first, the target cannot exist; the separate unterminated-line case adds the required output newline.

## Complexity

Time is `O(p)`, where `p` is the prefix through the selected line or the whole file if absent. Auxiliary space is `O(1)`.

## Common pitfalls

Avoid treating an empty file as one line, losing the first character of a line, printing two newlines, and accepting zero or a number with trailing junk.
