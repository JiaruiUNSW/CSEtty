# Vowel Bookends — solution

## Approach

Scan the word to count characters accepted by the vowel helper and determine its length, then call the helper for positions zero and length minus one.


## Step-by-step

1. Parse the input exactly once and write down the state maintained by the main loop.
2. Update that state for one element, character, or record at a time.
3. Treat the smallest legal input and every equality boundary explicitly.
4. Emit exactly the requested text and verify the final newline and spacing.

## Worked example

The first public test, `apple`, runs `./c1511_core_018`.

Input:

```text
apple
```

Expected standard output:

```text
vowels: 2
bookended: yes
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

The scan visits every character once and increments exactly for vowels, giving the exact count. The endpoint conjunction matches the definition of bookended.

## Complexity

O(L) time and O(L) storage for a word of length L.

## Common pitfalls

The final character is at length minus one, not at the null terminator. Both endpoints must be vowels. Keep the submitted filename and required output format unchanged.
