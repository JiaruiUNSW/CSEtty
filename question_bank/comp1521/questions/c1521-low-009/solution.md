# Euclidean Pair — solution guide

## Approach

Repeatedly divide `a` by `b`, move the remainder into `b`, and the old `b` into `a`. Stop when `b` is zero.


## Step-by-step

1. Decide which values must survive syscalls, and assign them to stable registers.
2. Translate the loop or function invariant into labels and explicit branches.
3. Put the required result in `$a0`, use the documented print syscall, and emit one newline.
4. Check the zero/empty case separately before tracing the general case.

## Worked example

The first public test, `shared`, runs `mipsy c1521_low_009.s`.

Input:

```text
84
30
```

Expected standard output:

```text
6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Euclid's identity gives `gcd(a,b)=gcd(b,a mod b)`. Each iteration preserves the gcd and decreases the non-negative second operand. At zero, `gcd(a,0)=a`, which is printed.

## Complexity

O(log min(a,b)) time and O(1) storage.

## Common pitfalls

Printing the remainder after termination produces zero. Remember that `div` does not put its remainder in a general register automatically.
