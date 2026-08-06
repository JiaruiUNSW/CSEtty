# Solution

## Approach

Scan entries and retain a copied best name plus size. Replace it when a regular file is larger, or when sizes tie and its name compares smaller with `strcmp`.

## Correctness

After each examined entry, the retained candidate is the specified maximum among regular entries seen so far: replacement handles both ordering criteria. Induction gives the correct candidate after the final entry; absence of a candidate means no regular file existed.

## Complexity

Scanning `n` entries takes `O(n)` metadata operations and stores `O(1)` candidate records plus one name.

## Common pitfalls

Do not rely on iteration order, forget the tie rule, use `stat` and follow links, or print an implementation-dependent directory size.
