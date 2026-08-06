# Solution

## Approach

For every regular child, find its last dot with `strrchr` and derive the extension under the stated rules. Find or create that group in a growing array, updating count and bytes. Sort groups by extension before printing.

## Correctness

Each immediate regular file maps to exactly one defined extension key and contributes its size once to that key. Non-regular entries never contribute. Aggregation therefore forms the exact groups, and sorting produces the required report order.

## Complexity

With `n` files and `g` extensions, a simple linear group lookup costs `O(ng)` and sorting `O(g log g)`; storage is `O(g)`.

## Common pitfalls

Use the last dot, classify a leading-only or trailing dot as no extension, do not include subdirectory contents, and avoid relying on `d_type`.
