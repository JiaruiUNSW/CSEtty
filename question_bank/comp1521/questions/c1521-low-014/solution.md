# Rotate an Eight-Bit Dial — solution guide

## Approach

For zero rotation, return `x`. Otherwise form the left and wrapped right pieces using variable shifts, OR them, and retain only the low byte.

## Correctness

For nonzero `k`, the left piece moves every retained bit up by `k`, while the right piece places the `k` bits that crossed bit 7 back at the bottom. Their OR is exactly an eight-bit rotation; masking removes higher copies.

## Complexity

O(1) time and O(1) storage.

## Common pitfalls

A 32-bit rotation is not the same operation. Do not use `8-k` when `k=0` unless you have explicitly handled that case.
