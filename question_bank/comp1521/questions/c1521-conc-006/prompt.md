# Sharded Manifest Statistics

## Background

Independent processes can scan the same regular text file and select disjoint records. This resembles analysing a build manifest without sharing stdio state after `fork`.

## Requirements

- Implement `c1521_conc_006.c` as `./c1521_conc_006 FILE WORKERS`, with 1 to 8 workers.
- Fork all workers.
- Worker (i) must open the file independently, read it with `getline`, and process lines whose zero-based line number modulo WORKERS equals (i).
- For assigned lines count: lines; bytes excluding one trailing newline; and whitespace-separated words.
- Send one fixed-size record through a dedicated pipe.
- The parent validates/reaps all workers, prints every worker line in numeric order, then an additive total line.
- Empty lines count as lines with zero bytes and words.
- Print one line per worker as `worker I lines=L bytes=B words=W`, then print `total lines=L bytes=B words=W`.

## Examples

Command:

```text
./c1521_conc_006 manifest.txt 2
```

Files provided for this example:

- `manifest.txt` (15 bytes) contains:

  ```text
  red green
  blue
  ```

Output:

```text
worker 0 lines=1 bytes=9 words=2
worker 1 lines=1 bytes=4 words=1
total lines=2 bytes=13 words=3
```

## Implementation notes

Open the input after `fork` inside each child so buffered state and file offsets are not shared. Word counting is a transition from whitespace to non-whitespace using `unsigned char` with `isspace`. Close unowned descriptors, loop for record transfers, and print only in the parent. Submit `c1521_conc_006.c`.
