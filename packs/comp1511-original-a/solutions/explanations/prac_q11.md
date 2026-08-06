# Worked solution

## Approach

Maintain one accumulator in the command-reading loop. Dispatch with `strcmp`; scan and apply an operand for `add`/`mul`, print for `print`, and break for `quit`.

## Correctness

Inductively, after every processed command the variable equals the result of applying that command to the prior state. Each `print` therefore reports the specified state, and `quit` processes nothing further.

## Complexity

For `k` commands, time is `O(k)` and extra space is `O(1)` apart from the fixed command buffer.

## Common pitfalls

Reading an operand after `print`, resetting the accumulator inside the loop, or allowing `quit` to fall through.

