#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        return 1;
    }
    long n = strtol(argv[1], NULL, 10);

    // TODO: create a pipe and one child. The child computes 1 + ... + n and
    // writes the binary long result through the pipe. The parent reads exactly
    // one long, waits for a successful child exit, and prints the result.
    (void)n;
    (void)errno;
    return 1;
}
