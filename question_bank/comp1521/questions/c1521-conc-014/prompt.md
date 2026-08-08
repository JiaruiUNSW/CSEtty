# Two-Stage Word Pipeline

## Background

A pipeline can separate byte-oriented tokenisation from aggregation. Each stage owns one transformation and communicates with fixed binary records.

## Requirements

- Implement `c1521_conc_014.c` for one input file.
- Create two children and two pipes.
- The producer child opens the file, identifies whitespace-separated words, and writes each positive word length as a `uint32_t` to the producer-to-aggregator pipe, followed by a zero sentinel.
- The aggregator child reads complete lengths, computes word count, total word characters, and maximum length, then writes one result structure to the aggregator-to-parent pipe.
- The parent owns both PIDs, closes every unused end, reads the result, reaps both stages, and prints `words=N chars=C longest=L`.
- Failures return 1.

## Examples

Command:

```text
./c1521_conc_014 input.txt
```

Files provided for this example:

- `input.txt` (14 bytes) contains:

  ```text
  one two three
  ```

Output:

```text
words=3 chars=11 longest=5
```

## Implementation notes

Fork the producer and aggregator with deliberate descriptor ownership: the producer owns only the first writer; the aggregator owns the first reader and second writer; the parent owns only the second reader. Use complete record transfer helpers and `unsigned char` with `isspace`. A zero word length is reserved for end-of-stream. Submit `c1521_conc_014.c`.
