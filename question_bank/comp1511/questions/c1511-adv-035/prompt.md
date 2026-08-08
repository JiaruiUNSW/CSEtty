# Labelled reading summaries

## Background

Build a record processor that maintains count, sum, minimum, and maximum for up to 16 labelled integer streams. Unlike a single-function task, you should decompose parsing, state updates, output, and cleanup into clear helpers.

## Requirements

- `READ label value` creates or updates a summary.
- `STATS label` prints `label count=N min=L max=H mean=M`, where M is integer division of sum by count, or `MISSING label`.
- `RESET label` removes its summary and prints `RESET label`, or `MISSING label`.
- `END` stops.
- Read commands from standard input, process them in order, write only specified responses, and exit successfully after `END`.
- Labels contain 1–20 non-whitespace ASCII characters, at most 16 summaries exist at once, sums fit in `long`, and input is syntactically valid.

## Examples

Command:

```text
./c1511_adv_035
```

Input:

```text
READ zone 4
READ zone 8
STATS zone
END
```

Output:

```text
zone count=2 min=4 max=8 mean=6
```

## Implementation notes

The starter deliberately contains only the data definitions and a minimal command loop; implement the complete behaviour. Use bounded `scanf` conversions for names, check allocation where applicable, and release every owned allocation before normal exit. Submit `c1511_adv_035.c`.
