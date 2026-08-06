# Vowel Bookends — solution

## Approach

Scan the word to count characters accepted by the vowel helper and determine its length, then call the helper for positions zero and length minus one.

## Correctness

The scan visits every character once and increments exactly for vowels, giving the exact count. The endpoint conjunction matches the definition of bookended.

## Complexity

O(L) time and O(L) storage for a word of length L.

## Common pitfalls

The final character is at length minus one, not at the null terminator. Both endpoints must be vowels. Keep the submitted filename and required output format unchanged.

