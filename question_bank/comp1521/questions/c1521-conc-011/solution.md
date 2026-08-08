# Joined Vowel Workers solution

## Approach

Create an argument record per input containing the source pointer and count field. Each worker scans its string, lowercases unsigned bytes, and increments its own count for the five vowels. The main thread joins all created thread IDs, handles errors, and prints the records by ascending index.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-strings`, runs `./c1521_conc_011 apple SKY`.

Input:

```text
(empty)
```

Expected standard output:

```text
0 vowels=2
1 vowels=0
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

Worker (i) examines every character of string (i) once and increments exactly for the defined vowel set, so its field is the correct count. Fields are disjoint, avoiding write/write races. A successful join makes the worker's writes visible to main; index-order traversal yields the required deterministic lines.

## Complexity

For total input length (C), work is (O(C)), metadata is (O(N)) for (N\le8), and each worker uses constant extra memory.

## Common pitfalls

Printing inside workers makes output order scheduler-dependent. Sharing one counter without a mutex is a data race, while a shared counter also loses per-string results. Passing temporary or reused argument records can make threads read the wrong string.
