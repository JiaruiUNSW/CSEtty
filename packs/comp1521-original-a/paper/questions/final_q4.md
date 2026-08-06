# Q4 — Sum one through n in MIPS

## Background

This question practises translating a simple C counting loop into labels,
branches, and register updates. The starter reads a non-negative integer `n`.

## Program requirements

Complete `final_q4.s` so that it computes the inclusive sum
`1 + 2 + ... + n`, prints the signed integer result followed by a newline, and
exits.

- Use a MIPS loop; do not replace the loop with a closed-form multiplication
  formula.
- The supplied tests use values whose sum fits in a signed 32-bit integer.
- For `n == 0`, print `0`.
- Do not print prompts or other text.

## Examples

```text
$ printf '5\n' | mipsy final_q4.s
15
$ printf '10\n' | mipsy final_q4.s
55
```

## Implementation notes

It is useful to keep `n`, the running sum, and the next integer in three
separate registers. Test the loop condition before adding so that the zero case
needs no special output path.

