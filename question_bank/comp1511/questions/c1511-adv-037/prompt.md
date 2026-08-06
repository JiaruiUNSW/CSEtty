# Resizable integer console

## Background

This is an original whole-program exercise. Build a console around a dynamically growing integer buffer with stack, rotation, and duplicate-compaction operations. Unlike a single-function task, you should decompose parsing, state updates, output, and cleanup into clear helpers.

## Requirements

- `PUSH value` appends, growing capacity geometrically.
- `DROP` removes and prints `DROPPED value`, or prints `EMPTY` when no value exists.
- `ROLL amount` rotates the current buffer right by the nonnegative amount; `UNIQUE` removes later duplicate values in place.
- `PRINT` prints one space-separated line or `EMPTY`; `END` frees storage and stops.
- Read commands from standard input, process them in order, write only specified responses, and exit successfully after `END`.
- Integers and amounts fit their types, allocation failure exits status 1, and every command is valid. UNIQUE preserves the first occurrence order.

## Examples

`PUSH 1`, `PUSH 2`, `PUSH 3`, `ROLL 1`, `PRINT` produces `3 1 2`. Each mentioned fragment is one input line, and every described output occupies its own newline exactly as shown.

## Implementation notes

The starter deliberately contains only the data definitions and a minimal command loop; implement the complete behaviour rather than printing sample-specific answers. Use bounded `scanf` conversions for names, check allocation where applicable, and release every owned allocation before normal exit. Submit `c1511_adv_037.c`, compiled using the supplied shell-free `dcc -Werror` argument array.
