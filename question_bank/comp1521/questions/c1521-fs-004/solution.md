# Solution

## Approach

Parse the positive target number, then scan one character at a time while tracking the current line. Emit characters only while on the target line. A newline completes it; EOF completes an unterminated selected line and requires an added newline.

## Correctness

The line counter advances exactly at each newline, so before every character it identifies that character's logical line. Consequently only target-line characters are copied. If scanning reaches EOF first, the target cannot exist; the separate unterminated-line case adds the required output newline.

## Complexity

Time is `O(p)`, where `p` is the prefix through the selected line or the whole file if absent. Auxiliary space is `O(1)`.

## Common pitfalls

Avoid treating an empty file as one line, losing the first character of a line, printing two newlines, and accepting zero or a number with trailing junk.
