# Undoable event journal

## Background

This is an original whole-program exercise. Build a journal that counts event categories while retaining a stack of up to 100 logged categories for undo. Unlike a single-function task, you should decompose parsing, state updates, output, and cleanup into clear helpers.

## Requirements

- `LOG category` appends one event and increments that category's count.
- `UNDO` removes the most recently logged event and prints `UNDONE category`, or prints `NOTHING` when history is empty.
- `COUNT category` prints `category count`, including zero for an unseen category.
- `TOTAL` prints `TOTAL number`; `END` stops.
- Read commands from standard input, process them in order, write only specified responses, and exit successfully after `END`.
- Category names contain 1–20 non-whitespace ASCII characters, at most 32 categories occur, and no more than 100 events are simultaneously logged.

## Examples

After `LOG rain`, `LOG wind`, `LOG rain`, `COUNT rain`, `TOTAL`, the two output lines are `rain 2` and `TOTAL 3`. Each mentioned fragment is one input line, and every described output occupies its own newline exactly as shown.

## Implementation notes

The starter deliberately contains only the data definitions and a minimal command loop; implement the complete behaviour rather than printing sample-specific answers. Use bounded `scanf` conversions for names, check allocation where applicable, and release every owned allocation before normal exit. Submit `c1511_adv_034.c`, compiled using the supplied shell-free `dcc -Werror` argument array.
