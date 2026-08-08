# Character Runs in a Barcode Note

## Background

A line-oriented tool must summarise human-readable text without tokenising beyond the rule in the title. The complete line, including spaces, is meaningful.

## Requirements

Read one line of at most 255 characters, excluding the final newline from the calculation. Print `result: X` and a newline. Character classification is ASCII for these tests.

**Exact rule.** Count maximal contiguous runs of identical characters; the empty line has 0 runs.

Submit `c1511_text_007.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
A1 beta
```

Output:

```text
result: 7
```

## Implementation notes

Use `fgets`, remove at most one trailing newline, and cast to `unsigned char` before calling `<ctype.h>` functions.
