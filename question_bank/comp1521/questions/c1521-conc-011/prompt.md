# Joined Vowel Workers

## Background

Independent string analysis is a natural thread task. Deterministic reporting comes from giving each thread an owned result slot and printing after all joins.

## Requirements

- Implement `c1521_conc_011.c`.
- Accept one to eight strings.
- Create one thread per string; worker (i) counts ASCII vowels `a e i o u` case-insensitively in argument (i) and writes only result slot (i).
- The main thread must join all workers and then print `INDEX vowels=N` in argument order.
- Punctuation and non-vowels are ignored.
- Invalid argument counts or pthread failures return 1 after joining every thread that was created.

## Examples

Command:

```text
./c1521_conc_011 apple SKY
```

Output:

```text
0 vowels=2
1 vowels=0
```

## Implementation notes

Argument strings remain valid for the process lifetime, but per-thread metadata must also have stable storage. Cast to `unsigned char` before `tolower`, or compare both ASCII cases directly. No mutex is needed for disjoint result fields. Submit `c1521_conc_011.c`.
