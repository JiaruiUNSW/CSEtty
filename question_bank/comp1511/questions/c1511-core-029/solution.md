# Restock Manifest — solution

## Approach

Read all item structs, then scan them once. For each, compute `target - current` when positive, print positive needs, and add them to the total.

## Correctness

The helper returns exactly the missing quantity for below-target items and zero otherwise. The scan visits every item once in input order, so all required lines and the summed total are exact.

## Complexity

O(n) time and O(n) space.

## Common pitfalls

Do not print items exactly at target, never add a negative need, and keep the final summary even when no item needs stock. Verify boundary inputs as well as the worked example.

