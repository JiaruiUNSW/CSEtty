#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s START STEP COUNT\n", argv[0]);
        return 1;
    }
    // TODO: stream sequence records from a child and reduce them.
    return 0;
}
