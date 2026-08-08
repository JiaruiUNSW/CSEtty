# Bounded Pump Setting

## Background

A small control program receives three signed readings and must make one deterministic decision. Equality and signed boundary cases are intentional.

## Requirements

Read exactly three signed integers from standard input. Apply the rule named in the title and print `result: X` followed by one newline.

**Exact rule.** Treat the first and third inputs as unordered inclusive bounds and clamp the second input between them.

Submit `c1511_logic_003.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
-4 9 2
```

Output:

```text
result: 2
```

## Implementation notes

Use named intermediate values when that makes the tie rule visible. Do not rely on undefined signed overflow.
