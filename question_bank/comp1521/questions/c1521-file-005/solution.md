# Byte Sum Modulo 65536 — worked solution

## Idea in one sentence

Read the file as bytes and scan once to compute byte sum modulo 65536.

## Exact rule

Add every unsigned byte value and return the sum modulo 65536.

## Approach

Read the file as bytes and scan once to compute byte sum modulo 65536. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Validate the argument and open the file read-only.
2. Read until EOF, handling short reads and capacity growth.
3. Apply the byte-level invariant without string functions.
4. Close, print, and free all owned storage.

## Worked example

Command-line arguments: `input.bin`

Files provided for this example:

- `input.bin` contains:

  ```text
  A1b2C3
  ```

Output:

```text
result: 390
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

The read loop appends every byte exactly once and stops only at EOF. The helper processes exactly that byte array, so its accumulator equals the defined file metric.

## Complexity

Reading and scanning use `O(n)` time and the byte buffer uses `O(n)` space.

## Common pitfalls

Do not use `strlen`, treat byte 255 as EOF, assume one `read` fills the buffer, or leak the descriptor after an allocation error.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
