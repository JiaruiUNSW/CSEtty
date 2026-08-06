# Pipe Sequence Reduction

## Background

A pipe is a byte stream: the producer chooses a record format and the consumer must reconstruct complete records before reducing them.

## Requirements

Implement `c1521_conc_009.c` with arguments `START STEP COUNT`, where COUNT is 1 through 1000 and all generated values/sums fit `long long`. Create one child. The child generates `START + i*STEP` for (i=0..COUNT-1) and writes each as a binary `long long` to the pipe. The parent reads exactly COUNT complete records, computes their sum, minimum, and maximum, checks that EOF follows, waits for the child, and prints `count=N sum=S min=L max=H`. Invalid input or any pipe/process error returns 1.

## Examples

`1 1 5` represents 1,2,3,4,5 and prints sum 15, minimum 1, maximum 5. A negative step is allowed.

## Implementation notes

Do not assume one `read` or `write` transfers eight bytes. Close the parent's writer and child's reader immediately. Binary records need no textual parsing in the parent, but both processes must agree on type and count. Check normal child exit with `waitpid`. Submit `c1521_conc_009.c`.
