# Deterministic Build Waves solution

## Approach

Parse each line into a bounded target record and store dependency names. Resolve each dependency name to a record index after parsing. Repeatedly scan unfinished records, selecting those whose dependencies were completed in earlier waves. Sort the selected indices by target name, print them, and then mark all selected records complete.

## Correctness

A target is selected exactly when all of its dependency records are already complete, matching the readiness rule. Because no selected target is marked until the full wave is collected, targets cannot depend on another target in the same wave. Every printed target is then completed once. If a scan selects none while unfinished targets exist, every remaining target depends transitively on another remaining target, so a cycle exists.

## Complexity

With (V) targets and (E) dependency edges, parsing is (O(V+E)). The simple repeated scan costs (O(V(V+E))) in the stated bound, and each wave sort costs at most (O(V\log V)). Storage is (O(V+E)).

## Common pitfalls

Marking a ready target during the scan collapses multiple waves incorrectly. Input order is not the required output order. Dependency names must be resolved only after all targets have been read, and a cycle must use exit status 2 rather than masquerading as malformed input.

