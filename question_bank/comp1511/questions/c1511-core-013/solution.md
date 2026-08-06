# Metro Fare Band — solution

## Approach

Initialise the fare to four, use an if/else-if chain for one distance band, add two if peak is set, and print the result.

## Correctness

The chain selects the unique band containing the valid distance and adds its specified surcharge. The final independent condition adds exactly the required peak amount, so the printed fare follows the rule.

## Complexity

O(1) time and O(1) space.

## Common pitfalls

Boundary distances 5 and 15 belong to the lower bands. The peak surcharge is in addition to exactly one distance band. Keep the submitted filename and required output format unchanged.

