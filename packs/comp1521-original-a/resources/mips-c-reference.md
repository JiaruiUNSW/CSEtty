# C and MIPS quick reference

- C file calls: `open`, `read`, `write`, `close`, `lseek`
- Process calls: `fork`, `_exit`, `waitpid`
- Thread calls: `pthread_create`, `pthread_join`
- MIPS syscall 5 reads an integer; syscall 1 prints an integer.
- MIPS syscall 11 prints a character; syscall 10 exits.
- Function arguments use `$a0`–`$a3`; return values use `$v0`.
- A function that calls another function must preserve `$ra`.

