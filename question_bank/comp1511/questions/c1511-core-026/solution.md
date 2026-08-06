# Repair the Clock Wrap — solution

## Approach

Convert the input to total minutes, add the offset, reduce modulo 1440, normalise a negative result, then divide and take remainder by 60.

## Correctness

Times differing by multiples of 1440 represent the same time of day. Normalisation selects its unique total in zero through 1439, whose quotient and remainder by 60 are the correct hour and minute.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not use modulo 24 on a minute total, and correct negative remainder before calculating the fields. Keep the submitted filename and required output format unchanged.

