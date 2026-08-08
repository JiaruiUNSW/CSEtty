#define _POSIX_C_SOURCE 200809L
#include <stdio.h>

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "usage: %s FILE_A FILE_B\n", argv[0]);
        return 1;
    }
    // TODO: create two children, scan the files, and collect pipe results.
    return 0;
}
