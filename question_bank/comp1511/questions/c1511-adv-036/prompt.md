# Reversible marker chain

## Background

This is an original whole-program exercise. Build a command-driven editor for a heap-allocated chain of short marker names. Unlike a single-function task, you should decompose parsing, state updates, output, and cleanup into clear helpers.

## Requirements

- `APPEND name` and `PREPEND name` allocate and insert one node.
- `REMOVE name` removes and frees the first matching node, printing `REMOVED name` or `MISSING name`.
- `REVERSE` relinks the chain in place; `PRINT` prints names joined by ` -> ` or `EMPTY`; `END` stops and frees the chain.
- Read commands from standard input, process them in order, write only specified responses, and exit successfully after `END`.
- Names contain 1–20 non-whitespace ASCII characters, allocation succeeds or the program exits with status 1, and commands are valid. Duplicate names are allowed.

## Examples

After `APPEND red`, `APPEND blue`, `PREPEND green`, `PRINT`, the line is `green -> red -> blue`. Each mentioned fragment is one input line, and every described output occupies its own newline exactly as shown.

## Implementation notes

The starter deliberately contains only the data definitions and a minimal command loop; implement the complete behaviour rather than printing sample-specific answers. Use bounded `scanf` conversions for names, check allocation where applicable, and release every owned allocation before normal exit. Submit `c1511_adv_036.c`, compiled using the supplied shell-free `dcc -Werror` argument array.
