# Euclidean Pair — solution guide

## Approach

Repeatedly divide `a` by `b`, move the remainder into `b`, and the old `b` into `a`. Stop when `b` is zero.

## Correctness

Euclid's identity gives `gcd(a,b)=gcd(b,a mod b)`. Each iteration preserves the gcd and decreases the non-negative second operand. At zero, `gcd(a,0)=a`, which is printed.

## Complexity

O(log min(a,b)) time and O(1) storage.

## Common pitfalls

Printing the remainder after termination produces zero. Remember that `div` does not put its remainder in a general register automatically.
