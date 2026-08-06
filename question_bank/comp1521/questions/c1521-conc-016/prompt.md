# Threaded Byte Histogram Merge

## Background

A scalable histogram lets workers count locally, then briefly lock while merging. This avoids a mutex operation for every input byte while still exercising safe shared updates.

## Requirements

Implement `c1521_conc_016.c` as `./c1521_conc_016 FILE THREADS`, with 1 to 8 threads. Main must open the regular file, read its bytes into owned memory, and partition offsets using integer-division boundaries. Every worker counts its slice into a private 256-entry `unsigned long long` array, locks one shared mutex, merges all nonzero local counters into the global histogram, and unlocks. Join all threads; print nonzero bytes in ascending value as two uppercase hex digits `HH=N`, then `total=N`. Empty slices are valid.

## Examples

For bytes `A B A newline`, print counts for 0A, 41, and 42 in numeric byte order, followed by total four.

## Implementation notes

Do not use C-string functions on binary data. The file buffer's size, not a terminator, defines work. Per-thread slices are disjoint; only the global merge needs the mutex. Check complete file reads, pthread calls, and allocation arithmetic. Destroy the mutex and free the buffer after joins. Submit `c1521_conc_016.c`.
