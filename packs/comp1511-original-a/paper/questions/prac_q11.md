# Q11 — Integer accumulator command processor

## Background

Implement a small stateful command interpreter. Its accumulator begins at zero and changes as commands arrive from standard input.

## Requirements

Complete `prac_q11.c` with four commands:

- `add N` adds integer `N` to the accumulator;
- `mul N` multiplies the accumulator by `N`;
- `print` prints the current accumulator followed by a newline; and
- `quit` stops immediately without printing anything extra.

Inputs contain only these valid commands and every `add` or `mul` has an integer operand. Processing also stops normally at end of input. All intermediate values fit in `int`.

## Examples

```text
add 5
mul 3
print
add -2
print
quit
```

prints:

```text
15
13
```

## Implementation notes

Read one command word at a time, compare it with `strcmp`, and scan an operand only for commands that require one. Preserve the accumulator between loop iterations. Submit `prac_q11.c`.

