# Three-Process Run Encoder

## Background

A Unix-style pipeline can stream raw file bytes through a transformation stage while a parent buffers and formats final records.

## Requirements

Implement `c1521_conc_019.c` for one file. Create a reader child, encoder child, raw-byte pipe, and run-record pipe. The reader opens the file and copies bytes to the raw pipe. The encoder reads that stream, groups adjacent equal bytes, and writes one binary record containing byte and run length for each maximal run. The parent reads complete records until clean EOF, buffers them, waits for both exact children, then prints each as uppercase `HH COUNT`, followed by `runs=R bytes=B`. Run lengths/totals fit `uint64_t`. On failure print no partial report and return 1.

## Examples

Bytes `aaabbc newline` produce runs for 61 length 3, 62 length 2, 63 length 1, and 0A length 1.

## Implementation notes

The encoder must flush its final run at input EOF. Give each process only its necessary descriptors: reader raw writer; encoder raw reader and record writer; parent record reader. A pipe is a stream, so reconstruct records across partial reads. Buffer parent records with checked `realloc` before printing. Submit `c1521_conc_019.c`.
