# Q1 — Rotate a 32-bit value right

## Background

A rotate moves bits around a fixed-width word instead of discarding them. When a
32-bit value is rotated right by one position, bit 0 becomes bit 31 and every
other bit moves one position towards bit 0. Rotations are common in checksums,
hash functions, and binary file formats.

## Program requirements

Complete `rotate_right` in `final_q1.c`:

```c
uint32_t rotate_right(uint32_t value, unsigned amount);
```

- `amount` is between 0 and 31 inclusive.
- Treat `value` as exactly 32 unsigned bits.
- Return the rotated value; do not print inside `rotate_right`.
- An amount of 0 must return `value` unchanged.
- Do not use loops, arrays, strings, or a wider integer type to perform the
  rotation.
- Leave the supplied `main` function and command-line interface unchanged.

## Examples

```text
$ ./final_q1 1 1
2147483648
$ ./final_q1 305419896 8
2014458966
```

The second input value is hexadecimal `0x12345678`; rotating it right by eight
bits produces `0x78123456`.

## Implementation notes

Use unsigned shifts. In C, shifting by the width of the type is invalid, so the
zero-rotation case must be handled before forming a shift by `32 - amount`.

