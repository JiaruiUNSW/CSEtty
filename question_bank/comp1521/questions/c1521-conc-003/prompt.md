# Deterministic Build Waves

## Background

Build tools reason about dependencies before scheduling commands. Targets that have no unfinished prerequisites form a wave that could be built concurrently.

## Requirements

- Write `c1521_conc_003.c`.
- It receives one manifest filename.
- Each non-empty line has `target: dependency ...`; names contain only lowercase letters, digits, and underscores.
- Every dependency is also declared as a target, there are at most 64 targets, and each line is at most 511 bytes.
- Print all currently ready targets on one line as `wave K: NAME ...`, sorting names lexicographically within the wave.
- Mark the entire wave complete only after printing it.
- If unfinished targets remain but no target is ready, print `cycle` and return 2.
- Malformed input or I/O/allocation failure returns 1.

## Examples

Command:

```text
./c1521_conc_003 deps.txt
```

Files provided for this example:

- `deps.txt` (49 bytes) contains:

  ```text
  app: object
  parser:
  object: lexer parser
  lexer:
  ```

Output:

```text
wave 0: lexer parser
wave 1: object
wave 2: app
```

## Implementation notes

This is dependency analysis, not a command runner: do not call `system`, `fork`, or `exec`. Preserve wave semantics by collecting all ready nodes before marking any of them built. Use `fgets`, validate the colon, and compare names with `strcmp`. Submit `c1521_conc_003.c`.
