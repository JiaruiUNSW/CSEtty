# Child-Built Line Index solution

## Approach

The child opens the file and scans bytes while tracking the absolute offset and whether the current byte begins a line. It writes offset zero when the first byte exists, then writes an offset whenever a byte follows a newline. The parent repeatedly reads complete 64-bit values, doubles a dynamic array when full, closes the channel at EOF, and checks the child's exit status before printing.


## Step-by-step

1. Separate input parsing from process/thread creation so every worker receives stable data.
2. Give each worker a disjoint unit of work and compute as much as possible locally.
3. Transfer or merge results through the required pipe/mutex boundary, then wait or join.
4. Print only after all results are complete, and release every descriptor and allocation.

## Worked example

The first public test, `two-lines-trailing-newline`, runs `./c1521_conc_005 input.txt`.
The test installs `tests/two.txt -> input.txt` before running.

Input:

```text
(empty)
```

Expected standard output:

```text
lines=2
1:0
2:6
```

Trace this case using the state described in **Approach**: initialise it from the first valid item, update it once per remaining item, then format the final state. The other tests deliberately cover a different boundary, so do not special-case this example.

## Correctness

A non-empty file's first byte starts line one, so zero is emitted once. Every later logical line starts exactly at a byte whose predecessor is newline; the algorithm emits exactly those offsets when that following byte is encountered. A terminal newline has no following byte and therefore creates no emitted start. The parent preserves the pipe order, which is increasing file order.

## Complexity

Scanning takes (O(B)) time for (B) bytes. The parent stores (O(L)) offsets for (L) lines; amortized append time is constant. Pipe traffic is (8L) bytes.

## Common pitfalls

Emitting immediately upon reading a newline invents a line after a final newline. Keeping the parent's write end open prevents EOF. Pipe reads may split a 64-bit value, and assigning `realloc` directly can lose the original pointer on failure.
