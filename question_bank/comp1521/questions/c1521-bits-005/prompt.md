# Clear Fault Mask Bits

## Background

A systems utility represents compact state in one 32-bit word. The transformation must be explicit about unsigned shifts, masks, and field widths.

## Requirements

Read two hexadecimal 32-bit words `x y` and a decimal shift/field value `k`. Compute the operation in the title and print `result: XXXXXXXX` using eight lowercase hexadecimal digits.

**Exact rule.** Treat every 1 bit in `y` as a bit to clear and return `x & ~y`; ignore `k`.

Submit `c1521_bits_005.c`. Your program must not print prompts or explanatory text.

## Examples

Command arguments: `(no command-line arguments)`

Input:

```text
12345678 00ff00ff 8
```

Output:

```text
result: 12005600
```

## Implementation notes

Use `uint32_t`. Reduce variable shifts to 0 through 31 before shifting, and never shift a 32-bit value by 32.
