# Same-Day Elapsed Minutes — solution

## Approach

Store both times in structs, map each to `hour * 60 + minute`, and subtract the start total from the finish total.

## Correctness

The conversion counts exact minutes since midnight. Because both times are on the same day, subtracting those positions gives precisely the elapsed duration.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Do not subtract hours and minutes independently without borrowing. Equal times yield zero. Keep the submitted filename and required output format unchanged.

