#define _POSIX_C_SOURCE 200809L
#include <pthread.h>
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 2) {
        fprintf(stderr, "usage: %s FILE\n", argv[0]);
        return 1;
    }
    // TODO: fork, analyse with three child threads, and send a summary.
    return 0;
}
