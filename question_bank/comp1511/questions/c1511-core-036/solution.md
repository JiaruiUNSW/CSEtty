# Digit-Run Redactor — solution

## Approach

Track whether the scan is currently inside a digit run. Print one marker and increment the count when entering a run; print non-digits normally and clear the state.

## Correctness

Every maximal digit run has exactly one transition from non-digit to digit, so it produces exactly one marker and count. Every non-digit is printed once unchanged.

## Complexity

O(L) time and O(L) storage.

## Common pitfalls

Do not emit one marker per digit, exclude the input newline from the transformed content, and still print a newline for EOF-terminated input. Verify boundary inputs as well as the worked example.

