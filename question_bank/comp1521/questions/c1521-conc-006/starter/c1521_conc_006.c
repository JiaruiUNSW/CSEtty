#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE WORKERS\n", argv[0]);
        return 1;
    }
    // TODO: shard lines across child processes and combine their records.
    return 0;
}
