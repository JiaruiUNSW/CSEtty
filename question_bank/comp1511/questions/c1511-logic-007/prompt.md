# Three-Reading Order Code

## Background

A small control program receives three signed readings and must make one deterministic decision. Equality and signed boundary cases are intentional.

## Requirements

Read exactly three signed integers from standard input. Apply the rule named in the title and print `result: X` followed by one newline.

**Exact rule.** Return 1 for nondecreasing order, -1 for nonincreasing order, and 0 otherwise; all-equal returns 1.

Submit `c1511_logic_007.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
-4 9 2
```

Output:

```text
result: 0
```

## Implementation notes

Use named intermediate values when that makes the tie rule visible. Do not rely on undefined signed overflow.
