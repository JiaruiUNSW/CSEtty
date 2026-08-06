# Q5 — Count UTF-8 code points

## Background

UTF-8 stores ASCII code points in one byte and other code points in a leading
byte followed by one to three continuation bytes. Every continuation byte has
the two high bits `10`. For valid UTF-8, counting bytes that are not
continuation bytes therefore counts code points without decoding their numeric
values.

## Program requirements

Complete `final_q5.c`. Read bytes from standard input until EOF and print the
number of UTF-8 code points followed by a newline.

- The input is guaranteed to be valid UTF-8.
- Count ASCII bytes and multibyte leading bytes.
- Do not count bytes whose binary prefix is `10`.
- Treat values obtained from `getchar` as unsigned bytes when testing their
  high bits.
- Do not use locale-dependent wide-character functions or external libraries.

The newline byte, when present in the input, is an ASCII code point and is
therefore counted.

## Examples

```text
$ printf hello | ./final_q5
5
$ printf 'é猫\n' | ./final_q5
3
```

## Implementation notes

A continuation byte satisfies `(byte & 0xC0) == 0x80`. Be careful to perform
the mask on a non-negative unsigned representation of the byte.

