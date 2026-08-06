# Frame Balance Checksum — solution

## Approach

Traverse every cell once. Add border cells to the accumulator and subtract non-border cells.

## Correctness

Every cell is uniquely classified as border or interior. The traversal contributes each border value with coefficient +1 and each interior value with coefficient -1, exactly matching the checksum.

## Complexity

O(rows * columns) time and O(rows * columns) storage.

## Common pitfalls

Independent loops over four edges can double-count corners. A single border predicate avoids that problem. Also check every `scanf` target and preserve the required output format.

