# Component stock ledger

## Background

Build a command interpreter that tracks integer quantities for up to 32 component names in first-seen order. Unlike a single-function task, you should decompose parsing, state updates, output, and cleanup into clear helpers.

## Requirements

- `ADD name amount` adds a positive amount, creating the record when first seen.
- `TAKE name amount` subtracts only when enough stock exists, printing `TAKEN name remaining`; otherwise print `REJECTED name`.
- `SHOW` prints each positive record as `name quantity` in first-seen order, or `EMPTY`, then always prints `--`.
- `END` stops immediately.
- Read commands from standard input, process them in order, write only specified responses, and exit successfully after `END`.
- Names contain 1–20 non-whitespace ASCII characters, amounts are positive, and at most 32 distinct names are added. Commands are uppercase and syntactically valid.

## Examples

Command:

```text
./c1511_adv_033
```

Input:

```text
ADD bolts 5
TAKE bolts 2
SHOW
END
```

Output:

```text
TAKEN bolts 3
bolts 3
--
```

## Implementation notes

The starter deliberately contains only the data definitions and a minimal command loop; implement the complete behaviour. Use bounded `scanf` conversions for names, check allocation where applicable, and release every owned allocation before normal exit. Submit `c1511_adv_033.c`.
