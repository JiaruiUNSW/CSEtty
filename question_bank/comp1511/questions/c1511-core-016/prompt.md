# Parcel Classifier

## Background

A dispatch desk classifies a rectangular parcel using its weight and dimensions.

## Requirements

Write or repair the complete C program in `c1511_core_016.c`.

**Input:** One line contains weight, length, width, and height as positive integers.

**Output:** Print `class: oversized` if any dimension is greater than 50 or volume is greater than 50000. Otherwise print `class: compact` when weight is at most 5 and volume is at most 1000; print `class: standard` for all other parcels.

**Assumptions:** The volume product fits in a C `int`.

**Restrictions:** Store the four input fields in a `struct parcel` and perform the classification in a helper function.

Submit exactly the file `c1511_core_016.c`.

## Examples

Input:

```text
4 10 10 8
```

Output:

```text
class: compact
```

The parcel weighs at most 5 and has volume 800.

## Implementation notes

Check oversized before compact so a long thin parcel cannot be called compact. Output spelling, spaces, punctuation, and newlines must match exactly.
