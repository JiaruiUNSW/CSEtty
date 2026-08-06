# Solution: Recursive mirror check

## Approach

Recursively reach the list end with a right pointer. During unwinding compare each right-side value with a shared front pointer, then advance that front pointer.

## Correctness

Unwinding visits right-side nodes from last to first while the shared pointer visits left-side nodes from first to last. Each symmetric pair is compared once; conjunction of all comparisons is true exactly for a palindrome.

## Complexity

`O(n)` time and `O(n)` call-stack space.

## Common pitfalls

Advancing the front pointer on the downward recursion, mutating the list, or continuing to dereference after an earlier mismatch. Pay particular attention to ownership transitions and to saving links before a node is relinked or freed; hard-coded output does not satisfy the tests.
