# Allocate the vowel trace

## Background

`char *vowel_trace(const char *text)` returns a newly allocated string containing only ASCII vowels from `text`, preserving case and order.

## Requirements

- Treat `a e i o u` and their uppercase forms as vowels; no other byte qualifies.
- Allocate exactly enough bytes for the vowels plus the terminating null byte.
- Return a valid empty string allocation when there are no vowels, and leave the input unchanged.
- On valid input the executable must use exactly the demonstrated output format and exit successfully.

## Examples

Command:

```text
./c1511_adv_020 Granite
```

Output:

```text
aie
```

## Implementation notes

Exactly one input string argument is supplied. A count pass and copy pass make the allocation exact. Submit `c1511_adv_020.c`. Keep all provided function signatures and starter code unless the task explicitly identifies a starter bug.
