# Maximum File Tree Depth — worked solution

## Idea in one sentence

Use depth-first traversal and merge each entry into a summary for maximum file tree depth.

## Exact rule

The root has depth 0 and a file's depth is the number of containing subdirectories below the root; return the maximum file depth, or 0 if there are no files.

## Approach

Use depth-first traversal and merge each entry into a summary for maximum file tree depth. Keep the input, state update, and output-formatting phases separate so each can be checked independently.

## Step-by-step

1. Open the current directory and count/initialise its summary.
2. Skip dot entries and classify each child with `lstat`.
3. Recurse into directories and update file metrics exactly once for regular files.
4. Close the directory and print the requested summary field.

## Worked example

Command arguments: `tree`
Fixture files: tree/src/one.c, tree/build/two.o

Input:

```text
(empty)
```

Output:

```text
result: 1
```

Trace the state after every input item. The final state is printed only after the complete input has been processed.

## Correctness

Induction on the directory tree shows that each recursive call accounts for every regular file and subdirectory in its subtree exactly once. Combining those disjoint summaries yields the correct root metric.

## Complexity

Traversal is `O(e)` in the number of entries, with call-stack/path space proportional to maximum depth.

## Common pitfalls

Do not recurse into `.`/`..`, count the same file twice, use the process working directory instead of the argument, or leak a directory stream after an error.

## Reading the reference solution

The reference file follows the same three-part layout as the steps above: input validation in `main`, the core invariant in a small helper, and one exact output statement. Read the helper first, then check how `main` constructs its arguments and handles the smallest legal input.
