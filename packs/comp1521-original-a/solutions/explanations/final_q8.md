# Worked solution — Q8

## Approach

Read the first integer into the current maximum. Set a counter to four, then
loop: read another value, replace the maximum only when the new value is
greater, and decrement the counter. Print after all five inputs have been read.

## Correctness

After the first read, the stored maximum is the maximum of the first one value.
Each loop iteration compares the next input and retains the greater of it and
the previous maximum, so after k reads the register holds the maximum of those k
values. After five reads it therefore holds the maximum of all inputs, which is
printed.

## Complexity

The program makes five reads and uses a fixed number of registers, so time and
space are O(1).

## Common pitfalls

- Initialising the maximum to zero and failing all-negative cases.
- Using an unsigned comparison for signed inputs.
- Reading four or six values because of a counter error.

